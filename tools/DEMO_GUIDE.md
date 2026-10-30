# Concept demo in 15 minutes

Every prospect gets a homepage concept built from their real Google Maps listing.
It is a sales sample, not their website: it is labelled "تصميم مقترح للعرض (نموذج تجريبي)",
says in the footer that it is not their official site, and carries `noindex`.

## Steps

1. **Research (3 min).** From their Google Maps listing take only real facts:
   name as on their sign, services, area and address, hours, phone, rating and
   review count, coordinates from the URL, one short real review (original Arabic).
   Check whether the Maps website button is missing, broken or points to social media.
2. **Write the input (5 min).** Copy `demo_example.json` to `demos/<slug>.json`
   (`<slug>` = short lowercase latin name). Leave out anything you don't know.
   Never invent prices, packages, slogans, awards or reviews; without real prices
   the page shows "السعر حسب نوع السيارة".
3. **Build (1 min).** `python3 tools/make_demo.py tools/demos/<slug>.json`
   writes `sample/demos/<slug>/index.html`. The design (7 layouts, fonts, corners,
   palettes) is picked so neighbouring shops never look alike. To choose one:
   `"design": {"layout": "showroom"}`; `"theme": "dark"` or `"light"`.
4. **Check (3 min).** Open it at phone width (390 px): no sideways scroll, name
   and services correct, the label visible at the top.
5. **Publish (2 min).** Commit both files and push to `main`; Cloudflare Pages
   publishes `https://carcare-sample.pages.dev/demos/<slug>/` within a minute.
   Confirm the deployment succeeded before sending the link.

## Rules

- A demo is never published as the customer's official site. A client site is built
  only after the deposit, with `"client": true` (no label, no noindex) in `clients/<slug>/`.
- Use the customer's logo or photos only after they send them.
- Keep free work per prospect to about 15 minutes; anything more waits for the deposit.
