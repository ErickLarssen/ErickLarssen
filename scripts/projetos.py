#!/usr/bin/env python3
"""Cards de projetos — um SVG por projeto, para cada card ser clicável."""
from base import *

PROJETOS = [
    dict(slug="edutrack", nome="EduTrack", online=True, tags=["JavaScript"], arte="painel",
         desc="Gestão de equipamentos escolares do programa PROATI (SEDUC-SP): o ciclo completo de tablets, notebooks e Chromebooks, do empréstimo à devolução, num dashboard em tempo real."),
    dict(slug="briefing", nome="Briefing Digital", online=True, tags=["JavaScript"], arte="passos",
         desc="Plataforma interativa que coleta o briefing antes do projeto começar: uma experiência guiada e objetiva no lugar do formulário estático, pensada para poucos minutos."),
    dict(slug="portfolio", nome="Portfólio", online=False, tags=["HTML", "CSS"], arte="grade",
         desc="Portfólio pessoal reunindo projetos de design e desenvolvimento, com identidade visual autoral."),
    dict(slug="cinerick", nome="Cinerick", online=False, tags=["HTML", "CSS"], arte="filme",
         desc="Site pessoal dedicado a filmes, séries, animações e personagens favoritos: um santuário cinematográfico com curadoria própria."),
]

W, H = 480, 290
AX, AY, AW, AH = 330, 64, 122, 118   # área da ilustração


def quebrar(T, texto, estilo, tam, largura):
    linhas, atual = [], ""
    for p in texto.split():
        teste = (atual + " " + p).strip()
        if T.medir(teste, estilo, tam, 0.1) > largura and atual:
            linhas.append(atual)
            atual = p
        else:
            atual = teste
    return linhas + [atual]


# ── ilustrações ─────────────────────────────────────────
def arte_painel():
    a = []
    alturas = [38, 58, 46, 72, 54, 84]
    base = AY + AH - 26
    for i, h in enumerate(alturas):
        x = AX + 14 + i * 16
        cor = "url(#ouroV)" if i == 5 else ACO
        op = "1" if i == 5 else ".55"
        a.append(f'<rect class="barra" style="animation-delay:{i*0.12:.2f}s" x="{x}" y="{base-h}" width="10" height="{h}" rx="2" fill="{cor}" opacity="{op}"/>')
    a.append(f'<rect x="{AX+10}" y="{base+1}" width="{AW-20}" height="1" fill="{ACO}" opacity=".4"/>')
    for i in range(3):
        x = AX + 16 + i * 34
        a.append(f'<rect x="{x}" y="{base+9}" width="24" height="14" rx="2.5" fill="none" stroke="{ACO}" stroke-opacity=".6"/>')
        a.append(f'<circle class="pisca" style="animation-delay:{i*0.7:.1f}s" cx="{x+20}" cy="{base+12.5}" r="1.8" fill="{OURO_C}"/>')
    return "".join(a)


def arte_passos():
    a = []
    y = AY + 30
    xs = [AX + 18 + i * 29 for i in range(4)]
    a.append(f'<rect x="{xs[0]}" y="{y-0.5}" width="{xs[-1]-xs[0]}" height="1" fill="{ACO}" opacity=".35"/>')
    a.append(f'<rect class="progresso" x="{xs[0]}" y="{y-1}" width="{xs[-1]-xs[0]}" height="2" fill="url(#ouroH)"/>')
    for i, x in enumerate(xs):
        a.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#111015" stroke="{ACO}" stroke-opacity=".6"/>')
        a.append(f'<circle class="passo" style="animation-delay:{i*1.0:.1f}s" cx="{x}" cy="{y}" r="7" fill="{OURO}" stroke="{LUZ}"/>')
    # formulário
    for k, (wl, ativo) in enumerate([(92, False), (70, True), (84, False)]):
        yy = AY + 56 + k * 20
        a.append(f'<rect x="{AX+12}" y="{yy}" width="{AW-24}" height="14" rx="3" fill="#111015" stroke="{OURO if ativo else ACO}" stroke-opacity="{.6 if ativo else .3}"/>')
        if ativo:
            a.append(f'<rect class="digita" x="{AX+18}" y="{yy+6}" width="{wl-30}" height="2" rx="1" fill="{MARFIM}" opacity=".7"/>')
            a.append(f'<rect class="cursor" x="{AX+18}" y="{yy+3}" width="1.2" height="8" fill="{LUZ}"/>')
        else:
            a.append(f'<rect x="{AX+18}" y="{yy+6}" width="{wl-40}" height="2" rx="1" fill="{SUAVE}" opacity=".3"/>')
    return "".join(a)


