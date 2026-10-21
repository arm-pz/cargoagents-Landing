import math, re, sys

P = "/tmp/claude-0/-home-claude/78095222-ebea-5708-9122-e405feeca108/scratchpad/"
proj = P + "cargo-footer/project/"
tpl = open(P + "site-test/page.src.html", encoding="utf-8").read()


def ns(svg, prefix):
    """prefix every id inside an extracted svg, and every reference to it"""
    ids = re.findall(r'\bid="([^"]+)"', svg)
    for i in sorted(set(ids), key=len, reverse=True):
        svg = svg.replace('id="%s"' % i, 'id="%s%s"' % (prefix, i))
        svg = svg.replace('href="#%s"' % i, 'href="#%s%s"' % (prefix, i))
        svg = svg.replace('url(#%s)' % i, 'url(#%s%s)' % (prefix, i))
    return svg


# ---------- hero svg (from the celestial artboard), split into parallax layers ----------
hl = open(proj + "HeroCelestial.dc.html", encoding="utf-8").read().split("\n")
hero = "\n".join(hl[88:283])  # lines 89..283
assert hero.lstrip().startswith("<svg") and hero.rstrip().endswith("</svg>")
hero = re.sub(r'^<svg[^>]*>', '<svg id="heroSvg" viewBox="0 0 1440 1100" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">', hero, count=1)
hero = ns(hero, "h-")

rays = (
    '<defs><radialGradient id="rayfade" cx="720" cy="640" r="900" gradientUnits="userSpaceOnUse">'
    '<stop offset="0.52" stop-color="#fff" stop-opacity="0"/><stop offset="0.62" stop-color="#fff" stop-opacity="1"/>'
    '<stop offset="0.85" stop-color="#fff" stop-opacity="0.55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
    '<mask id="raymask" maskUnits="userSpaceOnUse" x="-300" y="-400" width="2040" height="1900"><rect x="-300" y="-400" width="2040" height="1900" fill="url(#rayfade)"/></mask></defs>'
    '<g id="pxRays"><g class="pt" data-d="0.25"><g mask="url(#raymask)"><circle cx="720" cy="640" r="450" fill="none" stroke="#CFE3EE" stroke-opacity="0.075" stroke-width="900" stroke-dasharray="2.8 20.76"/></g></g></g>\n'
)
# four depth layers, each an outer scroll group (#px*) holding an inner pointer group (.pt)
a_far = '<g class="stars-a" fill="#DCEAF2">'
assert hero.count(a_far) == 1
hero = hero.replace(a_far, rays + '<g id="pxFar"><g class="pt" data-d="0.4">\n' + a_far, 1)
a_mid = '<circle cx="720" cy="640" r="522"'
assert hero.count(a_mid) == 1
hero = hero.replace(a_mid, '</g></g>\n<g id="pxMid"><g class="pt" data-d="0.9">\n' + a_mid, 1)
a_near = '<path d="M-20 850V834C60 826 120 832'
assert hero.count(a_near) == 2  # base + hatch overlay
i = hero.index(a_near)
ext = '<rect x="-200" y="1090" width="1840" height="1700" fill="#07131F"/>\n'  # deep water under the quay so the near layer can rise
hero = hero[:i] + '</g></g>\n<g id="pxNear"><g class="pt" data-d="1.7">\n' + ext + hero[i:]
assert hero.rstrip().endswith("</svg>")
hero = hero.rstrip()[:-len("</svg>")] + '</g></g>\n</svg>'
# widen the quay, hills and sea so the near layer can shift sideways without showing an edge
assert hero.count('M-20 850V834C60 826 120 832') == 2
hero = hero.replace('M-20 850V834C60 826 120 832', 'M-90 850V834H-20C60 826 120 832')
assert hero.count('C1290 832 1360 826 1460 832V850Z') == 2
hero = hero.replace('C1290 832 1360 826 1460 832V850Z', 'C1290 832 1360 826 1460 832H1530V850Z')
for old, new_ in (('<rect x="-20" y="850" width="1480" height="260" fill="url(#h-sea)"/>', '<rect x="-90" y="850" width="1620" height="260" fill="url(#h-sea)"/>'),
                  ('<rect x="-20" y="838" width="1480" height="40" fill="url(#h-mist)"/>', '<rect x="-90" y="838" width="1620" height="40" fill="url(#h-mist)"/>'),
                  ('<path d="M-20 850H1460"', '<path d="M-90 850H1530"')):
    assert hero.count(old) == 1, old
    hero = hero.replace(old, new_)

