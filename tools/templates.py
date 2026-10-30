"""Six completely different website designs for car-care shops.

Each template builds its own page from scratch: its own structure, sections,
CSS and interactions. They share only the shop data (ctx) and the WhatsApp
booking script. The "classic" design lives in make_demo.py (it uses base.css).

ctx keys (all text already HTML-escaped unless noted):
  name sub latin city area loc addr phone(digits) pdisp rating reviews rline
  services[{title,text,icon(svg)}] packs[{name,items[],price,pick}] review
  hours[] hours_short q(map query) slogan headline intro c(colors) F(fonts)
  S(shape) words badge(bool: demo label) head_extra(meta/fonts) title options
"""

BOOK_JS = """<script>
(function(){
  document.querySelectorAll('[data-book]').forEach(function(form){
    form.addEventListener('submit',function(ev){ev.preventDefault();
      var f=function(n){var el=form.querySelector('[name='+n+']');if(!el)return '';
        if(el.type==='radio'){var c=form.querySelector('[name='+n+']:checked');return c?c.value:'';}return el.value.trim();};
      var svc=f('svc'),car=f('car'),nm=f('nm');
      var text='السلام عليكم، أبغى أحجز موعد'+(svc?' لخدمة '+svc:'')+(car?' لسيارة '+car:'')+(nm?'. الاسم: '+nm:'')+'.';
      var out=form.querySelector('.out');if(out){out.textContent=text;out.hidden=false;}
      window.open('https://wa.me/'+form.dataset.book+'?text='+encodeURIComponent(text),'_blank');});
  });
  document.querySelectorAll('[data-tabs]').forEach(function(t){
    var btns=t.querySelectorAll('[role=tab]'),panels=document.querySelectorAll('[data-panel]');
    t.hidden=false;panels.forEach(function(p,i){p.hidden=i>0;});
    btns.forEach(function(b,i){b.addEventListener('click',function(){
      btns.forEach(function(x){x.setAttribute('aria-selected','false');});b.setAttribute('aria-selected','true');
      panels.forEach(function(p,j){p.hidden=j!==i;});});});
  });
  var cmp=document.getElementById('cmp');
  if(cmp){var r=cmp.querySelector('input'),h=cmp.querySelector('.handle'),b=cmp.querySelector('.before');
    r.addEventListener('input',function(){b.style.clipPath='inset(0 0 0 '+r.value+'%)';h.style.left=r.value+'%';});}
})();
</script>"""


def _root(ctx, extra=""):
    c, F, S = ctx["c"], ctx["F"], ctx["S"]
    return f""":root{{--bg:{c['bg']};--sf:{c['surface']};--sf2:{c['surface2']};--tx:{c['text']};--tx2:{c['text2']};--ln:{c['line']};
--ac:{c['accent']};--act:{c['accent_text']};--r:{S['r']}px;--rs:{S['rs']}px;--btn:{S['btn']}px;--fd:{S['field']}px;
--disp:"{F['display']}","Segoe UI",Tahoma,sans-serif;--txt:"{F['text']}","Segoe UI",Tahoma,sans-serif;--dw:{F['dw']};
--lat:"Montserrat","Segoe UI",sans-serif;{extra}}}
*{{box-sizing:border-box}}[hidden]{{display:none!important}}html{{scroll-behavior:smooth;overflow-x:clip}}
body{{margin:0;background:var(--bg);color:var(--tx);font:400 17px/1.65 var(--txt);overflow-x:clip;padding-bottom:calc(72px + env(safe-area-inset-bottom,0px))}}
h1,h2,h3{{font-family:var(--disp);font-weight:var(--dw);margin:0;line-height:1.15;text-wrap:balance}}
p{{margin:0}}a{{color:inherit}}
.in{{padding-inline:max(16px,calc((100% - 1080px) / 2))}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;padding:0 22px;border-radius:var(--btn);
font:600 1rem var(--txt);text-decoration:none;border:2px solid transparent;cursor:pointer;background:var(--ac);color:var(--act)}}
.btn.alt{{background:transparent;border-color:currentColor;color:inherit}}
.btn:active{{transform:scale(.97)}}
:focus-visible{{outline:3px solid var(--ac);outline-offset:3px}}
.demo{{display:inline-block;padding:3px 12px;border-radius:999px;background:#fff3cd;color:#7a5b00;font:700 .82rem var(--txt)}}
.dock{{position:fixed;inset:auto 0 0 0;z-index:30;display:flex;gap:8px;padding:8px 16px calc(8px + env(safe-area-inset-bottom,0px));background:var(--bg);border-top:1px solid var(--ln)}}
.dock .btn{{flex:1}}
.ico{{width:24px;height:24px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex:none}}
label{{display:grid;gap:6px;font-weight:500;font-size:.95rem}}
input[type=text],select{{width:100%;min-height:48px;border-radius:var(--fd);border:1px solid var(--ln);padding:0 14px;font:400 1rem var(--txt);background:var(--sf);color:var(--tx)}}
.out{{font-size:.92rem;color:var(--tx2);border:1px dashed var(--ln);border-radius:var(--fd);padding:12px}}
.lat{{direction:ltr;unicode-bidi:plaintext}}
iframe.map{{width:100%;height:280px;border:0;border-radius:var(--rs);display:block}}
@media (min-width:860px){{body{{padding-bottom:0}}.dock{{display:none}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}html{{scroll-behavior:auto}}}}
"""


