# PRD: Running JELANI THE LABEL with Claude Code

**Owner:** Jelani (jelani.project@gmail.com)
**Status:** Draft v1 (2026-10-08)
**Store:** JELANI THE LABEL · jelani.com.au · Shopify Basic · AUD · Australia (AEDT)

---

## 1. Goal

Use Claude Code as an operating partner for Jelani: it reads live store data, does routine
admin work, drafts content, and flags problems, while you stay in control of anything
customer-facing or money-related.

**What success looks like (first 30 days)**
- You can ask in plain English ("how did swim sell last week?", "draft the summer drop
  product pages", "what's low on stock?") and get correct answers from live Shopify data.
- Weekly admin (stock checks, tidying the catalogue, reports) takes less of your time.
- Claude never changes live prices, publishes products, or creates discounts unless you approve it.

## 2. Where things stand today

| Item | Status |
|---|---|
| Shopify connector (MCP) in Claude Code | **Connected and working.** Verified read access to the shop, products, collections and orders |
| GitHub repo `jelaniproject-wq/main` | Empty. It will hold `CLAUDE.md`, docs and later skills |
| `CLAUDE.md` (business brain) | Skeleton created. It gets filled in by the interview |
| Theme code | Not in the repo. Theme edits go through Shopify admin for now |

**What I found in the store (read-only check on 2026-10-08)**
- 73 products: 9 active on the first page, plus many drafts and archived items (swim, lounge/tracksuits, tees, accessories).
- 25 collections, including smart collections driven by tags (`bikini`, `swim`, `recycled`, `NEW ARRIVAL`, `sale`, `bestseller`, `goosebumps`, ...).
- About 3,900 orders in total. Recent orders are mostly $46–$140 AUD and all paid and fulfilled.
- Possible tidy-ups to confirm with you (nothing has been changed):
  - Negative stock on *Flowers In The Jungle – Top* (draft) and *Cherry On Top – Adjustable Bikini Top*.
  - Two products named *Heavy Weight Black Tee*.
  - Two "tops" collections (`Tops` and `TOPS`) and an empty `Coming Soon` collection.
  - Tags are inconsistent (`PANT` / `PANTS`, `NEW ARRIVAL` / `new arrivals`, `HOODIE` / `hoodies`).

## 3. The simplest path to getting set up

You don't need to write code, use an API key or build a custom app. Everything goes through
the official Shopify connector, which is already authorised.

| Step | What | Who | Effort |
|---|---|---|---|
| 1 | Connect Shopify to Claude | Done | — |
| 2 | Create `CLAUDE.md` with store facts and guardrails | Claude (done, skeleton) | — |
| 3 | **Interview**: brand, products, customers, operations, goals | You + Claude | ~30–45 min |
| 4 | Fill `CLAUDE.md` from the interview and commit it | Claude | 10 min |
| 5 | Try three everyday tasks: a sales report, a stock check, one product description | You + Claude | 15 min |
| 6 | Turn repeated tasks into slash-command skills (`/weekly-report`, `/new-product`, `/stock-check`) | Claude | Later, once usage settles |

Steps 1–5 are the whole minimum setup. Everything after that is optional.

## 4. What Claude can do through the connector

| Area | Read | Write (with your approval) |
|---|---|---|
| Products and variants | Search, details, inventory | Create (as drafts), edit copy/tags/prices, bulk status changes |
| Collections | List, rules, contents | Create, update, add products |
| Inventory | Levels by location | Set quantities |
| Orders | List, details, fulfilment and tracking | — (read only) |
| Customers | Search and segment by spend, orders, location, marketing opt-in | — |
| Analytics | ShopifyQL sales, product and order reports | — |
| Discounts | — | Percentage codes (start date and audience must be confirmed) |
| Anything else in the Admin API | GraphQL queries | GraphQL mutations. Shopify blocks refunds, gift cards, staff changes and publishing the live theme |

**Out of scope for now:** refunds, editing the live theme, sending emails or SMS to customers,
ad platforms, accounting, and third-party apps that have no connector. Each can be added
later as its own decision.

## 5. Guardrails (written into `CLAUDE.md`)

1. **Read freely, write carefully.** Before changing anything, Claude lists the exact change and waits for a "yes".
2. New products are always created as **DRAFT**.
3. Price changes, discounts, publishing or archiving, and stock adjustments always need explicit approval.
4. Bulk changes (more than 5 items) get a preview table first.
5. Customer personal data stays in the conversation. It is never written to the repo.
6. Always use live data. Claude never quotes sales or stock from memory.

## 6. Everyday use cases (to confirm in the interview)

- **Weekly pulse:** revenue, orders, average order value, best and worst sellers, compared with last week.
- **Stock watch:** low or negative stock, sold-out bestsellers, dead stock.
- **New drop:** product copy in Jelani's voice, tags, collections, SEO title and description, all created as drafts.
- **Catalogue hygiene:** tag clean-up, duplicates, empty collections, missing alt text and images.
- **Customer insight:** repeat buyers, top spenders, where customers are located.
- **Promotions:** plan and set up discount codes for launches and sales.
- **Content:** Instagram captions, emails, launch plans (drafted only, never sent).

## 7. Open questions (answered by the interview)

See the interview in the chat. Answers go into `CLAUDE.md`, sections "Brand", "Products",
"Customers", "Operations" and "Goals".
