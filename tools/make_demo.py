#!/usr/bin/env python3
"""Build a custom demo page from a small JSON file. Every shop gets its own design.

Usage:  python3 tools/make_demo.py tools/demos/<slug>.json
Writes: sample/demos/<slug>/index.html  (live at carcare-sample.pages.dev/demos/<slug>/)

Only facts from the business's real Google Maps listing go in the JSON.
Leave a field out (or null) when it is unknown: the section is then hidden
or shows a neutral placeholder. Never invent prices, reviews or claims.
See tools/demo_example.json for every field.

Design: there are 7 completely different website designs: classic (built here
from base.css) and showroom, garage, clean, magazine, blocks, local (tools/templates.py),
each with its own structure and sections, plus 6 font pairs, 3 corner shapes and
9 palettes (tools/designs.py). The generator picks the least-used design, fonts, shape
and palette among the demos and client sites already in the repo, so no two shops look
the same. The shop's own brand colour ("colors": {"accent"}) and "theme" are kept.
To force a choice: "design": {"layout": "garage", "fonts": "changa", "shape": "sharp",
"palette": "carbon-lime"}.
Re-running for a slug that already exists keeps that shop's design.
"""
import json, sys, html, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import designs as D  # noqa: E402
import templates as T  # noqa: E402

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
e = lambda s: html.escape(str(s), quote=True)


