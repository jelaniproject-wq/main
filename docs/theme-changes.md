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
