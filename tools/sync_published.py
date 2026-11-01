#!/usr/bin/env python3
"""Copy the demos already published on the Cloudflare Worker into this checkout, so the
design picker and the copy check in make_demo.py see them (otherwise every new demo
is compared only with the old repo demos and ends up looking like the last one).

Usage:  python3 tools/sync_published.py <slug> [<slug> ...]
Get the slugs from the KV namespace key list (carcare-demos). Run before make_demo.py.
Writes sample/demos/<slug>/index.html (the live version wins over an older repo copy).
"""
import os, re, sys, urllib.request

BASE = "https://carcare-demos.abuljadayelabdulrahman.workers.dev/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if len(sys.argv) < 2:
    sys.exit(__doc__)
for slug in sys.argv[1:]:
    if not re.fullmatch(r"[a-z0-9-]+", slug):
        print(f"skip {slug!r}: not a slug")
        continue
    try:
        req = urllib.request.Request(BASE + slug + "/", headers={"User-Agent": "curl/8 carcare-sync"})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    except Exception as ex:  # noqa: BLE001
        print(f"skip {slug}: {ex}")
        continue
    if "<html" not in html[:500].lower():
        print(f"skip {slug}: not a page")
        continue
    d = os.path.join(ROOT, "sample", "demos", slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)
    print(f"synced {slug}")
