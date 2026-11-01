"""The "pro" demo design: a dark, photo-led automotive page built for phones.

Made 2026-11-01 after the owner rejected the text-only demos. What it fixes:
- real photography (free Unsplash stock, labelled "صور توضيحية" until the shop sends its own)
- one small demo line at the top instead of the big badge, plus the footer note
- service cards with photos, a work gallery, a "how it works" strip instead of empty
  "price depends on car type" packages (packages only appear when real prices exist)
- real Google rating and review only; no invented numbers, names or prices
- booking form that opens a ready WhatsApp message, location card instead of a heavy map
- sticky WhatsApp + call dock with page padding so it never covers content
"""
import html

e = lambda s: html.escape(str(s), quote=True)

# Free Unsplash photos (Unsplash License: free for commercial use, no permission needed).
# Checked by eye 2026-11-01. key -> (photo id, short description)
PHOTOS = {
    "hero": ("1567808291548-fc3ee04dbcf0", "سيارة سوداء في ورشة مضاءة"),
    "sun": ("1485291571150-772bcfc10da5", "سيدان سوداء بزجاج مظلل"),
    "shield": ("1646531840695-62810bcd1171", "تركيب فيلم حماية على سيارة"),
    "drop": ("1770700391793-22fc46041c2b", "قطرات ماء على طلاء محمي"),
    "polish": ("1780558852670-3f49298ecc1f", "تلميع بماكينة البوليش"),
    "wash": ("1761312834150-4beefff097a7", "غسيل سيارة بالرغوة"),
    "seat": ("1771491237218-cbd4a707497e", "تنظيف داخلي تفصيلي"),
    "wrench": ("1708805282683-50a060eba80f", "تنظيف الجنوط"),
    "sparkle": ("1518306727298-4c17e1bf6942", "سيارة لامعة ليلاً"),
    "extra1": ("1554294314-80a5fb7e6bd5", "سيارة فاخرة سوداء"),
    "extra2": ("1758376316871-96e1feea03f4", "سيارة رياضية سوداء"),
}


def alt(key):
    return e(PHOTOS.get(key, PHOTOS["sparkle"])[1] + " (صورة توضيحية)")


def img(key, w=800):
    pid = PHOTOS.get(key, PHOTOS["sparkle"])[0]
    return f"https://images.unsplash.com/photo-{pid}?w={w}&q=70&auto=format&fit=crop"


STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg>'
WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3zm4.6 12.6c-.2.6-1.2 1.1-1.7 1.2-.5 0-1 .2-3.2-.7-2.7-1.1-4.4-3.9-4.5-4.1-.1-.2-1.1-1.5-1.1-2.8 0-1.3.7-2 1-2.3.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.8.9c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1z"/></svg>'
PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/></svg>'
CLOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'


