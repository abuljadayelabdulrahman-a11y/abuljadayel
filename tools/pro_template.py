"""The "pro" demo design: a dark, photo-led automotive page built for phones.

Made 2026-11-01 after the owner rejected the text-only demos. What it fixes:
- real photography (free Unsplash stock, labelled "صور توضيحية" until the shop sends its own)
- one small demo line at the top instead of the big badge, plus the footer note
- service cards with photos, a work gallery, a "how it works" strip instead of empty
  "price depends on car type" packages (packages only appear when real prices exist)
- real Google rating and review only; no invented numbers, names or prices
- booking form that opens a ready WhatsApp message, location card instead of a heavy map
- sticky WhatsApp + call dock with page padding so it never covers content

Uniqueness (owner, 2026-11-01: "unique website and animations on every site"): inside this
design every site gets its own look (page structure), hero photo and signature animation,
picked by designs.pick_design so no two sites match. The gallery only shows photos of
services the shop really offers plus neutral car photos (no PPF photo for a shop without PPF).
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


NEUTRAL = {"hero", "sparkle", "extra1", "extra2"}

# section order and headings per look
ORDER = {"split": ["services", "gallery", "middle", "reviews"],
         "full": ["services", "middle", "gallery", "reviews"],
         "frame": ["reviews", "services", "gallery", "middle"],
         "editorial": ["services", "reviews", "gallery", "middle"]}
TITLES = {"split": dict(services="خدماتنا", work="من أعمالنا", reviews="وش يقولون عملاؤنا"),
          "full": dict(services="وش نقدم لسيارتك", work="أجواء الشغل", reviews="كلام عملائنا"),
          "frame": dict(services="خدماتنا", work="لقطات", reviews="تقييمات عملائنا"),
          "editorial": dict(services="الخدمات", work="معرض الصور", reviews="من تقييمات قوقل")}

# ---- looks: the same content in a different page structure ----
LOOK_CSS = """
.look-full .hero-img{height:74vh;min-height:460px;max-height:760px;object-position:58% 50%}
.look-full .shade{background:linear-gradient(180deg,rgba(0,0,0,.25) 0%,rgba(0,0,0,.1) 35%,var(--bg) 96%)}
.look-full .hero-in{position:absolute;inset:auto 0 0 0;margin:0;max-width:none;padding-bottom:28px}
.look-full .svcs{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px 6px;scrollbar-width:none}
.look-full .svcs::-webkit-scrollbar{display:none}
.look-full .svc,.look-full .svcs .svc:last-child:nth-child(odd){flex:0 0 78%;scroll-snap-align:start;grid-column:auto}
.look-full .svc img,.look-full .svcs .svc:last-child:nth-child(odd) img{aspect-ratio:4/5}
.look-full .strip{display:grid;grid-template-columns:1fr 1fr;overflow:visible;margin:0;padding:0}
.look-full .strip img{aspect-ratio:1}.look-full .strip img:first-child{grid-column:1/-1;aspect-ratio:16/9}
.look-frame .hero-in{order:-1;margin-top:0;padding-top:28px}
.look-frame .hero-media{margin:0 16px;border-radius:22px;border:1px solid var(--ac)}
.look-frame .shade{display:none}.look-frame .hero-img{height:38vh;min-height:220px}
.look-frame h2::after{width:100%;height:1px;opacity:.5}
.look-frame .svcs{grid-template-columns:1fr}
.look-frame .svc{display:flex;align-items:center}
.look-frame .svc img,.look-frame .svcs .svc:last-child:nth-child(odd) img{width:36%;aspect-ratio:1;flex:none}
.look-frame .strip img{flex-basis:58%;aspect-ratio:3/4;border-radius:999px 999px 14px 14px}
.look-editorial .hero-in{order:-1;margin-top:0;padding-top:30px;position:relative}
.look-editorial .hero-in::before{content:attr(data-latin);position:absolute;inset:6px 16px auto auto;font:800 clamp(2.4rem,13vw,5rem)/1 Montserrat,sans-serif;color:transparent;-webkit-text-stroke:1px var(--ln);white-space:nowrap;overflow:hidden;max-width:calc(100% - 32px);z-index:-1}
.look-editorial h1{font-size:clamp(2.2rem,10vw,3.6rem)}
.look-editorial .hero-media{margin:0 16px;border-radius:6px}.look-editorial .shade{display:none}
.look-editorial .hero-img{height:auto;aspect-ratio:16/10;min-height:0}
.look-editorial h2{font-size:2rem}.look-editorial h2::after{display:none}
.look-editorial .svcs{grid-template-columns:1fr;counter-reset:s;gap:18px}
.look-editorial .svc{background:none;border:0;border-top:1px solid var(--ln);border-radius:0;padding-top:14px;counter-increment:s}
.look-editorial .svc img,.look-editorial .svcs .svc:last-child:nth-child(odd) img{aspect-ratio:16/9;border-radius:6px}
.look-editorial .svc-t{padding:10px 0 0}.look-editorial .svc-t::before{content:"0" counter(s);font:700 .8rem Montserrat,sans-serif;color:var(--ac);letter-spacing:.12em}
.look-editorial .strip{display:block;columns:2;column-gap:10px;overflow:visible;margin:0;padding:0}
.look-editorial .strip img{width:100%;margin-bottom:10px;border-radius:6px;aspect-ratio:3/4;break-inside:avoid}
.look-editorial .strip img:nth-child(even){aspect-ratio:1}
@media (min-width:760px){
.look-full .svc,.look-full .svcs .svc:last-child:nth-child(odd){flex-basis:32%}
.look-frame .svcs{grid-template-columns:1fr 1fr}.look-frame .hero-img{height:56vh}
.look-editorial .svc{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:center}
.look-editorial .svc:nth-child(even) img{order:2}.look-editorial .strip{columns:3}}
"""

# ---- signature animations: one per site ----
SIG_CSS = """
.fx-beads i,.fx-foam i{position:absolute;border-radius:50%;opacity:0}
.fx-beads i{background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.95) 0 10%,rgba(255,255,255,.3) 28%,rgba(255,255,255,.06) 58%,transparent 70%);box-shadow:0 2px 3px rgba(0,0,0,.35);animation:bead 7s ease-in infinite}
@keyframes bead{0%{opacity:0;transform:scale(.3)}12%{opacity:1;transform:scale(1)}65%{opacity:1;transform:translateY(0)}100%{opacity:0;transform:translateY(70px) scaleY(1.3)}}
.fx-foam i{bottom:-30px;border:1px solid rgba(255,255,255,.55);background:radial-gradient(circle at 30% 30%,rgba(255,255,255,.5),rgba(255,255,255,.05) 60%);animation:foam 6s linear infinite}
@keyframes foam{0%{opacity:0;transform:translate(0,0)}10%{opacity:.9}50%{transform:translate(12px,-28vh)}100%{opacity:0;transform:translate(-8px,-56vh)}}
.fx-sweep::after{content:"";position:absolute;top:0;bottom:0;left:-50%;width:35%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.22),transparent);transform:skewX(-18deg);animation:sweep 5.5s ease-in-out 1s infinite}
@keyframes sweep{0%{left:-50%}45%,100%{left:130%}}
.fx-film::after,.fx-tint::after{content:"";position:absolute;inset:0;clip-path:inset(0 0 0 100%);animation:film 2.4s cubic-bezier(.6,.1,.2,1) .5s forwards}
.fx-film::after{background:linear-gradient(105deg,rgba(255,255,255,.14),rgba(255,255,255,.02) 40%,rgba(255,255,255,.16) 62%,rgba(255,255,255,.03))}
.fx-tint::after{background:linear-gradient(90deg,rgba(4,6,10,.62),rgba(4,6,10,.35))}
.fx-film b,.fx-tint b{position:absolute;top:0;bottom:0;left:100%;width:2px;background:linear-gradient(transparent,rgba(255,255,255,.9),transparent);box-shadow:0 0 14px rgba(255,255,255,.6);animation:edge 2.4s cubic-bezier(.6,.1,.2,1) .5s forwards}
@keyframes film{to{clip-path:inset(0)}}@keyframes edge{90%{opacity:1}to{left:0;opacity:0}}
.sig-zoom .hero-img{animation:kb 14s ease-out both;transform-origin:60% 70%}
@keyframes kb{from{transform:scale(1.18)}to{transform:scale(1)}}
.sig-kinetic h1 .w{display:inline-block;opacity:0;transform:translateY(.55em);animation:wordin .6s cubic-bezier(.2,.7,.2,1) forwards;animation-delay:calc(var(--i)*110ms + 150ms)}
@keyframes wordin{to{opacity:1;transform:none}}
.drawcar{display:block;width:100%;max-width:380px;height:auto;margin-top:22px}
.drawcar path,.drawcar circle{fill:none;stroke:var(--ac);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.6s ease-in-out .4s forwards}
.drawcar circle{animation-delay:2s;animation-duration:1s}
@keyframes draw{to{stroke-dashoffset:0}}
.sig-tilt .svcs{perspective:900px}
.sig-tilt .js .svc{opacity:0;transform:rotateX(16deg) translateY(28px);transition:opacity .6s ease,transform .7s cubic-bezier(.2,.7,.2,1)}
.sig-tilt .js .svc.in{opacity:1;transform:none}
.sig-countup .stars .on{transition:width 1.4s ease-out}
@media (prefers-reduced-motion:reduce){.fx{display:none}
.sig-zoom .hero-img,.sig-kinetic h1 .w,.drawcar path,.drawcar circle{animation:none;opacity:1;transform:none;stroke-dashoffset:0}
.sig-tilt .js .svc{opacity:1;transform:none;transition:none}}
"""

CAR = ('<svg class="drawcar" viewBox="0 0 400 110" aria-hidden="true">'
       '<path pathLength="1" d="M12 88H40M86 88H286M332 88H388V72Q386 62 362 58L306 52Q276 26 244 19L156 17Q122 19 98 42L44 52Q16 58 12 74Z"/>'
       '<path pathLength="1" d="M112 44Q130 27 156 26L200 25V46ZM212 25L240 27Q262 33 284 50L212 48Z"/>'
       '<circle pathLength="1" cx="63" cy="88" r="20"/><circle pathLength="1" cx="309" cy="88" r="20"/></svg>')

SIG_JS = {
    "tilt": """<script>(function(){if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window))return;
