#!/usr/bin/env python3
"""Build a custom demo page from a small JSON file (Vantage standard).

Usage:  python3 tools/make_demo.py tools/demos/<slug>.json
Writes: sample/demos/<slug>/index.html  (live at carcare-sample.pages.dev/demos/<slug>/)

Only facts from the business's real Google Maps listing go in the JSON.
Leave a field out (or null) when it is unknown: the section is then hidden
or shows a neutral placeholder. Never invent prices, reviews or claims.
See tools/demo_example.json for every field.
"""
import json, sys, html, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ICONS = {
    "shield": '<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/>',
    "drop": '<path d="M12 3c3 4 6 6.5 6 10a6 6 0 0 1-12 0c0-3.5 3-6 6-10z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4L7 17M17 7l1.4-1.4"/>',
    "polish": '<path d="M4 16c4-1 6-5 8-9 2 4 4 8 8 9M4 20h16"/>',
    "wash": '<path d="M5 14h14l-1.5-5h-11zM7 14v3M17 14v3M8 6l1-2M12 6V3M16 6l-1-2"/>',
    "seat": '<path d="M8 4h5l1 9H9zM7 13h9l1 4H7zM9 17v3M15 17v3"/>',
    "wrench": '<path d="M14 6a4 4 0 0 0 5 5l-8 8a2 2 0 0 1-3-3l8-8a4 4 0 0 1-2-2z"/>',
    "sparkle": '<path d="M12 3l2 6 6 2-6 2-2 6-2-6-6-2 6-2z"/>',
}

DARK = dict(bg="#0a0a0c", surface="#131317", surface2="#1b1b20", text="#f3f3f4",
            text2="#a3a3ab", line="#26262c", accent="#cfae6b", accent_text="#0a0a0c")
LIGHT = dict(bg="#eef1f4", surface="#ffffff", surface2="#e1e6eb", text="#0d1b26",
             text2="#3b4b58", line="#cfd6dd", accent="#c8141f", accent_text="#ffffff")

e = lambda s: html.escape(str(s), quote=True)


