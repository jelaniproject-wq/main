# Theme change log

## 2026-10-08: Speed pass 1 (on copy, not yet live)
- Duplicated live theme **October** (`191099338936`) as **October – speed** (`192394461368`, unpublished).
- Edited `layout/theme.liquid` in the copy only:
  - Removed Rivo reviews loader (`booster-apps-common` include). It also pulled in polyfill.io (compromised domain, 2024).
  - Removed Nosto tagging (`nosto-tagging` render). Nosto not in use.
  - YouTube iframe API now loads only on product pages with YouTube (`external_video`) media. No products currently have any.
    Uploaded product videos (5 products) use Plyr, so its CSS stays.
- Left in place (unused, harmless): `snippets/booster-apps-common`, `rev-widget`, `nosto-tagging`, `nosto-element`, `sections/nosto-placement`.

### Still to do
- Uninstall Rivo and Nosto apps in Shopify admin (app embeds may still inject scripts).
- Klarna `document.cloneNode(true)` on product/cart pages: check whether Klarna's current app embed still needs it.
- Trim `theme.css` (642 KB); move/deduplicate Meta Pixel.
- Publish the copy from Shopify admin after previewing (publishing is blocked for the connector).

## 2026-10-11: Speed pass on Restock + October (on copy, not yet live)
- Duplicated **Restock + October** (`192379322552`) as **Restock + October – speed** (`192484999352`, unpublished).
  This is the copy to publish with the bikini restock (planned Tue 13 Oct).
- `layout/theme.liquid` (same fixes as pass 1, plus Klarna):
  - Removed Rivo `booster-apps-common` include (also loaded polyfill.io). Reviews run on Judge.me (app embed).
  - Removed `nosto-tagging` render.
  - Removed legacy inline `KlarnaThemeGlobals` script (`document.cloneNode(true)` on product/cart).
    Klarna still works at checkout and its on-site messaging app block stays on product pages.
  - YouTube iframe API now loads only on product pages with YouTube media. Homepage video is Shopify-hosted.
- Afterpay on-site messaging block (same settings as live **October**) added to product templates:
  `product` (default), `product.bikinis` (Isla Bottoms), `product.camohat` (Camo Hat), `product.preorder`.
  Not added to `landing` / `with-tabs` (no products use them), `gift-card` or `quick-view`.

### Check in preview before publishing
- A bikini product, the Camo Hat and a tee: Afterpay **and** Klarna messages show under the price, amounts correct.
- Judge.me reviews still show; cart and checkout work; homepage video plays.

### Still to do
- Uninstall Rivo and Nosto apps in Shopify admin.
- Trim `assets/theme.css` (642 KB). Review duplicate Meta Pixel (hardcoded in layout and possibly via the Facebook channel).