def _page(ctx, css, body, layout):
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{ctx['title']}</title>
{ctx['head_extra']}
<style>{css}</style>
</head>
<body class="t-{layout}">
{body}
<nav class="dock" aria-label="تواصل سريع"><a class="btn" href="https://wa.me/{ctx['phone']}" target="_blank" rel="noopener">{ctx['words']['dock']}</a><a class="btn alt" href="tel:+{ctx['phone']}">اتصال</a></nav>
{BOOK_JS}
</body>
</html>
"""


def _demo(ctx):
    return '<span class="demo">تصميم مقترح للعرض (نموذج تجريبي)</span>' if ctx["badge"] else ""


def _note(ctx):
    if not ctx["badge"]:
        return ""
    return ('<p class="fine">هذا تصميم مقترح للعرض فقط، وليس الموقع الرسمي لـ' + ctx["name"]
            + '. الصور والأسعار تُستبدل ببياناتكم الحقيقية.</p>')


def _map(ctx):
    return (f'<iframe class="map" title="موقع {ctx["name"]} على الخريطة" src="https://maps.google.com/maps?q={ctx["q"]}&z=15&output=embed" '
            f'loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')


def _dir(ctx):
    return f'https://www.google.com/maps/search/?api=1&query={ctx["q"]}'


def _price(p):
    return p["price"] if p.get("price") else "السعر حسب نوع السيارة"


def _form(ctx, cls="", radio=False):
    if radio:
        svc = "".join(f'<label class="opt"><input type="radio" name="svc" value="{s["title"]}"{" checked" if i == 0 else ""}><span>{s["title"]}</span></label>'
                      for i, s in enumerate(ctx["services"]))
        svc = f'<fieldset class="opts"><legend>وش تحتاج سيارتك؟</legend>{svc}</fieldset>'
    else:
        svc = f'<label>الخدمة<select name="svc">{ctx["options"]}</select></label>'
    return (f'<form class="{cls}" data-book="{ctx["phone"]}">{svc}'
            f'<label>موديل السيارة<input type="text" name="car" placeholder="مثال: لكزس 2023"></label>'
            f'<label>الاسم<input type="text" name="nm" autocomplete="name"></label>'
            f'<button class="btn" type="submit">أرسل الطلب على واتساب</button><p class="out" hidden role="status"></p></form>')


def _hours(ctx):
    return "<br>".join(ctx["hours"]) if ctx["hours"] else ""


# ---------------------------------------------------------------- showroom
def showroom(ctx):
    c = ctx["c"]
    css = _root(ctx) + f"""
.hero{{min-height:min(92svh,820px);display:grid;place-items:center;text-align:center;position:relative;overflow:hidden;padding:96px 16px 64px;
background:radial-gradient(80% 60% at 50% 110%,color-mix(in srgb,var(--ac) 45%,transparent) 0%,transparent 70%),radial-gradient(60% 40% at 50% 0%,var(--sf2) 0%,transparent 70%),var(--bg)}}
.hero::after{{content:"";position:absolute;inset:-40% -60%;background:linear-gradient(100deg,transparent 45%,rgba(255,255,255,.07) 50%,transparent 55%);animation:sheen 7s ease-in-out infinite}}
@keyframes sheen{{0%{{transform:translateX(-30%)}}60%,100%{{transform:translateX(30%)}}}}
.hero>div{{position:relative;z-index:1;display:grid;gap:18px;justify-items:center;max-width:46rem}}
.top{{position:absolute;top:0;inset-inline:0;z-index:2;display:flex;justify-content:space-between;align-items:center;padding-block:18px}}
.top a{{text-decoration:none;font-weight:600}}
.mark{{font:var(--dw) clamp(2.8rem,11vw,6.2rem)/1 var(--disp);letter-spacing:.01em}}
.mark.latin{{font:700 clamp(2.2rem,9vw,5rem)/1 var(--lat);letter-spacing:.18em}}
.slog{{color:var(--ac);font-weight:600;letter-spacing:.04em}}
.hero h1{{font-size:clamp(1.3rem,4vw,1.8rem);color:var(--tx2);font-family:var(--txt);font-weight:500}}
.cta{{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}}
section{{padding-block:64px}}
.kicker{{color:var(--ac);font-weight:600;font-size:.9rem;letter-spacing:.08em;margin-bottom:8px}}
h2{{font-size:clamp(1.9rem,6vw,3rem);margin-bottom:28px}}
.rail{{display:grid;grid-auto-flow:column;grid-auto-columns:min(78%,300px);gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:10px}}
.card{{scroll-snap-align:start;background:linear-gradient(180deg,var(--sf2),var(--sf));border:1px solid var(--ln);border-radius:var(--r);padding:26px;display:grid;gap:12px;align-content:start;min-height:220px}}
.card .ico{{width:40px;height:40px;color:var(--ac)}}
.card b{{font-size:1.2rem}}.card p{{color:var(--tx2)}}
.menu{{display:grid;gap:22px;max-width:44rem}}
.row .line{{display:flex;align-items:baseline;gap:10px}}
.row b{{font:var(--dw) 1.4rem var(--disp)}}
.row .dots{{flex:1;border-bottom:2px dotted var(--ln);transform:translateY(-6px)}}
.row .pr{{color:var(--ac);font-weight:700;white-space:nowrap}}
.row p{{color:var(--tx2);font-size:.95rem}}
.quote{{text-align:center;max-width:42rem;margin-inline:auto;font:var(--dw) clamp(1.4rem,4.5vw,2.1rem)/1.5 var(--disp)}}
.quote::before{{content:"“";display:block;font-size:4rem;line-height:.6;color:var(--ac)}}
.quote small{{display:block;margin-top:14px;font:400 .95rem var(--txt);color:var(--tx2)}}
.info{{display:grid;gap:1px;background:var(--ln);border:1px solid var(--ln);border-radius:var(--r);overflow:hidden;margin-bottom:18px}}
.info div{{background:var(--sf);padding:18px}}.info b{{display:block;color:var(--ac);font-size:.9rem;margin-bottom:4px}}
form{{display:grid;gap:14px;max-width:34rem;background:var(--sf);border:1px solid var(--ln);border-radius:var(--r);padding:24px}}
footer{{padding-block:36px;color:var(--tx2);font-size:.9rem;border-top:1px solid var(--ln);display:grid;gap:6px}}
@media (min-width:860px){{.info{{grid-template-columns:repeat(3,1fr)}}.book{{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}}}}
"""
    svc = "".join(f'<div class="card"><svg class="ico" viewBox="0 0 24 24">{s["icon"]}</svg><b>{s["title"]}</b>{"<p>"+s["text"]+"</p>" if s["text"] else ""}</div>' for s in ctx["services"])
    menu = "".join(f'<div class="row"><div class="line"><b>{p["name"]}</b><span class="dots"></span><span class="pr">{_price(p)}</span></div><p>{"، ".join(p["items"])}</p></div>' for p in ctx["packs"])
    quote = f'<section class="in"><p class="quote">{ctx["review"]}<small>من زائر على خرائط قوقل{" • " + ctx["rline"] if ctx["rline"] else ""}</small></p></section>' if ctx["review"] else ""
    info = ""
    if ctx["hours"]:
        info += f'<div><b>أوقات العمل</b>{_hours(ctx)}</div>'
    info += f'<div><b>العنوان</b>{ctx["addr"]}</div><div><b>للتواصل</b><a class="lat" href="tel:+{ctx["phone"]}">{ctx["pdisp"]}</a></div>'
    mark = f'<p class="mark{" latin" if ctx["latin"] else ""}">{ctx["name"]}</p>'
    body = f"""<header class="top in"><span>{_demo(ctx)}</span><a class="lat" href="tel:+{ctx['phone']}">{ctx['pdisp']}</a></header>