def arte_grade():
    a = []
    for i in range(4):
        x = AX + 12 + (i % 2) * 52
        y = AY + 10 + (i // 2) * 52
        a.append(f'<rect x="{x}" y="{y}" width="46" height="46" rx="5" fill="#15141A" stroke="{ACO}" stroke-opacity=".35"/>')
        motivo = [f'<circle cx="{x+23}" cy="{y+23}" r="10" fill="none" stroke="{OURO_C}" stroke-opacity=".7"/>',
                  f'<path d="M{x+10} {y+34} L{x+20} {y+20} L{x+28} {y+28} L{x+36} {y+16}" fill="none" stroke="{ACO}" stroke-opacity=".8"/>',
                  losango(x + 23, y + 23, 9, "none", f' stroke="{OURO_C}" stroke-opacity=".7"'),
                  f'<rect x="{x+11}" y="{y+16}" width="24" height="3" rx="1.5" fill="{MARFIM}" opacity=".4"/><rect x="{x+11}" y="{y+24}" width="16" height="3" rx="1.5" fill="{MARFIM}" opacity=".25"/>']
        a.append(motivo[i])
        a.append(f'<rect class="moldura" style="animation-delay:{i*1.1:.1f}s" x="{x}" y="{y}" width="46" height="46" rx="5" fill="{OURO}" fill-opacity=".08" stroke="{LUZ}"/>')
    return "".join(a)


def arte_filme():
    a = []
    y0, fh = AY + 26, 58
    quadros = []
    for i in range(8):
        x = AX - 20 + i * 36
        quadros.append(f'<rect x="{x}" y="{y0+10}" width="30" height="{fh-20}" rx="2" fill="#1A1820" stroke="{ACO}" stroke-opacity=".3"/>')
        quadros.append(f'<rect x="{x+3}" y="{y0+3}" width="6" height="4" rx="1" fill="{ACO}" opacity=".45"/><rect x="{x+18}" y="{y0+3}" width="6" height="4" rx="1" fill="{ACO}" opacity=".45"/>')
        quadros.append(f'<rect x="{x+3}" y="{y0+fh-7}" width="6" height="4" rx="1" fill="{ACO}" opacity=".45"/><rect x="{x+18}" y="{y0+fh-7}" width="6" height="4" rx="1" fill="{ACO}" opacity=".45"/>')
    a.append(f'<g clip-path="url(#pArte)"><rect x="{AX}" y="{y0}" width="{AW}" height="{fh}" fill="#0F0E13"/>'
             f'<g class="rola">{"".join(quadros)}</g></g>')
    cx, cy = AX + AW / 2, y0 + fh / 2
    a.append(f'<circle class="pulsa" cx="{cx}" cy="{cy}" r="17" fill="{OURO}" opacity=".35" filter="url(#neonFino)"/>')
    a.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="{OBS}" stroke="{OURO_C}"/>')
    a.append(f'<path d="M{cx-4} {cy-6} L{cx+7} {cy} L{cx-4} {cy+6}Z" fill="{OURO_C}"/>')
    for k in range(5):
        a.append(f'<path d="M{AX+22+k*20} {y0+fh+20} l2.4 4.8 5.3.8-3.8 3.7.9 5.3-4.8-2.5-4.8 2.5.9-5.3-3.8-3.7 5.3-.8z" fill="{OURO_C if k < 4 else "none"}" stroke="{OURO_C}" stroke-width=".8" opacity=".85"/>')
    return "".join(a)


ARTES = dict(painel=arte_painel, passos=arte_passos, grade=arte_grade, filme=arte_filme)

CSS = f"""
      .varre {{ animation: varre 12s cubic-bezier(.45,0,.25,1) infinite }}
      @keyframes varre {{ 0%{{transform:skewX(-20deg) translateX(0)}} 20%,100%{{transform:skewX(-20deg) translateX({W+300}px)}} }}
      .barra {{ transform-box:fill-box; transform-origin:bottom; animation: barra 5s cubic-bezier(.3,.7,.3,1) infinite }}
      @keyframes barra {{ 0%{{transform:scaleY(.15)}} 25%,80%{{transform:scaleY(1)}} 100%{{transform:scaleY(.15)}} }}
      .progresso {{ transform-box:fill-box; transform-origin:left; animation: prog 4s ease-in-out infinite }}
      @keyframes prog {{ 0%{{transform:scaleX(0)}} 75%,90%{{transform:scaleX(1)}} 100%{{transform:scaleX(0)}} }}
      .passo {{ opacity:0; animation: passo 4s ease infinite }}
      @keyframes passo {{ 0%{{opacity:0}} 5%,88%{{opacity:1}} 100%{{opacity:0}} }}
      .digita {{ transform-box:fill-box; transform-origin:left; animation: digita 4s steps(12) infinite }}
      @keyframes digita {{ 0%{{transform:scaleX(0)}} 70%,100%{{transform:scaleX(1)}} }}
      .cursor {{ animation: cursor 4s steps(12) infinite, pisca 1s steps(2) infinite }}
      @keyframes cursor {{ 0%{{transform:translateX(0)}} 70%,100%{{transform:translateX(62px)}} }}
      .moldura {{ opacity:0; animation: moldura 4.4s ease-in-out infinite }}
      @keyframes moldura {{ 0%,100%{{opacity:0}} 10%,22%{{opacity:1}} 35%{{opacity:0}} }}
      .rola {{ animation: rola 6s linear infinite }}
      @keyframes rola {{ to{{transform:translateX(-72px)}} }}
      .pulsa {{ transform-box:fill-box; transform-origin:center; animation: pulsa 2.8s ease-in-out infinite }}
      @keyframes pulsa {{ 0%,100%{{opacity:.25;transform:scale(.9)}} 50%{{opacity:.7;transform:scale(1.25)}} }}"""


def card(i, p):
    T = Texto("k")
    a = []
    a.append(T(f"PROJETO {i+1:02d}", MONO, 10, 32, 48, 3, fill=SUAVE))
    if p["online"]:
        a.append(f'<rect x="132" y="35" width="70" height="18" rx="9" fill="{OURO}" fill-opacity=".1" stroke="{OURO}" stroke-opacity=".45"/>')
        a.append(f'<circle class="pisca" cx="144" cy="44" r="2.6" fill="{OURO_C}"/>')
        a.append(T("ONLINE", MONO, 8.5, 152, 47.2, 1.6, fill=OURO_C))
    else:
        a.append(f'<rect x="132" y="35" width="66" height="18" rx="9" fill="none" stroke="{ACO}" stroke-opacity=".45"/>')
        a.append(T("CÓDIGO", MONO, 8.5, 165, 47.2, 1.6, "middle", fill=ACO))
    a.append(em_ouro(T(p["nome"].upper(), SERIF, 23, 32, 92, 1), 30, 66, 290, 34, p="k"))
    for k, l in enumerate(quebrar(T, p["desc"], SANS, 13.2, 268)):
        a.append(T(l, SANS, 13.2, 32, 122 + k * 19.5, 0.1, fill=SUAVE))
    # tags
    tx = 32
    for t in p["tags"]:
        tw = T.medir(t, MONO_R, 10, 0.4) + 20
        a.append(f'<rect x="{tx}" y="{H-50}" width="{tw:.1f}" height="22" rx="11" fill="#15141A" stroke="{ACO}" stroke-opacity=".4"/>')
        a.append(T(t, MONO_R, 10, tx + 10, H - 35.5, 0.4, fill=ACO))
        tx += tw + 8
    cta = "ACESSAR PROJETO" if p["online"] else "VER REPOSITÓRIO"
    a.append(T(cta, SANS_B, 10.5, W - 52, H - 35, 2.6, "end", fill=OURO_C))
    a.append(f'<circle cx="{W-36}" cy="{H-39}" r="11" fill="none" stroke="{OURO}" stroke-opacity=".5"/>')
    a.append(f'<path d="M{W-40} {H-35} L{W-32} {H-43} M{W-38} {H-43} H{W-32} V{H-37}" fill="none" stroke="{OURO_C}" stroke-width="1.4" stroke-linecap="round"/>')
    # ilustração
    a.append(f'<rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" rx="12" fill="#0E0D12" stroke="{OURO}" stroke-opacity=".16"/>')
    a.append(f'<g clip-path="url(#pArte)">{ARTES[p["arte"]]()}</g>')

    defs = defs_vidro(W, H, rx=22) + f'''
    <linearGradient id="ouroV" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{OURO_E}"/><stop offset="1" stop-color="{LUZ}"/></linearGradient>
    <linearGradient id="ouroH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{OURO_E}"/><stop offset="1" stop-color="{LUZ}"/></linearGradient>
    <linearGradient id="brilhoK" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="pArte"><rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" rx="12"/></clipPath>'''
    corpo = f'''<g clip-path="url(#card)">
  {fundo_vidro(W, H, rx=22, grade=.1, luz=(120, 60, 260, 160))}
  {"".join(a)}
  <rect class="varre" style="animation-delay:{2+i*0.6:.1f}s" x="-200" y="0" width="140" height="{H}" fill="url(#brilhoK)"/>
  {borda_vidro(W, H, rx=22)}
</g>'''
    label = f"{p['nome']} — {p['desc']} Tecnologias: {', '.join(p['tags'])}."
    return svg(W, H, label, defs + T.defs(), corpo, CSS, rx=22)


if __name__ == "__main__":
    for i, p in enumerate(PROJETOS):
        gravar(f"projeto-{p['slug']}.svg", card(i, p))
