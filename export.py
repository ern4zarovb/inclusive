"""export.py — рендер всех HTML-страниц в PDF и PNG (Playwright, Chromium).
Запуск: python export.py  (нужно: pip install playwright && playwright install chromium)"""
import glob, os
from playwright.sync_api import sync_playwright

os.makedirs("export", exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in sorted(glob.glob("booklet-*.html") + glob.glob("poster*.html")):
        name = os.path.splitext(f)[0]
        is_poster = name.startswith("poster")
        w, h = (210, 297) if is_poster else (297, 210)
        pg = b.new_page(viewport={"width": round(w / 25.4 * 96), "height": round(h / 25.4 * 96)}, device_scale_factor=2)
        pg.goto("file://" + os.path.abspath(f)); pg.wait_for_timeout(600)
        over = pg.evaluate("[...document.querySelectorAll('.panel, .poster-sheet')].filter(e=>e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1).length")
        pg.screenshot(path=f"export/{name}.png")
        pg.pdf(path=f"export/{name}.pdf", width=f"{w}mm", height=f"{h}mm", print_background=True, prefer_css_page_size=True)
        print(f"{name}: OK" + (f"  ВНИМАНИЕ: переполнение в {over} блоках" if over else ""))
        pg.close()
    b.close()