<div class="hero"><div>{mark}{'<p class="slog">'+ctx['slogan']+'</p>' if ctx['slogan'] else ''}<h1>{ctx['headline'] or ('سيارتك تستاهل عناية تليق فيها في ' + ctx['city'])}</h1>
{'<p>'+ctx['rline']+'</p>' if ctx['rline'] else ''}<div class="cta"><a class="btn" href="#book">احجز موعدك</a><a class="btn alt" href="#menu">الباقات</a></div></div></div>
<section class="in" id="services"><p class="kicker">الخدمات</p><h2>كل اللي تحتاجه سيارتك</h2><div class="rail">{svc}</div></section>
<section class="in" id="menu"><p class="kicker">الباقات</p><h2>قائمة الأسعار</h2><div class="menu">{menu}</div><p style="color:var(--tx2);font-size:.9rem;margin-top:18px">أسماء الباقات وأسعارها أمثلة تُستبدل بباقاتكم الفعلية.</p></section>
{quote}
<section class="in" id="visit"><p class="kicker">الزيارة</p><h2>نستقبلك في {ctx['loc']}</h2><div class="info">{info}</div>{_map(ctx)}</section>
<section class="in book" id="book"><div><p class="kicker">الحجز</p><h2>احجز موعدك</h2><p style="color:var(--tx2)">اختر الخدمة واكتب نوع سيارتك، وتنفتح لك رسالة جاهزة في واتساب.</p></div>{_form(ctx)}</section>
<footer class="in"><b>{ctx['name']}</b><span>{ctx['addr']}</span>{_note(ctx)}</footer>"""
    return _page(ctx, css, body, "showroom")


# ---------------------------------------------------------------- garage
def garage(ctx):
    css = _root(ctx) + """
