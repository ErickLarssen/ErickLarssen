#!/usr/bin/env python3
"""Rodapé: chamada final com a águia em marca d'água, brasas e reflexo."""
import random
from base import *

W, H = 1000, 300
T = Texto("f")
logo = "".join(f'<path d="{d}"/>' for d in logo_pecas())

# águia grande à direita, em marca d'água
S = 0.42
LX, LY = 1000 - 1080 * S * 0.62, 30 - 220 * S

titulo1 = T("VAMOS CONSTRUIR ALGO", SERIF, 36, 56, 122, 1.5, fill=MARFIM)
titulo2 = T("COM PROPÓSITO?", SERIF, 36, 56, 168, 1.5)
links = [("globe", "ericksilva.dev"), ("linkedin", "in/ericklarssen"), ("github", "github.com/ErickLarssen")]
pills, x = [], 56
for ic, txt in links:
    w = T.medir(txt, MONO_R, 10.5, 0.4) + 44
    pills.append(f'<rect x="{x}" y="200" width="{w:.0f}" height="30" rx="15" fill="#141319" stroke="{OURO}" stroke-opacity=".35"/>'
                 + icone(ic, x + 12, 208, 14, OURO_C) + T(txt, MONO_R, 10.5, x + 32, 219, 0.4, fill=MARFIM, extra=' fill-opacity=".85"'))
    x += w + 10

random.seed(3)
brasas = "".join(
    f'<circle cx="{random.uniform(560, 960):.0f}" cy="{random.uniform(200, 290):.0f}" r="{random.choice([1, 1.4, 1.8])}" '
    f'fill="{random.choice([OURO_C, LUZ, OURO, ACO])}" class="brasa" style="--dx:{random.uniform(-20,20):.0f}px;'
    f'--rise:-{random.uniform(110,190):.0f}px;animation-duration:{random.uniform(7,12):.1f}s;animation-delay:-{random.uniform(0,10):.1f}s"/>'
    for _ in range(14))

defs = defs_vidro(W, H) + f'''
    <linearGradient id="fLogo" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{OURO_C}" stop-opacity=".22"/><stop offset="1" stop-color="{OURO_E}" stop-opacity=".05"/>
    </linearGradient>
    <mask id="fBrilho" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect class="varre" x="-220" y="-40" width="180" height="{H+80}" fill="url(#reflexo)" transform="skewX(-18)"/>
    </mask>'''
css = """
      .varre { animation: varre 9s cubic-bezier(.45,0,.25,1) 2s infinite }
      @keyframes varre { 0%{transform:skewX(-18deg) translateX(0)} 32%,100%{transform:skewX(-18deg) translateX(1400px)} }
      .brasa { opacity:0; animation-name: brasa; animation-timing-function: linear; animation-iteration-count: infinite }
      @keyframes brasa { 0%{opacity:0;transform:translate(0,0)} 15%{opacity:.85} 70%{opacity:.4} 100%{opacity:0;transform:translate(var(--dx),var(--rise))} }
      .respira { transform-box:fill-box; transform-origin:center; animation: respira 7s ease-in-out infinite }
      @keyframes respira { 0%,100%{opacity:.7;transform:scale(.96)} 50%{opacity:1;transform:scale(1.04)} }"""

corpo = f'''<g clip-path="url(#card)">
  {fundo_vidro(W, H, grade=.1)}
  <ellipse class="respira" cx="{LX + 540*S:.0f}" cy="150" rx="300" ry="200" fill="url(#ouroAmb)"/>
  <g transform="translate({LX:.1f} {LY:.1f}) scale({S})" fill="url(#fLogo)" stroke="{OURO_C}" stroke-opacity=".18" stroke-width="2">{logo}</g>
  {brasas}
  <g class="sobe">
    {losango(60, 72, 4, OURO_C)}{T("PRÓXIMO PROJETO", MONO, 10.5, 74, 76, 3.6, fill=OURO_C)}
    {titulo1}
    {em_ouro(titulo2, 54, 132, 460, 46, p="f")}
  </g>
  <g mask="url(#fBrilho)" fill="#FFF6DD">{titulo1}{titulo2}</g>
  <g class="sobe" style="animation-delay:.3s">{"".join(pills)}</g>
  {T("ERICK SILVA  ·  FULL-STACK DEVELOPMENT  ·  DESIGN × TECHNOLOGY", MONO_R, 8.5, 56, 268, 2.4, fill=SUAVE, extra=' fill-opacity=".6"')}
  {borda_vidro(W, H)}
</g>'''

if __name__ == "__main__":
    gravar("footer.svg", svg(W, H, "Vamos construir algo com propósito? ericksilva.dev · LinkedIn in/ericklarssen · GitHub ErickLarssen",
                             defs + T.defs(), corpo, css))
