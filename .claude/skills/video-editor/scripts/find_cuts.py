#!/usr/bin/env python3
"""First-pass cut list from a Whisper JSON transcript (run with --word_timestamps True).

Drops pauses longer than --pause seconds and flags likely retakes (a phrase restarted,
or "let's redo that"-style cues), keeping the later take. Prints JSON:
  {"keep": [[start, end], ...], "removed": [{"start", "end", "reason", "text"}], ...}
Review the output before cutting; it's a suggestion, not a decision.
"""
import argparse
import json
import re

REDO_CUES = re.compile(
    r"\b(let'?s (redo|re-do|do) that( again)?|redo that|take two|scratch that|start (that )?again|one more time)\b",
    re.I,
)


def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


def load_words(path):
    data = json.load(open(path))
    words = []
    for seg in data.get("segments", []):
        for w in seg.get("words", []):
            words.append({"start": w["start"], "end": w["end"], "text": w["word"].strip()})
    return words, data.get("segments", [])


def find_retakes(segments, n=3):
    """A segment whose first n words match the next segment's first n words is a retake."""
    drops = []
    for a, b in zip(segments, segments[1:]):
        wa = [norm(x) for x in a["text"].split()][:n]
        wb = [norm(x) for x in b["text"].split()][:n]
        if len(wa) == n and wa == wb:
            drops.append({"start": a["start"], "end": b["start"], "reason": "retake", "text": a["text"].strip()})
        elif REDO_CUES.search(a["text"]):
            drops.append({"start": a["start"], "end": b["start"], "reason": "redo cue", "text": a["text"].strip()})
    return drops


def main():
    p = argparse.ArgumentParser()
    p.add_argument("transcript")
    p.add_argument("--pause", type=float, default=0.5)
    p.add_argument("--pad", type=float, default=0.08)
    a = p.parse_args()

    words, segments = load_words(a.transcript)
    if not words:
        raise SystemExit("No word timestamps found; re-run whisper with --word_timestamps True")

    removed = find_retakes(segments)
    in_removed = lambda t: any(r["start"] <= t < r["end"] for r in removed)

    keep, cur = [], None
    for w in words:
        if in_removed(w["start"]):
            continue
        s, e = max(0.0, w["start"] - a.pad), w["end"] + a.pad
        if cur and s - cur[1] <= a.pause:
            cur[1] = e
        else:
            if cur:
                removed.append({"start": cur[1], "end": s, "reason": "pause", "text": ""})
                keep.append(cur)
            cur = [s, e]
    if cur:
        keep.append(cur)

    kept = sum(e - s for s, e in keep)
    print(json.dumps({
        "keep": [[round(s, 3), round(e, 3)] for s, e in keep],
        "removed": sorted(removed, key=lambda r: r["start"]),
        "original_seconds": round(words[-1]["end"], 2),
        "kept_seconds": round(kept, 2),
    }, indent=2))


if __name__ == "__main__":
    main()