.stripe{height:12px;background:repeating-linear-gradient(-45deg,var(--ac) 0 14px,#111 14px 28px)}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px;padding-block:14px;background:#111;color:#f5f5f5}
.top b{font:var(--dw) 1.3rem var(--disp)}
.top a{font-weight:700;text-decoration:none}
.hero{display:grid;gap:22px;padding-block:36px 48px}
.tagline{font-weight:700;color:var(--ac);text-transform:uppercase;letter-spacing:.06em;font-size:.9rem}
.hero h1{font-size:clamp(2.4rem,10vw,5rem);line-height:1.02}
.hero p{color:var(--tx2);max-width:36rem}
.sign{background:#111;color:#f5f5f5;border:4px solid var(--ac);border-radius:var(--rs);padding:20px;display:grid;gap:8px;max-width:26rem}
.sign b{color:var(--ac);font:var(--dw) 1.2rem var(--disp)}
.cta{display:flex;flex-wrap:wrap;gap:10px}
h2{font-size:clamp(1.8rem,6vw,2.8rem);margin-bottom:22px}
section{padding-block:48px;border-top:4px solid var(--tx)}
.steps{display:grid;gap:12px;counter-reset:s}
.step{display:flex;gap:16px;align-items:flex-start;background:var(--sf);border:2px solid var(--tx);border-radius:var(--rs);padding:18px}
.step::before{counter-increment:s;content:counter(s);font:var(--dw) 2.4rem/1 var(--disp);color:var(--ac);min-width:1.2em}
.tbl{display:grid;border:2px solid var(--tx);border-radius:var(--rs);overflow:hidden}
.tr{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;align-items:center;padding:16px;background:var(--sf)}
.tr+.tr{border-top:2px solid var(--tx)}
.tr .ico{grid-row:span 2;width:32px;height:32px;color:var(--ac)}
.tr b{font-size:1.1rem}.tr p{color:var(--tx2);font-size:.95rem}
.tickets{display:grid;gap:16px}
.ticket{position:relative;background:var(--sf);border:2px dashed var(--tx);border-radius:var(--rs);padding:22px 24px;display:grid;gap:8px}
.ticket::before,.ticket::after{content:"";position:absolute;top:50%;width:22px;height:22px;border-radius:50%;background:var(--bg);border:2px dashed var(--tx);transform:translateY(-50%)}
.ticket::before{right:-13px}.ticket::after{left:-13px}
.ticket .pr{font:var(--dw) 1.6rem var(--disp);color:var(--ac)}
.ticket ul{margin:0;padding-inline-start:18px;color:var(--tx2)}
.film{display:grid;grid-auto-flow:column;grid-auto-columns:70%;gap:8px;overflow-x:auto;background:#111;padding:14px;border-radius:var(--rs)}
.film div{aspect-ratio:4/3;border:2px dashed #555;display:grid;place-items:center;color:#aaa;font-size:.9rem;text-align:center;padding:10px}
form{display:grid;gap:14px;background:var(--sf);border:2px solid var(--tx);border-radius:var(--rs);padding:22px}
footer{background:#111;color:#cfcfcf;padding-block:28px;font-size:.9rem;display:grid;gap:6px}
.fine{color:#9a9a9a}
@media (min-width:860px){.hero{grid-template-columns:1.4fr 1fr;align-items:end}.steps{grid-template-columns:repeat(3,1fr)}.tickets{grid-template-columns:repeat(3,1fr)}.film{grid-auto-columns:32%}
.two{display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:start}}
"""
    rows = "".join(f'<div class="tr"><svg class="ico" viewBox="0 0 24 24">{s["icon"]}</svg><b>{s["title"]}</b>{"<p>"+s["text"]+"</p>" if s["text"] else "<p></p>"}</div>' for s in ctx["services"])
    tickets = "".join(f'<div class="ticket"><b>{p["name"]}</b><span class="pr">{_price(p)}</span><ul>{"".join("<li>"+i+"</li>" for i in p["items"])}</ul></div>' for p in ctx["packs"])
    sign = f'<div class="sign"><b>أوقات الدوام</b><span>{_hours(ctx)}</span></div>' if ctx["hours"] else (f'<div class="sign"><b>تقييمنا</b><span>{ctx["rline"]}</span></div>' if ctx["rline"] else "")
    body = f"""<div class="stripe"></div><header class="top in"><b>{ctx['name']}</b><a class="lat" href="tel:+{ctx['phone']}">{ctx['pdisp']}</a></header><div class="stripe"></div>
<div class="hero in"><div style="display:grid;gap:16px">{_demo(ctx)}<p class="tagline">مركز عناية بالسيارات • {ctx['city']}</p><h1>{ctx['headline'] or 'شغل نظيف، وسيارتك ترجع غير'}</h1>
<p>{ctx['intro']}</p>{'<p style="font-weight:700">'+ctx['rline']+'</p>' if ctx['rline'] and ctx['hours'] else ''}<div class="cta"><a class="btn" href="#book">احجز الحين</a><a class="btn alt" href="#svc">الخدمات</a></div></div>{sign}</div>
<section class="in"><h2>كيف تحجز؟</h2><div class="steps"><div class="step"><p>اختر الخدمة اللي تبيها من القائمة.</p></div><div class="step"><p>اكتب نوع سيارتك واسمك.</p></div><div class="step"><p>تنفتح لك رسالة جاهزة في واتساب، أرسلها ونرد عليك.</p></div></div></section>
<section class="in" id="svc"><h2>الخدمات</h2><div class="tbl">{rows}</div></section>
<section class="in"><h2>الباقات</h2><div class="tickets">{tickets}</div><p style="color:var(--tx2);font-size:.9rem;margin-top:14px">أسماء الباقات وأسعارها أمثلة تُستبدل بباقاتكم الفعلية.</p></section>
<section class="in"><h2>من الورشة</h2><div class="film"><div>صورة من أعمالكم</div><div>صورة من أعمالكم</div><div>صورة من أعمالكم</div><div>صورة من أعمالكم</div></div></section>
<section class="in two" id="book"><div><h2>احجز موعدك</h2>{_form(ctx)}</div><div><h2>الموقع</h2><p style="margin-bottom:12px">{ctx['addr']}</p>{_map(ctx)}</div></section>
<div class="stripe"></div><footer class="in"><b>{ctx['name']}</b><span>{ctx['addr']}</span>{_note(ctx)}</footer>"""
    return _page(ctx, css, body, "garage")


# ---------------------------------------------------------------- clean (app-like)
def clean(ctx):
    css = _root(ctx) + """
body{background:var(--sf2)}
.app{max-width:560px;margin-inline:auto;padding:0 16px 24px}
.bar{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px 0;background:var(--sf2)}
.bar b{font:var(--dw) 1.15rem var(--disp)}
.round{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:var(--sf);border:1px solid var(--ln);color:var(--tx)}
.hcard{background:var(--sf);border-radius:var(--r);padding:22px;display:grid;gap:12px;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.pill{justify-self:start;display:inline-flex;gap:6px;align-items:center;background:var(--sf2);border-radius:999px;padding:5px 12px;font-weight:600;font-size:.9rem}
.hcard h1{font-size:clamp(1.8rem,7vw,2.4rem)}
.hcard p{color:var(--tx2)}
.tabs{display:flex;gap:4px;background:var(--sf);border-radius:999px;padding:4px;margin:18px 0 12px;border:1px solid var(--ln)}
.tabs button{flex:1;min-height:42px;border:0;border-radius:999px;background:transparent;font:600 .95rem var(--txt);color:var(--tx2);cursor:pointer}
.tabs button[aria-selected=true]{background:var(--ac);color:var(--act)}
.panel{display:grid;gap:10px}
.li{display:flex;gap:14px;align-items:center;background:var(--sf);border-radius:var(--rs);padding:14px 16px}
.li .ico{color:var(--ac);width:28px;height:28px}
.li div{display:grid}.li span{color:var(--tx2);font-size:.9rem}
.pk{background:var(--sf);border-radius:var(--rs);padding:16px;display:grid;gap:6px;border:2px solid transparent}
.pk.pick{border-color:var(--ac)}
.pk .t{display:flex;justify-content:space-between;gap:10px;font-weight:700}
.pk .t span{color:var(--ac)}.pk p{color:var(--tx2);font-size:.92rem}
.small{font-size:.85rem;color:var(--tx2)}
h2{font-size:1.4rem;margin:26px 0 12px}
form{display:grid;gap:14px;background:var(--sf);border-radius:var(--r);padding:20px}
.opts{border:0;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}
.opts legend{font-weight:600;margin-bottom:8px}
.opt input{position:absolute;opacity:0}
.opt span{display:inline-flex;align-items:center;min-height:42px;padding:0 16px;border-radius:999px;border:1px solid var(--ln);background:var(--sf2);cursor:pointer}
.opt input:checked+span{background:var(--ac);color:var(--act);border-color:var(--ac)}
.opt input:focus-visible+span{outline:3px solid var(--ac);outline-offset:2px}
.rev{background:var(--sf);border-radius:var(--r);padding:18px;display:grid;gap:6px}
footer{text-align:center;color:var(--tx2);font-size:.85rem;padding:24px 0;display:grid;gap:4px}
@media (min-width:860px){body{padding-bottom:0}}
"""
    svc = "".join(f'<div class="li"><svg class="ico" viewBox="0 0 24 24">{s["icon"]}</svg><div><b>{s["title"]}</b>{"<span>"+s["text"]+"</span>" if s["text"] else ""}</div></div>' for s in ctx["services"])
    pk = "".join(f'<div class="pk{" pick" if p.get("pick") else ""}"><div class="t"><b>{p["name"]}</b><span>{_price(p)}</span></div><p>{"، ".join(p["items"])}</p></div>' for p in ctx["packs"])
    loc = (f'<div class="li"><svg class="ico" viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg><div><b>{ctx["loc"]}</b><span>{ctx["addr"]}</span></div></div>'
           + (f'<div class="li"><svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg><div><b>أوقات العمل</b><span>{_hours(ctx)}</span></div></div>' if ctx["hours"] else "")
           + _map(ctx))
    rev = f'<h2>من تقييمات العملاء</h2><div class="rev"><b>{ctx["rline"]}</b>{"<p>«"+ctx["review"]+"»</p>" if ctx["review"] else ""}</div>' if (ctx["review"] or ctx["rline"]) else ""
    body = f"""<div class="app"><header class="bar"><b>{ctx['name']}</b><a class="round" href="tel:+{ctx['phone']}" aria-label="اتصال"><svg class="ico" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg></a></header>
<div class="hcard">{_demo(ctx)}{'<span class="pill">⭐ '+str(ctx['rating'])+' • '+str(ctx['reviews'])+' تقييم</span>' if ctx['rating'] and ctx['reviews'] else ''}<h1>{ctx['headline'] or 'احجز عناية سيارتك بضغطة'}</h1><p>{ctx['intro']}</p><a class="btn" href="#book">ابدأ الحجز</a></div>
<div class="tabs" role="tablist" data-tabs hidden><button role="tab" aria-selected="true">الخدمات</button><button role="tab" aria-selected="false">الباقات</button><button role="tab" aria-selected="false">الموقع</button></div>
<div class="panel" data-panel>{svc}</div><div class="panel" data-panel>{pk}<p class="small">أسماء الباقات وأسعارها أمثلة تُستبدل بباقاتكم الفعلية.</p></div><div class="panel" data-panel>{loc}</div>
{rev}
<h2 id="book">الحجز</h2>{_form(ctx, radio=True)}
<footer><b>{ctx['name']}</b>{_note(ctx)}</footer></div>"""
    return _page(ctx, css, body, "clean")


# ---------------------------------------------------------------- magazine
def magazine(ctx):
    css = _root(ctx) + """
.mast{text-align:center;padding-block:22px 18px;border-bottom:3px double var(--tx)}
.mast .rule{display:flex;justify-content:space-between;gap:10px;font-size:.82rem;color:var(--tx2);border-bottom:1px solid var(--tx);padding-bottom:8px;margin-bottom:14px}
.mast .nm{font:var(--dw) clamp(2.6rem,12vw,6rem)/1 var(--disp)}
.mast .nm.latin{font:700 clamp(2rem,9vw,4.6rem)/1 var(--lat);letter-spacing:.12em}
.mast .sl{margin-top:10px;font-style:normal;color:var(--tx2)}
.lead{padding-block:36px;display:grid;gap:18px}
.lead h1{font-size:clamp(2rem,7vw,3.6rem)}
.drop::first-letter{float:right;font:var(--dw) 3.6em/0.9 var(--disp);color:var(--ac);margin-left:10px}
.cols{color:var(--tx2)}
.pull{border-block:2px solid var(--tx);padding-block:22px;margin-block:12px;font:var(--dw) clamp(1.4rem,5vw,2.2rem)/1.45 var(--disp);text-align:center}
.pull small{display:block;font:400 .9rem var(--txt);color:var(--tx2);margin-top:10px}
section{padding-block:40px;border-top:1px solid var(--tx)}
h2{font-size:clamp(1.6rem,5vw,2.4rem);margin-bottom:22px}
.feat{display:grid;grid-template-columns:auto 1fr;gap:4px 18px;padding-block:18px;border-bottom:1px solid var(--ln)}
.feat .n{grid-row:span 2;font:var(--dw) 3rem/1 var(--disp);color:var(--ac)}
.feat b{font-size:1.2rem}.feat p{color:var(--tx2)}
details{border-bottom:1px solid var(--ln);padding-block:14px}
summary{cursor:pointer;font-weight:700;list-style:none;display:flex;justify-content:space-between;gap:12px}
summary::after{content:"+";color:var(--ac);font-size:1.3rem;line-height:1}
details[open] summary::after{content:"–"}
details p{color:var(--tx2);margin-top:8px}
.plist{display:grid;gap:14px}
.plist div{display:grid;gap:4px;padding:16px 0;border-bottom:1px solid var(--ln)}
.plist .t{display:flex;justify-content:space-between;gap:12px;font-weight:700}
.plist .t span{color:var(--ac)}.plist p{color:var(--tx2);font-size:.95rem}
form{display:grid;gap:14px;border:1px solid var(--tx);padding:22px;border-radius:var(--rs)}
footer{border-top:3px double var(--tx);padding-block:24px;text-align:center;color:var(--tx2);font-size:.88rem;display:grid;gap:6px}
@media (min-width:860px){.cols{columns:2;column-gap:40px}.two{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}}
"""
    names = [s["title"] for s in ctx["services"]]
    feats = "".join(f'<div class="feat"><span class="n">{i + 1:02d}</span><b>{s["title"]}</b><p>{s["text"] or "تفاصيل الخدمة تُكتب هنا بكلام المركز."}</p></div>' for i, s in enumerate(ctx["services"]))
    plist = "".join(f'<div><span class="t"><b>{p["name"]}</b><span>{_price(p)}</span></span><p>{"، ".join(p["items"])}</p></div>' for p in ctx["packs"])
    faq = (f'<details><summary>كيف أحجز موعد؟</summary><p>من نموذج الحجز تحت: تختار الخدمة وتكتب نوع سيارتك، وتنفتح لك رسالة جاهزة في واتساب {ctx["name"]}.</p></details>'
           f'<details><summary>وين مكانكم؟</summary><p>{ctx["addr"]}. الخريطة تحت توصلك على طول.</p></details>'
           + (f'<details><summary>متى تفتحون؟</summary><p>{_hours(ctx)}</p></details>' if ctx["hours"] else "")
           + f'<details><summary>وش الخدمات اللي تقدمونها؟</summary><p>{"، ".join(names)}.</p></details>')
    first = ctx["intro"][:1]
    story = (f'<p class="{"drop" if first in "اأإآدذرزوؤءة" else ""}">{ctx["intro"]}</p>'
             + (f'<p style="margin-top:12px">تقييم {ctx["name"]} على خرائط قوقل {ctx["rating"]} من {ctx["reviews"]} تقييم، وتلقاه في {ctx["loc"]}.</p>' if ctx["rline"] else f'<p style="margin-top:12px">تلقانا في {ctx["loc"]}.</p>'))
    pull = f'<p class="pull">«{ctx["review"]}»<small>من زائر على خرائط قوقل</small></p>' if ctx["review"] else ""
    body = f"""<header class="mast in"><div class="rule"><span>{ctx['city']}</span><span>{_demo(ctx) or 'عناية بالسيارات'}</span><span class="lat">{ctx['pdisp']}</span></div>
<p class="nm{' latin' if ctx['latin'] else ''}">{ctx['name']}</p>{'<p class="sl">'+ctx['slogan']+'</p>' if ctx['slogan'] else ''}</header>
<div class="lead in"><h1>{ctx['headline'] or 'سيارتك بين أيدٍ تعرف قيمتها'}</h1><div class="cols">{story}</div>{pull}<div><a class="btn" href="#book">اطلب موعد</a></div></div>
<section class="in"><h2>الخدمات</h2>{feats}</section>
<section class="in"><h2>الباقات</h2><div class="plist">{plist}</div><p style="color:var(--tx2);font-size:.88rem;margin-top:12px">أسماء الباقات وأسعارها أمثلة تُستبدل بباقاتكم الفعلية.</p></section>
<section class="in"><h2>أسئلة تتكرر</h2>{faq}</section>
<section class="in two" id="book"><div><h2>طلب موعد</h2>{_form(ctx)}</div><div><h2>العنوان</h2>{_map(ctx)}</div></section>
<footer class="in"><b>{ctx['name']}</b><span>{ctx['addr']}</span>{_note(ctx)}</footer>"""
    return _page(ctx, css, body, "magazine")


# ---------------------------------------------------------------- blocks
def blocks(ctx):
    css = _root(ctx) + """
.blk{padding-block:56px}
.b-ac{background:var(--ac);color:var(--act)}
.b-ink{background:var(--tx);color:var(--bg)}
.b-sf{background:var(--sf2)}
.top{display:flex;justify-content:space-between;align-items:center;padding-block:16px;background:var(--ac);color:var(--act)}
.top a{font-weight:700;text-decoration:none}
.hero{padding-block:28px 0;display:grid;gap:18px}
.hero .nm{font:var(--dw) clamp(3rem,15vw,8rem)/.95 var(--disp)}
.hero .nm.latin{font:800 clamp(2.4rem,12vw,6.4rem)/.95 var(--lat);letter-spacing:.06em}
.hero p{max-width:34rem;opacity:.9}
.badge{width:118px;height:118px;border-radius:50%;background:var(--tx);color:var(--bg);display:grid;place-items:center;text-align:center;font-weight:700;line-height:1.2}
.badge b{font:var(--dw) 2rem var(--disp);display:block}
.row{display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between}
.b-ac .btn{background:var(--tx);color:var(--bg)}
.b-ac .btn.alt{background:transparent;color:var(--act);border-color:var(--act)}
.marquee{overflow:hidden;white-space:nowrap;border-block:2px solid currentColor;padding-block:12px;margin-top:28px}
.marquee div{display:inline-block;animation:mq 22s linear infinite;font:var(--dw) 1.4rem var(--disp)}
.marquee span{margin-inline:18px}
@keyframes mq{from{transform:translateX(0)}to{transform:translateX(50%)}}
h2{font-size:clamp(2rem,8vw,3.6rem);margin-bottom:26px}
.tiles{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.tile{aspect-ratio:1;border-radius:var(--r);padding:18px;display:flex;flex-direction:column;justify-content:space-between;background:var(--sf);border:1px solid var(--ln)}
.tile:nth-child(3n+1){background:var(--ac);color:var(--act);border-color:var(--ac)}
.tile:nth-child(3n+2){background:var(--tx);color:var(--bg);border-color:var(--tx)}
.tile .ico{width:36px;height:36px}
.tile b{font:var(--dw) 1.25rem/1.2 var(--disp)}
.packs{display:grid;gap:14px}
.pk{border:2px solid currentColor;border-radius:var(--r);padding:22px;display:grid;gap:8px}
.pk .pr{font:var(--dw) 2rem var(--disp);color:var(--ac)}
.pk p{opacity:.8}
.mosaic{display:grid;gap:10px;grid-template-columns:1fr 1fr}
.mosaic div{border:2px dashed currentColor;border-radius:var(--rs);display:grid;place-items:center;aspect-ratio:1;text-align:center;font-size:.9rem;opacity:.7;padding:8px}
.mosaic div:first-child{grid-column:span 2;aspect-ratio:2/1}
form{display:grid;gap:14px;background:var(--bg);color:var(--tx);border-radius:var(--r);padding:22px}
blockquote{margin:0;font:var(--dw) clamp(1.5rem,5vw,2.4rem)/1.4 var(--disp)}
footer{padding-block:26px;font-size:.9rem;display:grid;gap:6px}
@media (min-width:860px){.packs{grid-template-columns:repeat(3,1fr)}.two{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}.mosaic{grid-template-columns:repeat(4,1fr)}.mosaic div:first-child{grid-column:span 2;grid-row:span 2;aspect-ratio:auto}}
"""
    names = [s["title"] for s in ctx["services"]]
    ticker = "".join(f"<span>{n}</span><span>✦</span>" for n in names) * 4
    tiles = "".join(f'<div class="tile"><svg class="ico" viewBox="0 0 24 24">{s["icon"]}</svg><b>{s["title"]}</b></div>' for s in ctx["services"])
    pk = "".join(f'<div class="pk"><b style="font-size:1.2rem">{p["name"]}</b><span class="pr">{_price(p)}</span><p>{"، ".join(p["items"])}</p></div>' for p in ctx["packs"])
    badge = f'<div class="badge"><div><b>{ctx["rating"]}</b>من {ctx["reviews"]} تقييم</div></div>' if ctx["rating"] and ctx["reviews"] else ""
    rev = f'<div class="blk b-sf"><div class="in"><blockquote>«{ctx["review"]}»</blockquote><p style="margin-top:12px;color:var(--tx2)">من زائر على خرائط قوقل</p></div></div>' if ctx["review"] else ""
    body = f"""<header class="top in"><span>{_demo(ctx)}</span><a class="lat" href="tel:+{ctx['phone']}">{ctx['pdisp']}</a></header>
<div class="blk b-ac" style="padding-top:12px"><div class="in hero"><p class="nm{' latin' if ctx['latin'] else ''}">{ctx['name']}</p>
<div class="row"><div style="display:grid;gap:14px"><h1 style="font-size:clamp(1.4rem,5vw,2rem)">{ctx['headline'] or 'عناية بسيارتك في ' + ctx['city']}</h1><p>{ctx['intro']}</p>
<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="#book">احجز</a><a class="btn alt" href="#svc">الخدمات</a></div></div>{badge}</div></div>
<div class="marquee" aria-hidden="true"><div>{ticker}</div></div></div>
<div class="blk" id="svc"><div class="in"><h2>الخدمات</h2><div class="tiles">{tiles}</div></div></div>
<div class="blk b-ink"><div class="in"><h2>الباقات</h2><div class="packs">{pk}</div><p style="opacity:.7;font-size:.88rem;margin-top:14px">أسماء الباقات وأسعارها أمثلة تُستبدل بباقاتكم الفعلية.</p></div></div>
<div class="blk"><div class="in"><h2>الشغل</h2><div class="mosaic"><div>صورة من أعمالكم</div><div>صورة</div><div>صورة</div><div>صورة</div><div>صورة</div></div></div></div>
{rev}
<div class="blk b-ac" id="book"><div class="in two"><div><h2>احجز موعدك</h2><p style="margin-bottom:16px">{ctx['addr']}</p>{_map(ctx)}</div>{_form(ctx)}</div></div>
<footer class="in"><b>{ctx['name']}</b>{_note(ctx)}</footer>"""
    return _page(ctx, css, body, "blocks")


# ---------------------------------------------------------------- local (map-first)
def local(ctx):
    css = _root(ctx) + """
.mapwrap{position:relative}
.mapwrap iframe.map{height:min(46svh,420px);border-radius:0}
.card{position:relative;margin:-48px 16px 0;background:var(--sf);border:1px solid var(--ln);border-radius:var(--r);padding:20px;display:grid;gap:10px;box-shadow:0 10px 30px rgba(0,0,0,.12);max-width:720px}
.card h1{font-size:clamp(1.7rem,7vw,2.6rem)}
.card .cat{color:var(--tx2)}
.stars{color:#f5a524;letter-spacing:2px}
.acts{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:6px}
.act{display:grid;justify-items:center;gap:6px;text-decoration:none;font-weight:600;font-size:.9rem;padding:12px 4px;border-radius:var(--rs);background:var(--sf2)}
.act .ico{color:var(--ac);width:28px;height:28px}
.act.main{background:var(--ac);color:var(--act)}.act.main .ico{color:var(--act)}
section{padding-block:36px}
h2{font-size:1.5rem;margin-bottom:16px}
.hrs{width:100%;border-collapse:collapse}
.hrs td{padding:10px 0;border-bottom:1px solid var(--ln)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips span{border:1px solid var(--ln);border-radius:999px;padding:6px 14px;background:var(--sf)}
.list{display:grid;gap:10px;margin-top:16px}
.list div{display:flex;gap:12px;align-items:flex-start;background:var(--sf);border:1px solid var(--ln);border-radius:var(--rs);padding:14px}
.list .ico{color:var(--ac)}.list p{color:var(--tx2);font-size:.93rem}
.rv{display:flex;gap:12px;background:var(--sf);border:1px solid var(--ln);border-radius:var(--r);padding:16px}
.av{width:42px;height:42px;border-radius:50%;background:var(--ac);color:var(--act);display:grid;place-items:center;font-weight:700;flex:none}
.pk{display:flex;justify-content:space-between;gap:12px;padding:14px 0;border-bottom:1px solid var(--ln)}
.pk p{color:var(--tx2);font-size:.9rem}.pk span{color:var(--ac);font-weight:700;white-space:nowrap}
form{display:grid;gap:14px;background:var(--sf);border:1px solid var(--ln);border-radius:var(--r);padding:20px}
footer{padding-block:24px;color:var(--tx2);font-size:.88rem;display:grid;gap:4px;border-top:1px solid var(--ln)}
.wrapc{max-width:760px;margin-inline:auto}
"""
    stars = "★" * int(round(float(ctx["rating"]))) if ctx["rating"] else ""
    rating = f'<p><b>{ctx["rating"]}</b> <span class="stars">{stars}</span> <span style="color:var(--tx2)">({ctx["reviews"]} تقييم)</span></p>' if ctx["rating"] and ctx["reviews"] else ""
    cat = " • ".join(s["title"] for s in ctx["services"][:3])
    hrs = ("<section class='in wrapc'><h2>أوقات العمل</h2><table class='hrs'>" + "".join(f"<tr><td>{h}</td></tr>" for h in ctx["hours"]) + "</table></section>") if ctx["hours"] else ""
    lst = "".join(f'<div><svg class="ico" viewBox="0 0 24 24">{s["icon"]}</svg><span><b>{s["title"]}</b>{"<p>"+s["text"]+"</p>" if s["text"] else ""}</span></div>' for s in ctx["services"])
    rev = f'<section class="in wrapc"><h2>التقييمات</h2><div class="rv"><span class="av">ز</span><div><b>زائر على خرائط قوقل</b><p>{ctx["review"]}</p></div></div></section>' if ctx["review"] else ""
    pk = "".join(f'<div class="pk"><div><b>{p["name"]}</b><p>{"، ".join(p["items"])}</p></div><span>{_price(p)}</span></div>' for p in ctx["packs"])
    pin = '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>'
    tel = '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>'
    chat = '<path d="M4 20l1.5-4A8 8 0 1 1 9 19z"/>'
    body = f"""<div class="mapwrap">{_map(ctx)}</div>
<div class="wrapc"><div class="card">{_demo(ctx)}<h1>{ctx['name']}</h1><p class="cat">{cat} • {ctx['loc']}</p>{rating}
<div class="acts"><a class="act main" href="https://wa.me/{ctx['phone']}" target="_blank" rel="noopener"><svg class="ico" viewBox="0 0 24 24">{chat}</svg>واتساب</a>
<a class="act" href="tel:+{ctx['phone']}"><svg class="ico" viewBox="0 0 24 24">{tel}</svg>اتصال</a>
<a class="act" href="{_dir(ctx)}" target="_blank" rel="noopener"><svg class="ico" viewBox="0 0 24 24">{pin}</svg>الاتجاهات</a></div>
<p style="color:var(--tx2)">{ctx['addr']}</p></div></div>
<section class="in wrapc"><h2>{ctx['headline'] or 'الخدمات'}</h2><div class="chips">{''.join('<span>'+s['title']+'</span>' for s in ctx['services'])}</div><div class="list">{lst}</div></section>
{hrs}{rev}
<section class="in wrapc"><h2>الباقات</h2>{pk}<p style="color:var(--tx2);font-size:.88rem;margin-top:10px">أسماء الباقات وأسعارها أمثلة تُستبدل بباقاتكم الفعلية.</p></section>
<section class="in wrapc" id="book"><h2>احجز موعد</h2>{_form(ctx, radio=True)}</section>
<footer class="in wrapc"><b>{ctx['name']}</b><span class="lat">{ctx['pdisp']}</span>{_note(ctx)}</footer>"""
    return _page(ctx, css, body, "local")


TEMPLATES = {"showroom": showroom, "garage": garage, "clean": clean, "magazine": magazine, "blocks": blocks, "local": local}
