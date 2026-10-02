#!/usr/bin/env python3
"""Pílulas de link (uma imagem por link, para cada uma ser clicável) e o divisor."""
from base import *

LINKS = [
    ("globe", "PORTFÓLIO", "ericksilva.dev", 0.0),
    ("linkedin", "LINKEDIN", "in/ericklarssen", 0.35),
    ("github", "GITHUB", "ErickLarssen", 0.7),
]

W, H, RX = 280, 72, 36


def pilula(icon, rotulo, sub, atraso):
    T = Texto("p")
    defs = f'''
    <linearGradient id="vidro" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1A1820"/><stop offset="1" stop-color="{OBS}"/>
    </linearGradient>
    <linearGradient id="borda" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{OURO_C}" stop-opacity=".7"/><stop offset=".55" stop-color="{OURO}" stop-opacity=".18"/><stop offset="1" stop-color="{ACO}" stop-opacity=".45"/>
    </linearGradient>
    <linearGradient id="topo" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="{LUZ}" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="aura" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{OURO}" stop-opacity=".35"/><stop offset="1" stop-color="{OURO}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="reflexo" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="forma"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="{RX-2}"/></clipPath>'''
    css = f"""
      .varre {{ animation: varre 7s cubic-bezier(.45,0,.25,1) {1.2+atraso:.2f}s infinite }}
      @keyframes varre {{ 0%{{transform:skewX(-20deg) translateX(0)}} 28%,100%{{transform:skewX(-20deg) translateX({W+160}px)}} }}
      .aura {{ transform-box:fill-box; transform-origin:center; animation: aura 4.5s ease-in-out {atraso:.2f}s infinite }}
      @keyframes aura {{ 0%,100%{{opacity:.55;transform:scale(.9)}} 50%{{opacity:1;transform:scale(1.08)}} }}"""
    cx, cy = 38, H / 2
    corpo = f'''
  <g clip-path="url(#forma)">
    <rect width="{W}" height="{H}" fill="url(#vidro)"/>
    <rect width="{W}" height="{H}" fill="#fff" opacity=".015"/>
    <rect class="varre" x="-140" y="0" width="90" height="{H}" fill="url(#reflexo)"/>
  </g>
  <rect x="{RX}" y="2" width="{W-2*RX}" height="1" fill="url(#topo)"/>
  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="{RX-1.5}" fill="none" stroke="url(#borda)" stroke-width="1.5"/>
  <circle class="aura" cx="{cx}" cy="{cy}" r="26" fill="url(#aura)"/>
  <circle cx="{cx}" cy="{cy}" r="19" fill="{OBS}" stroke="{OURO}" stroke-opacity=".45"/>
  {icone(icon, cx-10, cy-10, 20, OURO_C)}
  {T(rotulo, SANS_B, 14, 70, 33, 3.6, fill=MARFIM)}
  {T(sub, MONO_R, 11, 70, 52, 0.6, fill=ACO)}
  <path d="M{W-42} {cy+5} L{W-32} {cy-5} M{W-39} {cy-5} H{W-32} V{cy+2}" fill="none" stroke="{OURO_C}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'''
    return svg(W, H, f"{rotulo.title()} — {sub}", defs + T.defs(), corpo, css)


def divisor():
    W, H = 1000, 40
    y = H / 2
    defs = f'''
    <linearGradient id="linha" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACO}" stop-opacity="0"/><stop offset=".25" stop-color="{ACO}" stop-opacity=".35"/>
      <stop offset=".5" stop-color="{OURO_C}" stop-opacity=".9"/><stop offset=".75" stop-color="{ACO}" stop-opacity=".35"/>
      <stop offset="1" stop-color="{ACO}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="faisca" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="{LUZ}" stop-opacity=".9"/><stop offset="1" stop-color="{OURO}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rastro" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{OURO}" stop-opacity="0"/><stop offset="1" stop-color="{LUZ}" stop-opacity=".9"/>
    </linearGradient>
    <filter id="brilho" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3"/></filter>'''
    css = """
      .corre { animation: corre 6.5s cubic-bezier(.6,0,.4,1) infinite }
      @keyframes corre { 0%{transform:translateX(0);opacity:0} 8%{opacity:1} 92%{opacity:1} 100%{transform:translateX(880px);opacity:0} }
      .pulsa { transform-box:fill-box; transform-origin:center; animation: pulsa 3.2s ease-in-out infinite }
      @keyframes pulsa { 0%,100%{opacity:.45;transform:scale(.8)} 50%{opacity:1;transform:scale(1.25)} }
      .gira { transform-box:fill-box; transform-origin:center; animation: gira 12s linear infinite }
      @keyframes gira { to{transform:rotate(360deg)} }"""
    ticks = "".join(f'<rect x="{x}" y="{y-3}" width="1" height="6" fill="{ACO}" opacity="{0.15 + 0.25*(1-abs(x-500)/500):.2f}"/>'
                    for x in range(80, 921, 40) if abs(x - 500) > 40)
    corpo = f'''
  <rect x="0" y="{y-0.5}" width="{W}" height="1" fill="url(#linha)"/>
  {ticks}
  <g class="corre">
    <rect x="20" y="{y-0.75}" width="80" height="1.5" fill="url(#rastro)"/>
    <circle cx="100" cy="{y}" r="7" fill="url(#faisca)"/>
  </g>
  <circle class="pulsa" cx="500" cy="{y}" r="11" fill="{OURO}" opacity=".5" filter="url(#brilho)"/>
  <g class="gira"><path d="M500 {y-9} L509 {y} L500 {y+9} L491 {y}Z" fill="none" stroke="{OURO_C}" stroke-opacity=".55"/></g>
  {losango(500, y, 4.5, LUZ)}
  {losango(470, y, 1.8, OURO)}{losango(530, y, 1.8, OURO)}'''
    return svg(W, H, "", defs, corpo, css)


if __name__ == "__main__":
    for icon, rot, sub, at in LINKS:
        gravar(f"link-{rot.lower().replace('ó','o')}.svg", pilula(icon, rot, sub, at))
    gravar("divisor.svg", divisor())
