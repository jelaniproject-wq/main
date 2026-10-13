#!/usr/bin/env python3
"""Build a JELANI Meta ad from a JSON spec: cut segments, burn brand captions from Whisper
word timings, add an end card, export 9:16 (1080x1920) and 4:5 (1080x1350) at max quality.

spec = {
  "name": "scout_warm",
  "segments": [{"clip": "3805", "start": 149.3, "end": 152.9, "zoom": 1.0}, ...],
  "fix": {"scalp": "Scout"},           # whisper corrections (case-insensitive)
  "highlight": ["SCOUT", "BACK"],      # words shown in Soft Yellow
  "endcard": ["SCOUT SET", "RESTOCKED", "XS – L · jelani.com.au"],
  "endcard_secs": 2.0
}
"""
import json, os, re, subprocess, sys

SRC = "../src"
TX = "tx"
W, H, FPS = 1080, 1920, 30
CREAM, RUST, YELLOW, BLUSH = "F0FAFC", "2E3DB2", "7CDEF6", "E4DFF9"  # ASS BGR
X264 = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
        "-profile:v", "high", "-r", str(FPS)]
AAC = ["-c:a", "aac", "-b:a", "320k", "-ar", "48000"]


def run(cmd):
    subprocess.run(cmd, check=True)


def ts(x):
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


PAUSE = 0.5  # cut any pause longer than this (seconds)


def all_words(clip):
    d = json.load(open(f"{TX}/a{clip}.json"))
    return [dict(w) for s in d["segments"] for w in s.get("words", [])]


_MODEL = None


def window_words(clip, a, b, pad=2.0):
    """Re-transcribe just [a-pad, b+pad]: short windows give far more accurate word times than a
    full-clip pass, and expose stumbles/retakes that the long pass merges. Cached in tx/."""
    global _MODEL
    a0 = max(0.0, a - pad)
    cache = f"{TX}/win_{clip}_{a0:.2f}_{b + pad:.2f}.json"
    if not os.path.exists(cache):
        import whisper
        _MODEL = _MODEL or whisper.load_model("small.en")
        wav = f"{TX}/win_tmp.wav"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a0:.3f}", "-t", f"{b + pad - a0:.3f}",
             "-i", f"a{clip}.wav", wav])
        r = _MODEL.transcribe(wav, language="en", word_timestamps=True, fp16=False,
                              condition_on_previous_text=False)
        json.dump([{"word": w["word"], "start": a0 + w["start"], "end": a0 + w["end"]}
                   for sg in r["segments"] for w in sg.get("words", [])], open(cache, "w"))
    return json.load(open(cache))


def merge_tokens(ws):
    """Whisper splits "pre -order" / "1 ,000"; glue those back onto the previous word."""
    out = []
    for w in ws:
        t = w["word"].strip()
        if t.startswith(("-", ",")) and out:
            out[-1]["end"] = w["end"]
            out[-1]["t"] += t
        else:
            w["t"] = t
            out.append(w)
    return out


