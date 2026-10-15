import json
import urllib.request

USER = "otacs-dev"
HIDE = {"Jupyter Notebook"}
COLS = 3          # muda aqui pra 4, 2 etc.
W, PAD = 600, 25
FONT = 'font-family="Segoe UI, Ubuntu, sans-serif"'
COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178C6", "JavaScript": "#F1E05A",
    "TSQL": "#E38C00", "Haskell": "#5E5086", "HTML": "#E34C26",
    "CSS": "#563D7C", "R": "#198CE7", "Shell": "#89E051",
}

def get(url):
    return json.load(urllib.request.urlopen(url))

totals = {}
for repo in get(f"https://api.github.com/users/{USER}/repos?per_page=100"):
    if repo["fork"]:
        continue
    for lang, size in get(repo["languages_url"]).items():
        if lang not in HIDE:
            totals[lang] = totals.get(lang, 0) + size

langs = sorted(totals.items(), key=lambda kv: -kv[1])[:12]
shown = sum(size for _, size in langs)
rows = -(-len(langs) // COLS)
H = 85 + rows * 25
bar_w = W - 2 * PAD
col_w = bar_w / COLS

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="#fff" stroke="#d0d7de"/>',
    f'<text x="{PAD}" y="35" {FONT} font-size="18" font-weight="600" fill="#24292f">Most used languages</text>',
    f'<clipPath id="c"><rect x="{PAD}" y="48" width="{bar_w}" height="8" rx="4"/></clipPath>',
    '<g clip-path="url(#c)">',
]
x = PAD
for lang, size in langs:
    w = bar_w * size / shown
    svg.append(f'<rect x="{x:.1f}" y="48" width="{w:.1f}" height="8" fill="{COLORS.get(lang, "#8B949E")}"/>')
    x += w
svg.append("</g>")

for i, (lang, size) in enumerate(langs):
    cx = PAD + (i % COLS) * col_w
    cy = 85 + (i // COLS) * 25
    color = COLORS.get(lang, "#8B949E")
    svg.append(f'<circle cx="{cx + 5:.1f}" cy="{cy - 4}" r="5" fill="{color}"/>')
    svg.append(f'<text x="{cx + 16:.1f}" y="{cy}" {FONT} font-size="12" fill="#57606a">{lang} {size / shown * 100:.2f}%</text>')

svg.append("</svg>")
open("languages.svg", "w", encoding="utf-8").write("\n".join(svg))
