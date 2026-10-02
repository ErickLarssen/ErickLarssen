#!/usr/bin/env python3
"""Manifesto + Design × Development.
Uma planta técnica em azul-aço vira interface renderizada em ouro quando a linha de varredura passa."""
from base import *

W, H = 1000, 440
T = Texto("m")

# ── coluna esquerda ─────────────────────────────────────
L = 52
linhas = [("LÓGICA ROBUSTA,", MARFIM), ("ARQUITETURA LIMPA", MARFIM), ("& EXPERIÊNCIA", "url(#ouro)"), ("MEMORÁVEL.", "url(#ouro)")]
TAM = 30
esq = [
    losango(L + 4, 66, 4, OURO_C),
    T("MANIFESTO", MONO, 11, L + 18, 70, 4, fill=OURO_C),
]
y = 118
for txt, cor in linhas:
    if cor.startswith("url"):
        esq.append(em_ouro(T(txt, SERIF, TAM, L, y, 1.5), L - 2, y - TAM, 440, TAM + 10))
    else:
        esq.append(T(txt, SERIF, TAM, L, y, 1.5, fill=cor))
    y += 38
esq.append(f'<rect class="cresce" x="{L}" y="{y-16}" width="64" height="2" rx="1" fill="url(#ouro)"/>')

col_y = y + 22
DESIGN = ["Brand Design & identidade", "UI/UX", "Direção de arte", "Design Systems", "Prototipagem"]
DEV = ["Front-End", "Back-End", "APIs", "Arquitetura Full-Stack", "Bancos de dados"]
listas = []
for i, (titulo, itens, cor, x) in enumerate([("DESIGN", DESIGN, OURO_C, L), ("DEVELOPMENT", DEV, ACO, L + 220)]):
    g = [f'<circle cx="{x+3}" cy="{col_y-4}" r="3" fill="{cor}"/>', T(titulo, MONO, 10.5, x + 14, col_y, 3.2, fill=cor)]
    for j, it in enumerate(itens):
        yy = col_y + 26 + j * 21
        g.append(f'<rect x="{x}" y="{yy-5}" width="6" height="1.2" fill="{cor}" opacity=".7"/>')
        g.append(T(it, SANS, 14, x + 14, yy, 0.2, fill=MARFIM, extra=' fill-opacity=".82"'))
    listas.append(f'<g class="sobe" style="animation-delay:{0.5+i*0.15}s">' + "".join(g) + "</g>")

# ── janela à direita ─────────────────────────────────────
WX, WY, WW, WH = 500, 40, 452, 360
CX, CY, CW, CH = WX + 16, WY + 52, WW - 32, WH - 88   # área de desenho


