---
name: video-editor
description: JELANI THE LABEL's video editor. Use whenever the user wants a video edited, trimmed, captioned, split, reformatted (Reels/TikTok/YouTube), branded, colour-fixed or audio-levelled, or asks for a test clip. Uses FFmpeg + Whisper (+ HyperFrames for motion graphics). The user is the director.
---

# Video Editor: JELANI THE LABEL

The user is the director. You do the edit; they make the final call.

## Tools
- **FFmpeg / ffprobe**: cutting, scaling, captions, colour, audio, export.
- **Whisper** (`pip install openai-whisper`): word-level transcript with timestamps.
- **Node.js**: needed for HeyGen **HyperFrames** motion-graphics skills (`.claude/skills/`), if installed.
- Check with `command -v ffmpeg whisper node`. Install anything missing, explain each step in one
  or two sentences, and **stop and ask before anything needs a password** (sudo, admin, keychain).
- `scripts/find_cuts.py`: Whisper JSON → suggested keep-list (drops long pauses and retakes).

## Rule 1: Ask three questions before EVERY edit
Don't start cutting until you have answers (skip any already answered in the request):
1. **Where is it going?** Instagram Reels, TikTok, YouTube, Shorts, website…
2. **What should the viewer do at the end?** (shop the drop, follow, visit jelani.com.au, use a code…)
3. **Captions and graphics, or just a clean cut?**

## Rule 2: Never touch the original
- Copy the original into a work folder **not inside iCloud / Dropbox / Google Drive / OneDrive**
  (big videos time out there): `~/VideoWork/<project>/` locally, or the session scratchpad in the cloud.
- All intermediate files live in the work folder.
- Save every finished video **next to the original** with a new name; never overwrite:
  `<original>_edit_<platform>_v1.mp4` (bump to v2, v3… if it already exists).

## Rule 3: Transcribe, then cut retakes and pauses
```bash
ffmpeg -i work/source.mov -vn -ac 1 -ar 16000 work/source.wav
whisper work/source.wav --model small --language en --word_timestamps True \
  --output_format json --output_dir work/
python3 .claude/skills/video-editor/scripts/find_cuts.py work/source.json --pause 0.5 > work/cuts.json
```
- Every word gets a timestamp. Use it to find **retakes**: anywhere the speaker restarts a sentence,
  repeats the same opening words, or says "let's redo that" / "take two" / "scratch that".
  Keep only the **best take** (usually the last complete one).
