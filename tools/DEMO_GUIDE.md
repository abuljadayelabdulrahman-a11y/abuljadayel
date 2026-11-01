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
   Write the `headline`, `intro` and `brand_sub` fresh for this shop, never copied from
   another demo or the example (see "Every site is different" below).
   Never invent prices, packages, slogans, awards or reviews; without real prices
   the page shows "السعر حسب نوع السيارة".
3. **Build (1 min).** First sync the demos already published on the Cloudflare Worker
   (list the KV keys of namespace c2697f0e83a54a778107e0a3ffbcbafb, then
   `python3 tools/sync_published.py <every key>`), so the builder compares against them
   too. Then `python3 tools/make_demo.py tools/demos/<slug>.json`
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

## Default design: "pro" (2026-11-01)

The owner rejected the old text-only designs. Every new demo now uses the `pro` layout
(`tools/pro_template.py`): dark, photo-led, phone-first. It uses free Unsplash photos
labelled "صور توضيحية" (no shop photos until they send them), one small demo line, real
Google rating and review only, a "3 steps" strip instead of empty packages (packages only
show with real prices), a WhatsApp booking form and a location card. Choose the colour with
`"design": {"palette": "obsidian-gold"}` (dark palettes only) and add `"latin_name"` for the
English line under the name. Before any demo link goes to a customer, check it at 390 px and
get the owner's OK on the first demos built with this design.

## Every site is different (owner, 2026-11-01)

The owner wants a unique website and animation on every site. The same PPF wording,
photos and layout kept appearing on every demo; that must not happen again.

- **Content comes only from this shop.** List only services on its real listing, in the
  order that matters for *this* shop. PPF (or any service) appears only if the shop
  really offers it, and leads only if it is clearly their main thing. Lead with what
  makes them different (their speciality, area, a detail from their reviews).
- **Own words every time.** The headline and intro are written for this shop. The
  builder refuses a new demo with no headline, with a stock line used before
  ("اختر الخدمة واكتب نوع سيارتك"، "وتوصلنا رسالتك على الواتساب مباشرة"،
  "حيث تلتقي الفخامة بالحماية"، "عناية احترافية بسيارتك في") or with five words in a
  row copied from another demo. Rewrite until it passes; don't add the slug to get round it.
- **Own design.** Within "pro" each site gets a different look (page structure: split,
  full, frame, editorial), hero photo and signature animation (water beads, foam, light
  sweep, film, tint, slow zoom, word-by-word headline, car outline drawing, 3D cards,
  rating count-up), on top of its own fonts, corners and palette. The builder picks the
  least-used of each and prefers animations that fit the shop's services. Force one with
  `"design": {"look": "frame", "sig": "foam"}` only when there's a reason.
- **Relevant photos only.** The gallery shows neutral car photos and photos of services
  the shop offers, never a service it doesn't do.
- **Check the log.** Every build updates `tools/DESIGN_LOG.md` (each site's layout,
  look, animation, hero photo, fonts, shape, palette). `python3 tools/make_demo.py --log`
  prints it. Before sending, compare the new demo with the last few: if it still feels
  like the same site, change the look or animation.
- Demos already sent to customers are not rebuilt or changed.
