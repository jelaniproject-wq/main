#!/usr/bin/env python3
"""Swap a finished ad's end card for the JELANI brand end board.

The ad's last shot cross-fades into the end board (brand/endboard_9x16.png), which holds with a
slow push-in while "jelani.com.au" fades in under the logo. Writes 9:16 and a 4:5 crop.

usage: endboard.py ad_9x16.mp4 out_prefix [--old-endcard 1.8] [--hold 2.6] [--fade 0.6]
"""
import argparse
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(HERE, "..", "brand", "endboard_9x16.png")
W, H, FPS = 1080, 1920, 30
X264 = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-profile:v", "high",
        "-r", str(FPS)]


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", p]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out_prefix")
    ap.add_argument("--old-endcard", type=float, default=1.8)
    ap.add_argument("--hold", type=float, default=2.6)
    ap.add_argument("--fade", type=float, default=0.6)
    ap.add_argument("--url", default="jelani.com.au")
    a = ap.parse_args()

    main_len = dur(a.src) - a.old_endcard
    off = main_len - a.fade
    total = off + a.hold
    frames = int(a.hold * FPS)
    ass = a.out_prefix + "_url.ass"
    t_in = a.fade + 0.35
    open(ass, "w").write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Url,Inter Medium,32,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,9,0,1,0,1.5,8,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:{t_in:05.2f},0:00:{a.hold:05.2f},Url,,0,0,0,,{{\\pos({W // 2},1068)\\fad(400,0)}}{a.url}
""")
    # slow push-in on the board (rendered at 2x for smooth sub-pixel zoom), url on top
    fc = (f"[0:v]trim=0:{main_len:.3f},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p[m];"
          f"[1:v]scale={W * 2}:{H * 2},zoompan=z='1+0.05*on/{frames}':d={frames}:"
          f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
          f"ass={ass},format=yuv420p,setsar=1[e];"
          f"[m][e]xfade=transition=fade:duration={a.fade}:offset={off:.3f}[v];"
          f"[0:a]atrim=0:{main_len:.3f},asetpts=PTS-STARTPTS,"
          f"afade=t=out:st={max(0, off):.3f}:d={a.fade},apad=whole_dur={total:.3f}[au]")
    o916 = a.out_prefix + "_9x16.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.src, "-i", BOARD, "-filter_complex", fc, "-map", "[v]", "-map", "[au]",
                    *X264, "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", o916],
                   check=True)
    o45 = a.out_prefix + "_4x5.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", o916, "-vf",
                    f"crop={W}:1350:0:285", *X264, "-c:a", "copy", "-movflags", "+faststart", o45], check=True)
    print(f"{o916} ({dur(o916):.1f}s), {o45}")


if __name__ == "__main__":
    main()