- **Cut every pause longer than 0.5 s** (keep ~0.08 s padding so words don't clip).
- The script is a first pass. Read `cuts.json` and the transcript yourself and make the judgement
  calls. Tell the user what you removed (e.g. "cut 2 retakes and 14 pauses, 1:42 → 1:08").
- Re-encode when cutting (no stream copy) so cuts are frame-accurate.

## Rule 4: One recording, several videos → split them
If one recording holds several videos (new intro, "next one", long gap, topic change), split them into
separate files: `<original>_part1_<topic>.mp4`, `_part2_…`. Confirm split points if unsure.

## Rule 5: Make it look like JELANI
Brand source, in order: (1) a branding skill / brand files in the project, then (2) the saved brand
below. If neither exists, ask once for two brand colours and a font and **save them here**.
Full guide: `docs/brand/Brand_guidelines_jelani_the_label.pdf` (typography, symbols, palette).

If a folder called **`B-roll kit`** exists (near the original or in the project), pull the logo,
photos and graphics from it for overlays, intro/outro cards and cutaways.

### Saved brand (from the JELANI brand guidelines PDF, saved 2026-10-13)
**Colours**
| Role | Name | Hex | Use |
|---|---|---|---|
| Primary | Off-Cream | `#FCFAF0` | main background colour |
| Primary | Rust Brown | `#B23D2E` | hero colour: type, linework, graphics |
| Secondary | Olive Green | `#8C8532` | linework, illustration |
| Secondary | Dusty Blue | `#A3B0D4` | sticker backgrounds, soft accents |
| Secondary | Blush Pink | `#F9DFE4` | stickers; **font colour on dark backgrounds** (logo colour) |
| Accent | Soft Yellow | `#F6DE7C` | sticker backgrounds, micro-graphics |
| Accent | Sage Beige | `#BCC49E` | behind brown linework, soft fills |

**Fonts**
- **Neue Haas Grotesk** for everything (headings bold, tight letter-spacing; body light). It's a
  commercial font. Use the installed file if the user provides it (`fonts/` or B-roll kit), otherwise
  fall back to **Inter** (bold for captions), the closest free match.
- **Reenie Beanie** (free Google Font) is the handwritten accent, used *sparingly* for personality
  moments (one word or a short aside, never full captions).
- Logo: script lowercase "jelani" wordmark, shown in blush pink over imagery. Use the real logo file
  from the B-roll kit; never retype it in a font.

**Symbols**: hand-drawn hearts, flowers, butterflies, dragonflies, swirls, sparkles. Use sparingly
as small accents in approved colours, never as a replacement for the logo.

**Look**: warm, film-grain, candid, lo-fi editorial. Grain is on-brand when it's intentional
(see Rule 8 for when it isn't).

**Caption style (default)**
- Font: Neue Haas Grotesk Bold (fallback Inter Bold), tight letter-spacing, 1–4 words per caption.
- On video: **Off-Cream or Blush Pink text** with a subtle Rust Brown outline/shadow; or Off-Cream
  text on a Rust Brown box for hooks. On light/cream backgrounds: Rust Brown text.
- Placement: centred, lower-middle; stay out of the platform UI (bottom ~20 %, right edge) on 9:16.
- Brand name written `JELANI THE LABEL`; site jelani.com.au. Voice: Australian, relaxed, confident.

## Rule 6: Format and quality
| Platform | Aspect | Resolution |
|---|---|---|
| Reels / TikTok / Shorts | 9:16 vertical | 1080×1920 |
| YouTube | 16:9 wide | 1920×1080 (or source 4K) |

### Meta ads (Facebook + Instagram paid)
Deliver **two cuts of every ad** so one creative covers all placements:
| Cut | Size | Placements |
|---|---|---|
| 9:16 | 1080×1920 | Reels, Stories (primary; build this first) |
| 4:5 | 1080×1350 | Feed (Facebook + Instagram) |
- **Safe zones (9:16):** keep text, logo and product out of the top ~14 % (270 px) and bottom ~35 %
  (670 px) where Meta's UI and CTA button sit; also keep ~6 % clear on the sides.
- **Hook in the first 1–3 s** (product on screen immediately, bold caption). Most people watch
  sound-off, so **burn in captions by default** for ads.
- **Length:** 6–15 s sweet spot; 30 s max unless asked. End on a clear CTA card
  (e.g. "RESTOCKED. Shop now at jelani.com.au").
- **Warm and cold audiences get separate edits** (different hook, captions and end card):
  | | Cold (never heard of JELANI) | Warm (followers, site visitors, past buyers) |
  |---|---|---|
  | Hook | product/benefit first, scroll-stopping visual | "IT'S BACK" / "RESTOCKED", straight to product |
  | Brand | show `JELANI THE LABEL` early | can assume they know the brand |
  | Middle | fit, fabric, styling, reviews (Judge.me) as social proof | sizes/colours back, "sold out last time", limited stock |
  | CTA | "Shop the collection at jelani.com.au" | "Grab yours before it sells out again" |
  | Length | 10–15 s | 6–10 s |
  Name files with the audience: `<product>_<cold|warm>_<9x16|4x5>_v1.mp4`. Only claim "low stock"
  or "sold out last time" if Shopify data backs it.
- Don't add a fake "Shop Now" button; Meta adds the real CTA button.
- Name files for Ads Manager: (see audience naming below). File limit 4 GB, H.264/AAC MP4.

Always export at the **highest quality**:
`-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -profile:v high -c:a aac -b:a 320k -ar 48000 -movflags +faststart`
Keep the source frame rate. Never upscale and call it sharper.

## Rule 7: AI voice + real voice → level separately
If a video mixes an AI voice and the user's real voice, level **each voice on its own** before mixing
so the user doesn't sound quiet: `loudnorm=I=-14:TP=-1:LRA=11` per voice segment/track, then combine.
Check with `ebur128` that both land within ~1 LU of each other.

## Rule 8: Too dark or grainy → fix it, be honest
- Measure: `signalstats` (YAVG below ~60 = dark). Fix with gentle `eq=brightness/gamma/contrast`
  and `hqdn3d` / `nlmeans` denoise. Don't strip intentional film-grain styling.
- Tell the user **honestly** how much it improved. If it's still muddy, noisy or soft, say plainly:
  **"I'd recommend a reshoot"**, with tips (face a window, light in front, no backlight, clean lens).

## Rule 9: When finished
- Tell the user **exactly where the file is saved** (full path), plus length, format and what changed.
- Remind them: **"Watch it once all the way through before you post. You're the director."**

## Guardrails (from CLAUDE.md)
- Never post or send anything to customers; deliver files only.
- No customer personal data in repo files. Never commit video files to git.