def blueprint():
    """A mesma tela, como planta técnica."""
    s = f'stroke="{ACO}" fill="none" stroke-width="1"'
    a = []
    # grade fina
    for gx in range(CX, CX + CW + 1, 20):
        a.append(f'<line x1="{gx}" y1="{CY}" x2="{gx}" y2="{CY+CH}" stroke="{ACO}" stroke-opacity=".08"/>')
    for gy in range(CY, CY + CH + 1, 20):
        a.append(f'<line x1="{CX}" y1="{gy}" x2="{CX+CW}" y2="{gy}" stroke="{ACO}" stroke-opacity=".08"/>')
    # navbar
    a.append(f'<rect x="{CX+16}" y="{CY+14}" width="{CW-32}" height="24" rx="6" {s} stroke-dasharray="3 3"/>')
    a.append(f'<circle cx="{CX+30}" cy="{CY+26}" r="5" {s}/>')
    for k in range(3):
        a.append(f'<line x1="{CX+CW-130+k*36}" y1="{CY+26}" x2="{CX+CW-108+k*36}" y2="{CY+26}" {s}/>')
    # imagem (X)
    ix, iy, iw, ih = CX + 16, CY + 52, 230, 120
    a.append(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="8" {s}/>')
    a.append(f'<path d="M{ix} {iy} L{ix+iw} {iy+ih} M{ix+iw} {iy} L{ix} {iy+ih}" {s} stroke-opacity=".35"/>')
    # cota da largura
    a.append(f'<path d="M{ix} {iy-6} H{ix+iw} M{ix} {iy-9} V{iy-3} M{ix+iw} {iy-9} V{iy-3}" {s} stroke-opacity=".7"/>')
    a.append(f'<rect x="{ix+iw/2-16}" y="{iy-12}" width="32" height="11" fill="#0C0D11"/>')
    a.append(T("320", MONO_R, 8.5, ix + iw / 2, iy - 3.5, 0.5, "middle", fill=ACO))
    # título + texto
    a.append(f'<rect x="{ix}" y="{iy+ih+16}" width="150" height="16" rx="2" {s}/>')
    a.append(T("H2 · CINZEL 24", MONO_R, 7.5, ix + 158, iy + ih + 28, 0.6, fill=ACO, extra=' fill-opacity=".7"'))
    for k, wl in enumerate([210, 180]):
        a.append(f'<line x1="{ix}" y1="{iy+ih+46+k*12}" x2="{ix+wl}" y2="{iy+ih+46+k*12}" {s} stroke-opacity=".6"/>')
    # botão
    a.append(f'<rect x="{ix}" y="{CY+CH-40}" width="104" height="26" rx="13" {s}/>')
    a.append(T("btn/primary", MONO_R, 7.5, ix + 112, CY + CH - 23, 0.6, fill=ACO, extra=' fill-opacity=".7"'))
    # coluna lateral (3 cards)
    sx = CX + 264
    for k in range(3):
        yy = CY + 52 + k * 64
        a.append(f'<rect x="{sx}" y="{yy}" width="{CW-280}" height="52" rx="8" {s} stroke-dasharray="3 3"/>')
        a.append(f'<line x1="{sx+12}" y1="{yy+18}" x2="{sx+60}" y2="{yy+18}" {s}/>')
        a.append(f'<line x1="{sx+12}" y1="{yy+34}" x2="{sx+90}" y2="{yy+34}" {s} stroke-opacity=".6"/>')
    a.append(T("gap 24", MONO_R, 7.5, sx + 8, CY + CH - 10, 0.6, fill=ACO, extra=' fill-opacity=".7"'))
    # miras nos cantos
    for (mx, my) in [(CX + 8, CY + 8), (CX + CW - 8, CY + 8), (CX + 8, CY + CH - 8), (CX + CW - 8, CY + CH - 8)]:
        a.append(f'<path d="M{mx-4} {my} H{mx+4} M{mx} {my-4} V{my+4}" stroke="{ACO}" stroke-opacity=".6"/>')
    return "".join(a)


def render():
    """A mesma tela, renderizada."""
    a = [f'<rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" fill="#0E0D12"/>',
         f'<rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" fill="url(#mAmb)"/>']
    a.append(f'<rect x="{CX+16}" y="{CY+14}" width="{CW-32}" height="24" rx="6" fill="#17151D" stroke="{FIO}"/>')
    a.append(f'<circle cx="{CX+30}" cy="{CY+26}" r="5" fill="url(#ouro)"/>')
    for k in range(3):
        a.append(f'<rect x="{CX+CW-130+k*36}" y="{CY+25}" width="22" height="2" rx="1" fill="{MARFIM}" opacity="{0.75 if k==0 else 0.35}"/>')
    ix, iy, iw, ih = CX + 16, CY + 52, 230, 120
    a.append(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="8" fill="url(#mImg)"/>')
    # arte: arcos dourados (sol nascendo atrás de montanhas)
    a.append(f'<g clip-path="url(#mImgClip)"><circle cx="{ix+150}" cy="{iy+86}" r="30" fill="url(#ouro)" opacity=".9"/>'
             f'<path d="M{ix} {iy+ih} L{ix+70} {iy+60} L{ix+120} {iy+100} L{ix+170} {iy+70} L{ix+iw} {iy+ih}Z" fill="#0B0A0E" opacity=".92"/>'
             f'<path d="M{ix+70} {iy+60} L{ix+120} {iy+100} L{ix+170} {iy+70}" fill="none" stroke="{OURO_C}" stroke-opacity=".5"/></g>')
    a.append(T("Projeto Aurum", SERIF, 15, ix, iy + ih + 30, 0.4, fill=MARFIM))
    for k, wl in enumerate([210, 180]):
        a.append(f'<rect x="{ix}" y="{iy+ih+45+k*12}" width="{wl}" height="3" rx="1.5" fill="{SUAVE}" opacity=".35"/>')
    a.append(f'<rect x="{ix}" y="{CY+CH-40}" width="104" height="26" rx="13" fill="url(#ouro)"/>')
    a.append(T("ACESSAR", SANS_B, 9.5, ix + 52, CY + CH - 23.5, 2.2, "middle", fill=OBS))
    sx = CX + 264
    valores = [("98", "PERFORMANCE"), ("100", "ACESSIBILIDADE"), ("0.4s", "CARREGAMENTO")]
    for k, (v, r) in enumerate(valores):
        yy = CY + 52 + k * 64
        a.append(f'<rect x="{sx}" y="{yy}" width="{CW-280}" height="52" rx="8" fill="#16141B" stroke="{OURO}" stroke-opacity=".22"/>')
        a.append(T(v, SERIF, 17, sx + 12, yy + 26, 0.3, fill=OURO_C))
        a.append(T(r, MONO_R, 7, sx + 12, yy + 40, 1.2, fill=SUAVE))
    return "".join(a)


defs = defs_vidro(W, H) + f'''
    <linearGradient id="mImg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2A2112"/><stop offset="1" stop-color="#121016"/>
    </linearGradient>
    <radialGradient id="mAmb" cx="30%" cy="35%" r="70%">
      <stop offset="0" stop-color="{OURO}" stop-opacity=".10"/><stop offset="1" stop-color="{OURO}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="mScan" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{OURO}" stop-opacity="0"/><stop offset=".85" stop-color="{OURO}" stop-opacity=".18"/><stop offset="1" stop-color="{LUZ}" stop-opacity=".5"/>
    </linearGradient>
    <clipPath id="mImgClip"><rect x="{CX+16}" y="{CY+52}" width="230" height="120" rx="8"/></clipPath>
    <clipPath id="mArea"><rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="6"/></clipPath>
    <mask id="mRevela" maskUnits="userSpaceOnUse" x="{CX}" y="{CY}" width="{CW}" height="{CH}">
      <rect class="scan" x="{CX-CW}" y="{CY}" width="{CW}" height="{CH}" fill="#fff"/>
    </mask>'''

css = f"""
      .scan {{ animation: scan 11s cubic-bezier(.65,0,.35,1) 1s infinite }}
      @keyframes scan {{
        0%,8%   {{ transform:translateX(0) }}
        38%,62% {{ transform:translateX({CW}px) }}
        92%,100%{{ transform:translateX(0) }}
      }}
      .tabR {{ animation: tabR 11s cubic-bezier(.65,0,.35,1) 1s infinite }}
      @keyframes tabR {{ 0%,24%{{opacity:0}} 30%,72%{{opacity:1}} 78%,100%{{opacity:0}} }}
      .tabB {{ animation: tabB 11s cubic-bezier(.65,0,.35,1) 1s infinite }}
      @keyframes tabB {{ 0%,24%{{opacity:1}} 30%,72%{{opacity:0}} 78%,100%{{opacity:1}} }}
      .cresce {{ transform-box:fill-box; transform-origin:left; animation: cresce 1.1s cubic-bezier(.2,.7,.3,1) .5s both }}
      @keyframes cresce {{ from{{transform:scaleX(0)}} to{{transform:scaleX(1)}} }}"""

tab_y = WY + 18
janela = f'''
  <g class="sobe" style="animation-delay:.3s">
    <rect x="{WX+6}" y="{WY+14}" width="{WW}" height="{WH}" rx="16" fill="#000" opacity=".35"/>
    <rect x="{WX}" y="{WY}" width="{WW}" height="{WH}" rx="16" fill="#111015" stroke="{OURO}" stroke-opacity=".22"/>
    <rect x="{WX+40}" y="{WY}" width="{WW-80}" height="1" fill="url(#fioTopo)"/>
    <circle cx="{WX+22}" cy="{WY+22}" r="4.5" fill="{OURO_C}"/><circle cx="{WX+38}" cy="{WY+22}" r="4.5" fill="{ACO}"/><circle cx="{WX+54}" cy="{WY+22}" r="4.5" fill="{MARFIM}" opacity=".3"/>
    <g>
      <rect class="tabB" x="{WX+150}" y="{tab_y-8}" width="96" height="21" rx="10.5" fill="{ACO}" fill-opacity=".12" stroke="{ACO}" stroke-opacity=".45"/>
      {T("blueprint.fig", MONO_R, 9.5, WX+198, tab_y+6, 0.4, "middle", fill=ACO)}
      <rect class="tabR" x="{WX+256}" y="{tab_y-8}" width="86" height="21" rx="10.5" fill="{OURO}" fill-opacity=".12" stroke="{OURO}" stroke-opacity=".5"/>
      {T("render.tsx", MONO_R, 9.5, WX+299, tab_y+6, 0.4, "middle", fill=OURO_C)}
    </g>
    <g clip-path="url(#mArea)">
      <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" fill="#0C0D11"/>
      {blueprint()}
      <g mask="url(#mRevela)">{render()}</g>
      <g class="scan">
        <rect x="{CX-60}" y="{CY}" width="60" height="{CH}" fill="url(#mScan)"/>
        <rect x="{CX-1.5}" y="{CY}" width="3" height="{CH}" fill="{LUZ}" filter="url(#neonFino)"/>
        <rect x="{CX-0.5}" y="{CY}" width="1" height="{CH}" fill="#fff"/>
      </g>
    </g>
    <circle class="pisca" cx="{CX+4}" cy="{WY+WH-17}" r="2.6" fill="{OURO_C}"/>
    {T("DESIGN → CÓDIGO", MONO_R, 8.5, CX+14, WY+WH-14, 2, fill=SUAVE)}
    {T("mesma decisão, duas linguagens", MONO_R, 8.5, CX+CW, WY+WH-14, 0.4, "end", fill=ACO, extra=' fill-opacity=".8"')}
  </g>'''

corpo = f'''<g clip-path="url(#card)">
  {fundo_vidro(W, H, luz=(260, 160, 320, 200))}
  <g class="sobe">{"".join(esq)}</g>
  {"".join(listas)}
  {janela}
  {borda_vidro(W, H)}
</g>'''

if __name__ == "__main__":
    gravar("manifesto.svg", svg(W, H,
        "Manifesto: lógica robusta, arquitetura limpa e experiência memorável. Design: brand design e identidade, UI/UX, direção de arte, design systems, prototipagem. Development: front-end, back-end, APIs, arquitetura full-stack, bancos de dados.",
        defs + T.defs(), corpo, css))