var w=document.querySelector('.svcs');w.classList.add('js');var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){
setTimeout(function(){x.target.classList.add('in')},[].indexOf.call(w.children,x.target)%3*120);io.unobserve(x.target);}})},{threshold:.2});
[].forEach.call(w.children,function(c){io.observe(c);});})();</script>""",
    "countup": """<script>(function(){if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window))return;
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(!x.isIntersecting)return;io.unobserve(x.target);var el=x.target,t=parseFloat(el.dataset.n),d=(el.dataset.n.split('.')[1]||'').length,s=null;
function f(ts){if(!s)s=ts;var p=Math.min(1,(ts-s)/1400);el.textContent=(t*(1-Math.pow(1-p,3))).toFixed(d);if(p<1)requestAnimationFrame(f);}requestAnimationFrame(f);
var st=el.parentNode.querySelector('.stars .on');if(st){var w=st.style.width;st.style.width='0';requestAnimationFrame(function(){requestAnimationFrame(function(){st.style.width=w;});});}});});
[].forEach.call(document.querySelectorAll('[data-n]'),function(el){io.observe(el);});})();</script>""",
}


def sig_markup(sig, seed):
    """Return (overlay html inside the hero photo, extra html under the hero buttons)."""
    import hashlib
    rnd = lambda i, n: int(hashlib.md5(f"{seed}{sig}{i}".encode()).hexdigest(), 16) % n
    if sig == "beads":
        dots = "".join(f'<i style="left:{rnd(i, 92) + 3}%;top:{rnd(i + 50, 70) + 5}%;width:{rnd(i + 99, 9) + 6}px;height:{rnd(i + 99, 9) + 6}px;animation-delay:{rnd(i + 7, 60) / 10}s"></i>' for i in range(16))
        return f'<div class="fx fx-beads">{dots}</div>', ""
    if sig == "foam":
        dots = "".join(f'<i style="left:{rnd(i, 94) + 2}%;width:{rnd(i + 99, 16) + 8}px;height:{rnd(i + 99, 16) + 8}px;animation-delay:{rnd(i + 7, 60) / 10}s;animation-duration:{rnd(i + 3, 30) / 10 + 4.5}s"></i>' for i in range(14))
        return f'<div class="fx fx-foam">{dots}</div>', ""
    if sig in ("sweep",):
        return '<div class="fx fx-sweep"></div>', ""
    if sig in ("film", "tint"):
        return f'<div class="fx fx-{sig}"><b></b></div>', ""
    if sig == "draw":
        return "", CAR
    return "", ""


STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg>'
WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3zm4.6 12.6c-.2.6-1.2 1.1-1.7 1.2-.5 0-1 .2-3.2-.7-2.7-1.1-4.4-3.9-4.5-4.1-.1-.2-1.1-1.5-1.1-2.8 0-1.3.7-2 1-2.3.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.8.9c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1z"/></svg>'
PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/></svg>'
CLOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'


def render(d, c, F, phone, pdisp, fonts_url, design_meta, design=None):
    """d = demo JSON, c = colours (designs.colors), F = font pair. Returns the full HTML page."""
    client = bool(d.get("client"))
    design = design or {}
    look = design.get("look", "split")
    sig = design.get("sig", "")
    hero_key = design.get("hero", "hero")
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
        rate_chip = (f'<a class="chip" href="{maps}" target="_blank" rel="noopener">{STAR}<b data-n="{e(rating)}">{e(rating)}</b>'
                     f'<span>من {e(reviews)} تقييم على قوقل</span></a>')
    if sig == "kinetic":
        h1_html = " ".join(f'<span class="w" style="--i:{i}">{e(w)}</span>' for i, w in enumerate(h1.split()))
    else:
        h1_html = e(h1)
    fx, extra = sig_markup(sig, d.get("slug", name))
    hero = f"""