def build(d):
    req = ["slug", "name", "city", "phone", "services"]
    miss = [k for k in req if not d.get(k)]
    if miss:
        sys.exit("missing fields: " + ", ".join(miss))
    dark = d.get("theme", "dark") == "dark"
    c = dict(DARK if dark else LIGHT)
    c.update(d.get("colors") or {})
    phone = re.sub(r"\D", "", d["phone"])
    if phone.startswith("0"):
        phone = "966" + phone[1:]
    pdisp = d.get("phone_display") or ("0" + phone[3:5] + " " + phone[5:8] + " " + phone[8:])
    name = d["name"]
    sub = d.get("brand_sub") or ""
    area = d.get("area") or ""
    city = d["city"]
    loc = "، ".join(x for x in [area, city] if x)
    rating, reviews = d.get("rating"), d.get("reviews")
    rline = f"⭐ {rating} من {reviews} تقييم على خرائط قوقل" if rating and reviews else ""
    services = d["services"]
    svc_names = [s["title"] for s in services]

    css = open(os.path.join(HERE, "base.css"), encoding="utf-8").read()
    theme = f"""
:root{{--pearl:{c['bg']};--pearl-2:{c['surface2']};--ink:{c['text']};--ink-2:{c['text2']};--candy:{c['accent']};
--candy-deep:{c['accent']};--gold:{c['accent']};--line:{c['line']};--white:{c['surface']};--latin:"Montserrat","Segoe UI",sans-serif}}
.brand{{font-size:1.25rem}}{'.brand.latin{font:700 1.1rem var(--latin);letter-spacing:.14em}' if d.get('latin_name') else ''}
.brand small{{letter-spacing:0;margin-top:2px}}
.eyebrow{{font:500 .9rem var(--text);color:var(--gold)}}
.btn-primary{{color:{c['accent_text']}}}
@media (hover:hover){{.btn-primary:hover{{filter:brightness(.92)}}.btn-ghost:hover{{background:var(--ink);color:var(--pearl)}}}}
.btn-ghost{{border-color:var(--line)}}
.paint-after{{background:radial-gradient(120% 70% at 20% -10%,rgba(255,255,255,.55) 0%,rgba(255,255,255,0) 45%),linear-gradient(105deg,rgba(255,255,255,0) 40%,rgba(255,255,255,.35) 47%,rgba(255,255,255,0) 54%),linear-gradient(180deg,{c.get('paint','#4a4a52')} 0%,#16161a 55%,#000 100%)}}
.paint-before{{background:repeating-radial-gradient(circle at 28% 35%,rgba(255,255,255,.2) 0 1px,transparent 1px 7px),repeating-radial-gradient(circle at 72% 62%,rgba(255,255,255,.16) 0 1px,transparent 1px 9px),linear-gradient(180deg,#3b3b40 0%,#2a2a2e 45%,#1c1c1f 100%)}}
.tag{{background:rgba(0,0,0,.72);color:#fff}}
.handle::before{{color:#0a0a0c}}.handle::after{{background-image:none}}
.service svg{{stroke:var(--gold)}}
.pack.pick{{background:var(--pearl-2);color:var(--ink);border-color:var(--gold)}}
.pack .price,.pack.pick .price{{color:var(--gold)}}
.pack li::before,.pack.pick li::before{{background:var(--gold)}}
.pack .badge{{background:var(--gold);color:{c['accent_text']}}}
.frame{{border-color:var(--line)}}
.facts{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin-bottom:20px}}
.fact{{background:var(--white);border:1px solid var(--line);border-radius:18px;padding:16px 18px}}
.fact b{{display:block;color:var(--gold);font-weight:600;margin-bottom:4px}}
.quote{{background:var(--white);border:1px solid var(--line);border-radius:22px;padding:24px;display:grid;gap:12px;max-width:40em}}
.quote p{{font-size:1.1rem}}.quote span{{color:var(--ink-2);font-size:.9rem}}
.top{{gap:12px}}.top a.tel{{white-space:nowrap;font-size:.95rem}}
@media (max-width:400px){{.brand{{font-size:1rem}}}}
"""
    if dark:
        theme += "body{background:radial-gradient(90% 50% at 50% -10%," + c["surface2"] + " 0%,var(--pearl) 60%) fixed,var(--pearl)}\n"

    svc_html = "".join(
        f'<div class="service"><div class="glyph"><svg viewBox="0 0 24 24">{ICONS.get(s.get("icon","sparkle"),ICONS["sparkle"])}</svg></div>'
        f'<b>{e(s["title"])}</b>{"<p>"+e(s["text"])+"</p>" if s.get("text") else ""}</div>' for s in services)

    packs = d.get("packs") or [
        {"name": "باقة الأساس", "items": svc_names[:2] or ["خدمتكم هنا"]},
        {"name": "الباقة المميزة", "items": svc_names[:3], "pick": True},
        {"name": "الباقة الكاملة", "items": svc_names[:4]},
    ]
    pk = ""
    for p in packs:
        pick = p.get("pick")
        price = e(p["price"]) if p.get("price") else "سعر باقتكم هنا"
        pk += (f'<div class="pack{" pick" if pick else ""}">{"<span class=badge>الأكثر طلبًا</span>" if pick else ""}'
               f'<h3>{e(p["name"])}</h3><div class="price" style="font-size:1.3rem">{price}</div>'
               f'<ul>{"".join("<li>"+e(i)+"</li>" for i in p["items"])}</ul>'
               f'<a class="btn {"btn-primary" if pick else "btn-ghost"}" href="#book">اختر الباقة</a></div>')

    review = d.get("review")
    rev_html = ""
    if review or rline:
        rev_html = (f'<section id="reviews"><div class="sec-head"><h2>آراء عملائنا</h2>{"<p>"+rline+".</p>" if rline else ""}</div>'
                    + (f'<div class="quote"><p>«{e(review)}»</p><span>من زائر على خرائط قوقل</span></div>' if review else "")
                    + "</section>")

    hours = d.get("hours") or []
    hours_html = "<br>".join(e(h) for h in hours)
    lat, lng = d.get("lat"), d.get("lng")
    q = f"{lat},{lng}" if lat and lng else e(d.get("maps_query") or (name + " " + city))
    addr = d.get("address") or loc
    facts = ""
    if hours_html:
        facts += f'<div class="fact"><b>أوقات العمل</b>{hours_html}</div>'
    facts += (f'<div class="fact"><b>تواصل معنا</b><a href="tel:+{phone}" style="direction:ltr;unicode-bidi:plaintext;'
              f'text-decoration:none">{e(pdisp)}</a> • واتساب</div>')

    eyebrow = f'<span class="eyebrow">{e(d["slogan"])}</span>' if d.get("slogan") else ""
    h1 = e(d.get("headline") or f"عناية احترافية بسيارتك في {city}")
    intro = e(d.get("intro") or f"{'، '.join(svc_names[:4])} في {loc}. أرسل نوع سيارتك والخدمة اللي تبيها، ويرد عليك فريقنا بأسرع وقت.")
    options = "".join(f"<option>{e(n)}</option>" for n in svc_names)
    title = f"{e(name)} | {e('، '.join(svc_names[:3]))} في {e(city)} (نموذج تجريبي)"
    foot_bits = " • ".join(x for x in [e(addr), e(d.get("hours_short") or ""), e(pdisp)] if x)

    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="نموذج موقع عربي للجوال لمراكز العناية بالسيارات: الباقات، صور الأعمال، وحجز بضغطة واتساب.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lalezar&family=Montserrat:wght@500;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}{theme}</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="brand{' latin' if d.get('latin_name') else ''}">{e(name)}{'<small>'+e(sub)+'</small>' if sub else ''}</div>
    <a class="tel" href="tel:+{phone}">{e(pdisp)}</a>
  </header>
  <main>
    <div class="hero">
      <div class="hero-copy">
        <p style="display:inline-block;align-self:flex-start;margin:0 0 10px;padding:4px 12px;border-radius:999px;background:#fff3cd;color:#7a5b00;font-weight:700;font-size:.85rem">نموذج تجريبي</p>
        {eyebrow}
        <h1>{h1}</h1>
        {'<p style="font-weight:700">'+rline+'</p>' if rline else ''}
        <p>{intro}</p>
        <div class="cta-row"><a class="btn btn-primary" href="#book">احجز موعدك</a><a class="btn btn-ghost" href="#packs">شوف الباقات</a></div>
      </div>
      <div>
        <div class="compare" id="cmp" aria-label="مقارنة قبل وبعد">
          <div class="paint paint-after"></div><div class="paint paint-before"></div>
          <span class="tag tag-before">قبل</span><span class="tag tag-after">بعد</span>
          <div class="handle" id="handle"></div>
          <input type="range" min="0" max="100" value="50" id="range" aria-label="حرّك للمقارنة قبل وبعد">
        </div>
        <p class="hint">تصميم توضيحي للمقارنة. تُستبدل بصور أعمالكم الحقيقية: صورة قبل وصورة بعد لنفس السيارة.</p>
      </div>
    </div>
    <section id="services"><div class="sec-head"><h2>خدماتنا</h2><p>كل خدمة واضحة قبل ما تراسلنا.</p></div><div class="services">{svc_html}</div></section>
    <section id="packs"><div class="sec-head"><h2>الباقات والأسعار</h2><p>أسعار وتفاصيل باقاتكم تظهر هنا بترتيب يفهمه العميل من أول نظرة.</p></div>
      <div class="packs">{pk}</div><p class="note">أسماء الباقات ومحتوياتها وأسعارها أمثلة تُستبدل بباقاتكم الفعلية.</p></section>
    <section id="work"><div class="sec-head"><h2>أعمالنا</h2><p>هنا تظهر صور سياراتكم قبل وبعد، بحجم واضح على الجوال.</p></div>
      <div class="gallery"><div class="frame">صورة من أعمالكم</div><div class="frame">صورة من أعمالكم</div><div class="frame">صورة من أعمالكم</div><div class="frame">صورة من أعمالكم</div></div></section>
    {rev_html}
    <section id="map"><div class="sec-head"><h2>موقعنا</h2><p>{e(addr)}. اضغط على الخريطة للاتجاهات.</p></div>
      <div class="facts">{facts}</div>
      <iframe title="موقع {e(name)} على الخريطة" src="https://maps.google.com/maps?q={q}&z=15&output=embed" style="width:100%;height:260px;border:0;border-radius:16px" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      <p style="margin-top:10px"><a class="btn btn-ghost" href="https://www.google.com/maps/search/?api=1&query={q}" target="_blank" rel="noopener">افتح في خرائط قوقل</a></p></section>
    <section id="book" class="book"><div class="sec-head"><h2>احجز موعدك</h2><p>اختر الخدمة واكتب نوع سيارتك، وتنفتح لك رسالة جاهزة في واتساب {e(name)}.</p></div>
      <form id="form">
        <label>الخدمة<select id="svc">{options}</select></label>
        <label>موديل السيارة<input type="text" id="car" placeholder="مثال: كامري 2022"></label>
        <label>الاسم<input type="text" id="nm" autocomplete="name"></label>
        <button class="btn btn-primary" type="submit">جهّز رسالة الحجز</button>
        <div class="out" id="out" role="status"><span id="msg"></span><button class="btn btn-ghost" type="button" id="copy">انسخ الرسالة</button></div>
      </form></section>
  </main>
  <footer>
    <div><span class="brand" style="font-size:.95rem">{e(name)}</span>{' — '+e(d['slogan']) if d.get('slogan') else ''}</div>
    <div style="margin-top:6px">{foot_bits}</div>
    <div style="margin-top:6px">نموذج مصمم ليوضح شكل موقعكم. الأسعار والصور تُستبدل ببياناتكم.</div>
  </footer>
