"""Builds the animated SVGs used in the profile README.

    python tools/make_svgs.py

Colours match jackwent.co.uk (amber phosphor terminal). Everything is plain
SVG + CSS/SMIL so GitHub renders it inside an <img> with no scripts.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

INK_DEEP = "#0c0a07"
INK = "#15110c"
PANEL = "#1e1913"
LINE = "#3a3127"
TEXT = "#eadfcb"
DIM = "#a0907a"
AMBER = "#ffb000"
AMBER_DIM = "#7a5a1a"
OK = "#9ccb7f"
CRIT = "#ff7a5c"
INFO = "#7fb8d4"
MONO = "'IBM Plex Mono','JetBrains Mono','Cascadia Mono',Consolas,'DejaVu Sans Mono',monospace"


def window(w, h, title):
    """Terminal window chrome shared by both SVGs."""
    return f"""
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="{INK_DEEP}" stroke="{LINE}"/>
  <path d="M0.5 34 V10.5 a10 10 0 0 1 10 -10 H{w - 10.5} a10 10 0 0 1 10 10 V34 Z" fill="{PANEL}"/>
  <line x1="0.5" y1="34" x2="{w - 0.5}" y2="34" stroke="{LINE}"/>
  <circle cx="20" cy="17" r="5.5" fill="{CRIT}"/>
  <circle cx="38" cy="17" r="5.5" fill="{AMBER}"/>
  <circle cx="56" cy="17" r="5.5" fill="{OK}"/>
  <text x="{w / 2}" y="21.5" text-anchor="middle" class="t" fill="{DIM}" font-size="12">{escape(title)}</text>"""


def scanlines(w, h):
    return f"""
  <defs>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#000" opacity="0.35"/>
    </pattern>
    <radialGradient id="vig" cx="50%" cy="50%" r="75%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.45"/>
    </radialGradient>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="2.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>""", f"""
  <rect x="1" y="35" width="{w - 2}" height="{h - 36}" fill="url(#scan)" pointer-events="none"/>
  <rect x="1" y="35" width="{w - 2}" height="{h - 36}" rx="9" fill="url(#vig)" pointer-events="none"/>"""


# --------------------------------------------------------------------------
# 1. Terminal header
# --------------------------------------------------------------------------

JACK = [
    "     ██╗  █████╗   ██████╗ ██╗  ██╗",
    "     ██║ ██╔══██╗ ██╔════╝ ██║ ██╔╝",
    "     ██║ ███████║ ██║      █████╔╝ ",
    "██   ██║ ██╔══██║ ██║      ██╔═██╗ ",
    "╚█████╔╝ ██║  ██║ ╚██████╗ ██║  ██╗",
    " ╚════╝  ╚═╝  ╚═╝  ╚═════╝ ╚═╝  ╚═╝",
]
WENT = [
    "██╗    ██╗ ███████╗ ███╗   ██╗ ████████╗",
    "██║    ██║ ██╔════╝ ████╗  ██║ ╚══██╔══╝",
    "██║ █╗ ██║ █████╗   ██╔██╗ ██║    ██║   ",
    "██║███╗██║ ██╔══╝   ██║╚██╗██║    ██║   ",
    "╚███╔███╔╝ ███████╗ ██║ ╚████║    ██║   ",
    " ╚══╝╚══╝  ╚══════╝ ╚═╝  ╚═══╝    ╚═╝   ",
]

FACTS = [
    ("Role", "Head of Technical Delivery, MSP"),
    ("Uptime", "20+ years in IT"),
    ("OS", "Ubuntu 26.04 LTS"),
    ("Host", "Home Assistant Yellow"),
    ("Devices", "~200, 40+ automations"),
    ("Zigbee", "Connect ZBT-2, 25 devices"),
    ("Shells", "bash, PowerShell, Python"),
    ("Certs", "VCP, Meraki CMNA, +31 more"),
]


def typed(text, x, y, start, step=0.07, cls="tx"):
    """A command that types itself out one character at a time."""
    spans = "".join(
        f'<tspan class="ch" style="animation-delay:{start + i * step:.2f}s">{escape(c)}</tspan>'
        for i, c in enumerate(text)
    )
    return f'<text x="{x}" y="{y}" class="t {cls}" xml:space="preserve">{spans}</text>'


