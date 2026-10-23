# Jelani swim development: handoff brief

Read this first. It summarises a design session (23 Oct 2026) so you can continue the work.

## Who / what
- Natalia, founder of **Jelani**, a sustainable swimwear and apparel label (Sydney). Manufacturer: **Fanny**.
- Goal: develop the next bikini drop. The vibe is edgy, cool and eclectic.
- **Current step: lock FABRICS first, then apply them to shapes.**

## Colours: decisions so far
- **Keep:** Racing Red **19-1763 TCX** + Rifle Green **19-0419 TCX**, as solids, either way round (body/binding). This is a favourite.
- **Rejected:** the red + khaki **plaid** ("looks too much like Christmas"). Never weave red and green together.
- **Rejected:** retro multi-stripe and olive + burgundy dot (from `jelani_board_direction.png`).
- **On the fence:** the blue + red plaid (not sold on the colours).
- **Liked earlier:** pink gingham/plaid with brown binding; khaki + orange contrast stitch (Flame 17-1462 TCX or Red Orange 17-1464 TCX); leopard body with red binding (matches her leopard mules); lace-up cups are "ok".
- **Palette from her Pinterest board:** tomato red, burgundy, chocolate, rust, olive, butter, sky blue, cobalt, cream.

## Fabric shortlist (see `mockups/jelani_fabric_swatches.png`)
Waiting for Natalia to keep or cut options:
- Kept: Racing Red/Rifle Green both ways
- Checks: pink + chocolate plaid, sky + chocolate plaid, butter + burgundy plaid, lilac gingham
- Knit stripes (from a sage/chocolate knit bikini ref): sage, butter, pink/burgundy, sky/rust uneven
- Dots/other: butter + burgundy dot, cream + chocolate painterly dot, chocolate pinstripe w/ red piping, leopard
- Solids: Racing Red/chocolate, Rifle Green/Flame stitch, cobalt/chocolate, butter/sky
- Production notes: digital print on swim lycra is cheapest. A real knit-stripe texture means a knitted swim fabric (ask Fanny). The "cotton textured gingham" look = seersucker/crinkle swim fabric.

## Shapes explored (after fabric is locked)
- Original Jelani triangle + tie-side (`mockups/src.png` is her flat sketch)
- `jelani_top_concepts.png`: lace-up cups, grommet binding, ring lattice, buckle straps, corset centre
- `jelani_style_options.png`: sporty scoop + boyshort, balconette + high-leg, ruffle triangle, twist bandeau + cheeky ring-slider bottom (Monete/Solkissed refs)
- `jelani_lattice_bandeau.png` (rough): bandeau with laced centre, amber beads on halter, wooden ring on bottom, ruched sides (from knit-stripe ref)
- Red halter one-piece with brown binding (on her board twice)
- Hardware notes: swim-safe, non-rust (coated brass/stainless). Satin ribbon isn't swim-grade.

## Apparel side-project
- Tulip graphic tee (`jelani_tulip_tee_bleach.png`): bleach on 100% cotton (stencil + spray, lifts blue to peachy-pink, one-offs) vs **discharge screen print** for baby blue + maroon flower or consistent batches.

## Files
- `mockups/`: all PNG mock-ups from the session
- `scripts/`: the Python (PIL/numpy) used to draw them. `recolor.py`/`leo_mock.py`/`stitch_mock.py`/`mock2.py` recolour her sketch `src.png`. `styles.py` has the drawing helpers + 4 silhouettes. `swatches.py` builds the fabric board. Paths take the folder as `argv[1]`.

## Next step
Ask Natalia which swatches to keep. Refine those (colour, scale, binding), then apply the shortlist to 2–3 shapes.
