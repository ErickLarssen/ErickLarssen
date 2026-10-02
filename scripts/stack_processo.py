#!/usr/bin/env python3
"""Stack (painel de vidro com ícones em ouro) e Como trabalho (linha do tempo com pulso)."""
from base import *

# ═════════════════════════ STACK ═════════════════════════
# (nome, ícone, aprendendo?)
STACK = [
    ("FRONT-END", OURO_C, [("HTML5", "html5"), ("CSS3", "css"), ("JavaScript", "javascript"), ("TypeScript", "typescript")]),
    ("FRAMEWORKS", ACO, [("React", "react", 1), ("Vite", "vite"), ("Tailwind CSS", "tailwindcss"), ("Bootstrap", "bootstrap"), ("GSAP", "gsap")]),
    ("BACK-END", OURO_C, [("Node.js", "nodedotjs"), ("PHP", "php"), ("Python", "python"), ("Flask", "flask"), ("Java", "openjdk", 1), ("Spring Boot", "springboot", 1)]),
    ("DATABASE", ACO, [("MySQL", "mysql"), ("Firebase", "firebase")]),
    ("DESIGN & TOOLS", OURO_C, [("Figma", "figma"), ("Git", "git"), ("GitHub", "github")]),
]


def stack():
    T = Texto("s")
    W = 1000
    X0, Y0, LIN = 236, 52, 58
    H = Y0 + LIN * len(STACK) + 12
    corpo, idx = [], 0
    for r, (rotulo, cor, itens) in enumerate(STACK):
        cy = Y0 + r * LIN
        corpo.append(f'<g class="sobe" style="animation-delay:{0.1*r:.1f}s">')
        corpo.append(f'<circle cx="52" cy="{cy}" r="3.2" fill="{cor}"/>')
        corpo.append(T(rotulo, MONO, 10.5, 64, cy + 3.8, 3.2, fill=cor))
        corpo.append(f'<rect x="64" y="{cy+14}" width="{T.medir(rotulo, MONO, 10.5, 3.2):.0f}" height="1" fill="{cor}" opacity=".25"/>')
        x = X0
        for it in itens:
            nome, ic, aprendendo = it[0], it[1], (len(it) > 2)
            tw = T.medir(nome, SANS_M, 13.5, 0.3)
            pw = 16 + 16 + 9 + tw + 16
            ph, py = 34, cy - 17
            borda = (f'stroke="{ACO}" stroke-opacity=".55" stroke-dasharray="3 3"' if aprendendo
                     else f'stroke="{OURO}" stroke-opacity=".26"')
            corpo.append(f'<rect x="{x:.1f}" y="{py}" width="{pw:.1f}" height="{ph}" rx="17" fill="#15141A" {borda}/>')
            corpo.append(f'<rect class="onda" style="animation-delay:{1.2 + idx*0.16:.2f}s" x="{x:.1f}" y="{py}" width="{pw:.1f}" height="{ph}" rx="17" fill="{OURO}" fill-opacity=".07" stroke="{LUZ}" stroke-opacity=".8"/>')
            corpo.append(icone(ic, x + 16, cy - 8, 16, ACO if aprendendo else OURO_C))
            corpo.append(T(nome, SANS_M, 13.5, x + 41, cy + 4.6, 0.3, fill=MARFIM, extra=' fill-opacity=".9"'))
            if aprendendo:
                corpo.append(f'<circle class="pisca" cx="{x+pw-7:.1f}" cy="{py+7}" r="2.6" fill="{ACO}"/>')
            x += pw + 10
            idx += 1
        assert x < W - 30, (rotulo, x)
        corpo.append("</g>")
    # legenda
    ly = H - 22
    corpo.append(f'<rect x="{W-252}" y="{ly-11}" width="26" height="15" rx="7.5" fill="none" stroke="{ACO}" stroke-opacity=".6" stroke-dasharray="3 3"/>')
    corpo.append(f'<circle class="pisca" cx="{W-232}" cy="{ly-7}" r="2.2" fill="{ACO}"/>')
    corpo.append(T("EM APRENDIZADO AGORA", MONO_R, 9.5, W - 216, ly, 2.2, fill=ACO))
    css = """
      .onda { opacity:0; animation: onda 10s ease-in-out infinite }
      @keyframes onda { 0%{opacity:0} 4%{opacity:1} 14%{opacity:0} 100%{opacity:0} }"""
    tudo = f'''<g clip-path="url(#card)">
  {fundo_vidro(W, H, grade=.12, luz=(500, H/2, 420, 160))}
  {"".join(corpo)}
  {borda_vidro(W, H)}
</g>'''
    nomes = ", ".join(it[0] for _, _, its in STACK for it in its)
    return svg(W, H, f"Stack: {nomes}. Em aprendizado: React, Java e Spring Boot.", defs_vidro(W, H) + T.defs(), tudo, css)