def prompt(x, y, delay):
    return (
        f'<text x="{x}" y="{y}" class="t in" style="animation-delay:{delay:.2f}s" xml:space="preserve">'
        f'<tspan fill="{OK}">jack@jackwent</tspan><tspan fill="{DIM}">:</tspan>'
        f'<tspan fill="{INFO}">~</tspan><tspan fill="{DIM}">$ </tspan></text>'
    )


def header():
    w, h = 900, 400
    defs, overlay = scanlines(w, h)
    p_w = 17 * 7.8  # prompt width at 13px
    parts = []

    parts.append(prompt(28, 64, 0.2))
    parts.append(typed("whoami", 28 + p_w, 64, 0.6))

    art = [j + "  " + k for j, k in zip(JACK, WENT)]
    for i, line in enumerate(art):
        parts.append(
            f'<text x="28" y="{94 + i * 14}" class="t art in" fill="{AMBER}" textLength="604" lengthAdjust="spacingAndGlyphs" '
            f'style="animation-delay:{1.3 + i * 0.12:.2f}s" xml:space="preserve">{escape(line)}</text>'
        )

    parts.append(
        f'<text x="28" y="196" class="t in" fill="{DIM}" style="animation-delay:2.3s">'
        "Smart home and homelab projects, from someone who runs it all at home.</text>"
    )

    parts.append(prompt(28, 230, 2.7))
    parts.append(typed("neofetch --short", 28 + p_w, 230, 3.0))

    for i, (k, v) in enumerate(FACTS):
        col, row = divmod(i, 4)
        x = 28 + col * 430
        y = 258 + row * 22
        parts.append(
            f'<text x="{x}" y="{y}" class="t in" style="animation-delay:{4.3 + i * 0.1:.2f}s" xml:space="preserve">'
            f'<tspan fill="{AMBER}" font-weight="600">{k:<9}</tspan><tspan fill="{TEXT}">{escape(v)}</tspan></text>'
        )

    swatches = [INK, LINE, AMBER_DIM, AMBER, OK, INFO, CRIT, TEXT]
    for i, c in enumerate(swatches):
        parts.append(
            f'<rect x="{28 + i * 26}" y="340" width="22" height="10" fill="{c}" class="in" '
            f'style="animation-delay:{5.2 + i * 0.05:.2f}s"/>'
        )

    parts.append(prompt(28, 380, 5.7))
    parts.append(
        f'<rect x="{28 + p_w + 2}" y="369" width="8" height="14" fill="{AMBER}" class="cur"/>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" fill="{TEXT}" role="img" aria-label="Terminal: whoami prints JACK WENT, then a neofetch of Jack's homelab">
  <style>
    .t {{ font-family: {MONO}; font-size: 13px; }}
    .art {{ font-size: 12px; filter: url(#glow); }}
    .in, .ch {{ opacity: 0; animation: show 0.01s linear forwards; }}
    .art.in {{ animation: wipe 0.35s ease-out forwards; }}
    .cur {{ opacity: 0; animation: blink 1s steps(1) 5.8s infinite; }}
    @keyframes show {{ to {{ opacity: 1; }} }}
    @keyframes wipe {{ 0% {{ opacity: 0; }} 40% {{ opacity: 1; fill: #fff3d0; }} 100% {{ opacity: 1; }} }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .in, .ch, .art.in {{ animation: none; opacity: 1; }}
      .cur {{ animation: none; opacity: 1; }}
    }}
  </style>{defs}{window(w, h, "jack@jackwent: ~")}
  {chr(10).join("  " + p for p in parts)}{overlay}
</svg>
"""


# --------------------------------------------------------------------------
# 2. Block the Attacks, playing itself
# --------------------------------------------------------------------------

D = 12.0  # loop length in seconds
SLOT = D / 6
FALL = 70  # px per second
HIT = 1.45  # seconds after spawn that the firewall shoots
TOP = 58
GUN_Y = 262

# Documentation-range IPs only (RFC 5737), so nobody real gets named.
ATTACKS = [
    (95, "SSH :22", "203.0.113.41", "ssh brute force"),
    (470, "RDP :3389", "198.51.100.7", "rdp scan"),
    (250, "HTTP :80", "192.0.2.180", "/wp-login.php"),
    (560, "SMB :445", "203.0.113.9", "smb probe"),
    (160, "TELNET :23", "198.51.100.66", "mirai botnet"),
    (385, "MSSQL :1433", "192.0.2.23", "sql login spray"),
]


def kt(*pairs):
    """keyTimes/values for a SMIL animation from (time, value) pairs."""
    clean = []
    for t, v in pairs:
        t = max(0.0, min(1.0, t / D))
        if clean and abs(clean[-1][0] - t) < 1e-6:
            clean[-1] = (t, v)
        else:
            clean.append((t, v))
    return ";".join(f"{t:.4f}" for t, _ in clean), ";".join(str(v) for _, v in clean)


def anim(attr, pairs, mode="linear", transform=None):
    keys, vals = kt(*pairs)
    if mode == "spline":
        ease = ";".join(["0.4 0 0.2 1"] * (len(keys.split(";")) - 1))
        mode = f'spline" keySplines="{ease}'
    if transform:
        return (
            f'<animateTransform attributeName="transform" type="{transform}" dur="{D}s" '
            f'repeatCount="indefinite" calcMode="{mode}" keyTimes="{keys}" values="{vals}"/>'
        )
    return (
        f'<animate attributeName="{attr}" dur="{D}s" repeatCount="indefinite" '
        f'calcMode="{mode}" keyTimes="{keys}" values="{vals}"/>'
    )


def visible(start, end):
    """Discrete opacity: hidden, shown from start to end, hidden again."""
    pairs = []
    if start > 0:
        pairs.append((0, 0))
    pairs.append((start, 1))
    if end < D:
        pairs.append((end, 0))
    return anim("opacity", pairs, mode="discrete")


def arcade():
    w, h = 900, 320
    defs, overlay = scanlines(w, h)
    field_r = 640
    parts = []

    # Background grid and ground.
    parts.append(
        f'<defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">'
        f'<path d="M32 0H0V32" fill="none" stroke="{LINE}" stroke-width="0.6" opacity="0.5"/></pattern></defs>'
        f'<rect x="12" y="44" width="{field_r - 12}" height="{h - 56}" fill="url(#grid)"/>'
        f'<line x1="12" y1="290" x2="{field_r}" y2="290" stroke="{AMBER_DIM}" stroke-dasharray="6 4"/>'
        f'<text x="{field_r - 6}" y="304" text-anchor="end" class="t" font-size="10" fill="{AMBER_DIM}">jackwent.co.uk perimeter</text>'
        f'<line x1="{field_r + 10}" y1="44" x2="{field_r + 10}" y2="{h - 12}" stroke="{LINE}"/>'
    )

    for i, (x, label, ip, why) in enumerate(ATTACKS):
        t0 = i * SLOT
        th = t0 + HIT
        y_hit = TOP + FALL * HIT
        bw = 8 * len(label) + 20

        # The incoming packet: falls, then vanishes when it is hit.
        parts.append(
            f'<g opacity="0">{visible(t0, th)}'
            f'<g>{anim(None, [(0, f"{x} {TOP}"), (t0, f"{x} {TOP}"), (th, f"{x} {y_hit:.0f}"), (D, f"{x} {y_hit:.0f}")], transform="translate")}'
            f'<text x="0" y="-8" text-anchor="middle" class="t" font-size="10" fill="{DIM}">{ip}</text>'
            f'<rect x="{-bw / 2}" y="0" width="{bw}" height="24" rx="3" fill="{CRIT}" fill-opacity="0.12" stroke="{CRIT}"/>'
            f'<text x="0" y="16" text-anchor="middle" class="t" font-size="12" fill="{CRIT}" font-weight="600">{label}</text>'
            f"</g></g>"
        )

        # The shot: a beam from the firewall up to the packet.
        parts.append(
            f'<g opacity="0" filter="url(#glow)">{visible(th - 0.12, th + 0.1)}'
            f'<line x1="{x}" y1="{GUN_Y}" x2="{x}" y2="{y_hit + 24:.0f}" stroke="{AMBER}" stroke-width="3"/>'
            f'<line x1="{x}" y1="{GUN_Y}" x2="{x}" y2="{y_hit + 24:.0f}" stroke="#fff3d0" stroke-width="1"/></g>'
        )

        # The explosion: a ring, some debris and a "+1 DROP".
        cy = y_hit + 12
        boom = [f'<circle cx="{x}" cy="{cy:.0f}" r="4" fill="none" stroke="{AMBER}" stroke-width="2">'
                f'{anim("r", [(0, 4), (th, 4), (th + 0.45, 34), (D, 34)])}'
                f'{anim("stroke-opacity", [(0, 1), (th, 1), (th + 0.45, 0), (D, 0)])}</circle>']
        for dx, dy in [(-30, -18), (28, -22), (-22, 16), (34, 12), (0, -32), (6, 26)]:
            boom.append(
                f'<rect x="{x - 2}" y="{cy - 2:.0f}" width="4" height="4" fill="{CRIT}">'
                f'{anim(None, [(0, "0 0"), (th, "0 0"), (th + 0.5, f"{dx} {dy}"), (D, f"{dx} {dy}")], transform="translate")}</rect>'
            )
        boom.append(
            f'<text x="{x}" y="{cy:.0f}" text-anchor="middle" class="t" font-size="12" fill="{OK}" font-weight="600">+1 DROP'
            f'{anim("y", [(0, round(cy)), (th, round(cy)), (th + 0.8, round(cy) - 26), (D, round(cy) - 26)])}</text>'
        )
        parts.append(f'<g opacity="0">{visible(th, th + 0.8)}{"".join(boom)}</g>')

    # The firewall turret slides under each packet before it fires.
    moves = [(0, f"{ATTACKS[-1][0]} 0")]
    for i, (x, *_rest) in enumerate(ATTACKS):
        t0 = i * SLOT
        prev = ATTACKS[i - 1][0]
        moves += [(t0 + 0.45, f"{prev} 0"), (t0 + 1.15, f"{x} 0")]
    moves.append((D, f"{ATTACKS[-1][0]} 0"))
    parts.append(
        f"<g>{anim(None, moves, transform='translate', mode='spline')}"
        f'<rect x="-3" y="{GUN_Y}" width="6" height="12" fill="{AMBER}"/>'
        f'<rect x="-24" y="272" width="48" height="16" rx="3" fill="{AMBER_DIM}" stroke="{AMBER}"/>'
        f'<text x="0" y="284" text-anchor="middle" class="t" font-size="10" font-weight="700" fill="{AMBER}">FW</text></g>'
    )

    # Right-hand HUD: score, lives, and a drop log that fills as it plays.
    hx = field_r + 26
    parts.append(
        f'<text x="{hx}" y="66" class="t" font-size="11" fill="{DIM}">BLOCKED / 24H</text>'
        f'<text x="{hx}" y="138" class="t" font-size="11" fill="{DIM}">LIVES</text>'
        f'<text x="{hx + 52}" y="138" class="t" font-size="13" fill="{CRIT}">♥ ♥ ♥</text>'
        f'<text x="{hx}" y="168" class="t" font-size="11" fill="{DIM}">$ tail -f drops.log</text>'
    )
    base = 21843
    for n in range(len(ATTACKS) + 1):
        start = 0 if n == 0 else (n - 1) * SLOT + HIT
        end = D if n == len(ATTACKS) else n * SLOT + HIT
        parts.append(
            f'<text x="{hx}" y="104" class="t" font-size="30" font-weight="700" fill="{AMBER}" filter="url(#glow)" '
            f'opacity="{1 if n == 0 else 0}">{visible(start, end)}{base + n:,}</text>'
        )
    for i, (_x, label, ip, why) in enumerate(ATTACKS):
        th = i * SLOT + HIT
        parts.append(
            f'<text x="{hx}" y="{190 + i * 18}" class="t" font-size="10.5" opacity="0" xml:space="preserve">{visible(th, D - 0.05)}'
            f'<tspan fill="{OK}">DROP</tspan><tspan fill="{TEXT}"> {ip:<14}</tspan><tspan fill="{DIM}">{escape(why)}</tspan></text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" fill="{TEXT}" role="img" aria-label="Block the Attacks playing itself: a firewall shoots down incoming SSH, RDP, HTTP, SMB, Telnet and MSSQL attacks">
  <style>
    .t {{ font-family: {MONO}; }}
  </style>{defs}{window(w, h, "~/games/block-the-attacks  [autoplay]")}
  {chr(10).join("  " + p for p in parts)}{overlay}
</svg>
"""


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "terminal.svg").write_text(header(), encoding="utf-8")
    (OUT / "block-the-attacks.svg").write_text(arcade(), encoding="utf-8")
    print("wrote", *(p.name for p in OUT.glob("*.svg")))