</div>
<nav class="dock" aria-label="تواصل سريع">
  <a class="btn btn-primary" href="https://wa.me/{phone}" target="_blank" rel="noopener">احجز بالواتساب</a>
  <a class="btn btn-ghost" href="tel:+{phone}">اتصل بنا</a>
</nav>
<script>
(function(){{
  var cmp=document.getElementById('cmp'),range=document.getElementById('range'),handle=document.getElementById('handle'),before=cmp.querySelector('.paint-before');
  range.addEventListener('input',function(){{var v=+range.value;before.style.clipPath='inset(0 0 0 '+v+'%)';handle.style.left=v+'%';}});
  var form=document.getElementById('form'),out=document.getElementById('out'),msg=document.getElementById('msg');
  form.addEventListener('submit',function(ev){{ev.preventDefault();
    var svc=document.getElementById('svc').value,car=document.getElementById('car').value.trim(),nm=document.getElementById('nm').value.trim();
    var text='السلام عليكم، أبغى أحجز موعد لخدمة '+svc+(car?' لسيارة '+car:'')+(nm?'. الاسم: '+nm:'')+'.';
    msg.textContent=text;out.classList.add('show');window.open('https://wa.me/{phone}?text='+encodeURIComponent(text),'_blank');}});
  document.getElementById('copy').addEventListener('click',function(){{var b=this;if(navigator.clipboard)navigator.clipboard.writeText(msg.textContent).then(function(){{b.textContent='تم النسخ';}});}});
}})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    slug = re.sub(r"[^a-z0-9-]", "", data.get("slug", "").lower())
    if not slug:
        sys.exit("slug must be lowercase latin letters/numbers")
    out_dir = os.path.join(ROOT, "sample", "demos", slug)
    os.makedirs(out_dir, exist_ok=True)
    page = build(data)
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(page)
    print(f"wrote sample/demos/{slug}/index.html -> https://carcare-sample.pages.dev/demos/{slug}/")
