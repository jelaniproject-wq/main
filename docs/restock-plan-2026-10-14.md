# Restock tracking: corrected 14 Oct 2026

> **The first version of this file was wrong and has been replaced.** It worked out "months of cover" from 12-month sales averages, but those averages include long stretches where sizes were out of stock (Isla Small was at 0 from at least mid-June to 13 Oct; Darcy Small was at 0 from Aug to 13 Oct). It also used Shopify's analytics stock table, which lags live stock by about a day.

## What was restocked on 13 Oct (from stock history)
| Style | Sizes restocked (units added) | Not restocked |
|---|---|---|
| Scout Top | XS +35, Small +56, Medium +50, Large +20 | — |
| Scout Bottoms | XS +30, Small +50, Medium +50, Large +20 | — |
| Darcy Top / Bottoms | **Small only** (+58 / +57) | Medium (2–3 left since early Sept), Large, XL |
| Isla Top / Bottoms | **Small only** (+50 / +50) | Medium, Large, XL |

## Live stock (Shopify product API, 14 Oct) and sold since the restock (~2 days, includes gifted `collab` units)
| Variant | Live stock | Sold since restock |
|---|---|---|
| Darcy Top Small | 41 | ~17 |
| Darcy Bottoms Small | 41 | ~15 |
| Darcy Top / Bottoms Medium | **0 / 0** | last 2 / 3 went at launch |
| Darcy Top Large / XL | −2 / −1 | old miscount, needs recount |
| Scout Top XS / S / M / L | 24 / 44 / 48 / 18 | 11 / 13 / 1 / 2 |
| Scout Bottoms XS / S / M / L | 23 / 44 / 47 / 35 | 7 / 6 / 2 / 0 |
| Isla Top / Bottoms Small | 46 / 46 | 7 / 7 (incl. 2 gifted) |
| Flowers In The Jungle Top S / M / L / XS | **0** / 9 / 13 / 46 | — |
| Flowers In The Jungle Bottoms S / M / L / XS | **0** / 9 / **0** / 46 | — |
| Romi | restock on the way (Jelani) | — |

## Method from now on
1. Use **live stock** from the Shopify product API, never the analytics stock table.
2. Measure the sales rate **only over days a size was in stock**.
3. Day 1–2 after a launch is a spike, so base forecasts on **day 7 and day 14** sell-through.
4. Ask Jelani what was restocked and what's incoming rather than inferring it.
5. Label anything inferred (not measured) as an assumption.

## Next check-ins
- **Tue 20 Oct (day 7):** units sold per in-stock day for each size, then projected sell-out dates.
- **Tue 27 Oct (day 14):** firm reorder recommendation with dates, once lead times are known.
- Jelani's target: sell through Isla Small in 1–2 months. That needs ~23–46 a month per piece (about 5–11 a week).

## Still needed from Jelani
Lead time per supplier, minimum order quantities, unit costs, and incoming Romi and new-style quantities by size.
