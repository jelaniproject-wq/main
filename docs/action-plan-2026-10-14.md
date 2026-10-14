# Action plan: 14 Oct 2026 (after the Restock launch)

Everything here is tracked on the Monday board **JELANI To-Do** (id 5031836014), group "This week".

## Done in this session
- **Stop selling when out of stock:** checked. It's already ON (DENY) for all 247 variants and every active variant tracks inventory. No change needed.
- **Size names standardised** on 42 products (8 active, 21 draft, 13 archived). The standard is now **XS / Small / Medium / Large / Extra large / XXL**.
  - "Extra large" was used instead of "XL" because Darcy Top, Isla Top, Romi Top, both KALANI products and the Bomber use Shopify's linked standard size list, which can't be renamed.
  - Variant IDs, stock, prices and back-in-stock subscriptions are unchanged.
  - Exception: the archived From The Heavens Bundle keeps its two option names ("Terry Short (Size)" / "Terry Shirt (Size)") because a product can't have two options both called "Size".
- **Correction to the launch report:** Darcy L/XL negative stock was **not** caused by the launch. No launch order bought those sizes, so it's an old miscount that needs a physical recount.

## Back-in-stock demand (Klaviyo, last 180 days)
The back-in-stock form and flow are both **live**. The flow is the best performing one: 13.9% click rate and $4.15 per recipient.

| Product / size | Signups | Stock now |
|---|---|---|
| Scout Top XS | 50 | 30 |
| Scout Bottoms Small | 31 | 50 |
| Scout Top Small | 22 | ~50 |
| Scout Bottoms XS | 21 | 30 |
| Darcy Bottoms Small | 19 | ~41 |
| Darcy Top Small | 17 | ~41 |
| Flowers In The Jungle – Sustainable Top XS (draft product) | 16 | — |
| Flowers In The Jungle – Sustainable Bottoms XS (draft product) | 15 | — |
| Romi Bottoms Small | 15 | **1** |
| Camo Hat | 14 | 96 |
| Scout Bottoms / Top Medium | 13 / 12 | 49 |
| Darcy Top Large / XL | 4 / 2 | **−2 / −1** |

Scout and Darcy demand was mostly met by the restock. Still open: Romi, Darcy M/L/XL, and the draft sustainable FITJ set.

## Meta ads: push spend to Instagram
- In Meta, Facebook and Instagram are **placements** inside the same ad set. Untick the Facebook placements and Instagram keeps running.
- Steps:
  1. Ads Manager → ad set → Placements → Manual. Keep IG Feed, Stories, Reels and Explore. Untick Facebook, Audience Network and Messenger.
  2. Safer option: duplicate the ad set, make the copy Instagram-only, and run both for 3 days.
  3. Objective: Sales, optimised for **Purchase** (not Traffic or Link clicks).
  4. Add a retargeting ad set: site visitors and IG engagers from the last 30 days, excluding purchasers, using Darcy and Scout creative.
- Evidence (13–14 Oct): Instagram had 173 sessions, a 5.8% conversion rate and $1,577 in sales. Facebook had 145 sessions and 0 add-to-carts.

## Email flows (Klaviyo, last 90 days)
| Flow | Status | Sent | Orders | $ per recipient | Note |
|---|---|---|---|---|---|
| Back in Stock | live | 237 | 7 | $4.15 | Best flow |
| Abandoned Checkout | live | 242 | 4 | $2.73 | **Email 1: 53 opens, 0 clicks. Check the button link** |
| Welcome (10%) | live | 831 | 7 | $1.34 | The old $10-off version got $2.14 (email 1: 4.0% vs 1.55% conversion) |
| Browse Abandonment | live | 230 | 2 | $0.88 | |
| Winback (75 days) | live | 848 | **0** | $0 | 45% open but 0.85% click |
| Thank You / Review | draft | — | — | — | Turn on for the 25 new customers |

### Winback rebuild
1. **Trigger:** use the metric Placed Order, wait 75 days, and filter on "Placed Order zero times since starting this flow". Today it's "Added to List", which depends on someone populating that list.
2. **Email 1:** what's new (Scout/Darcy restock), using product blocks and no discount.
3. **Email 2 (+7 days):** personalised by what they bought before. Keep the swim split and add reviews or UGC.
4. **Email 3 (+7 days):** free shipping or $10 off, with a 72-hour deadline.
5. Delete the old duplicate "Customer Winback" flow.

## Growing the email list (1,106 subscribed out of 7,270 Klaviyo profiles)
1. **Checkout opt-in:** Shopify Settings → Checkout → Marketing options → show the email sign-up box.
2. **Back-in-stock form:** add a "keep me updated" opt-in. 139 recent back-in-stock signups aren't subscribed.
3. **VIP early access:** drops go to subscribers 1 hour early. Promote it on IG Stories, the broadcast channel and the link in bio. This is the strongest hook for a drop-based brand.
4. **Pop-up:** test $10 off, add an SMS step, and design for mobile first (72% of launch traffic was mobile).
5. **Creators:** collab/gifting creators run a giveaway with entry through a Klaviyo form.
6. **Meta lead ads:** sync them to Klaviyo (the "Filled Out Lead Ad" metric already exists).
7. Only email people who have opted in (Spam Act 2003).