def render(d, c, F, phone, pdisp, fonts_url, design_meta):
    """d = demo JSON, c = colours (designs.colors), F = font pair. Returns the full HTML page."""
    client = bool(d.get("client"))
    name = d["name"]
    city = d["city"]
    area = d.get("area") or ""
    loc = "، ".join(x for x in [area, city] if x)
    addr = d.get("address") or loc
    services = d["services"]
    svc_names = [s["title"] for s in services]
    rating, reviews = d.get("rating"), d.get("reviews")
    h1 = d.get("headline") or f"عناية احترافية بسيارتك في {city}"
    intro = d.get("intro") or f"{'، '.join(svc_names[:3])} في {loc}."
    wa = f"https://wa.me/{phone}"
    wa_hi = wa + "?text=" + __import__("urllib.parse").parse.quote("السلام عليكم، أبغى أستفسر عن خدماتكم")
    lat, lng = d.get("lat"), d.get("lng")
    q = f"{lat},{lng}" if lat and lng else e(d.get("maps_query") or (name + " " + city))
    maps = f"https://www.google.com/maps/search/?api=1&amp;query={q}"
    photos_note = "" if client else '<p class="note">الصور توضيحية، وتُستبدل بصور أعمالكم الحقيقية.</p>'

    # ---- hero ----
    rate_chip = ""
    if rating and reviews:
        rate_chip = (f'<a class="chip" href="{maps}" target="_blank" rel="noopener">{STAR}<b>{e(rating)}</b>'
                     f'<span>من {e(reviews)} تقييم على قوقل</span></a>')
    hero = f"""
<section class="hero">
  <img class="hero-img" src="{img('hero', 1000)}" alt="{alt('hero')}" fetchpriority="high">
  <div class="hero-in">
    {rate_chip}
    <h1>{e(h1)}</h1>
    <p class="lead">{e(intro)}</p>
    <div class="cta">
      <a class="btn primary" href="#book">{WA}احجز موعدك</a>
      <a class="btn ghost" href="tel:+{phone}">{PHONE}اتصل</a>
    </div>
  </div>
</section>"""

    # ---- quick facts ----
    facts = []
    if d.get("hours_short"):
        facts.append(f'<div class="fact">{CLOCK}<span>{e(d["hours_short"])}</span></div>')
    facts.append(f'<div class="fact">{PIN}<span>{e(loc)}</span></div>')
    facts_html = f'<div class="facts">{"".join(facts)}</div>'

    # ---- services ----
    cards = ""
    used = set()
    for s in services:
        key = s.get("photo") or s.get("icon") or "sparkle"
        if key in used:  # never show the same photo twice
            key = next((k for k in PHOTOS if k not in used and k != "hero"), "sparkle")
        used.add(key)
        txt = f'<p>{e(s["text"])}</p>' if s.get("text") else ""
        cards += (f'<article class="svc"><img src="{img(key, 600)}" alt="{alt(key)}" loading="lazy">'
                  f'<div class="svc-t"><h3>{e(s["title"])}</h3>{txt}</div></article>')
    services_html = f"""
<section id="services" class="sec">
  <h2>خدماتنا</h2>
  <div class="svcs">{cards}</div>
</section>"""

    # ---- gallery ----
    gkeys = [k for k in PHOTOS if k not in used and k != "hero"][:6]
    gallery = "".join(f'<img src="{img(k, 600)}" alt="{alt(k)}" loading="lazy">' for k in gkeys)
    gallery_html = f"""
<section id="work" class="sec">
  <h2>من أعمالنا</h2>
  <div class="strip">{gallery}</div>
  {photos_note}
</section>"""

    # ---- packages only with real prices, otherwise how-it-works ----
    packs = [p for p in (d.get("packs") or []) if p.get("price")]
    if packs:
        pk = "".join(
            f'<div class="pack{" pick" if p.get("pick") else ""}"><h3>{e(p["name"])}</h3><div class="price">{e(p["price"])}</div>'
            f'<ul>{"".join("<li>" + e(i) + "</li>" for i in p.get("items", []))}</ul></div>' for p in packs)
        middle = f'<section id="packs" class="sec"><h2>الباقات</h2><div class="packs">{pk}</div></section>'
    else:
        steps = [("اختر الخدمة", "من القائمة تحت أو راسلنا مباشرة."),
                 ("اكتب نوع سيارتك", "عشان نعطيك السعر والوقت المناسب."),
                 ("احجز موعدك", "يوصلنا طلبك على الواتساب ونرد عليك.")]
        st = "".join(f'<li><b>{i + 1}</b><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(steps))
        middle = f'<section class="sec"><h2>الحجز بثلاث خطوات</h2><ol class="steps">{st}</ol></section>'

    # ---- reviews (real ones only) ----
    rev_list = d.get("reviews_list") or ([{"text": d["review"]}] if d.get("review") else [])
    reviews_html = ""
    if rev_list or (rating and reviews):
        head = ""
        if rating and reviews:
            pct = max(0, min(100, float(rating) / 5 * 100))
            head = (f'<div class="score"><b>{e(rating)}</b><div><div class="stars" aria-label="{e(rating)} من 5">'
                    f'<div class="on" style="width:{pct:.0f}%">{STAR * 5}</div><div class="off">{STAR * 5}</div></div>'
                    f'<span>{e(reviews)} تقييم على خرائط قوقل</span></div></div>')
        qs = "".join(
            f'<blockquote><p>«{e(r["text"])}»</p>'
            f'<cite>{e(r.get("by") or "من تقييمات قوقل")}</cite></blockquote>' for r in rev_list)
        reviews_html = f'<section id="reviews" class="sec"><h2>وش يقولون عملاؤنا</h2>{head}{qs}</section>'

    # ---- booking ----
    options = "".join(f"<option>{e(n)}</option>" for n in svc_names)
    book_html = f"""
<section id="book" class="sec">
  <div class="book">
    <h2>احجز موعدك</h2>
    <p class="sub">اختر الخدمة ونوع سيارتك، وتنفتح لك رسالة جاهزة على واتساب.</p>
    <form id="form">
      <label>الخدمة<select id="svc">{options}</select></label>
      <label>نوع السيارة وموديلها<input type="text" id="car" placeholder="مثال: لكزس ES 2023" autocomplete="off" required></label>
      <label>الوقت المناسب<select id="tm"><option>الصباح</option><option selected>المساء</option></select></label>
      <label>الاسم<input type="text" id="nm" autocomplete="name"></label>
      <button class="btn primary wide" type="submit">{WA}أرسل الطلب على واتساب</button>
    </form>
  </div>
</section>"""

    # ---- location ----
    hours = d.get("hours") or []
    hours_html = "".join(f"<li>{e(h)}</li>" for h in hours)
    loc_html = f"""
<section id="map" class="sec">
  <h2>موقعنا</h2>
  <div class="loc">
    <div class="loc-row">{PIN}<div><b>{e(name)}</b><span>{e(addr)}</span></div></div>
    {f'<div class="loc-row">{CLOCK}<ul>{hours_html}</ul></div>' if hours_html else ''}
    <div class="loc-btns">
      <a class="btn primary" href="{maps}" target="_blank" rel="noopener">{PIN}الاتجاهات</a>
      <a class="btn ghost" href="tel:+{phone}" dir="ltr">{e(pdisp)}</a>
    </div>
  </div>
</section>"""

    demo_line = "" if client else '<div class="demo">تصميم مقترح للعرض • نموذج تجريبي</div>'
    foot_note = "" if client else f'<p>هذا تصميم مقترح للعرض فقط، وليس الموقع الرسمي لـ{e(name)}. الصور توضيحية وتُستبدل ببياناتكم.</p>'
    title = f"{e(name)} | {e('، '.join(svc_names[:3]))} في {e(city)}" + ("" if client else " (نموذج تجريبي)")
    robots = "" if client else '<meta name="robots" content="noindex, nofollow">\n'
    acc, at = c["accent"], c["accent_text"]
    latin_sub = e(d.get("latin_name") or "")

    css = f"""
:root{{--bg:{c['bg']};--s1:{c['surface']};--s2:{c['surface2']};--tx:{c['text']};--tx2:{c['text2']};--ln:{c['line']};
--ac:{acc};--at:{at};--d:"{F['display']}",system-ui,sans-serif;--t:"{F['text']}",system-ui,sans-serif;--dw:{F['dw']}}}
*{{box-sizing:border-box;margin:0}}html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--tx);font:16px/1.7 var(--t);-webkit-font-smoothing:antialiased;padding-bottom:84px;overflow-x:hidden}}
img{{display:block;max-width:100%}}a{{color:inherit}}
h1,h2,h3{{font-family:var(--d);font-weight:var(--dw);line-height:1.25}}
svg{{width:20px;height:20px;fill:currentColor;flex:none}}
.demo{{background:var(--s2);color:var(--tx2);text-align:center;font-size:.75rem;padding:4px 16px}}
header{{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:12px;
padding:12px 16px;background:var(--bg);background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--ln)}}
.logo{{font:var(--dw) 1.15rem/1.2 var(--d);min-width:0}}.logo small{{display:block;font:500 .7rem var(--t);color:var(--ac);letter-spacing:.08em}}
.call{{display:grid;place-items:center;width:44px;height:44px;border-radius:50%;background:var(--s2);border:1px solid var(--ln);color:var(--ac)}}
.hero{{position:relative;display:flex;flex-direction:column}}
.hero-img{{width:100%;height:46vh;min-height:260px;max-height:520px;object-fit:cover;object-position:50% 70%}}
.hero::before{{content:"";position:absolute;inset:0 0 auto 0;height:46vh;min-height:260px;max-height:520px;z-index:1;background:linear-gradient(180deg,rgba(0,0,0,0) 45%,var(--bg) 100%);pointer-events:none}}
.hero-in{{position:relative;z-index:2;padding:0 16px 24px;margin-top:-56px;width:100%;max-width:640px}}
.chip{{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:999px;background:rgba(0,0,0,.55);
border:1px solid rgba(255,255,255,.15);font-size:.85rem;text-decoration:none;color:#fff;margin-bottom:14px}}
.chip svg{{width:16px;height:16px;fill:#f5b400}}.chip span{{color:#d9d9de}}
h1{{font-size:clamp(1.8rem,7.6vw,2.8rem);color:var(--tx);margin-bottom:10px}}
.lead{{color:var(--tx2);font-size:1rem;margin-bottom:20px;max-width:34em}}
.cta{{display:flex;gap:10px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:50px;padding:0 20px;border-radius:12px;
font:600 1rem var(--t);text-decoration:none;border:1px solid transparent;cursor:pointer}}
.btn.primary{{background:var(--ac);color:var(--at);flex:1}}
.btn.ghost{{background:rgba(255,255,255,.06);border-color:var(--ln);color:var(--tx)}}
.btn.wide{{width:100%}}
.facts{{display:flex;flex-wrap:wrap;gap:8px;padding:4px 16px 8px}}
.fact{{display:flex;align-items:center;gap:6px;padding:8px 12px;border-radius:10px;background:var(--s1);border:1px solid var(--ln);font-size:.85rem;color:var(--tx2)}}
.fact svg{{color:var(--ac);width:16px;height:16px}}
.sec{{padding:36px 16px 8px;max-width:960px;margin:0 auto}}
h2{{font-size:1.6rem;margin-bottom:16px}}
h2::after{{content:"";display:block;width:36px;height:3px;border-radius:2px;background:var(--ac);margin-top:8px}}
.svcs{{display:grid;gap:12px;grid-template-columns:1fr 1fr}}
.svc{{background:var(--s1);border:1px solid var(--ln);border-radius:14px;overflow:hidden}}
.svc img{{width:100%;aspect-ratio:4/3;object-fit:cover}}
.svc-t{{padding:10px 12px 14px}}.svc h3{{font-size:1rem;margin-bottom:4px}}.svc p{{font-size:.82rem;color:var(--tx2);line-height:1.6}}
.svcs .svc:only-child,.svcs .svc:last-child:nth-child(odd){{grid-column:1/-1}}
.svcs .svc:last-child:nth-child(odd) img{{aspect-ratio:16/8}}
.strip{{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px 6px;scrollbar-width:none}}
.strip::-webkit-scrollbar{{display:none}}
.strip img{{flex:0 0 72%;aspect-ratio:4/5;object-fit:cover;border-radius:14px;scroll-snap-align:start}}
.note{{font-size:.78rem;color:var(--tx2);margin-top:8px}}
.steps{{list-style:none;padding:0;display:grid;gap:10px}}
.steps li{{display:flex;gap:14px;align-items:flex-start;background:var(--s1);border:1px solid var(--ln);border-radius:14px;padding:14px}}
.steps b{{display:grid;place-items:center;width:36px;height:36px;border-radius:50%;background:var(--ac);color:var(--at);font:700 1rem var(--d);flex:none}}
.steps h3{{font-size:1rem}}.steps p{{font-size:.85rem;color:var(--tx2)}}
.packs{{display:grid;gap:12px}}.pack{{background:var(--s1);border:1px solid var(--ln);border-radius:14px;padding:16px}}
.pack.pick{{border-color:var(--ac)}}.pack .price{{color:var(--ac);font:700 1.3rem var(--d);margin:4px 0 8px}}
.pack ul{{padding-inline-start:18px;color:var(--tx2);font-size:.9rem}}
.score{{display:flex;align-items:center;gap:14px;margin-bottom:12px}}
.score>b{{font:800 2.6rem/1 var(--d);color:var(--tx)}}.score span{{font-size:.85rem;color:var(--tx2)}}
.stars{{position:relative;width:100px;height:18px}}.stars>div{{position:absolute;inset:0;display:flex;gap:2px;overflow:hidden;white-space:nowrap}}.stars svg{{width:18px;height:18px}}.stars .on{{z-index:1}}.stars .on svg{{fill:#f5b400}}.stars .off svg{{fill:var(--ln)}}
blockquote{{background:var(--s1);border:1px solid var(--ln);border-radius:14px;padding:16px;margin-bottom:10px}}
blockquote p{{font-size:1rem;margin:0 0 8px}}cite{{font-style:normal;font-size:.8rem;color:var(--tx2)}}
.book{{background:var(--s1);border:1px solid var(--ln);border-radius:18px;padding:20px 16px}}
.book h2{{margin-bottom:6px}}.book .sub{{color:var(--tx2);font-size:.9rem;margin-bottom:16px}}
form{{display:grid;gap:12px}}label{{display:grid;gap:6px;font-size:.88rem;font-weight:600}}
select,input{{width:100%;min-height:48px;padding:0 12px;border-radius:10px;border:1px solid var(--ln);background:var(--bg);color:var(--tx);font:16px var(--t)}}
select:focus,input:focus,.btn:focus-visible,.call:focus-visible,.chip:focus-visible{{outline:2px solid var(--ac);outline-offset:2px}}
.loc{{background:var(--s1);border:1px solid var(--ln);border-radius:18px;padding:16px;display:grid;gap:14px}}
.loc-row{{display:flex;gap:10px;align-items:flex-start}}.loc-row svg{{color:var(--ac);margin-top:4px}}
.loc-row b{{display:block}}.loc-row span,.loc-row ul{{color:var(--tx2);font-size:.9rem}}.loc-row ul{{list-style:none;padding:0}}
.loc-btns{{display:flex;gap:10px}}.loc-btns .btn{{flex:1;padding:0 12px}}
footer{{text-align:center;padding:32px 16px 16px;color:var(--tx2);font-size:.8rem;border-top:1px solid var(--ln);margin-top:36px}}
footer b{{display:block;color:var(--tx);font:var(--dw) 1rem var(--d);margin-bottom:4px}}footer p{{margin-top:6px}}
.dock{{position:fixed;inset:auto 0 0 0;z-index:30;display:flex;gap:10px;padding:10px 16px calc(10px + env(safe-area-inset-bottom));
background:var(--bg);background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(10px);border-top:1px solid var(--ln)}}
.dock{{transform:translateY(110%);transition:transform .25s ease}}.dock.on{{transform:none}}
.dock .primary{{flex:1}}.dock .ghost{{width:52px;padding:0}}
@media (min-width:760px){{.svcs{{grid-template-columns:repeat(3,1fr)}}.strip img{{flex-basis:30%}}.hero-in{{padding:48px 32px}}
.dock{{display:none}}body{{padding-bottom:0}}}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}.dock{{transition:none}}}}
"""

    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
{robots}<meta name="design" content="{design_meta}">
<meta name="description" content="{e(name)}: {e('، '.join(svc_names))} في {e(loc)}.">
<meta name="theme-color" content="{c['bg']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link href="{fonts_url}" rel="stylesheet">
<style>{css}</style>
</head>
<body>
{demo_line}
<header>
  <div class="logo">{e(name)}{f'<small>{latin_sub}</small>' if latin_sub else ''}</div>
  <a class="call" href="tel:+{phone}" aria-label="اتصل بنا">{PHONE}</a>
</header>
<main>
{hero}
{facts_html}
{services_html}
{gallery_html}
{middle}
{reviews_html}
{book_html}
{loc_html}
</main>
<footer>
  <b>{e(name)}</b>
  <span>{e(addr)}</span>
  {foot_note}
</footer>
<nav class="dock" aria-label="تواصل سريع">
  <a class="btn primary" href="{wa_hi}" target="_blank" rel="noopener">{WA}احجز بالواتساب</a>
  <a class="btn ghost" href="tel:+{phone}" aria-label="اتصل">{PHONE}</a>
</nav>
<script>
(function(){{var dk=document.querySelector('.dock'),h=document.querySelector('.hero');
  if('IntersectionObserver' in window){{new IntersectionObserver(function(es){{dk.classList.toggle('on',!es[0].isIntersecting);}}).observe(h);}}else{{dk.classList.add('on');}}}})();
document.getElementById('form').addEventListener('submit',function(ev){{ev.preventDefault();
  var v=function(id){{return document.getElementById(id).value.trim();}};
  var t='السلام عليكم، أبغى أحجز موعد لخدمة '+v('svc')+(v('car')?' لسيارة '+v('car'):'')+'، الوقت المناسب: '+v('tm')+(v('nm')?'. الاسم: '+v('nm'):'')+'.';
  window.open('{wa}?text='+encodeURIComponent(t),'_blank');}});
</script>
</body>
</html>
"""