# ---------- footer scene (from the footer artboard) ----------
ml = open(proj + "Main.dc.html", encoding="utf-8").read().split("\n")
foot = "\n".join(ml[146:289])  # lines 147..289
assert foot.lstrip().startswith("<svg") and foot.rstrip().endswith("</svg>")
foot = re.sub(r'^<svg[^>]*>', '<svg viewBox="0 0 1440 460" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">', foot, count=1)
foot = ns(foot, "f-")
foot = foot.replace('class="ship"', 'class="fship"')

# ---------- globe graticule ----------
R, CX, CY, TILT = 230, 260, 260, math.radians(22)
g = []
for lon in (20, 40, 60, 80):
    rx = R * math.sin(math.radians(lon))
    g.append('<ellipse cx="%d" cy="%d" rx="%.1f" ry="%d"/>' % (CX, CY, rx, R))
g.append('<path d="M%d %dV%d"/>' % (CX, CY - R, CY + R))
for lat in (-60, -30, 0, 30, 60):
    la = math.radians(lat)
    rx = R * math.cos(la)
    ry = rx * math.sin(TILT)
    cy = CY - R * math.sin(la) * math.cos(TILT)
    g.append('<ellipse cx="%d" cy="%.1f" rx="%.1f" ry="%.1f"/>' % (CX, cy, rx, ry))
graticule = "\n".join("            " + x for x in g)


# ---------- mode art ----------
INK = "#CFE3EE"
def cont(x, y, kind="k", w=40, h=10, ribs=True):
    fills = {"k": "#10304A", "o": "#C8602A", "t": "#1D6574", "g": "#58798F"}
    stroke = "#F4B08A" if kind == "o" else INK
    s = '<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="%s" stroke="%s" stroke-opacity="%s"/>' % (x + .5, y + .5, w - 1, h - 1, fills[kind], stroke, "0.9" if kind == "o" else "0.7")
    if ribs:
        for rx in range(5, w - 1, 5):
            s += '<path d="M%.1f %.1fV%.1f" stroke="%s" stroke-opacity="0.2"/>' % (x + rx, y + 1.5, y + h - 1.5, "#000" if kind in ("o", "g") else INK)
    return s


def plate(inner, extra=""):
    stars = "".join('<circle cx="%d" cy="%d" r="%.1f"/>' % t for t in [(40, 36, 1.1), (92, 70, 1), (150, 28, 1.2), (214, 52, 1), (300, 30, 1.1), (366, 62, 1), (430, 34, 1.2), (452, 90, 1), (24, 110, 1), (260, 86, 1)])
    return ('<svg viewBox="0 0 480 300" preserveAspectRatio="xMidYMid slice" focusable="false">'
            '<g fill="#DCEAF2" fill-opacity="0.7">%s</g><circle cx="404" cy="66" r="20" fill="#DDEAF2" fill-opacity="0.92"/><circle cx="404" cy="66" r="30" fill="none" stroke="#CFE3EE" stroke-opacity="0.25"/>%s%s</svg>' % (stars, inner, extra))


def waves(y, n=4):
    out = ""
    for i in range(n):
        out += '<path d="M0 %d H480" stroke="%s" stroke-opacity="%.2f" stroke-dasharray="%s" fill="none"/>' % (y + i * 12, INK, 0.2 - i * 0.04, ["60 14 26 20", "30 20 90 14", "80 16 30 24", "40 26 60 18"][i])
    return out


# full container: a quay crane lifting a 40 ft box onto a vessel
fc = '<defs><radialGradient id="fcl-glow"><stop offset="0" stop-color="#F0803C" stop-opacity="0.38"/><stop offset="1" stop-color="#F0803C" stop-opacity="0"/></radialGradient>'
fc += '<linearGradient id="fcl-fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
fc += '<mask id="fcl-rm" maskUnits="userSpaceOnUse" x="0" y="226" width="480" height="74"><rect x="0" y="226" width="480" height="74" fill="url(#fcl-fade)"/></mask></defs>'
fc += '<path d="M0 226H480V300H0Z" fill="#0A2033"/>'
WL = 226
# the vessel: stern and bridge on the left, bow on the right
hull = '<path d="M128 184H412C430 184 444 176 454 162L440 %d H142Z" fill="#0B2236" stroke="%s" stroke-opacity="0.85" stroke-linejoin="round"/>' % (WL, INK)
hull += '<path d="M142 %d H440 L434 238 H148Z" fill="#B5502A" fill-opacity="0.9"/>' % WL
hull += '<path d="M146 192H430" stroke="%s" stroke-opacity="0.18"/><path d="M150 204H424" stroke="%s" stroke-opacity="0.12"/>' % (INK, INK)
stacks = ""
heights = [3, 4, 3, 3, 4, 2]
kinds = [["g", "k", "t"], ["k", "o", "g", "k"], ["t", "k", "g"], ["o", "k", "k"], ["k", "t", "o", "g"], ["g", "k"]]
for ci in range(6):
    for r in range(heights[ci]):
        stacks += cont(196 + ci * 36, 184 - 14 * (r + 1), kinds[ci][r], 36, 14)
