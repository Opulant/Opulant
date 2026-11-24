#!/usr/bin/env python3
"""Builds the GitHub profile README panels as self-contained SVGs in the opulant.dev style.
GitHub strips CSS from READMEs, so the look lives in images: fonts are embedded, nothing loads remotely."""
import base64, pathlib
from xml.sax.saxutils import escape as x

ROOT = pathlib.Path(__file__).parent
FONTS = pathlib.Path.home() / "Developer/opulant-blog/site/fonts"
W = 1200
GX = 48
FG, DIM, RED, LINE, SOFT = "#efeef5", "#8b8a9e", "#ff2d46", "rgba(239,238,245,.17)", "#c9c8d6"

def font(family, weight, file):
    data = base64.b64encode((FONTS / file).read_bytes()).decode()
    return f'@font-face{{font-family:"{family}";font-weight:{weight};src:url(data:font/woff2;base64,{data}) format("woff2")}}'

STYLE = "".join([
    font("Silkscreen", 400, "silkscreen-400.woff2"), font("Silkscreen", 700, "silkscreen-700.woff2"),
    font("IBM Plex Mono", 400, "plex-mono-400.woff2"), font("DotGothic16", 400, "dotgothic-kana.woff2"),
    '.px{font-family:"Silkscreen","DotGothic16",monospace;text-transform:uppercase}',
    '.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace}',
    '.jp{font-family:"DotGothic16","Hiragino Kaku Gothic ProN",sans-serif}',
    ".lbl{font-size:13px;letter-spacing:2.1px}",
    "@keyframes blink{50%{opacity:0}}.blink{animation:blink 1.1s steps(1) infinite}.lamp{animation:blink 2.4s steps(1) infinite}",
    "@keyframes ga{0%,89%,100%{opacity:0}90%{opacity:.9;transform:translate(-6px,0)}91.5%{opacity:.9;transform:translate(5px,0)}93%{opacity:.9;transform:translate(-3px,0)}94.5%{opacity:0}}",
    "@keyframes gb{0%,89%,100%{opacity:0}90%{opacity:.8;transform:translate(6px,0)}92%{opacity:.8;transform:translate(-5px,0)}93.5%{opacity:.8;transform:translate(3px,0)}94.5%{opacity:0}}",
    ".ga{opacity:0;animation:ga 6s steps(1) infinite}.gb{opacity:0;animation:gb 6s steps(1) infinite}",
    "@media (prefers-reduced-motion:reduce){.blink,.lamp,.ga,.gb{animation:none}}",
])

DEFS = f'''<defs><style>{STYLE}</style>
<pattern id="grid" width="112" height="112" patternUnits="userSpaceOnUse"><path d="M0 .5H112M.5 0V112" stroke="rgba(150,160,255,.075)" stroke-width="1" fill="none"/></pattern>
<pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse"><rect y="2" width="3" height="1" fill="rgba(0,0,0,.2)"/></pattern>
<pattern id="ink" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="2" fill="{FG}"/><rect y="2" width="3" height="1" fill="rgba(239,238,245,.5)"/></pattern>
</defs>'''

def svg(name, h, body, title):
    out = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="{x(title)}">
<title>{x(title)}</title>{DEFS}
<rect width="{W}" height="{h}" fill="#000"/><rect width="{W}" height="{h}" fill="url(#grid)"/>
{body}
<rect width="{W}" height="{h}" fill="url(#scan)"/>
</svg>'''
    (ROOT / "assets" / name).write_text(out)

def heading(layer, text, sub, y=0):
    return f'''<text class="px" x="{GX}" y="{y+62}" font-size="12" letter-spacing="1.9" fill="{RED}">layer:{layer}</text>
