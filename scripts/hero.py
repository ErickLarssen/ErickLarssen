#!/usr/bin/env python3
"""Gera assets/hero.svg — cabeçalho animado com o logo Erick Silva.

O logo vem do .ai original (camadas E, Águia e S, Olho, Coroa, Asas).
Todo texto é convertido em vetor, então o resultado é idêntico em qualquer sistema.
"""
import json, os, random, re
from textpath import text

AQUI = os.path.dirname(os.path.abspath(__file__))
_LOGO = os.path.join(AQUI, "logo.json")
if not os.path.exists(_LOGO):
    _LOGO = os.path.join(AQUI, "..", "logo", "pieces.json")
P = json.load(open(_LOGO))

W, H = 1000, 560

# ── paleta ───────────────────────────────────────────────
OBS = "#0A0A0C"
OBS2 = "#121116"
FIO = "#2A2722"
OURO_E = "#BA8529"
OURO = "#D4A24C"
OURO_C = "#E2AE61"
LUZ = "#F5D79A"
MARFIM = "#F5F1E8"
ACO = "#7FA6C9"

# ── logo: peças do .ai (artboard 1080×1350) ─────────────
def enxuga(d):
    d = re.sub(r"-?\d+\.\d+", lambda m: f"{float(m.group(0)):.1f}".rstrip("0").rstrip("."), d)
    return re.sub(r"\s+", " ", d).strip()
for p in P:
    p["d"] = enxuga(p["d"])
E, AGUIA_S, OLHO, FAIXA, COROA = (P[i]["d"] for i in (0, 1, 2, 3, 4))
ASA_DIR = [P[i]["d"] for i in (5, 6, 8, 9)]      # de cima para baixo
ASA_ESQ = [P[i]["d"] for i in (10, 11, 12, 13)]  # de cima para baixo

S = 0.30                      # escala do logo
LX = 500 - 540 * S            # centro do logo no x=500
LY = 34 - 220 * S             # topo da coroa em y=34
CROWN_TIP = (540.6, 219.8)
EYE = (533, 573)


def to_hero(x, y):
    return LX + x * S, LY + y * S


# ── texto em vetor ───────────────────────────────────────
nome_d, nome_w = text("Cinzel", 700, "ERICK SILVA", 62, 500, 386, tracking=9)
sub_items = ["FULL-STACK DEVELOPER", "UI/UX & BRAND DESIGN", "FRONT-END ENGINEERING"]
SUB_SIZE, SUB_TR = 12.5, 3.6
# mede cada item para distribuir com losangos entre eles
medidas = [text("Jost", 500, t, SUB_SIZE, 0, 0, SUB_TR)[1] for t in sub_items]
GAP = 40
total = sum(medidas) + GAP * (len(sub_items) - 1)
x = 500 - total / 2
sub_paths, losangos = [], []
for t, w in zip(sub_items, medidas):
    sub_paths.append(text("Jost", 500, t, SUB_SIZE, x, 448, SUB_TR, anchor="start")[0])
    x += w
    if len(sub_paths) < len(sub_items):
        losangos.append(x + GAP / 2)
        x += GAP

tag_d, _ = text("Jost", 400, "DESENHO A EXPERIÊNCIA E ESCREVO O CÓDIGO QUE A COLOCA DE PÉ.", 10.5, 500, 476, 3.2)

# HUD (mono, azul-aço)
hud_tl, _ = text("JetBrainsMono", 500, "ERICKSILVA.DEV", 9.5, 56, 44, 2.4, anchor="start")
hud_tr, _ = text("JetBrainsMono", 500, "DESIGN × TECHNOLOGY", 9.5, 956, 44, 2.4, anchor="end")
hud_bl, _ = text("JetBrainsMono", 400, "ES/001", 9, 44, 496, 2.2, anchor="start")
hud_br, _ = text("JetBrainsMono", 400, "FULL-STACK · 2026", 9, 956, 496, 2.2, anchor="end")

# ── faixa inferior (marquee) ─────────────────────────────
valores = ["LÓGICA ROBUSTA", "ARQUITETURA LIMPA", "EXPERIÊNCIA MEMORÁVEL",
           "BRAND DESIGN", "DESIGN × TECHNOLOGY", "CÓDIGO COM PROPÓSITO"]
