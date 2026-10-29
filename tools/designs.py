"""Design system for the demo generator: every demo gets its own look.

A design is a combination of four choices:
  layout   which website design (completely different pages, see templates.py;
           "classic" is the original page in make_demo.py)
  fonts    an Arabic display + text font pair
  shape    corner radius and button shape
  palette  background / surface / accent colours (the shop's own brand colour still wins)

pick_design() looks at the demos and client sites already in the repo (each page
records its design in <meta name="design">) and picks the least-used layout,
font pair, shape and palette, so two shops never get the same site.
"""
import glob, hashlib, os, re

LAYOUTS = ["classic", "showroom", "garage", "clean", "magazine", "blocks", "local"]
# layouts that only suit one theme (the rest work in light and dark)
LAYOUT_THEME = {"showroom": "dark", "magazine": "light"}

FONTS = {
    "lalezar": dict(display="Lalezar", dw=400, text="IBM Plex Sans Arabic",
                    css="family=Lalezar&family=IBM+Plex+Sans+Arabic:wght@400;500;600"),
    "changa": dict(display="Changa", dw=700, text="Cairo",
                   css="family=Changa:wght@600;700&family=Cairo:wght@400;600"),
    "reem": dict(display="Reem Kufi", dw=700, text="Tajawal",
                 css="family=Reem+Kufi:wght@600;700&family=Tajawal:wght@400;500;700"),
    "messiri": dict(display="El Messiri", dw=700, text="Almarai",
                    css="family=El+Messiri:wght@600;700&family=Almarai:wght@400;700"),
    "alexandria": dict(display="Alexandria", dw=800, text="Readex Pro",
                       css="family=Alexandria:wght@700;800&family=Readex+Pro:wght@400;500;600"),
    "kufi": dict(display="Noto Kufi Arabic", dw=800, text="Rubik",
                 css="family=Noto+Kufi+Arabic:wght@700;800&family=Rubik:wght@400;500;600"),
}

SHAPES = {
    "round": dict(r=26, rs=18, btn=999, field=12),
    "soft": dict(r=14, rs=10, btn=12, field=10),
    "sharp": dict(r=4, rs=3, btn=4, field=3),
}

# bg, surface, surface2, text, text2, line, accent
PALETTES = {
    "obsidian-gold": ("dark", "#0a0a0c", "#131317", "#1b1b20", "#f3f3f4", "#a3a3ab", "#26262c", "#cfae6b"),
    "midnight-sky": ("dark", "#0b1220", "#111a2c", "#18233a", "#eef3fb", "#9fb0c8", "#24314a", "#4cc3ff"),
    "carbon-lime": ("dark", "#0e0f0c", "#161813", "#1f221a", "#f2f5ea", "#a6ad98", "#2a2e23", "#c6f432"),
    "graphite-orange": ("dark", "#111214", "#18191c", "#212226", "#f4f4f5", "#a1a1aa", "#2c2d32", "#ff7a1a"),
    "forest-mint": ("dark", "#07130f", "#0d1c17", "#132620", "#ecf7f2", "#93b3a6", "#1e3a30", "#3ddc97"),
    "pearl-red": ("light", "#eef1f4", "#ffffff", "#e1e6eb", "#0d1b26", "#3b4b58", "#cfd6dd", "#c8141f"),
    "sand-bronze": ("light", "#f5efe6", "#fffaf3", "#ebe1d3", "#2a1d12", "#6b5845", "#ddd0bf", "#9a5b22"),
    "ice-navy": ("light", "#f1f5fb", "#ffffff", "#e2e9f4", "#0c1a33", "#43526b", "#d3dcea", "#1d4ed8"),
    "cream-teal": ("light", "#f6f4ee", "#ffffff", "#e9e6dc", "#14231f", "#4d5c57", "#dcd8cb", "#0f766e"),
}