class Envelope:
    """10 ms RMS envelope of a 16 kHz mono wav, used to cut in the quiet between words."""

    def __init__(self, path):
        import array, wave
        with wave.open(path) as f:
            sr = f.getframerate()
            a = array.array("h", f.readframes(f.getnframes()))
        hop = sr // 100
        self.rms = [(sum(x * x for x in a[k:k + hop]) / hop) ** 0.5 for k in range(0, len(a) - hop, hop)]
        srt = sorted(self.rms)
        floor, loud = srt[len(srt) // 5], srt[int(len(srt) * 0.9)]
        self.thr = floor + 0.12 * (loud - floor)

    def _q(self, t):
        k = int(t * 100)
        return 0 <= k < len(self.rms) and self.rms[k] < self.thr

    def quiet_after(self, t, limit):
        """First point after t where 80 ms stays quiet (word tail finished); never past the next word."""
        hi = min(limit - 0.03, t + 0.7)
        x = t
        while x < hi:
            if all(self._q(x + d / 100) for d in range(8)):
                return min(x + 0.06, hi)
            x += 0.01
        return max(min(hi, t + 0.25), t + 0.08)

    def speech_spans(self, a, b, gap=PAUSE, pad=0.1):
        """Split [a, b] wherever the audio stays quiet for longer than `gap` seconds."""
        spans, cur, q0 = [], a, None
        x = a
        while x < b:
            if self._q(x):
                q0 = x if q0 is None else q0
            else:
                if q0 is not None and x - q0 > gap and q0 > cur:
                    spans.append((cur, q0 + pad))
                    cur = x - pad
                q0 = None
            x += 0.01
        spans.append((cur, b))
        return [(sa, sb) for sa, sb in spans if sb - sa > 0.15]

    def quiet_before(self, t, limit):
        """Last quiet point before t (so the first word's onset isn't clipped)."""
        # Whisper often marks soft onsets ("Your", "Everything", "They're") late, and their first
        # frames are quieter than speech, so start looking well before t and demand real silence.
        lo = max(limit + 0.03, t - 0.7, 0)
        x = t - 0.15
        soft = self.thr * 0.6
        while x > lo:
            if all(0 <= int((x - d / 100) * 100) < len(self.rms) and self.rms[int((x - d / 100) * 100)] < soft
                   for d in range(15)):
                return max(x - 0.05, lo)
            x -= 0.01
        return max(lo, t - 0.3)


def words_for(clip, start, end):
    d = json.load(open(f"{TX}/a{clip}.json"))
    out = []
    for s in d["segments"]:
        for w in s.get("words", []):
            if w["start"] >= start - 0.05 and w["end"] <= end + 0.15:
                out.append(dict(w))
    return out


def chunk(words, fix, maxw=3):
    """Group words into 1-3 word captions, breaking on punctuation."""
    groups, cur = [], []
    for w in words:
        t = w["word"].strip()
        for k, v in fix.items():
            t = re.sub(rf"\b{k}\b", v, t, flags=re.I)
        w["t"] = t
        if t.startswith("-") and (cur or groups):
            if not cur:
                cur = groups.pop()  # whisper splits "go -to"
            cur[-1]["t"] += t
            cur[-1]["end"] = w["end"]
            continue
        cur.append(w)
        if len(cur) >= maxw or re.search(r"[.,!?]$", t):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


# Caption placement: keep text off the face and inside Meta's 9:16 safe area
SAFE_TOP, SAFE_BOTTOM = 290, 1250   # Meta UI covers top ~14% and bottom ~35%
LINE_H, CHAR_W, MAX_W = 112, 50, 940


def caption_height(tx):
    chars = len(re.sub(r"{[^}]*}", "", tx))
    return LINE_H * max(1, -(-chars * CHAR_W // MAX_W))


def faces_at(video, t):
    import cv2
    cap = cv2.VideoCapture(video)
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, frame = cap.read()
    cap.release()
    if not ok:
        return []
    g = cv2.cvtColor(cv2.resize(frame, (W // 2, H // 2)), cv2.COLOR_BGR2GRAY)
    det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    found = det.detectMultiScale(g, 1.1, 6, minSize=(50, 50))
    # pad: forehead/hair above, chin below (Haar boxes are tight)
    return [(int(y * 2 - h * 0.35), int((y + h) * 2 + h * 0.45)) for (x, y, w, h) in found]


def place_caption(video, st, en, tx):
    """Return caption top y: below the face if it fits, else above, else the least-overlapping spot."""
    h = caption_height(tx)
    boxes = [f for t in (st + 0.05, (st + en) / 2, max(st, en - 0.05)) for f in faces_at(video, t)]
    if not boxes:  # face hidden (e.g. product held up): borrow from the frames around it
        boxes = [f for t in (st - 1.0, st - 0.5, en + 0.5, en + 1.0) if t >= 0 for f in faces_at(video, t)]
    default = SAFE_BOTTOM - h - 100
    if not boxes:
        return default
    top, bot = min(b[0] for b in boxes), max(b[1] for b in boxes)
    if bot + 30 + h <= SAFE_BOTTOM:
        return max(bot + 30, default if default > bot + 30 else bot + 30)
    if top - 30 - h >= SAFE_TOP:
        return top - 30 - h
    cands = range(SAFE_TOP, SAFE_BOTTOM - h + 1, 10)
    return min(cands, key=lambda y: max(0, min(y + h, bot) - max(y, top)))


def dm_takeover(cat, wall, b):
    """All DMs flood in fast, overlap to fill the screen, hold, then clear together."""
    import random
    from PIL import Image
    rnd = random.Random(7)
    t1, t2 = wall["start"], wall["end"]
    sc, stg, out = wall.get("scale", 0.82), wall.get("stagger", 0.17), 0.28
    imgs = wall["images"]
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                           "-of", "csv=p=0", cat]))
    # pre-rotate/scale each bubble a touch so the pile feels thrown together
    prepped, heights = [], []
    for k, img in enumerate(imgs):
        im = Image.open(img)
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        im = im.rotate(rnd.uniform(-4, 4), resample=Image.BICUBIC, expand=True)
        pth = f"{b}/to_{k:02d}.png"
        im.save(pth)
        prepped.append((pth, im.width, im.height))
        heights.append(im.height)
    # spread top-to-bottom across the whole frame, overlapping
    span = H - 80
    step = (span - heights[-1]) / max(1, len(imgs) - 1)
    pos = []
    for k, (pth, iw, ih) in enumerate(prepped):
        x = rnd.randint(-30, 60) if k % 2 == 0 else W - iw - rnd.randint(-30, 60)
        pos.append((x, int(40 + k * step + rnd.randint(-25, 25))))
    order = list(range(len(imgs)))
    rnd.shuffle(order)  # pop in random order so it reads as a flood, not a list
    ins = []
    fc = [f"[0:v]split[a][b];[b]boxblur=18:2,eq=brightness=-0.12[bl];"
          f"[a][bl]overlay=enable='between(t,{t1},{t2})'[v0]"]
    for n, k in enumerate(order):
        pth, iw, ih = prepped[k]
        x, y = pos[k]
        tk = t1 + 0.1 + n * stg
        ins += ["-loop", "1", "-t", f"{total:.3f}", "-i", pth]
        fc.append(f"[{n + 1}:v]format=rgba,fade=t=in:st={tk:.2f}:d=0.12:alpha=1,"
                  f"fade=t=out:st={t2 - out:.2f}:d={out}:alpha=1[d{n}];"
                  f"[v{n}][d{n}]overlay={x}:{y}:enable='between(t,{tk:.2f},{t2})'[v{n + 1}]")
    walled = f"{b}/walled.mp4"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", cat, *ins,
         "-filter_complex", ";".join(fc), "-map", f"[v{len(imgs)}]", "-map", "0:a",
         *X264, "-crf", "12", "-c:a", "copy", walled])
    return walled


def main(spec_path):
    spec = json.load(open(spec_path))
    name = spec["name"]
    os.makedirs(f"build/{name}", exist_ok=True)
    b = f"build/{name}"
    fix = spec.get("fix", {})
    hl = {h.upper() for h in spec.get("highlight", [])}

    parts, events, t0 = [], [], 0.0
    for i, s in enumerate(spec["segments"]):
        z = s.get("zoom", 1.0)
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"scale=iw*{z}:ih*{z},crop={W}:{H},setsar=1,fps={FPS}" + (",hflip" if s.get("hflip") else ""))
        allw = window_words(s["clip"], s["start"], s["end"])
        ws = merge_tokens([w for w in allw if s["start"] - 0.05 <= w["start"] < s["end"]])
        # split into runs wherever the speaker pauses > PAUSE (skill rule 3)
        runs = [[ws[0]]]
        for w in ws[1:]:
            (runs.append([w]) if w["start"] - runs[-1][-1]["end"] > PAUSE else runs[-1].append(w))
        env = Envelope(f"a{s['clip']}.wav")
        offs = []  # (src_start, src_end, timeline_start)
        for j, r in enumerate(runs):
            prev_end = max([w["end"] for w in allw if w["end"] <= r[0]["start"]] or [0.0])
            nxt = min([w["start"] for w in allw if w["start"] >= r[-1]["end"] + 0.01] or [r[-1]["end"] + 0.8])
            a = env.quiet_before(r[0]["start"], prev_end)
            bnd = env.quiet_after(r[-1]["end"], nxt)
            for sa, sb in env.speech_spans(a, bnd):  # also drop silences Whisper hid inside long words
                p = f"{b}/seg{i:02d}_{j}_{len(parts)}.mp4"
                dur = sb - sa
                run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{sa:.3f}", "-t", f"{dur:.3f}",
                     "-i", f"{SRC}/IMG_{s['clip']}.MOV", "-vf", vf,
                     "-af", f"aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.015,afade=t=out:st={dur - 0.03:.3f}:d=0.03",
                     *X264, "-crf", "12", *AAC, p])
                parts.append(p)
                offs.append((sa, sb, t0))
                t0 += dur

        def remap(t):
            for a, bnd, tl in offs:
                if a - 0.01 <= t <= bnd + 0.01:
                    return tl + (t - a)
            best = min(offs, key=lambda o: min(abs(t - o[0]), abs(t - o[1])))
            return best[2] + (min(max(t, best[0]), best[1]) - best[0])

        if "caps" in s:  # hand-phrased captions: each takes as many words as it has
            groups, k = [], 0
            for c in s["caps"]:
                n = len(c.split())
                g = ws[k:k + n] or ws[-1:]
                groups.append([{"start": g[0]["start"], "end": g[-1]["end"], "t": c}])
                k += n
        else:
            groups = chunk(ws, fix)
        for g in groups:
            st, en = remap(g[0]["start"]), remap(g[-1]["end"]) + 0.12
            hl_bare = {re.sub(r"[^A-Z-]", "", h) for h in hl}
            txt = " ".join(
                (f"{{\\c&H00{YELLOW}&}}{tok}{{\\c&H00{CREAM}&}}"
                 if re.sub(r"[^A-Z-]", "", tok) in hl_bare else tok)
                for tok in " ".join(w["t"] for w in g).upper().split())
            events.append((st, min(en, t0), txt))

    # stretch captions to fill gaps (no flicker), cap at next caption start
    events.sort()
    for k in range(len(events) - 1):
        st, en, tx = events[k]
        events[k] = (st, min(max(en, events[k + 1][0] - 0.02), events[k + 1][0]), tx)

    # end card
    ec = spec.get("endcard_secs", 2.0)
    lines = spec["endcard"]
    ecf = f"{b}/endcard.mp4"
    ass_ec = f"{b}/endcard.ass"
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter,92,&H00{CREAM},&H00{CREAM},&H001A2A6E,&H64000000,-1,0,0,0,100,100,-2,0,1,6,3,2,70,70,740,1
Style: Big,Inter,150,&H00{RUST},&H00{RUST},&H00{RUST},&H00000000,-1,0,0,0,100,100,-6,0,1,0,0,5,60,60,0,1
Style: Mid,Inter,96,&H00{RUST},&H00{RUST},&H00{RUST},&H00000000,-1,0,0,0,100,100,-3,0,1,0,0,5,60,60,0,1
Style: Small,Inter,52,&H00{RUST},&H00{RUST},&H00{RUST},&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ys = [820, 980, 1110]
    styles = ["Big", "Mid", "Small"]
    ev = [f"Dialogue: 0,{ts(0.1 * k)},{ts(ec)},{styles[k]},,0,0,0,,{{\\pos({W // 2},{ys[k]})\\fad(150,0)}}{line}"
          for k, line in enumerate(lines[:3])]
    open(ass_ec, "w").write(hdr + "\n".join(ev) + "\n")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"color=c=0xFCFAF0:s={W}x{H}:r={FPS}:d={ec}",
         "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo", "-t", str(ec),
         "-vf", f"noise=alls=3:allf=t,ass={ass_ec}", *X264, "-crf", "12", *AAC, ecf])
    parts.append(ecf)

    with open(f"{b}/list.txt", "w") as L:
        for p in parts:
            L.write(f"file '{os.path.basename(p)}'\n")
    cat = f"{b}/concat.mp4"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{b}/list.txt",
         "-c", "copy", cat])

    wall = spec.get("dm_wall")  # {"start","end","images":[...],"scale","top","caption_y","stagger","mode"}
    if wall and wall.get("mode") == "takeover":
        cat = dm_takeover(cat, wall, b)
    elif wall:
        from PIL import Image
        t1, t2 = wall["start"], wall["end"]
        sc, y, stg = wall.get("scale", 0.85), wall.get("top", 430), wall.get("stagger", 0.45)
        total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                               "-of", "csv=p=0", cat]))
        ins, fc = [], [f"[0:v]split[a][b];[b]boxblur=22:2,eq=brightness=-0.08[bl];"
                       f"[a][bl]overlay=enable='between(t,{t1},{t2})'[v0]"]
        for k, img in enumerate(wall["images"]):
            iw, ih = Image.open(img).size
            iw, ih = int(iw * sc), int(ih * sc)
            x = 40 if k % 2 == 0 else W - iw - 40
            tk = t1 + 0.15 + k * stg
            ins += ["-loop", "1", "-t", f"{total:.3f}", "-i", img]
            fc.append(f"[{k + 1}:v]scale={iw}:{ih},format=rgba,fade=t=in:st={tk:.2f}:d=0.18:alpha=1[d{k}];"
                      f"[v{k}][d{k}]overlay={x}:{y}:enable='between(t,{tk:.2f},{t2})'[v{k + 1}]")
            y += ih - 12
        walled = f"{b}/walled.mp4"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", cat, *ins,
             "-filter_complex", ";".join(fc), "-map", f"[v{len(wall['images'])}]", "-map", "0:a",
             *X264, "-crf", "12", "-c:a", "copy", walled])
        cat = walled

    def cap_y(st, en, tx):
        if wall and st < wall["end"] and en > wall["start"]:
            return wall.get("caption_y", SAFE_TOP)
        return place_caption(cat, st, en, tx)

    ass = f"{b}/captions.ass"
    open(ass, "w").write(hdr + "\n".join(
        f"Dialogue: 1,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\an8\\pos({W // 2},{cap_y(st, en, tx)})"
        f"\\fscx85\\fscy85\\t(0,90,\\fscx100\\fscy100)}}{tx}"
        for st, en, tx in events) + "\n")

    out916 = f"out/{name}_9x16_v1.mp4"
    out45 = f"out/{name}_4x5_v1.mp4"
    os.makedirs("out", exist_ok=True)
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", cat, "-vf", f"ass={ass}",
         "-af", "loudnorm=I=-14:TP=-1:LRA=11", *X264, *AAC, "-movflags", "+faststart", out916])
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", out916, "-vf", f"crop={W}:1350:0:285",
         *X264, "-c:a", "copy", "-movflags", "+faststart", out45])
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out916]))
    print(f"{name}: {d:.1f}s -> {out916}, {out45}")
    for st, en, tx in events:
        print(f"  {st:5.2f}-{en:5.2f} {re.sub(r'{[^}]*}', '', tx)}")


if __name__ == "__main__":
    main(sys.argv[1])
