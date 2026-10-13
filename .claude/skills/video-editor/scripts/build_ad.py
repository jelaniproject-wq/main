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


def main(spec_path):
    spec = json.load(open(spec_path))
    name = spec["name"]
    os.makedirs(f"build/{name}", exist_ok=True)
    b = f"build/{name}"
    fix = spec.get("fix", {})
    hl = {h.upper() for h in spec.get("highlight", [])}

    parts, events, t0 = [], [], 0.0
    for i, s in enumerate(spec["segments"]):
        dur = s["end"] - s["start"]
        z = s.get("zoom", 1.0)
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"scale=iw*{z}:ih*{z},crop={W}:{H},setsar=1,fps={FPS}" + (",hflip" if s.get("hflip") else ""))
        p = f"{b}/seg{i:02d}.mp4"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(s["start"]), "-t", f"{dur:.3f}",
             "-i", f"{SRC}/IMG_{s['clip']}.MOV", "-vf", vf, "-af", "aresample=48000,aformat=channel_layouts=stereo",
             *X264, "-crf", "12", *AAC, p])
        parts.append(p)
        ws = words_for(s["clip"], s["start"], s["end"])
        if "caps" in s:  # hand-phrased captions: each takes as many words as it has (hyphen parts merged)
            merged = []
            for w in ws:
                if w["word"].strip().startswith(("-", ",")) and merged:
                    merged[-1]["end"] = w["end"]
                else:
                    merged.append(dict(w))
            groups, k = [], 0
            for c in s["caps"]:
                n = len(c.split())
                g = merged[k:k + n] or merged[-1:]
                groups.append([{"start": g[0]["start"], "end": g[-1]["end"], "t": c}])
                k += n
        else:
            groups = chunk(ws, fix)
        for g in groups:
            st = max(0, g[0]["start"] - s["start"]) + t0
            en = min(dur, g[-1]["end"] - s["start"] + 0.12) + t0
            hl_bare = {re.sub(r"[^A-Z-]", "", h) for h in hl}
            txt = " ".join(
                (f"{{\\c&H00{YELLOW}&}}{tok}{{\\c&H00{CREAM}&}}"
                 if re.sub(r"[^A-Z-]", "", tok) in hl_bare else tok)
                for tok in " ".join(w["t"] for w in g).upper().split())
            events.append((st, en, txt))
        t0 += dur

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

    ass = f"{b}/captions.ass"
    open(ass, "w").write(hdr + "\n".join(
        f"Dialogue: 1,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\fscx85\\fscy85\\t(0,90,\\fscx100\\fscy100)}}{tx}"
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