bridge = '<rect x="134" y="150" width="46" height="34" fill="#0E2A40" stroke="%s" stroke-opacity="0.8"/><rect x="143" y="132" width="30" height="18" fill="#0E2A40" stroke="%s" stroke-opacity="0.8"/><rect x="150" y="112" width="14" height="20" fill="#0E2A40" stroke="%s" stroke-opacity="0.8"/><rect x="150" y="118" width="14" height="6" fill="#E8793A"/>' % (INK, INK, INK)
bridge += '<path d="M140 141H166M138 160H176M138 172H176" stroke="#F5B56B" stroke-opacity="0.8" stroke-width="2" stroke-dasharray="3 5"/>'
bridge += '<path d="M157 112V98" stroke="%s" stroke-opacity="0.7"/><circle cx="157" cy="97" r="1.8" fill="#FF5A4A"/>' % INK
vessel = hull + stacks + bridge
# mirror image in the water, fading with depth
fc += '<g mask="url(#fcl-rm)" opacity="0.28"><g transform="translate(0 %d) scale(1 -1)">%s</g></g>' % (2 * WL, vessel)
fc += waves(238, 4)
fc += vessel
# mooring lines to the quay
fc += '<path d="M138 172C128 190 122 208 118 %d M136 180C130 196 126 210 122 %d" fill="none" stroke="%s" stroke-opacity="0.5"/>' % (WL, WL, INK)
# quay with stacked boxes and the crane
fc += '<path d="M0 %d H118 V300 H0Z" fill="#0C2539" stroke="%s" stroke-opacity="0.5"/>' % (WL, INK)
fc += '<path d="M118 %d V300 M112 %d V300" stroke="%s" stroke-opacity="0.25"/>' % (WL, WL, INK)
for qi, (qx, qk, qh) in enumerate([(4, "g", 2), (4 + 0, "k", 1)]):
    pass
fc += cont(6, WL - 14, "o", 36, 14) + cont(6, WL - 28, "k", 36, 14) + cont(46, WL - 14, "t", 36, 14) + cont(46, WL - 28, "g", 36, 14) + cont(86, WL - 14, "k", 30, 14)
crane = '<g fill="none" stroke="%s" stroke-linejoin="round" stroke-width="1.2">' % INK
crane += '<path d="M44 76L34 %d M104 76L114 %d" stroke-opacity="0.85"/>' % (WL, WL)
crane += '<path d="M40 120L108 120M37 170L111 170" stroke-opacity="0.45"/><path d="M44 76L106 120M104 76L42 120M42 120L109 170M108 120L39 170" stroke-opacity="0.28"/>'
crane += '<path d="M36 196H112" stroke-opacity="0.8"/>'
# lattice boom: backreach to boom tip, two chords with a zig-zag between
crane += '<path d="M30 68H352M30 76H352" stroke-opacity="0.85"/>'
zz = "M30 76"
x = 30
up = False
while x < 352:
    x += 10
    zz += "L%d %d" % (min(x, 352), 68 if not up else 76)
    up = not up
crane += '<path d="%s" stroke-opacity="0.4"/>' % zz
crane += '<path d="M74 34L352 68M74 34L30 68" stroke-opacity="0.7"/><path d="M74 34V68" stroke-opacity="0.7"/>'
crane += '<circle cx="74" cy="33" r="1.8" fill="#FF5A4A" stroke="none"/>'
crane += '</g>'
crane += '<rect x="56" y="50" width="36" height="18" fill="#0E2A40" stroke="%s" stroke-opacity="0.85"/><rect x="62" y="55" width="10" height="7" fill="#F5B56B" fill-opacity="0.85"/>' % INK
# trolley, hoist cables and spreader over the lifted box
crane += '<rect x="312" y="76" width="22" height="9" fill="#0E2A40" stroke="%s" stroke-opacity="0.9"/>' % INK
crane += '<path d="M316 85L308 91M330 85L336 91" stroke="%s" stroke-opacity="0.8"/>' % INK
crane += '<rect x="304" y="91" width="36" height="4" fill="#0E2A40" stroke="%s" stroke-opacity="0.9"/>' % INK
fc += crane
# the lifted box, with a glow and a callout
fc += '<circle cx="322" cy="102" r="46" fill="url(#fcl-glow)"/>'
fc += cont(304, 95, "o", 36, 14)
for cxp, cyp in ((305, 96), (339, 96), (305, 108), (339, 108)):
    fc += '<rect x="%.1f" y="%.1f" width="2.4" height="2.4" fill="#06131F" fill-opacity="0.8"/>' % (cxp - 1.4, cyp - 1.4)
