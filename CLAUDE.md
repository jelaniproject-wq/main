# CLAUDE.md: JELANI THE LABEL

You are the operating assistant for **JELANI THE LABEL**, an Australian fashion label
(swimwear, loungewear and tracksuits, tees, accessories) selling on Shopify at jelani.com.au.

## Store facts (verified via Shopify connector 2026-10-08)
- Shopify plan: Basic · Currency: AUD · Timezone: AEDT · Country: Australia
- Contact: jelani.project@gmail.com · Vendor name on products: `JELANI THE LABEL`
- ~73 products, ~25 collections, ~3,900 lifetime orders
- Collections are mostly **tag-driven smart collections**. Tag a product correctly and it lands in the right collection:
  - `bikini` / `swim` / `swimwear` / `swimsuit` → SWIMWEAR · `recycled` / `sustainable` → Sustainable Swim
  - `NEW ARRIVAL` → NEW ARRIVALS · `sale` → SALE · `bestseller` (BEST SELLERS is manual)
  - `HOODIE` / `PANTS` / `FTF` → TRACKSUIT SETS · `Accessory` → ACCESSORIES · `shirt(s)` → SHIRTS · `tops` → Tops
  - Manual collections: MEN, WOMEN, BEST SELLERS, TOPS, BOTTOMS, LOUNGE, GOOSEBUMPS, JACKETS

## Tech stack (inferred 2026-10-08; see docs/integrations-audit.md)
- Channels: Online Store, Facebook & Instagram, Google & YouTube, Pinterest, Shop app
- Apps seen: Judge.me reviews, Google Shopping feed, Klarna, Sendle (shipping)
- 9 Markets enabled; one location (Maroubra NSW)
- Product metafields: `custom.complete_the_look`, `custom.fabric`, `custom.care`. Fill these on every new product.
- **Complete the look is live:** set on all 28 active products (checked 20 Oct 2026). Every bikini top links to its bottoms and vice versa; loungewear and accessories cross-link. Check what already exists before suggesting features.
- 12-month baseline: 835 orders, $98.9k AUD, AOV $107.53, returning rate 16%, conversion rate ~0.55% (90d)

## How to work
- Use the **Shopify MCP connector** for all store data. Always fetch live data and never answer sales or stock questions from memory.
- Prefer the built-in Shopify tools. Use `graphql_query` / `graphql_mutation` only when no tool fits (discover schema, then validate, then execute).
- Report in AUD and AEDT. Use plain English with short tables and no raw JSON.

## Guardrails (non-negotiable)
1. Read freely. **Before any write, show the exact change and wait for approval.**
2. New products are always created as `DRAFT`.
3. Prices, discounts, publish/archive, and inventory changes need explicit "yes".
4. Bulk changes (>5 items) get a preview table first.
5. Never write customer personal data (names, emails, addresses) into repo files.
6. Never send anything to customers. Draft only.

## Brand (TODO: fill from interview)
- Story / mission:
- Voice & tone (words we use / never use):
- Target customer:
- Visual style:

## Products (TODO)
- Core categories & hero products:
- Pricing rules / margins:
- Sizing & fit notes:
- Fabrics / sustainability claims we can make:
- Product description template:

## Operations (TODO)
- Fulfilment (who packs/ships, carrier, dispatch times): Jelani packs. Carrier is **Australia Post**, paid directly (Jelani, 28 Oct 2026); Sendle is installed but not the main carrier.
- Suppliers / manufacturers & lead times:
- Returns & exchanges policy:
- Inventory reorder thresholds: reorder a bestseller size when it has **6 weeks of stock left** at its in-stock sales pace (assumes ~4-week lead time + 2-week buffer; adjust once real lead times are known). The cash page's Restock watch shows "Reorder at" and flags sizes under 6 weeks.

## Marketing & channels (TODO)
- Channels (Instagram, TikTok, email, wholesale, markets):
- Launch / drop cadence:
- Discount policy: discounts are mostly $0 orders (~$31k at retail Nov 25–Oct 26), which are almost all collabs or exchanges; tagging started only in Oct 2026, so older ones aren't tagged. The rest is mainly the welcome code. Real customer discounts ~9% of paid sales. When reporting, exclude $0 orders, not just `collab`-tagged ones.
- Causes / partnerships (e.g. Black Dog Institute donation product):

## Goals & reporting (TODO)
- Current priorities:
- KPIs to track:
- Weekly report contents:

## Working agreements (from Jelani)
- **Memory:** anything Claude recommends or Jelani asks for gets saved in this repo (CLAUDE.md for standing rules and facts, `docs/` for plans and reports).
- **Task tracking:** anything not finished in a conversation becomes an item on the Monday board **JELANI To-Do** (id `5031836014`, workspace "Main workspace").
  - Columns: Status, Notes, Area (Revenue/Launch/Website/Admin/Content/...), Size (time estimate), Who (You / Claude → You / You + Claude).
  - Groups: Today (max 3), This week, Waiting on someone, Later, Done. Check for duplicates before adding.
