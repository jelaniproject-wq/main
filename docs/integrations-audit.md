# Integrations audit: JELANI THE LABEL (2026-10-08)

This audit was read-only, done through the Shopify connector. The connector can't see the
installed-apps list, script tags or pixels, so the apps below were worked out from sales
channels, order sources, product metafields, store policies and analytics. **Confirm against
Shopify admin → Apps.**

## Store health, last 90 days
| Metric | Jelani | Typical fashion DTC |
|---|---|---|
| Sessions | 31,032 | — |
| Added to cart | 1,240 (4.0%) | 6–8% |
| Reached checkout | 560 (45% of carts) | 50–60% |
| Completed checkout | 170 (30% of checkouts) | 45–60% |
| Conversion rate | 0.55% | 1.2–2.5% |

| Metric | Last 12 months |
|---|---|
| Orders | 835 |
| Sales | $98,890 AUD |
| Average order value | $107.53 |
| Returning customer rate | 16% |

**Where orders came from (90 days):** Google search (49), direct or unknown (67),
jelani.com.au (31), Instagram (39), Shop app (5), Facebook, Klarna and Checkmate (1–2 each).
**No orders were attributed to email.**

## What's already in place
- **Sales channels:** Online Store, Facebook & Instagram, Google & YouTube, Pinterest, Shop app
- **Reviews:** Judge.me
- **Product feeds:** a Google Shopping feed app (`mm-google-shopping`) and the Meta catalogue
- **Payments:** Klarna (seen in referrers)
- **Coupon extension:** Checkmate (seen in referrers)
- **Markets:** 9 enabled (AU, NZ, US, UK, Canada, Germany, Euro, Singapore, International)
- **Shipping:** Sendle (named in the privacy policy). One location, in Maroubra.
- **Custom product data:** `complete_the_look`, `fabric`, `care` metafields, plus Shopify category attributes
- **Draft orders:** about 1 in 5 recent orders (gifting, influencers, wholesale or manual sales? To confirm)

## Gaps, by priority

### P1: biggest revenue impact
1. **Email and SMS marketing automation** (Klaviyo, or Shopify Email/Messaging to start). No email-attributed orders, yet the store has about 8,000 customer records. Core flows: welcome series, abandoned checkout, abandoned cart and browse, post-purchase, back in stock, win-back. *Klaviyo has an MCP connector, so Claude could build and report on flows directly.*
2. **Abandoned checkout recovery.** About 390 checkouts were abandoned in 90 days. Only 30% of people who reach checkout finish, about half the norm. Check shipping cost shown at checkout, payment options and the recovery email first.
3. **Afterpay.** It's the expected buy-now-pay-later option for Australian fashion. Klarna is visible; Afterpay isn't confirmed.
4. **Fix the policy pages (no app needed).** They still contain template placeholders:
   - Privacy policy: "[ADD OR SUBTRACT ANY OTHER TRACKING TECHNOLOGIES USED]", "[email address]", last updated 2021
   - Terms: "[LINK TO REFUND POLICY]", "[INSERT BUSINESS ADDRESS]", "[INSERT VAT NUMBER]" and others
   - Refund policy: add an Australian Consumer Law line ("this doesn't affect your rights for faulty items"), since "sale items are final" can't exclude refunds for faulty goods. Remove the leftover mention of candles.
   - Shipping policy: covers Australia only, but 9 markets are live. Add international rates, times, and duties and taxes.

### P2: conversion and retention
5. **Self-serve returns and exchanges.** Returns are handled by email today. Shopify's built-in self-serve returns is free; Loop or Rich Returns favour exchanges.
6. **Size guide and fit tool** for swimwear (Kiwi Sizing, or a metafield-driven size chart).
7. **Back-in-stock alerts.** Several bestsellers are sold out or have negative stock.
8. **Loyalty and referral program** (Smile.io, Rivo, or Shopify-native) to lift the 16% returning customer rate.
9. **Search and merchandising:** Shopify Search & Discovery (free) for filters, synonyms and product recommendations.
10. **Customer service inbox:** Shopify Inbox (free) or Gorgias, plus FAQ and order-tracking pages.

### P3: operations and insight
11. **Accounting:** connect Xero (or MYOB) to Shopify. *Xero has a Claude connector.*
12. **Tracking pixels:** confirm GA4, Meta pixel/CAPI, TikTok and Pinterest tags in Customer Events. I couldn't verify these from here.
13. **Branded shipment tracking and notifications** (Sendle tracking emails, or AfterShip/Parcel Panel).
14. **TikTok Shop / TikTok channel**, if TikTok is a marketing channel.
15. **Inventory and purchasing:** reorder points or a stock forecasting tool once supplier lead times are known.

## Making Claude more useful
Claude can only work with tools it has a connector for. Where you have a choice, prefer tools
with Claude connectors: Klaviyo, Gmail, Google Drive/Sheets, Xero, Canva, Notion.
Connect them in claude.ai → Settings → Connectors. Each one is a separate approval.