<section class="hero">
  <div class="hero-media">
    <img class="hero-img" src="{img(hero_key, 1000)}" alt="{alt(hero_key)}" fetchpriority="high">
    <div class="shade"></div>{fx}
  </div>
  <div class="hero-in" data-latin="{e(d.get('latin_name') or '')}">
    {rate_chip}
    <h1>{h1_html}</h1>
    <p class="lead">{e(intro)}</p>
    <div class="cta">
      <a class="btn primary" href="#book">{WA}احجز موعدك</a>
      <a class="btn ghost" href="tel:+{phone}">{PHONE}اتصل</a>
    </div>{extra}
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
    used = {hero_key}
    for s in services:
        key = s.get("photo") or s.get("icon") or "sparkle"
        if key in used:  # never show the same photo twice
            offered = {x.get("photo") or x.get("icon") or "sparkle" for x in services}
            key = next((k for k in PHOTOS if k not in used and (k in NEUTRAL or k in offered)), "sparkle")
        used.add(key)
        txt = f'<p>{e(s["text"])}</p>' if s.get("text") else ""
        cards += (f'<article class="svc"><img src="{img(key, 600)}" alt="{alt(key)}" loading="lazy">'
                  f'<div class="svc-t"><h3>{e(s["title"])}</h3>{txt}</div></article>')
    T = TITLES[look]
    services_html = f"""
<section id="services" class="sec">
  <h2>{T['services']}</h2>
  <div class="svcs">{cards}</div>
</section>"""

    # ---- gallery ----
    # only neutral car photos and photos of services this shop offers (never e.g. a PPF photo for a car wash)
    offered = {s.get("photo") or s.get("icon") or "sparkle" for s in services}
    gkeys = [k for k in PHOTOS if k not in used and (k in NEUTRAL or k in offered)][:6]
    gallery = "".join(f'<img src="{img(k, 600)}" alt="{alt(k)}" loading="lazy">' for k in gkeys)
    gallery_html = f"""
<section id="work" class="sec">
  <h2>{T['work']}</h2>
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
            head = (f'<div class="score"><b data-n="{e(rating)}">{e(rating)}</b><div><div class="stars" aria-label="{e(rating)} من 5">'
                    f'<div class="on" style="width:{pct:.0f}%">{STAR * 5}</div><div class="off">{STAR * 5}</div></div>'
                    f'<span>{e(reviews)} تقييم على خرائط قوقل</span></div></div>')
        qs = "".join(
            f'<blockquote><p>«{e(r["text"])}»</p>'
            f'<cite>{e(r.get("by") or "من تقييمات قوقل")}</cite></blockquote>' for r in rev_list)
        reviews_html = f'<section id="reviews" class="sec"><h2>{T["reviews"]}</h2>{head}{qs}</section>'

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

    parts = dict(services=services_html, gallery=gallery_html, middle=middle, reviews=reviews_html)
    body = "\n".join(parts[k] for k in ORDER[look])
    page_class = f"look-{look}" + (f" sig-{sig}" if sig else "")

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
.hero-media{{position:relative;overflow:hidden}}
.shade{{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(0,0,0,0) 45%,var(--bg) 100%);pointer-events:none}}
.fx{{position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden}}
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
""" + LOOK_CSS + SIG_CSS

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
<body class="{page_class}">
{demo_line}
<header>
  <div class="logo">{e(name)}{f'<small>{latin_sub}</small>' if latin_sub else ''}</div>
  <a class="call" href="tel:+{phone}" aria-label="اتصل بنا">{PHONE}</a>
</header>
<main>
{hero}
{facts_html}
{body}
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
{SIG_JS.get(sig, "")}
</body>
</html>
"""