# wording of the classic design (the other designs carry their own wording in templates.py)
WORDS = {
    "classic": dict(services=("خدماتنا", "كل خدمة واضحة قبل ما تراسلنا."), packs=("الباقات والأسعار", "أسعار وتفاصيل باقاتكم تظهر هنا بترتيب يفهمه العميل من أول نظرة."),
                    work=("أعمالنا", "هنا تظهر صور سياراتكم قبل وبعد، بحجم واضح على الجوال."), reviews="آراء عملائنا", map="موقعنا", book="احجز موعدك",
                    cta="احجز موعدك", cta2="شوف الباقات", dock="احجز بالواتساب"),
}
DOCK = {"showroom": "احجز بالواتساب", "garage": "احجز الحين", "clean": "واتساب", "magazine": "راسلنا", "blocks": "احجز", "local": "واتساب"}


def _used(root):
    used = []
    for f in glob.glob(os.path.join(root, "sample", "demos", "*", "index.html")) + glob.glob(os.path.join(root, "clients", "*", "index.html")):
        slug = os.path.basename(os.path.dirname(f))
        txt = open(f, encoding="utf-8").read(4000)
        m = re.search(r'<meta name="design" content="([^"]+)"', txt)
        if m:
            used.append((slug, dict(kv.split("=", 1) for kv in m.group(1).split(";") if "=" in kv)))
        else:  # pages made before the design system all used the classic layout and Lalezar
            used.append((slug, dict(layout="classic", fonts="lalezar", shape="round",
                                    palette="obsidian-gold" if "--pearl:#0a0a0c" in txt else "pearl-red")))
    return used


def _least_used(options, taken, seed):
    counts = {o: 0 for o in options}
    for t in taken:
        if t in counts:
            counts[t] += 1
    low = min(counts.values())
    pool = [o for o in options if counts[o] == low]
    return pool[int(hashlib.md5(seed.encode()).hexdigest(), 16) % len(pool)]


def pick_design(root, slug, theme=None, wanted=None):
    """Return {layout, fonts, shape, palette}. Re-running for the same slug keeps its design."""
    wanted = dict(wanted or {})
    used = [(s, d) for s, d in _used(root)]
    for s, d in used:
        if s == slug and not wanted:
            return d  # keep the design this shop already has
    others = [d for s, d in used if s != slug]
    out = {}
    lays = [l for l in LAYOUTS if not theme or LAYOUT_THEME.get(l, theme) == theme]
    out["layout"] = wanted.get("layout") or _least_used(lays, [d.get("layout") for d in others], slug + "L")
    theme = theme or LAYOUT_THEME.get(out["layout"])
    out["fonts"] = wanted.get("fonts") or _least_used(list(FONTS), [d.get("fonts") for d in others], slug + "F")
    out["shape"] = wanted.get("shape") or _least_used(list(SHAPES), [d.get("shape") for d in others], slug + "S")
    pals = [p for p, v in PALETTES.items() if not theme or v[0] == theme]
    out["palette"] = wanted.get("palette") or _least_used(pals, [d.get("palette") for d in others], slug + "P")
    for k, v in (("layout", LAYOUTS), ("fonts", FONTS), ("shape", SHAPES), ("palette", PALETTES)):
        if out[k] not in v:
            raise SystemExit(f"unknown {k}: {out[k]}")
    return out


def _lum(hexc):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def colors(design, override=None):
    t, bg, s, s2, tx, tx2, line, acc = PALETTES[design["palette"]]
    c = dict(dark=t == "dark", bg=bg, surface=s, surface2=s2, text=tx, text2=tx2, line=line, accent=acc)
    for k, v in (override or {}).items():
        if k in c and v:
            c[k] = v
    if not c.get("accent_text"):
        c["accent_text"] = "#0a0a0c" if _lum(c["accent"]) > 0.36 else "#ffffff"
    if (override or {}).get("accent_text"):
        c["accent_text"] = override["accent_text"]
    c["paint"] = (override or {}).get("paint") or "#4a4a52"
    return c