fc += '<path d="M302 102H278" stroke="#F4B08A" stroke-opacity="0.8"/><circle cx="302" cy="102" r="1.8" fill="#F4B08A"/>'
fc += '<text x="274" y="105" text-anchor="end" font-family="IBM Plex Mono, monospace" font-size="9" letter-spacing="1.6" fill="#F4B08A" fill-opacity="0.95">40′ HC</text>'
# where the box lands: dashed drop line and an empty slot above the third stack
fc += '<path d="M322 111V%d" stroke="#F4B08A" stroke-opacity="0.45" stroke-dasharray="3 4"/>' % (184 - 14 * 3 - 14)
fc += '<rect x="304.5" y="%d" width="35" height="13" fill="none" stroke="#F4B08A" stroke-opacity="0.6" stroke-dasharray="3 3"/>' % (184 - 14 * 3 - 14)
art_fcl = plate(fc)

# part load: open container with pallets from several shippers
BOX = {"o": ("#C8602A", "#F4B08A"), "t": ("#1D6574", INK), "g": ("#58798F", INK), "k": ("#10304A", INK)}
def crate(x, y, w, h, kind):
    f, st = BOX[kind]
    out = '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-opacity="0.8"/>' % (x, y, w, h, f, st)
    out += '<path d="M%d %dL%d %dM%d %dL%d %d" stroke="%s" stroke-opacity="0.22"/>' % (x, y, x + w, y + h, x + w, y, x, y + h, "#000" if kind in ("o", "g") else INK)
    out += '<path d="M%d %dH%d" stroke="%s" stroke-opacity="0.3"/>' % (x, y + h * 0.5, x + w, "#000" if kind in ("o", "g") else INK)
    return out
def pallet(x, y, w):
    return '<rect x="%d" y="%d" width="%d" height="5" fill="#0A1D2E" stroke="%s" stroke-opacity="0.55"/><path d="M%d %dV%d M%d %dV%d" stroke="%s" stroke-opacity="0.4"/>' % (x, y, w, INK, x + 6, y, y + 5, x + w - 6, y, y + 5, INK)

lcl = '<path d="M0 232H480V300H0Z" fill="#0A2033"/><path d="M0 232H480" stroke="%s" stroke-opacity="0.4"/>' % INK
lcl += '<path d="M0 248H480M0 266H480" stroke="%s" stroke-opacity="0.12" stroke-dasharray="40 20" fill="none"/>' % INK
# container shell (side cutaway)
lcl += '<rect x="56" y="96" width="368" height="130" fill="#0E2A40" stroke="%s" stroke-opacity="0.85"/>' % INK
lcl += '<rect x="68" y="108" width="344" height="106" fill="#06131F" stroke="%s" stroke-opacity="0.5"/>' % INK
for rx in range(76, 412, 12):
    lcl += '<path d="M%d 99V105M%d 217V223" stroke="%s" stroke-opacity="0.22"/>' % (rx, rx, INK)
lcl += '<path d="M56 226H424V232H56Z" fill="#0A1D2E" stroke="%s" stroke-opacity="0.6"/>' % INK
# pallets, three shippers: orange, teal, grey
x = 74
lcl += pallet(x, 209, 62) + crate(x + 2, 168, 58, 41, "o") + crate(x + 2, 128, 58, 40, "o"); x += 66
lcl += pallet(x, 209, 54) + crate(x + 2, 160, 50, 49, "t") + crate(x + 2, 126, 50, 34, "t"); x += 58
lcl += pallet(x, 209, 62) + crate(x + 2, 176, 58, 33, "t") + crate(x + 2, 140, 58, 36, "g"); x += 66
lcl += pallet(x, 209, 54) + crate(x + 2, 164, 50, 45, "g") + crate(x + 2, 126, 50, 38, "g"); x += 58
lcl += pallet(x, 209, 62) + crate(x + 2, 172, 58, 37, "k") + crate(x + 2, 132, 58, 40, "o")
# door end posts and lamp
lcl += '<path d="M56 96V226M424 96V226" stroke="%s" stroke-opacity="0.9" stroke-width="2"/>' % INK
lcl += '<path d="M76 118H400" stroke="#F5B56B" stroke-opacity="0.5" stroke-width="2" stroke-dasharray="2 10" stroke-linecap="round"/>'
lcl += '<text x="240" y="84" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="10" letter-spacing="3" fill="#CFE3EE" fill-opacity="0.55">THREE SHIPPERS · ONE BOX</text>'
art_lcl = plate(lcl)