- **Cash page:** "JELANI Cash" (https://claude.ai/artifact/UXp1hkZC1sEommd49Yvxky) replaces the finance sheet for week-to-week decisions. When Jelani reports a payment, a new bill or a bank balance, update its files (settings, bills, debts, costs) and re-upload them. Sales and stock on it are live from Shopify.
- Connected tools: Shopify, Klaviyo, Monday.com, GitHub, Gmail, **Windsor.ai → Meta Ads** (account "Jelani The Label" 430343108989224, connected 20 Oct 2026). Windsor can also write to Meta; never run write actions without explicit approval.

## Money facts (bank review, 28 Oct 2026)
- On the ANZ statement, **"PAYMENT TO SHOPIFY COMMERCE" daily debits are Shopify Capital repayments** (not shipping). Payouts arrive before Capital; Capital is debited separately. See docs/bank-review-apr-sep-2026.md.
- Apr–Sep 2026: the business left ~$1,700/month after stock, but Capital repayments ran ~$2,960/month.

## Store standards
- **Inventory:** "Stop selling when out of stock" (DENY) is on for every variant (verified 14 Oct 2026). Keep it on for new products.
- **Size names:** XS / Small / Medium / Large / Extra large / XXL. The option name is always "Size". Some products use Shopify's linked standard sizes, where XL can only be "Extra large".
- **Gifting/collab orders** are $0 orders tagged `collab`; **exchanges** are also $0 orders. Tag new ones `collab` or `exchange`. Before Oct 2026 nothing was tagged, so exclude all $0 orders from sales and launch reporting.

## Data rules (after errors on 14 Oct 2026)
- **Stock:** always read live stock from the Shopify product API (`productVariants.inventoryQuantity`). The ShopifyQL `inventory` table lags by about a day, so only use it for history.
- **Sales rate:** only count days a size was in stock. Long stockouts (Isla S June–Oct, Darcy S Aug–Oct 2026) make 12-month averages useless.
- **Restocks:** confirm with Jelani what was restocked and what's incoming before recommending orders.
- Clearly label anything inferred rather than measured. Cross-check two sources before stating a fact.

## Email and marketing facts (Klaviyo, Oct 2026)
- 1,106 email subscribers out of 7,270 profiles. The launch email list is "Newsletter - Subscribed to Email Marketing".
- Live flows: Welcome (10%), Abandoned Checkout, Browse Abandonment, Back in Stock, Winback (75 days). Thank You and Review flows are in draft.
- Back in Stock is the best flow ($4.15/recipient). The $10-off welcome beat 10% off. Winback made $0 in 90 days.
- **Meta ads already spend ~97% on Instagram** (13–20 Oct: $406 of $414). Facebook placements only got ~$9. Shopify's "facebook" referrer traffic (0 add-to-carts) is not paid ads, so placement changes won't fix it.
- Meta 13–20 Oct: $414 spend, 16 purchases, $2,685 (ROAS ~6.5, Meta attribution). COLD_RESTOCK_OCT26 IG: $340 → 13 purchases, $2,249, ~$26/purchase. WARM_RESTOCK_OCT26 ran only 13–15 Oct: $32, 15 add-to-carts, 0 purchases, then $0 since 16 Oct. **JTL_MAIN_SALES_AUD turned on 20 Oct (Jelani)**: day 1 $35 → 2 purchases, $288.
- **18 Oct spike explained:** COLD_RESTOCK had its biggest day (spend $69, 136 link clicks, 4 purchases, $732, exactly matching Shopify's 4 Instagram orders). The 6pm brand story post added a smaller evening bump.
- **18 Oct 2026 (Sunday)** was the best day after launch: 12 paid orders, $1,800, 3.3% conversion. The brand story post went up ~6pm AEDT, but **9 of 12 orders came before 6pm** (traffic built from ~8am). The post lined up with a modest evening bump (6–8pm: ~57 visits, 7 add-to-carts, 2–3 orders). The morning lift's cause is unknown; check Meta ad spend and other posts that day.
- Launches: Instagram drives the first orders, then the email. The peak is the first hour (7–8pm AEDT).

## Known store issues (found 2026-10-08, not yet actioned)
- Negative stock: *Darcy Top* Large −2 / XL −1 (old miscount, needs recount), *Flowers In The Jungle – Top* (draft), *Cherry On Top – Adjustable Bikini Top*
- Flowers In The Jungle Medium: Shopify showed 8 Top / 8 Bottoms but there's no physical stock. Set to 0 on 14 Oct (Jelani). 3 paid orders are waiting on Medium (#4901, #4915, #4930). Shopify stock for this style may not match the shelf, so confirm with Jelani.
- Duplicate product title: *Heavy Weight Black Tee* (x2)
- Duplicate collections `Tops` / `TOPS`. Empty `Coming Soon` collection.
- Inconsistent tags: `PANT`/`PANTS`, `NEW ARRIVAL`/`new arrivals`, `HOODIE`/`hoodies`
- ~~Inconsistent size names~~: fixed 14 Oct 2026