BAND_Y = 512
MQ_SIZE, MQ_TR, MQ_GAP = 11, 4.2, 64
mq_paths, mq_dots, mx = [], [], 0.0
for v in valores:
    d, w = text("Jost", 600, v, MQ_SIZE, mx, BAND_Y + 28, MQ_TR, anchor="start")
    mq_paths.append(d)
    mx += w + MQ_GAP / 2
    mq_dots.append(mx)
    mx += MQ_GAP / 2
MQ_W = mx  # largura de um ciclo


def losango(cx, cy, r, fill, extra=""):
    return f'<path d="M{cx:.1f} {cy-r:.1f}L{cx+r:.1f} {cy:.1f}L{cx:.1f} {cy+r:.1f}L{cx-r:.1f} {cy:.1f}Z" fill="{fill}"{extra}/>'


def estrela(cx, cy, r):
    """estrela de 4 pontas (brilho de joia)"""
    q = r * 0.16
    return (f'M{cx} {cy-r}C{cx+q} {cy-q} {cx+q} {cy-q} {cx+r} {cy}'
            f'C{cx+q} {cy+q} {cx+q} {cy+q} {cx} {cy+r}'
            f'C{cx-q} {cy+q} {cx-q} {cy+q} {cx-r} {cy}'
            f'C{cx-q} {cy-q} {cx-q} {cy-q} {cx} {cy-r}Z')


# ── brasas ───────────────────────────────────────────────
random.seed(7)
brasas = []
for i in range(16):
    bx = random.uniform(330, 670)
    by = random.uniform(250, 330)
    r = random.choice([1.1, 1.4, 1.8, 2.2])
    dur = random.uniform(7, 13)
    delay = -random.uniform(0, dur)
    dx = random.uniform(-26, 26)
    rise = random.uniform(150, 250)
    cor = random.choice([OURO_C, LUZ, OURO, ACO]) if i % 5 else ACO
    brasas.append(
        f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{r}" fill="{cor}" class="brasa" '
        f'style="--dx:{dx:.0f}px;--rise:-{rise:.0f}px;animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s"/>')

# ── penas: ordem de abertura de dentro (baixo) para fora (cima) ──
def penas(lista, lado):
    out = []
    n = len(lista)
    for i, d in enumerate(lista):
        ordem = n - 1 - i                       # a de baixo abre primeiro
        out.append(f'<path class="pena {lado}" pathLength="1" style="animation-delay:{2.15 + ordem*0.12:.2f}s" d="{d}"/>')
    return "\n        ".join(out)