<text class="px" x="{GX-3}" y="{y+132}" font-size="68" font-weight="700" fill="{FG}">{x(text)}</text>
<text class="mono" x="{W-GX}" y="{y+128}" font-size="15" fill="{DIM}" text-anchor="end">{x(sub)}</text>
<rect x="{GX}" y="{y+158}" width="{W-2*GX}" height="1" fill="{LINE}"/>'''

# ---------------------------------------------------------------- hero
H = 560
dots = "".join(
    f'<pattern id="d{i}" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="{r}" fill="{RED}"/></pattern>'
    for i, r in enumerate([.5, .9, 1.4, 1.9, 2.5, 3.1]))
band_top, row = H - 138, 23
dither = "".join(f'<rect x="0" y="{band_top + i*row}" width="{W}" height="{row}" fill="url(#d{i})"/>' for i in range(6))
lede = ["SOC analyst triaging 100+ alerts a day across", "200+ defense-industrial-base clients under CMMC",
        "and NIST SP 800-53. Sentinel, Defender XDR,", "Google SecOps, Entra ID. Working toward red team,",
        "where the job is producing the logs instead of", "reading them."]
name = lambda cls, fill: f'<text class="px {cls}" x="{GX-4}" y="352" font-size="86" font-weight="700" textLength="1036" lengthAdjust="spacingAndGlyphs" fill="{fill}">Celty Sturluson</text>'
hero = f'''<defs>{dots}</defs>
<circle cx="1010" cy="170" r="250" fill="none" stroke="rgba(150,160,255,.06)" stroke-width="1"/><circle cx="1010" cy="170" r="200" fill="none" stroke="rgba(150,160,255,.08)"/><circle cx="1010" cy="170" r="150" fill="none" stroke="rgba(150,160,255,.1)"/><circle cx="1010" cy="170" r="100" fill="none" stroke="rgba(150,160,255,.12)"/><circle cx="1010" cy="170" r="50" fill="none" stroke="rgba(150,160,255,.13)"/>
<rect x="{GX}" y="67" width="34" height="1" fill="{RED}"/>
<text class="px lbl" x="{GX+46}" y="72" fill="{RED}">Layer:00 / node online</text>
<text class="px" font-size="30" letter-spacing="2.6" fill="{FG}"><tspan x="{GX}" y="128">Reads the logs.</tspan><tspan x="{GX}" y="170">Hunts the signal.</tspan><tspan x="{GX}" y="212" fill="{RED}">Heading red.</tspan></text>
<text class="mono" font-size="15.5" fill="{SOFT}">{"".join(f'<tspan x="690" y="{92 + i*27}">{x(l)}</tspan>' for i, l in enumerate(lede))}</text>
<text class="jp" x="690" y="270" font-size="14" letter-spacing="7" fill="{DIM}">セルティ・ストゥルルソン</text>
{dither}
<g transform="translate(0,{H-255}) scale(.75)">
<g fill="none" stroke="{FG}" stroke-width="1.5">
<path d="M0 118 Q 110 152 230 112"/><path d="M0 136 Q 110 172 230 130"/><path d="M0 154 Q 110 192 230 148"/>
<path d="M230 112 Q 520 204 800 104"/><path d="M230 130 Q 520 224 800 122"/><path d="M230 148 Q 520 244 800 140"/><path d="M230 130 Q 520 176 800 140"/>
<path d="M800 104 Q 1080 190 1360 116"/><path d="M800 122 Q 1080 212 1360 134"/><path d="M800 140 Q 1080 232 1360 152"/><path d="M800 104 Q 1080 150 1360 134"/>
<path d="M1360 116 Q 1480 146 1600 126"/><path d="M1360 134 Q 1480 166 1600 144"/><path d="M1360 152 Q 1480 186 1600 162"/>
<path d="M818 196 Q 900 330 1010 340" stroke-width="1"/><path d="M236 150 Q 200 250 150 340" stroke-width="1"/></g>
<g fill="#000" stroke="{FG}" stroke-width="1.5">
<rect x="224" y="78" width="12" height="270"/><rect x="190" y="106" width="80" height="8"/><rect x="198" y="126" width="64" height="8"/><rect x="198" y="144" width="64" height="8"/>
<rect x="794" y="62" width="12" height="290"/><rect x="752" y="98" width="96" height="8"/><rect x="762" y="118" width="76" height="8"/><rect x="762" y="136" width="76" height="8"/>
<rect x="808" y="154" width="28" height="42"/>
<rect x="1354" y="84" width="12" height="270"/><rect x="1318" y="110" width="84" height="8"/><rect x="1326" y="130" width="68" height="8"/><rect x="1326" y="148" width="68" height="8"/></g>
<rect class="lamp" x="816" y="180" width="12" height="7" fill="{RED}"/></g>
{name("ga", RED)}{name("gb", "#7fd4e6")}{name("", "url(#ink)")}
<rect class="blink" x="1092" y="300" width="30" height="52" fill="{RED}"/>
<rect x="{GX}" y="{H-44}" width="318" height="30" fill="#000"/><rect class="blink" x="{GX+10}" y="{H-33}" width="7" height="7" fill="{RED}"/>
<text class="px lbl" x="{GX+28}" y="{H-24}" font-size="12" fill="{FG}">Carrier stable / 60hz hum</text>
<rect x="{W-GX-128}" y="{H-44}" width="128" height="30" fill="#000"/>
<text class="jp" x="{W-GX-12}" y="{H-23}" font-size="14" letter-spacing="5" fill="{RED}" text-anchor="end">ブーン…</text>'''
svg("hero.svg", H, hero, "Celty Sturluson. SOC analyst, detection and response. Reads the logs. Hunts the signal. Heading red.")

# ---------------------------------------------------------------- ident
stats = [("100", "+", "Alerts triaged a day"), ("200", "+", "Client environments"), ("10", "", "Escalations a day"), ("14", "", "Certifications")]
read = [("Role", "SOC I Analyst", FG), ("Side", "Blue, heading red", FG), ("In progress", "HTB CDSA", FG), ("Status", "Open to roles", RED)]
col = (W - 2*GX) / 4
body = heading("01", "Ident", "Who is on this node, and where the traffic is going.")
for i, (n, plus, label) in enumerate(stats):
    cx = GX + i*col + (22 if i else 0)
    if i: body += f'<rect x="{GX + i*col}" y="158" width="1" height="150" fill="{LINE}"/>'
    body += f'<text class="px" x="{cx-3}" y="246" font-size="72" font-weight="700" fill="{FG}">{n}<tspan fill="{RED}">{plus}</tspan></text>'
    body += f'<text class="px" x="{cx}" y="280" font-size="11.5" letter-spacing="1.8" fill="{DIM}">{x(label)}</text>'
body += f'<rect x="{GX}" y="308" width="{W-2*GX}" height="1" fill="{LINE}"/>'
for i, (k, v, c) in enumerate(read):
    cx = GX + i*col + (22 if i else 0)
    body += f'<text class="px" x="{cx}" y="352" font-size="11.5" letter-spacing="1.8" fill="{DIM}">{x(k)}</text><text class="mono" x="{cx}" y="382" font-size="16" fill="{c}">{x(v)}</text>'
svg("ident.svg", 424, body, "Ident. 100+ alerts triaged a day, 200+ client environments, about 10 escalations a day with evidence, 14 certifications. Role: SOC I Analyst. Side: blue, heading red. In progress: HTB CDSA. Status: open to roles.")

# ---------------------------------------------------------------- stack
groups = [
    ("SIEM and detection", ["Microsoft Sentinel", "Defender XDR", "Google SecOps (Chronicle)", "KQL", "UEBA", "Alert tuning"]),
    ("Incident response", ["Phishing analysis", "IOC enrichment", "VirusTotal", "AbuseIPDB", "MITRE ATT&CK"]),
    ("Identity and cloud", ["Microsoft Entra ID", "Conditional Access", "Azure", "Active Directory", "MFA"]),
    ("Compliance", ["NIST SP 800-53", "NIST RMF", "CMMC", "FISMA", "Findings reports"]),
    ("Security testing", ["Burp Suite", "Metasploit", "Nmap", "hashcat", "John the Ripper", "Hack The Box"]),
    ("Systems and scripting", ["Windows Server", "Linux", "Python", "SQL", "REST APIs"]),
]
body = heading("02", "Stack", "What I reach for, grouped by the job it does.")
y = 158
for label, chips in groups:
    body += f'<text class="px" x="{GX}" y="{y+40}" font-size="11.5" letter-spacing="1.8" fill="{DIM}">{x(label)}</text>'
    cx = 300
    for c in chips:
        w = round(len(c) * 8.45 + 26)
        body += f'<rect x="{cx}.5" y="{y+17}.5" width="{w}" height="34" fill="none" stroke="{LINE}"/><text class="mono" x="{cx+13}" y="{y+40}" font-size="14" fill="{FG}">{x(c)}</text>'
        cx += w + 9
    assert cx < W - GX + 9, (label, cx)
    y += 68
    body += f'<rect x="{GX}" y="{y}" width="{W-2*GX}" height="1" fill="{LINE}"/>'
svg("stack.svg", y + 40, body, "Stack. " + ". ".join(f"{g}: {', '.join(c)}" for g, c in groups) + ".")

# ---------------------------------------------------------------- contact rows (each one is its own link)
body_head = heading("03", "Contact", "Open to roles. The line is up.")
svg("contact.svg", 159, body_head, "Contact. Open to roles. The line is up.")
for file, k, v, go in [("link-site.svg", "Site", "opulant.dev", "Open"), ("link-email.svg", "Email", "celty@opulant.dev", "Send"), ("link-resume.svg", "Resume", "Download PDF", "Get")]:
    svg(file, 92, f'''<text class="px lbl" x="{GX}" y="56" font-size="12" fill="{DIM}">{k}</text>