def build(d, design):
    req = ["slug", "name", "city", "phone", "services"]
    miss = [k for k in req if not d.get(k)]
    if miss:
        sys.exit("missing fields: " + ", ".join(miss))
    L = design["layout"]
    F = D.FONTS[design["fonts"]]
    S = D.SHAPES[design["shape"]]
    c = D.colors(design, d.get("colors"))
    dark = c["dark"]

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
    latin = bool(d.get("latin_name"))
    design_meta = ";".join(f"{k}={v}" for k, v in design.items())
    fonts_url = f"https://fonts.googleapis.com/css2?{F['css']}&family=Montserrat:wght@500;700&display=swap"
    lat, lng = d.get("lat"), d.get("lng")
    q = f"{lat},{lng}" if lat and lng else e(d.get("maps_query") or (name + " " + city))

    if L != "classic":
        packs = d.get("packs") or [
            {"name": "باقة الأساس", "items": svc_names[:2] or ["خدمتكم هنا"]},
            {"name": "الباقة المميزة", "items": svc_names[:3], "pick": True},
            {"name": "الباقة الكاملة", "items": svc_names[:4]},
        ]
        ctx = dict(
            name=e(name), sub=e(sub), latin=latin, city=e(city), area=e(area), loc=e(loc), addr=e(d.get("address") or loc),
            phone=phone, pdisp=e(pdisp), rating=e(rating) if rating else "", reviews=e(reviews) if reviews else "", rline=e(rline),
            services=[dict(title=e(s["title"]), text=e(s.get("text") or ""), icon=ICONS.get(s.get("icon", "sparkle"), ICONS["sparkle"])) for s in services],
            packs=[dict(name=e(p["name"]), items=[e(i) for i in p.get("items", [])], price=e(p["price"]) if p.get("price") else "", pick=p.get("pick")) for p in packs],
            review=e(d.get("review") or ""), hours=[e(h) for h in (d.get("hours") or [])], hours_short=e(d.get("hours_short") or ""),
            q=q, slogan=e(d.get("slogan") or ""), headline=e(d.get("headline") or ""),
            intro=e(d.get("intro") or f"{'، '.join(svc_names[:4])} في {loc}. أرسل نوع سيارتك والخدمة اللي تبيها، ويرد عليك فريقنا بأسرع وقت."),
            c=c, F=F, S=S, words=dict(dock=D.DOCK[L]), badge=not d.get("client"),
            options="".join(f"<option>{e(n)}</option>" for n in svc_names),
            title=f"{e(name)} | {e('، '.join(svc_names[:3]))} في {e(city)}" + ("" if d.get("client") else " (نموذج تجريبي)"),
            head_extra=("" if d.get("client") else '<meta name="robots" content="noindex, nofollow">\n')
            + f'<meta name="design" content="{design_meta}">\n<link rel="preconnect" href="https://fonts.googleapis.com">\n'
              f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="{fonts_url}" rel="stylesheet">',
        )
        return T.TEMPLATES[L](ctx)

    W = D.WORDS["classic"]
    css = open(os.path.join(HERE, "base.css"), encoding="utf-8").read()
    theme = f"""
:root{{--pearl:{c['bg']};--pearl-2:{c['surface2']};--ink:{c['text']};--ink-2:{c['text2']};--candy:{c['accent']};
--candy-deep:{c['accent']};--gold:{c['accent']};--line:{c['line']};--white:{c['surface']};--latin:"Montserrat","Segoe UI",sans-serif;
--display:"{F['display']}","Segoe UI",Tahoma,sans-serif;--text:"{F['text']}","Segoe UI",Tahoma,sans-serif;--dw:{F['dw']};
--r:{S['r']}px;--rs:{S['rs']}px;--btn:{S['btn']}px;--field:{S['field']}px}}
h1,h2,h3{{font-weight:var(--dw)}}
.brand{{font-size:1.25rem;font-weight:var(--dw)}}{'.brand.latin{font:700 1.1rem var(--latin);letter-spacing:.14em}' if latin else ''}
.brand small{{letter-spacing:0;margin-top:2px;font-weight:500}}
.eyebrow{{font:500 .9rem var(--text);color:var(--gold)}}
.btn{{border-radius:var(--btn)}}
.btn-primary{{color:{c['accent_text']}}}
@media (hover:hover){{.btn-primary:hover{{filter:brightness(.92)}}.btn-ghost:hover{{background:var(--ink);color:var(--pearl)}}}}
.btn-ghost{{border-color:var(--line)}}
.compare{{border-radius:var(--r)}}.service{{border-radius:var(--r)}}.service .glyph{{border-radius:var(--rs)}}
.pack{{border-radius:var(--r)}}form{{border-radius:var(--r)}}.frame{{border-radius:var(--rs)}}
select,input[type=text]{{border-radius:var(--field)}}.out{{border-radius:var(--field)}}
.paint-after{{background:radial-gradient(120% 70% at 20% -10%,rgba(255,255,255,.55) 0%,rgba(255,255,255,0) 45%),linear-gradient(105deg,rgba(255,255,255,0) 40%,rgba(255,255,255,.35) 47%,rgba(255,255,255,0) 54%),linear-gradient(180deg,{c['paint']} 0%,#16161a 55%,#000 100%)}}
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
.fact{{background:var(--white);border:1px solid var(--line);border-radius:var(--rs);padding:16px 18px}}
.fact b{{display:block;color:var(--gold);font-weight:600;margin-bottom:4px}}
.quote{{background:var(--white);border:1px solid var(--line);border-radius:var(--r);padding:24px;display:grid;gap:12px;max-width:40em}}
.quote p{{font-size:1.1rem}}.quote span{{color:var(--ink-2);font-size:.9rem}}
.top{{gap:12px}}.top a.tel{{white-space:nowrap;font-size:.95rem}}
.demo-badge{{display:inline-block;align-self:flex-start;margin:0 0 10px;padding:4px 12px;border-radius:999px;background:#fff3cd;color:#7a5b00;font-weight:700;font-size:.85rem}}
@media (max-width:400px){{.brand{{font-size:1rem}}}}
"""
    if dark:
        theme += "body{background:radial-gradient(90% 50% at 50% -10%," + c["surface2"] + " 0%,var(--pearl) 60%) fixed,var(--pearl)}\n"

    # ---------- pieces ----------
    sec_no = [0]

    def head(title, sub=""):
        sec_no[0] += 1
        return f'<div class="sec-head"><h2>{e(title)}</h2>{"<p>"+e(sub)+"</p>" if sub else ""}</div>'

    def svc_item(i, s):
        icon = ICONS.get(s.get("icon", "sparkle"), ICONS["sparkle"])
        txt = "<p>" + e(s["text"]) + "</p>" if s.get("text") else ""
        return (f'<div class="service"><div class="glyph"><svg viewBox="0 0 24 24">{icon}</svg></div>'
                f'<b>{e(s["title"])}</b>{txt}</div>')

    svc_html = "".join(svc_item(i, s) for i, s in enumerate(services))

    packs = d.get("packs") or [
        {"name": "باقة الأساس", "items": svc_names[:2] or ["خدمتكم هنا"]},
        {"name": "الباقة المميزة", "items": svc_names[:3], "pick": True},
        {"name": "الباقة الكاملة", "items": svc_names[:4]},
    ]
    pk = ""
    for p in packs:
        pick = p.get("pick")
        price = e(p["price"]) if p.get("price") else "السعر حسب نوع السيارة"
        pk += (f'<div class="pack{" pick" if pick else ""}">{"<span class=badge>الأكثر طلبًا</span>" if pick else ""}'
               + (f'<h3>{e(p["name"])}</h3><div class="price" style="font-size:1.3rem">{price}</div><ul>{"".join("<li>"+e(i)+"</li>" for i in p["items"])}</ul>')
               + f'<a class="btn {"btn-primary" if pick else "btn-ghost"}" href="#book">اختر الباقة</a></div>')

    compare = """<div class="compare" id="cmp" aria-label="مقارنة قبل وبعد">
          <div class="paint paint-after"></div><div class="paint paint-before"></div>
          <span class="tag tag-before">قبل</span><span class="tag tag-after">بعد</span>
          <div class="handle" id="handle"></div>
          <input type="range" min="0" max="100" value="50" id="range" aria-label="حرّك للمقارنة قبل وبعد">
        </div>
        <p class="hint">تصميم توضيحي للمقارنة. تُستبدل بصور أعمالكم الحقيقية: صورة قبل وصورة بعد لنفس السيارة.</p>"""
    frames = '<div class="gallery">' + '<div class="frame">صورة من أعمالكم</div>' * 4 + "</div>"

    review = d.get("review")
    hours = d.get("hours") or []
    hours_html = "<br>".join(e(h) for h in hours)
    addr = d.get("address") or loc
    facts = ""
    if hours_html:
        facts += f'<div class="fact"><b>أوقات العمل</b>{hours_html}</div>'
    facts += (f'<div class="fact"><b>تواصل معنا</b><a href="tel:+{phone}" style="direction:ltr;unicode-bidi:plaintext;'
              f'text-decoration:none">{e(pdisp)}</a> • واتساب</div>')
    options = "".join(f"<option>{e(n)}</option>" for n in svc_names)

    sections = {}
    sections["services"] = f'<section id="services">{head(*W["services"])}<div class="services">{svc_html}</div></section>'
    sections["packs"] = (f'<section id="packs">{head(*W["packs"])}<div class="packs">{pk}</div>'
                         f'<p class="note">أسماء الباقات ومحتوياتها وأسعارها أمثلة تُستبدل بباقاتكم الفعلية.</p></section>')
    work_inner = frames
    sections["work"] = f'<section id="work">{head(*W["work"])}{work_inner}</section>'
    if review or rline:
        sections["reviews"] = (f'<section id="reviews">{head(W["reviews"], rline + "." if rline else "")}'
                               + (f'<div class="quote"><p>«{e(review)}»</p><span>من زائر على خرائط قوقل</span></div>' if review else "")
                               + "</section>")
    sections["map"] = (f'<section id="map">{head(W["map"], addr + ". اضغط على الخريطة للاتجاهات.")}<div class="facts">{facts}</div>'
                       f'<iframe title="موقع {e(name)} على الخريطة" src="https://maps.google.com/maps?q={q}&z=15&output=embed" style="width:100%;height:260px;border:0;border-radius:var(--rs)" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
                       f'<p style="margin-top:10px"><a class="btn btn-ghost" href="https://www.google.com/maps/search/?api=1&query={q}" target="_blank" rel="noopener">افتح في خرائط قوقل</a></p></section>')
    sections["book"] = (f'<section id="book" class="book">{head(W["book"], "اختر الخدمة واكتب نوع سيارتك، وتنفتح لك رسالة جاهزة في واتساب " + name + ".")}'
                        f'<form id="form"><label>الخدمة<select id="svc">{options}</select></label>'
                        f'<label>موديل السيارة<input type="text" id="car" placeholder="مثال: كامري 2022"></label>'
                        f'<label>الاسم<input type="text" id="nm" autocomplete="name"></label>'
                        f'<button class="btn btn-primary" type="submit">جهّز رسالة الحجز</button>'
                        f'<div class="out" id="out" role="status"><span id="msg"></span><button class="btn btn-ghost" type="button" id="copy">انسخ الرسالة</button></div>'
                        f'</form></section>')

    # ---------- hero per layout ----------
    badge = '<p class="demo-badge">تصميم مقترح للعرض (نموذج تجريبي)</p>'
    eyebrow = f'<span class="eyebrow">{e(d["slogan"])}</span>' if d.get("slogan") else ""
    default_h1 = f"عناية احترافية بسيارتك في {city}"
    h1 = e(d.get("headline") or default_h1)
    intro = e(d.get("intro") or f"{'، '.join(svc_names[:4])} في {loc}. أرسل نوع سيارتك والخدمة اللي تبيها، ويرد عليك فريقنا بأسرع وقت.")
    rl = f'<p style="font-weight:700">{rline}</p>' if rline else ""
    ctas = f'<div class="cta-row"><a class="btn btn-primary" href="#book">{e(W["cta"])}</a><a class="btn btn-ghost" href="#{"packs" if "باق" in W["cta2"] or "أسعار" in W["cta2"] else "services"}">{e(W["cta2"])}</a></div>'

    hero = f'<div class="hero"><div class="hero-copy">{badge}{eyebrow}<h1>{h1}</h1>{rl}<p>{intro}</p>{ctas}</div><div>{compare}</div></div>'

    body = hero + "".join(sections[k] for k in ["services", "packs", "work", "reviews", "map", "book"] if k in sections)

    title = f"{e(name)} | {e('، '.join(svc_names[:3]))} في {e(city)} (نموذج تجريبي)"
    foot_bits = " • ".join(x for x in [e(addr), e(d.get("hours_short") or ""), e(pdisp)] if x)
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="robots" content="noindex, nofollow">
<meta name="design" content="{design_meta}">
<meta name="description" content="نموذج موقع عربي للجوال لمراكز العناية بالسيارات: الباقات، صور الأعمال، وحجز بضغطة واتساب.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts_url}" rel="stylesheet">
<style>{css}{theme}</style>
</head>
<body class="layout-{L}">
<div class="wrap">
  <header class="top">
    <div class="brand{' latin' if latin else ''}">{e(name)}{'<small>'+e(sub)+'</small>' if sub else ''}</div>
    <a class="tel" href="tel:+{phone}">{e(pdisp)}</a>
  </header>
  <main>
    {body}
  </main>
  <footer>
    <div><span class="brand" style="font-size:.95rem">{e(name)}</span>{' — '+e(d['slogan']) if d.get('slogan') else ''}</div>
    <div style="margin-top:6px">{foot_bits}</div>
    <div style="margin-top:6px">هذا تصميم مقترح للعرض فقط، وليس الموقع الرسمي لـ{e(name)}. الصور والأسعار تُستبدل ببياناتكم الحقيقية.</div>
  </footer>
</div>
<nav class="dock" aria-label="تواصل سريع">
  <a class="btn btn-primary" href="https://wa.me/{phone}" target="_blank" rel="noopener">{e(W["dock"])}</a>
  <a class="btn btn-ghost" href="tel:+{phone}">اتصل بنا</a>
</nav>
<script>
(function(){{
  var cmp=document.getElementById('cmp');
  if(cmp){{var range=document.getElementById('range'),handle=document.getElementById('handle'),before=cmp.querySelector('.paint-before');
  range.addEventListener('input',function(){{var v=+range.value;before.style.clipPath='inset(0 0 0 '+v+'%)';handle.style.left=v+'%';}});}}
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
    theme = data.get("theme") if data.get("theme") in ("dark", "light") else None
    design = D.pick_design(ROOT, slug, theme, data.get("design"))
    out_dir = os.path.join(ROOT, "sample", "demos", slug)
    os.makedirs(out_dir, exist_ok=True)
    page = build(data, design)
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(page)
    print(f"wrote sample/demos/{slug}/index.html -> https://carcare-sample.pages.dev/demos/{slug}/")
    print("design: " + ", ".join(f"{k}={v}" for k, v in design.items()))