crown_x, crown_y = to_hero(*CROWN_TIP)
eye_x, eye_y = to_hero(*EYE)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Erick Silva — Full-Stack Developer, UI/UX &amp; Brand Design, Front-End Engineering. Design × Technology.">
  <defs>
    <!-- ouro metálico: o mesmo sentido do gradiente do .ai (escuro à esquerda, claro à direita) -->
    <linearGradient id="ouro" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1080" y2="0">
      <stop offset="0" stop-color="#9C6C1E"/>
      <stop offset=".30" stop-color="{OURO_E}"/>
      <stop offset=".55" stop-color="{OURO}"/>
      <stop offset=".75" stop-color="{OURO_C}"/>
      <stop offset="1" stop-color="#EBC27A"/>
    </linearGradient>
    <linearGradient id="ouroNome" gradientUnits="userSpaceOnUse" x1="{500-nome_w/2:.0f}" y1="0" x2="{500+nome_w/2:.0f}" y2="0">
      <stop offset="0" stop-color="{OURO_E}"/>
      <stop offset=".45" stop-color="{OURO_C}"/>
      <stop offset=".6" stop-color="{LUZ}"/>
      <stop offset="1" stop-color="{OURO}"/>
    </linearGradient>
    <linearGradient id="fundo" x1="0" y1="0" x2=".35" y2="1">
      <stop offset="0" stop-color="{OBS2}"/>
      <stop offset=".55" stop-color="{OBS}"/>
      <stop offset="1" stop-color="#0D0C10"/>
    </linearGradient>
    <radialGradient id="halo" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{OURO}" stop-opacity=".30"/>
      <stop offset=".45" stop-color="{OURO_E}" stop-opacity=".10"/>
      <stop offset="1" stop-color="{OURO_E}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="aco" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{ACO}" stop-opacity=".16"/>
      <stop offset="1" stop-color="{ACO}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="gradeFade" cx="50%" cy="42%" r="60%">
      <stop offset="0" stop-color="#fff" stop-opacity=".9"/>
      <stop offset=".7" stop-color="#fff" stop-opacity=".25"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="fioTopo" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="{LUZ}" stop-opacity=".55"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="borda" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{OURO_C}" stop-opacity=".45"/>
      <stop offset=".5" stop-color="{OURO}" stop-opacity=".08"/>
      <stop offset="1" stop-color="{ACO}" stop-opacity=".30"/>
    </linearGradient>
    <linearGradient id="reflexo" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#fff" stop-opacity="1"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="faixa" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{OURO}" stop-opacity=".02"/>
      <stop offset=".5" stop-color="{OURO}" stop-opacity=".07"/>
      <stop offset="1" stop-color="{ACO}" stop-opacity=".05"/>
    </linearGradient>
    <linearGradient id="regua" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{OURO}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{LUZ}"/>
      <stop offset="1" stop-color="{OURO}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="marqFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".12" stop-color="#fff"/>
      <stop offset=".88" stop-color="#fff"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>

    <pattern id="pontos" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="11" cy="11" r=".9" fill="{ACO}"/>
    </pattern>

    <clipPath id="card"><rect width="{W}" height="{H}" rx="28"/></clipPath>
    <mask id="gradeMask"><rect width="{W}" height="{H}" fill="url(#gradeFade)"/></mask>
    <mask id="marqMask"><rect x="0" y="{BAND_Y}" width="{W}" height="{H-BAND_Y}" fill="url(#marqFade)"/></mask>
    <mask id="brilhoMask" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect class="varre" x="-240" y="-40" width="200" height="{H+80}" fill="url(#reflexo)" transform="skewX(-18)"/>
    </mask>

    <filter id="neon" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
    <filter id="neonFino" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.2"/>
    </filter>

    <!-- o logo, peça por peça (coordenadas do artboard original) -->
    <g id="logo">
      <g class="asa esq">
        {penas(ASA_ESQ, "esq")}
      </g>
      <g class="asa dir">
        {penas(ASA_DIR, "dir")}
      </g>
      <path class="coroa" pathLength="1" d="{COROA}"/>
      <path class="coroa" pathLength="1" d="{FAIXA}"/>
      <path pathLength="1" d="{AGUIA_S}"/>
      <path pathLength="1" d="{OLHO}"/>
      <path pathLength="1" d="{E}"/>
    </g>
    <path id="nome" d="{nome_d}"/>

    <style>
      /* ── entrada (roda uma vez a cada carregamento) ───────────── */
      .traco {{ stroke-dasharray:1 1; animation: traca 2.1s cubic-bezier(.55,.1,.3,1) .25s both, apaga .9s ease 2.2s both }}
      @keyframes traca {{ from{{stroke-dashoffset:1}} to{{stroke-dashoffset:0}} }}
      @keyframes apaga {{ from{{opacity:1}} to{{opacity:0}} }}

      .derrete {{ animation: derrete 1.2s cubic-bezier(.3,.6,.3,1) 1.55s both }}
      @keyframes derrete {{ from{{opacity:0}} to{{opacity:1}} }}

      .pena {{ transform-box:fill-box; animation: abre .95s cubic-bezier(.2,.9,.25,1.15) both }}
      .pena.esq {{ transform-origin:100% 100% }}
      .pena.dir {{ transform-origin:0% 100% }}
      @keyframes abre {{ from{{transform:rotate(var(--r)) scale(.82)}} to{{transform:rotate(0) scale(1)}} }}
      .esq .pena, .pena.esq {{ --r:28deg }}
      .dir .pena, .pena.dir {{ --r:-28deg }}

      .sobe  {{ animation: sobe 1.1s cubic-bezier(.2,.7,.3,1) 3.25s both }}
      .sobe2 {{ animation: sobe 1.1s cubic-bezier(.2,.7,.3,1) 3.55s both }}
      .sobe3 {{ animation: sobe 1.1s cubic-bezier(.2,.7,.3,1) 3.8s both }}
      .hud   {{ animation: sobe 1.2s ease .6s both }}
      @keyframes sobe {{ from{{opacity:0;transform:translateY(14px)}} to{{opacity:1;transform:translateY(0)}} }}

      .cresce {{ transform-origin:500px 0; animation: cresce 1.2s cubic-bezier(.2,.7,.3,1) 3.5s both }}
      @keyframes cresce {{ from{{transform:scaleX(0)}} to{{transform:scaleX(1)}} }}

      .surge {{ animation: derrete 2.4s ease .1s both }}

      /* ── loop permanente ─────────────────────────────────────── */
      .varre {{ animation: varre 9s cubic-bezier(.45,0,.25,1) 4.6s infinite }}
      @keyframes varre {{ 0%{{transform:skewX(-18deg) translateX(0)}} 30%,100%{{transform:skewX(-18deg) translateX(1500px)}} }}

      .respira {{ transform-box:fill-box; transform-origin:center; animation: respira 6.5s ease-in-out 2.4s infinite both }}
      @keyframes respira {{ 0%,100%{{opacity:.75;transform:scale(.96)}} 50%{{opacity:1;transform:scale(1.05)}} }}

      .neon {{ animation: derrete 1.6s ease 1.9s both, pulsa 6.5s ease-in-out 3.5s infinite }}
      @keyframes pulsa {{ 0%,100%{{opacity:.4}} 50%{{opacity:.75}} }}

      .joia {{ transform-box:fill-box; transform-origin:center; opacity:0; animation: joia 6s ease-in-out 3.05s infinite }}
      @keyframes joia {{ 0%{{opacity:0;transform:scale(.2) rotate(0)}} 8%{{opacity:1;transform:scale(1.1) rotate(45deg)}} 20%{{opacity:0;transform:scale(.3) rotate(90deg)}} 100%{{opacity:0;transform:scale(.2) rotate(90deg)}} }}

      .olho {{ opacity:0; animation: olho 6s ease-in-out 3.35s infinite }}
      @keyframes olho {{ 0%,100%{{opacity:0}} 6%{{opacity:1}} 18%{{opacity:.15}} 60%{{opacity:.15}} }}

      .brasa {{ opacity:0; animation-name: brasa; animation-timing-function: linear; animation-iteration-count: infinite }}
      @keyframes brasa {{
        0%   {{ opacity:0; transform:translate(0,0) }}
        15%  {{ opacity:.9 }}
        70%  {{ opacity:.5 }}
        100% {{ opacity:0; transform:translate(var(--dx), var(--rise)) }}
      }}

      .marcha {{ animation: marcha {MQ_W/22:.1f}s linear infinite }}
      @keyframes marcha {{ from{{transform:translateX(0)}} to{{transform:translateX(-{MQ_W:.1f}px)}} }}

      .pisca {{ animation: pisca 2.6s ease-in-out infinite }}
      @keyframes pisca {{ 0%,100%{{opacity:.25}} 50%{{opacity:1}} }}

      @media (prefers-reduced-motion: reduce) {{
        *, .joia, .olho, .brasa {{ animation: none !important }}
        .traco {{ opacity:0 }}
      }}
    </style>
  </defs>

  <g clip-path="url(#card)">
    <!-- obsidiana + luz ambiente -->
    <rect width="{W}" height="{H}" fill="url(#fundo)"/>
    <rect width="{W}" height="{H}" fill="url(#pontos)" opacity=".22" mask="url(#gradeMask)" class="surge"/>
    <ellipse cx="90" cy="{H}" rx="340" ry="220" fill="url(#aco)"/>
    <ellipse cx="930" cy="20" rx="300" ry="190" fill="url(#aco)" opacity=".7"/>
    <ellipse class="respira" cx="500" cy="175" rx="330" ry="210" fill="url(#halo)"/>

    <!-- reflexo diagonal do vidro -->
    <path d="M610 0 L760 0 L520 {H} L370 {H} Z" fill="#fff" opacity=".018"/>
    <path d="M790 0 L830 0 L590 {H} L550 {H} Z" fill="#fff" opacity=".022"/>

    <!-- brasas atrás do logo -->
    <g>{''.join(brasas)}</g>

    <!-- LOGO -->
    <g transform="translate({LX:.2f} {LY:.2f}) scale({S})">
      <use xlink:href="#logo" href="#logo" class="neon" fill="{OURO}" filter="url(#neon)" opacity=".7"/>
      <use xlink:href="#logo" href="#logo" class="derrete" fill="url(#ouro)"/>
      <use xlink:href="#logo" href="#logo" class="traco" fill="none" stroke="{LUZ}" stroke-width="3.4" stroke-linejoin="round"/>
    </g>
    <!-- reflexo metálico (logo + nome), atravessa e descansa -->
    <g mask="url(#brilhoMask)" opacity=".85">
      <g transform="translate({LX:.2f} {LY:.2f}) scale({S})"><use xlink:href="#logo" href="#logo" fill="#FFF6DD"/></g>
      <use xlink:href="#nome" href="#nome" class="sobe" fill="#FFF8E6"/>
    </g>

    <!-- brilho da joia da coroa e do olho -->
    <g class="joia"><path d="{estrela(round(crown_x,1), round(crown_y-6,1), 13)}" fill="{LUZ}"/><circle cx="{crown_x:.1f}" cy="{crown_y-6:.1f}" r="5" fill="{LUZ}" filter="url(#neonFino)"/></g>
    <g class="olho"><circle cx="{eye_x:.1f}" cy="{eye_y:.1f}" r="3.2" fill="{LUZ}" filter="url(#neonFino)"/><circle cx="{eye_x:.1f}" cy="{eye_y:.1f}" r="1.2" fill="#fff"/></g>

    <!-- NOME -->
    <use xlink:href="#nome" href="#nome" class="sobe" fill="{OURO}" filter="url(#neon)" opacity=".35"/>
    <use xlink:href="#nome" href="#nome" class="sobe" fill="url(#ouroNome)"/>
    <rect class="cresce" x="380" y="404" width="240" height="1.6" fill="url(#regua)"/>
    {losango(500, 404.8, 3.6, LUZ, ' class="cresce"')}

    <g class="sobe2" fill="{MARFIM}" fill-opacity=".86">
      {''.join(f'<path d="{d}"/>' for d in sub_paths)}
      {''.join(losango(lx, 443.5, 3, OURO) for lx in losangos)}
    </g>
    <path class="sobe3" d="{tag_d}" fill="{ACO}" fill-opacity=".85"/>

    <!-- HUD em azul-aço -->
    <g class="hud" fill="{ACO}">
      <path d="M22 40 V22 H40" fill="none" stroke="{ACO}" stroke-opacity=".55" stroke-width="1.2"/>
      <path d="M978 40 V22 H960" fill="none" stroke="{ACO}" stroke-opacity=".55" stroke-width="1.2"/>
      <path d="M22 {BAND_Y-24} V{BAND_Y-6} H40" fill="none" stroke="{ACO}" stroke-opacity=".55" stroke-width="1.2"/>
      <path d="M978 {BAND_Y-24} V{BAND_Y-6} H960" fill="none" stroke="{ACO}" stroke-opacity=".55" stroke-width="1.2"/>
      <circle class="pisca" cx="46" cy="40.6" r="2.6" fill="{OURO_C}"/>
      <path d="{hud_tl}" fill-opacity=".8"/>
      <path d="{hud_tr}" fill-opacity=".8"/>
      <path d="{hud_bl}" fill-opacity=".55"/>
      <path d="{hud_br}" fill-opacity=".55"/>
    </g>

    <!-- faixa de vidro com valores -->
    <rect x="0" y="{BAND_Y}" width="{W}" height="{H-BAND_Y}" fill="url(#faixa)"/>
    <rect x="0" y="{BAND_Y}" width="{W}" height="1" fill="url(#fioTopo)" opacity=".7"/>
    <g mask="url(#marqMask)">
      <g class="marcha" fill="{MARFIM}" fill-opacity=".62">
        <g id="ciclo"><path d="{' '.join(mq_paths)}"/>{''.join(losango(dx, BAND_Y+24, 2.6, OURO) for dx in mq_dots)}</g>
        <use xlink:href="#ciclo" href="#ciclo" x="{MQ_W:.1f}"/>
      </g>
    </g>

    <!-- bordas de vidro -->
    <rect x="80" y="0" width="{W-160}" height="1.2" fill="url(#fioTopo)"/>
    <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="27" fill="none" stroke="url(#borda)" stroke-width="1.5"/>
  </g>
</svg>
'''

# coloca a classe .pena nas variáveis de rotação corretas
from base import gravar
gravar("hero.svg", svg)