<text class="px" x="300" y="60" font-size="34" letter-spacing=".7" fill="{FG}">{x(v)}</text>
<text class="px lbl" x="{W-GX}" y="56" font-size="12" fill="{RED}" text-anchor="end">{go} ›</text>
<rect x="{GX}" y="91" width="{W-2*GX}" height="1" fill="{LINE}"/>''', f"{k}: {v}")
svg("foot.svg", 96, f'''<text class="px lbl" x="{GX}" y="56" font-size="12" fill="{DIM}">Node CS / carrier stable / no signal is ever lost, only rerouted</text>
<text class="jp" x="{W-GX}" y="57" font-size="14" letter-spacing="5" fill="{RED}" text-anchor="end">接続中</text>''', "No signal is ever lost, only rerouted.")

import re
def alt(name): return re.search(r'aria-label="([^"]*)"', (ROOT / "assets" / name).read_text()).group(1)
img = lambda f: f'<img src="assets/{f}" width="100%" alt="{alt(f)}">'
link = lambda href, f: f'<a href="{href}">{img(f)}</a>'
(ROOT / "README.md").write_text("\n".join([
    '<div align="center">', "",
    link("https://opulant.dev", "hero.svg"), img("ident.svg"), img("stack.svg"), img("contact.svg"),
    link("https://opulant.dev", "link-site.svg"), link("mailto:celty@opulant.dev", "link-email.svg"),
    link("https://opulant.dev/Celty_Sturluson_Resume.pdf", "link-resume.svg"), img("foot.svg"),
    "", "</div>", ""]))
print({p.name: p.stat().st_size for p in sorted((ROOT / "assets").glob("*.svg"))})
