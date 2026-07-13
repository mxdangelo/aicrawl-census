"""Export report figures as PNGs for the slide deck.

Usage: python run_figures.py
Renders report.html in a headless browser, forces each theme, and screenshots
individual figure cards at 2x. Output: figures/*.png. Requires playwright
(`pip install playwright && playwright install chromium`).
"""
import pathlib

from playwright.sync_api import sync_playwright

REPORT = pathlib.Path("report.html").resolve().as_uri()
OUT = pathlib.Path("figures")
OUT.mkdir(exist_ok=True)

# (output name, CSS selector, theme)
SHOTS = [
    ("heatmap_light", "#f-heatmap", "light"),
    ("deciders_light", "#f-deciders", "light"),
    ("crawlers_light", "#f-crawlers", "light"),
    ("scatter_light", "#f-scatter", "light"),
    ("scatter_dark", "#f-scatter", "dark"),
]

# hide the long caption and table toggle so the chart fills the crop —
# otherwise the chart shrinks to make room and its text reads tiny on a slide;
# and bump the in-chart type ~25% so it holds up against slide body text.
HIDE = "document.querySelectorAll('figcaption, details.tv').forEach(e => e.style.display='none')"
BUMP = """
var s = document.createElement('style');
s.textContent = '.card text.lab, .card text.val, .card text.segl {font-size:15px}'
  + '.card .lab-t{font-size:14px} .card h3{font-size:19px} .card .legend{font-size:14px}';
document.head.appendChild(s);
"""


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": 960, "height": 1200},
                                  device_scale_factor=2)
        page = ctx.new_page()
        page.goto(REPORT)
        page.evaluate(HIDE)
        page.evaluate(BUMP)
        for name, sel, theme in SHOTS:
            page.evaluate(
                "t => document.querySelector('.viz').setAttribute('data-theme', t)",
                theme)
            page.wait_for_timeout(120)
            el = page.query_selector(sel)
            box = el.bounding_box()
            el.screenshot(path=str(OUT / f"{name}.png"))
            print(f"  {name}.png  {box['width']:.0f}x{box['height']:.0f} css px "
                  f"(ratio {box['width'] / box['height']:.2f})")
        browser.close()
    print(f"\nWrote {len(SHOTS)} PNGs to {OUT}/ (at 2x device scale).")


if __name__ == "__main__":
    main()