# ═════════════════════ COMO TRABALHO ═════════════════════
ETAPAS = [
    ("01", "DESCOBRIR", ["Briefing, contexto e", "requisitos reais do problema."]),
    ("02", "DESENHAR", ["Fluxo, wireframe e UI,", "validados antes do código."]),
    ("03", "CONSTRUIR", ["Front-end e back-end, com o", "mesmo padrão de qualidade."]),
    ("04", "ENTREGAR", ["Deploy, testes e", "refinamento pós-entrega."]),
]


def processo():
    T = Texto("c")
    W, H = 1000, 232
    xs = [140, 380, 620, 860]
    NY = 74
    CICLO, VIAGEM = 8.0, 0.6
    a = []
    a.append(f'<rect x="{xs[0]}" y="{NY-0.5}" width="{xs[-1]-xs[0]}" height="1" fill="{ACO}" opacity=".3"/>')
    for x in range(xs[0], xs[-1] + 1, 24):
        a.append(f'<rect x="{x}" y="{NY+5}" width="1" height="4" fill="{ACO}" opacity=".25"/>')
    a.append(f'<rect class="trilha" x="{xs[0]}" y="{NY-1}" width="{xs[-1]-xs[0]}" height="2" fill="url(#cTrilha)"/>')
    a.append(f'<g class="pulso"><circle cx="{xs[0]}" cy="{NY}" r="9" fill="url(#cFaisca)"/><circle cx="{xs[0]}" cy="{NY}" r="2.2" fill="#fff"/></g>')
    for i, (n, titulo, desc) in enumerate(ETAPAS):
        x = xs[i]
        atraso = CICLO * VIAGEM * i / 3
        a.append(f'<g class="sobe" style="animation-delay:{0.15*i:.2f}s">')
        a.append(f'<circle class="acende" style="animation-delay:{atraso:.2f}s" cx="{x}" cy="{NY}" r="30" fill="{OURO}" filter="url(#neon)"/>')
        a.append(f'<circle cx="{x}" cy="{NY}" r="24" fill="#111015" stroke="{OURO}" stroke-opacity=".3"/>')
        a.append(f'<circle class="acende" style="animation-delay:{atraso:.2f}s" cx="{x}" cy="{NY}" r="24" fill="{OURO}" fill-opacity=".14" stroke="{LUZ}" stroke-width="1.5"/>')
        a.append(em_ouro(T(n, SERIF, 17, x, NY + 6, 0.5, "middle"), x - 20, NY - 12, 40, 24, p="c"))
        a.append(T(titulo, SANS_B, 14, x, NY + 60, 4.2, "middle", fill=MARFIM))
        a.append(f'<rect x="{x-14}" y="{NY+72}" width="28" height="1.5" rx=".75" fill="{ACO if i % 2 else OURO_C}"/>')
        for k, linha in enumerate(desc):
            a.append(T(linha, SANS, 13, x, NY + 96 + k * 19, 0.2, "middle", fill=SUAVE))
        a.append("</g>")
    defs = defs_vidro(W, H) + f'''
    <linearGradient id="cTrilha" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{OURO}" stop-opacity=".2"/><stop offset="1" stop-color="{LUZ}"/>
    </linearGradient>
    <radialGradient id="cFaisca" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="{LUZ}" stop-opacity=".9"/><stop offset="1" stop-color="{OURO}" stop-opacity="0"/>
    </radialGradient>'''
    d = xs[-1] - xs[0]
    v = VIAGEM * 100
    css = f"""
      .pulso {{ animation: pulso {CICLO}s cubic-bezier(.45,0,.55,1) infinite }}
      @keyframes pulso {{ 0%{{transform:translateX(0);opacity:0}} 3%{{opacity:1}} {v:.0f}%{{transform:translateX({d}px);opacity:1}} {v+6:.0f}%,100%{{transform:translateX({d}px);opacity:0}} }}
      .trilha {{ transform-box:fill-box; transform-origin:left; animation: trilha {CICLO}s cubic-bezier(.45,0,.55,1) infinite }}
      @keyframes trilha {{ 0%{{transform:scaleX(0);opacity:1}} {v:.0f}%{{transform:scaleX(1);opacity:1}} 85%,100%{{transform:scaleX(1);opacity:0}} }}
      .acende {{ opacity:0; animation: acende {CICLO}s ease-out infinite }}
      @keyframes acende {{ 0%{{opacity:0}} 3%{{opacity:1}} 30%{{opacity:.35}} 70%,100%{{opacity:0}} }}"""
    tudo = f'''<g clip-path="url(#card)">
  {fundo_vidro(W, H, grade=.1)}
  {"".join(a)}
  {borda_vidro(W, H)}
</g>'''
    label = "Como trabalho: " + "; ".join(f"{n} {t.title()} — {' '.join(d)}" for n, t, d in ETAPAS)
    return svg(W, H, label, defs + T.defs(), tudo, css)


if __name__ == "__main__":
    gravar("stack.svg", stack())
    gravar("processo.svg", processo())