# refrigerated: reefer unit, set point, shore power
rf = '<path d="M0 232H480V300H0Z" fill="#0A2033"/><path d="M0 232H480" stroke="%s" stroke-opacity="0.4"/>' % INK
rf += '<path d="M0 250H480M0 268H480" stroke="%s" stroke-opacity="0.12" stroke-dasharray="40 20" fill="none"/>' % INK
rf += '<rect x="96" y="112" width="330" height="112" fill="#10304A" stroke="%s" stroke-opacity="0.85"/>' % INK
for rx in range(116, 426, 10):
    rf += '<path d="M%d 116V220" stroke="%s" stroke-opacity="0.16"/>' % (rx, INK)
rf += '<path d="M96 168H426" stroke="#C8602A" stroke-width="5"/>'
rf += '<rect x="96" y="224" width="330" height="8" fill="#0A1D2E" stroke="%s" stroke-opacity="0.6"/>' % INK
# reefer unit on the front end
rf += '<rect x="56" y="112" width="40" height="112" fill="#0E2A40" stroke="%s" stroke-opacity="0.9"/>' % INK
rf += '<circle cx="76" cy="148" r="14" fill="#06131F" stroke="%s" stroke-opacity="0.85"/><circle cx="76" cy="148" r="3" fill="%s" fill-opacity="0.8"/>' % (INK, INK)
rf += '<path d="M76 148L76 135M76 148L88 155M76 148L64 155" stroke="%s" stroke-opacity="0.7" stroke-width="2.4" stroke-linecap="round"/>' % INK
rf += '<path d="M62 180H90M62 188H90M62 196H90M62 204H90" stroke="%s" stroke-opacity="0.35"/>' % INK
rf += '<rect x="62" y="118" width="28" height="12" fill="#06131F" stroke="%s" stroke-opacity="0.6"/><text x="76" y="127.5" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="8" fill="#6FD0B4">-18C</text>' % INK
rf += '<circle cx="84" cy="214" r="2.4" fill="#6FD0B4"/>'
# cold air arrows above the box and snowflake
rf += '<path d="M104 100C170 82 250 82 330 100" fill="none" stroke="#6FD0B4" stroke-opacity="0.6" stroke-dasharray="5 7"/><path d="M322 94L332 100L322 106" fill="none" stroke="#6FD0B4" stroke-opacity="0.7" stroke-linecap="round" stroke-linejoin="round"/>'
fl = '<g transform="translate(246 48)" stroke="#CFE3EE" stroke-opacity="0.8" stroke-width="1.4" stroke-linecap="round" fill="none">'
for ang in (0, 60, 120):
    fl += '<path d="M0 -16L0 16" transform="rotate(%d)"/>' % ang
for ang in (0, 60, 120, 180, 240, 300):
    fl += '<path d="M-4 -12L0 -8L4 -12" transform="rotate(%d)"/>' % ang
fl += '</g>'
rf += fl
# shore power: cable down to a socket post
rf += '<path d="M56 206C40 206 34 222 34 240V246" fill="none" stroke="%s" stroke-opacity="0.7" stroke-width="1.6"/>' % INK
rf += '<rect x="22" y="246" width="24" height="26" fill="#0E2A40" stroke="%s" stroke-opacity="0.8"/><circle cx="34" cy="259" r="3" fill="#F5B56B"/>' % INK
rf += '<path d="M0 232H480" stroke="%s" stroke-opacity="0.0"/>' % INK
art_reefer = plate(rf)

out = tpl
out = out.replace("{{LANDMASK}}", open(P + "geo-src/landmask.b64").read().strip())
out = out.replace("{{HERO_SVG}}", hero).replace("{{FOOT_SVG}}", foot).replace("{{GRATICULE}}", graticule)
out = out.replace("{{ART_FCL}}", art_fcl).replace("{{ART_LCL}}", art_lcl).replace("{{ART_REEFER}}", art_reefer)
assert "{{" not in out, re.findall(r"\{\{[^}]+\}\}", out)
open(P + "site-test/site.html", "w", encoding="utf-8").write(out)
print("site.html", len(out), "bytes")
