#!/usr/bin/env python3
"""Princípio do dia — alterna um princípio de DESIGN (ouro) e um de ENGENHARIA (aço).
Roda toda madrugada pela GitHub Action e regrava assets/principio.svg.
Uso: python3 principio.py [indice]   (sem índice = escolhe pela data de hoje)"""
import sys, datetime
from base import *

try:
    from zoneinfo import ZoneInfo
    AGORA = datetime.datetime.now(ZoneInfo("America/Sao_Paulo"))
except Exception:
    AGORA = datetime.datetime.utcnow() - datetime.timedelta(hours=3)

W, H = 1000, 300
BX, BY, BW, BH = 640, 40, 308, 220   # área da ilustração
T = Texto("q")
s_aco = f'stroke="{ACO}" fill="none"'


def rot(txt, x, y, cor=ACO, tam=8, anc="middle", op=".8"):
    return T(txt, MONO_R, tam, x, y, 0.8, anc, fill=cor, extra=f' fill-opacity="{op}"')


# ═══════════════════════ ILUSTRAÇÕES ═══════════════════════
# cada uma desenha em coordenadas locais 0..308 × 0..220 e devolve (svg, css)

def fitts():
    g = [f'<rect x="232" y="30" width="34" height="18" rx="5" {s_aco} stroke-opacity=".5"/>',
         rot("PEQUENO E LONGE", 249, 62, op=".55", tam=7),
         f'<path d="M48 176 C110 170 170 160 196 146" {s_aco} stroke-opacity=".4" stroke-dasharray="3 4"/>',
         f'<rect class="fAnel" x="138" y="116" width="128" height="48" rx="24" fill="none" stroke="{LUZ}"/>',
         f'<rect x="138" y="116" width="128" height="48" rx="24" fill="url(#ouro)"/>',
         T("AÇÃO PRINCIPAL", SANS_B, 10, 202, 144, 2, "middle", fill=OBS),
         f'<g class="fCursor"><path d="M0 0 L0 17 L4.5 13 L7.5 20 L10 19 L7 12.5 L13 12.5Z" fill="{MARFIM}" stroke="{OBS}" stroke-width="1"/></g>',
         rot("T = a + b · log2(D/W + 1)", 154, 204, tam=8.5)]
    css = """
      .fCursor { animation: fCursor 4.5s cubic-bezier(.2,.8,.2,1) infinite }
      @keyframes fCursor { 0%,12%{transform:translate(42px,170px)} 42%{transform:translate(194px,138px)} 48%{transform:translate(194px,138px) scale(.85)} 54%,100%{transform:translate(194px,138px)} }
      .fAnel { transform-box:fill-box; transform-origin:center; opacity:0; animation: fAnel 4.5s ease-out infinite }
      @keyframes fAnel { 0%,44%{opacity:0;transform:scale(1)} 46%{opacity:.9} 70%,100%{opacity:0;transform:scale(1.35)} }"""
    return "".join(g), css


def hick():
    g = []
    for i in range(8):
        y = 18 + i * 15
        g.append(f'<path d="M30 70 C60 70 60 {y} 104 {y}" {s_aco} stroke-opacity=".55"/><circle cx="108" cy="{y}" r="3" fill="{ACO}" opacity=".7"/>')
    g.append(f'<circle cx="28" cy="70" r="5" fill="{ACO}"/>')
    for y in (40, 70, 100):
        g.append(f'<path d="M190 70 C220 70 220 {y} 262 {y}" stroke="{OURO_C}" fill="none"/><circle cx="266" cy="{y}" r="4" fill="{OURO_C}"/>')
    g.append(f'<circle cx="188" cy="70" r="5" fill="{OURO_C}"/>')
    g += [rot("8 OPÇÕES", 14, 162, anc="start"), f'<rect x="80" y="155" width="200" height="8" rx="4" fill="{ACO}" opacity=".12"/>',
          f'<rect class="hLento" x="80" y="155" width="200" height="8" rx="4" fill="{ACO}" opacity=".7"/>',
          rot("3 OPÇÕES", 14, 186, OURO_C, anc="start"), f'<rect x="80" y="179" width="200" height="8" rx="4" fill="{OURO}" opacity=".12"/>',
          f'<rect class="hRapido" x="80" y="179" width="74" height="8" rx="4" fill="url(#ouro)"/>',
          rot("TEMPO DE DECISÃO", 154, 212, op=".5", tam=7)]
    css = """
      .hLento { transform-box:fill-box; transform-origin:left; animation: hLento 5s ease-in-out infinite }
      @keyframes hLento { 0%{transform:scaleX(0)} 70%,90%{transform:scaleX(1)} 100%{transform:scaleX(0)} }
      .hRapido { transform-box:fill-box; transform-origin:left; animation: hRapido 5s ease-out infinite }
      @keyframes hRapido { 0%{transform:scaleX(0)} 22%,90%{transform:scaleX(1)} 100%{transform:scaleX(0)} }"""
    return "".join(g), css


def jakob():
    g = []
    for k, (x, rot_txt) in enumerate([(12, "OUTROS SITES"), (162, "O SEU SITE")]):
        g.append(f'<rect x="{x}" y="22" width="134" height="160" rx="8" fill="#111015" stroke="{ACO if k==0 else OURO}" stroke-opacity=".4"/>')
        g.append(f'<circle cx="{x+10}" cy="32" r="2" fill="{ACO}" opacity=".6"/><circle cx="{x+17}" cy="32" r="2" fill="{ACO}" opacity=".4"/>')
        g.append(f'<rect x="{x+10}" y="44" width="28" height="10" rx="2" fill="{ACO if k==0 else OURO_C}" opacity=".7"/>')
        for j in range(3):
            g.append(f'<rect x="{x+76+j*16}" y="48" width="11" height="2" rx="1" fill="{MARFIM}" opacity=".4"/>')
        g.append(f'<rect x="{x+10}" y="66" width="114" height="56" rx="4" fill="{ACO}" opacity=".1"/>')
        g.append(f'<rect x="{x+10}" y="130" width="80" height="3" rx="1.5" fill="{MARFIM}" opacity=".3"/><rect x="{x+10}" y="138" width="60" height="3" rx="1.5" fill="{MARFIM}" opacity=".2"/>')
        g.append(f'<rect x="{x+10}" y="152" width="44" height="14" rx="7" fill="{ACO if k==0 else OURO}" opacity=".75"/>')
        g.append(rot(rot_txt, x + 67, 202, ACO if k == 0 else OURO_C, tam=7.5))
        for n, (ex, ey, ew, eh) in enumerate([(6, 40, 36, 18), (70, 42, 58, 14), (6, 148, 52, 22)]):
            g.append(f'<rect class="jLuz" style="animation-delay:{n*1.4:.1f}s" x="{x+ex}" y="{ey}" width="{ew}" height="{eh}" rx="4" fill="none" stroke="{LUZ}" stroke-width="1.4"/>')
    css = """
      .jLuz { opacity:0; animation: jLuz 4.2s ease-in-out infinite }
      @keyframes jLuz { 0%{opacity:0} 8%,26%{opacity:1} 36%,100%{opacity:0} }"""
    return "".join(g), css


def miller():
    dig = "419827635"
    soltos = [22 + i * 30 for i in range(9)]
    grupos = [36 + (i // 3) * 92 + (i % 3) * 22 for i in range(9)]
    g, css = [], ["""
      @keyframes mJunta { 0%,20%{transform:translateX(0)} 45%,85%{transform:translateX(var(--d))} 100%{transform:translateX(0)} }
      .mD { animation: mJunta 6s cubic-bezier(.6,0,.3,1) infinite }
      .mChave { opacity:0; animation: mChave 6s ease infinite }
      @keyframes mChave { 0%,40%{opacity:0} 50%,82%{opacity:1} 95%,100%{opacity:0} }
      .mSolto { animation: mSolto 6s ease infinite }
      @keyframes mSolto { 0%,22%{opacity:1} 32%,90%{opacity:0} 100%{opacity:1} }"""]
    for i, c in enumerate(dig):
        g.append(f'<g class="mD" style="--d:{grupos[i]-soltos[i]}px">{T(c, MONO, 24, soltos[i], 96, 0, "middle", fill=MARFIM)}</g>')
    for k in range(3):
        x0 = grupos[k * 3] - 12
        g.append(f'<path class="mChave" d="M{x0} 112 v8 h68 v-8" stroke="{OURO_C}" fill="none"/>')
        g.append(f'<g class="mChave">{rot(["DDD", "PREFIXO", "FINAL"][k], x0+34, 136, OURO_C, tam=7)}</g>')
    g.append(f'<g class="mSolto">{rot("9 ITENS SOLTOS", 154, 136, op=".6", tam=7)}</g>')
    g.append(rot("A MEMÓRIA DE CURTO PRAZO GUARDA ~7 ± 2", 154, 190, tam=7.5))
    return "".join(g), "".join(css)


def restorff():
    g = []
    for i in range(12):
        x, y = 40 + (i % 4) * 60, 26 + (i // 4) * 56
        if i == 6:
            g.append(f'<rect class="rPulsa" x="{x-4}" y="{y-4}" width="48" height="48" rx="10" fill="{OURO}" opacity=".5" filter="url(#neonFino)"/>')
            g.append(f'<rect x="{x}" y="{y}" width="40" height="40" rx="8" fill="url(#ouro)"/>')
            g.append(losango(x + 20, y + 20, 7, OBS))
        else:
            g.append(f'<rect x="{x}" y="{y}" width="40" height="40" rx="8" fill="#141319" stroke="{ACO}" stroke-opacity=".35"/>')
            g.append(f'<circle cx="{x+20}" cy="{y+20}" r="5" fill="none" stroke="{ACO}" stroke-opacity=".45"/>')
    g.append(rot("O DIFERENTE É O QUE SE LEMBRA", 154, 204, tam=7.5))
    css = """
      .rPulsa { transform-box:fill-box; transform-origin:center; animation: rPulsa 2.8s ease-in-out infinite }
      @keyframes rPulsa { 0%,100%{opacity:.25;transform:scale(.92)} 50%{opacity:.8;transform:scale(1.12)} }"""
    return "".join(g), css


def proximidade():
    g = []
    for i in range(12):
        c, r = i % 6, i // 6
        x0, y0 = 34 + c * 48, 70 + r * 48
        grupo = c // 2
        x1 = 52 + grupo * 102 + (c % 2) * 26
        y1 = 80 + r * 26
        cor = [OURO_C, ACO, MARFIM][grupo]
        g.append(f'<circle class="pP" style="--dx:{x1-x0}px;--dy:{y1-y0}px" cx="{x0}" cy="{y0}" r="8" fill="{cor}" opacity=".85"/>')
    for k in range(3):
        g.append(f'<rect class="pBorda" x="{52+k*102-18}" y="62" width="62" height="62" rx="14" fill="none" stroke="{LUZ}" stroke-opacity=".6" stroke-dasharray="3 3"/>')
    g.append(rot("PERTO = RELACIONADO", 154, 196, tam=7.5))
    css = """
      .pP { animation: pP 6s cubic-bezier(.6,0,.3,1) infinite }
      @keyframes pP { 0%,18%{transform:translate(0,0)} 42%,84%{transform:translate(var(--dx),var(--dy))} 100%{transform:translate(0,0)} }
      .pBorda { opacity:0; animation: pB 6s ease infinite }
      @keyframes pB { 0%,40%{opacity:0} 50%,80%{opacity:1} 90%,100%{opacity:0} }"""
    return "".join(g), css


def doherty():
    g = [rot("> 400 ms", 16, 62, anc="start", tam=8.5),
         f'<rect x="90" y="54" width="190" height="10" rx="5" fill="{ACO}" opacity=".12"/>',
         f'<rect class="dLento" x="90" y="54" width="190" height="10" rx="5" fill="{ACO}" opacity=".6"/>',
         f'<g class="dGira"><circle cx="292" cy="59" r="6" fill="none" stroke="{ACO}" stroke-width="1.6" stroke-dasharray="20 18"/></g>',
         rot("< 400 ms", 16, 112, OURO_C, anc="start", tam=8.5),
         f'<rect x="90" y="104" width="190" height="10" rx="5" fill="{OURO}" opacity=".12"/>',
         f'<rect class="dRapido" x="90" y="104" width="190" height="10" rx="5" fill="url(#ouro)"/>',
         f'<path class="dOk" d="M286 109 l4 4 l8 -9" stroke="{LUZ}" stroke-width="2" fill="none" stroke-linecap="round"/>',
         f'<circle class="dClique" cx="154" cy="160" r="14" fill="none" stroke="{LUZ}"/>',
         f'<rect x="114" y="148" width="80" height="24" rx="12" fill="#16141B" stroke="{OURO}" stroke-opacity=".5"/>',
         T("CLIQUE", SANS_B, 9, 154, 163.5, 2, "middle", fill=OURO_C),
         rot("RESPOSTA RÁPIDA MANTÉM O FLUXO", 154, 204, tam=7.5)]
    css = """
      .dLento { transform-box:fill-box; transform-origin:left; animation: dLento 5s linear infinite }
      @keyframes dLento { 0%,10%{transform:scaleX(0)} 92%{transform:scaleX(1)} 100%{transform:scaleX(0)} }
      .dRapido { transform-box:fill-box; transform-origin:left; animation: dRapido 5s ease-out infinite }
      @keyframes dRapido { 0%,10%{transform:scaleX(0)} 20%,92%{transform:scaleX(1)} 100%{transform:scaleX(0)} }
      .dOk { opacity:0; animation: dOk 5s ease infinite }
      @keyframes dOk { 0%,20%{opacity:0} 24%,90%{opacity:1} 100%{opacity:0} }
      .dGira { transform-box:fill-box; transform-origin:center; animation: dGira 1s linear infinite }
      @keyframes dGira { to{transform:rotate(360deg)} }
      .dClique { transform-box:fill-box; transform-origin:center; opacity:0; animation: dClique 5s ease-out infinite }
      @keyframes dClique { 0%,6%{opacity:0;transform:scale(.6)} 8%{opacity:1} 20%,100%{opacity:0;transform:scale(2.2)} }"""
    return "".join(g), css


def _eng(x, y, cor):
    return (f'<circle cx="{x}" cy="{y}" r="7" fill="none" stroke="{cor}" stroke-width="1.6"/>'
            f'<circle cx="{x}" cy="{y}" r="2.4" fill="{cor}"/>'
            + "".join(f'<rect x="{x-1.5}" y="{y-11}" width="3" height="4" fill="{cor}" transform="rotate({a} {x} {y})"/>' for a in range(0, 360, 60)))


def _db(x, y, cor):
    return (f'<ellipse cx="{x}" cy="{y-7}" rx="9" ry="3.5" fill="none" stroke="{cor}" stroke-width="1.5"/>'
            f'<path d="M{x-9} {y-7} V{y+7} A9 3.5 0 0 0 {x+9} {y+7} V{y-7}" fill="none" stroke="{cor}" stroke-width="1.5"/>'
            f'<path d="M{x-9} {y} A9 3.5 0 0 0 {x+9} {y}" fill="none" stroke="{cor}" stroke-width="1.2"/>')


def _env(x, y, cor):
    return (f'<rect x="{x-10}" y="{y-7}" width="20" height="14" rx="2" fill="none" stroke="{cor}" stroke-width="1.5"/>'
            f'<path d="M{x-10} {y-6} L{x} {y+1} L{x+10} {y-6}" fill="none" stroke="{cor}" stroke-width="1.5"/>')


def srp():
    g = [f'<g class="sA"><rect x="64" y="34" width="180" height="120" rx="12" fill="#141319" stroke="{ACO}" stroke-opacity=".6"/>'
         + _eng(110, 80, ACO) + _db(160, 104, ACO) + _env(200, 74, ACO)
         + f'<path d="M110 80 L160 104 L200 74 L110 80" stroke="{ACO}" stroke-opacity=".35" fill="none" stroke-dasharray="2 3"/>'
         + rot("UserManager", 154, 140, tam=8) + "</g>"]
    nomes = ["Auth", "Repository", "Mailer"]
    icones = [_eng, _db, _env]
    for k in range(3):
        x = 18 + k * 98
        g.append(f'<g class="sB" style="animation-delay:{k*0.12:.2f}s"><rect x="{x}" y="54" width="78" height="80" rx="10" fill="#16141B" stroke="{OURO}" stroke-opacity=".55"/>'
                 + icones[k](x + 39, 86, OURO_C) + rot(nomes[k], x + 39, 122, OURO_C, tam=7.5) + "</g>")
    g.append(rot("UMA CLASSE, UM MOTIVO PARA MUDAR", 154, 196, tam=7.5))
    css = """
      .sA { animation: sA 6s ease-in-out infinite }
      @keyframes sA { 0%,30%{opacity:1;transform:scale(1)} 40%,90%{opacity:0;transform:scale(.94)} 100%{opacity:1} }
      .sB { transform-box:fill-box; transform-origin:center; opacity:0; animation: sB 6s cubic-bezier(.2,.8,.3,1) infinite }
      @keyframes sB { 0%,34%{opacity:0;transform:translateY(10px) scale(.9)} 46%,86%{opacity:1;transform:translateY(0) scale(1)} 94%,100%{opacity:0} }"""
    return "".join(g), css


def dry():
    g = []
    for k in range(3):
        y = 18 + k * 58
        g.append(f'<g class="yCopia"><rect x="14" y="{y}" width="108" height="44" rx="6" fill="#141319" stroke="{ACO}" stroke-opacity=".5"/>'
                 f'<rect x="24" y="{y+12}" width="70" height="3" rx="1.5" fill="{ACO}" opacity=".6"/>'
                 f'<rect x="24" y="{y+21}" width="52" height="3" rx="1.5" fill="{ACO}" opacity=".4"/>'
                 f'<rect x="24" y="{y+30}" width="62" height="3" rx="1.5" fill="{ACO}" opacity=".4"/></g>')
        g.append(f'<g class="yRef"><rect x="14" y="{y+12}" width="70" height="20" rx="10" fill="none" stroke="{ACO}" stroke-opacity=".6" stroke-dasharray="3 3"/>'
                 + rot("use()", 49, y + 25, tam=8) + "</g>")
        g.append(f'<path class="ySeta" pathLength="1" d="M86 {y+22} C150 {y+22} 150 105 186 105" stroke="{LUZ}" fill="none" stroke-dasharray="1" />')
    g.append(f'<g class="yUnica"><rect x="186" y="80" width="108" height="50" rx="8" fill="#17151D" stroke="{OURO_C}"/>'
             f'<rect x="198" y="94" width="70" height="3" rx="1.5" fill="{OURO_C}"/><rect x="198" y="103" width="52" height="3" rx="1.5" fill="{OURO_C}" opacity=".6"/>'
             f'<rect x="198" y="112" width="62" height="3" rx="1.5" fill="{OURO_C}" opacity=".6"/></g>')
    g.append(rot("UMA FONTE DA VERDADE", 154, 208, tam=7.5))
    css = """
      .yCopia { animation: yCopia 6s ease infinite }
      @keyframes yCopia { 0%,25%{opacity:1} 35%,90%{opacity:0} 100%{opacity:1} }
      .yRef { opacity:0; animation: yRef 6s ease infinite }
      @keyframes yRef { 0%,30%{opacity:0} 40%,88%{opacity:1} 96%,100%{opacity:0} }
      .yUnica { opacity:0; animation: yUnica 6s ease infinite }
      @keyframes yUnica { 0%,28%{opacity:0;transform:translateX(-12px)} 38%,90%{opacity:1;transform:translateX(0)} 100%{opacity:0} }
      .ySeta { stroke-dashoffset:1; animation: ySeta 6s ease-in-out infinite }
      @keyframes ySeta { 0%,40%{stroke-dashoffset:1} 55%,88%{stroke-dashoffset:0} 96%,100%{stroke-dashoffset:1} }"""
    return "".join(g), css


def kiss():
    confuso = "M34 110 C60 20 90 190 120 70 S170 30 150 150 S90 170 200 60 S250 200 274 110"
    g = [f'<path class="kConf" pathLength="1" d="{confuso}" stroke="{ACO}" stroke-width="1.5" fill="none" stroke-dasharray="1"/>',
         f'<path class="kReto" pathLength="1" d="M34 110 H274" stroke="url(#ouro)" stroke-width="3" fill="none" stroke-dasharray="1" stroke-linecap="round"/>',
         f'<circle cx="34" cy="110" r="7" fill="{OBS}" stroke="{MARFIM}"/>', rot("A", 34, 132, MARFIM, tam=8),
         f'<circle cx="274" cy="110" r="7" fill="{OBS}" stroke="{OURO_C}"/>', rot("B", 274, 132, OURO_C, tam=8),
         rot("O CAMINHO SIMPLES É O QUE SOBREVIVE", 154, 196, tam=7.5)]
    css = """
      .kConf { stroke-dashoffset:1; animation: kConf 6s ease-in-out infinite }
      @keyframes kConf { 0%{stroke-dashoffset:1;opacity:1} 34%{stroke-dashoffset:0;opacity:1} 44%{opacity:1} 56%,100%{stroke-dashoffset:0;opacity:.12} }
      .kReto { stroke-dashoffset:1; animation: kReto 6s cubic-bezier(.6,0,.3,1) infinite }
      @keyframes kReto { 0%,42%{stroke-dashoffset:1} 58%,92%{stroke-dashoffset:0} 100%{stroke-dashoffset:1} }"""
    return "".join(g), css


def yagni():
    itens = [("login", 1), ("dark mode v3", 0), ("busca", 1), ("IA preditiva", 0), ("checkout", 1), ("blockchain", 0)]
    g = []
    for i, (nome, essencial) in enumerate(itens):
        x, y = 22 + (i % 2) * 140, 24 + (i // 2) * 52
        tw = T.medir(nome, SANS_M, 12, 0.2) + 30
        if essencial:
            g.append(f'<rect x="{x}" y="{y}" width="{tw:.0f}" height="30" rx="15" fill="{OURO}" fill-opacity=".14" stroke="{OURO_C}"/>')
            g.append(T(nome, SANS_M, 12, x + 15, y + 19.5, 0.2, fill=MARFIM))
        else:
            g.append(f'<g class="yaFora" style="animation-delay:{i*0.25:.2f}s"><rect x="{x}" y="{y}" width="{tw:.0f}" height="30" rx="15" fill="none" stroke="{ACO}" stroke-opacity=".6" stroke-dasharray="3 3"/>'
                     + T(nome, SANS_M, 12, x + 15, y + 19.5, 0.2, fill=ACO) + "</g>")
            g.append(f'<rect class="yaRisco" style="animation-delay:{i*0.25:.2f}s" x="{x+8}" y="{y+14.5}" width="{tw-16:.0f}" height="1.4" fill="{LUZ}"/>')
    g.append(rot("SÓ O QUE É PRECISO AGORA", 154, 196, tam=7.5))
    css = """
      .yaRisco { transform-box:fill-box; transform-origin:left; animation: yaRisco 6s ease-in-out infinite }
      @keyframes yaRisco { 0%,20%{transform:scaleX(0);opacity:1} 34%,80%{transform:scaleX(1);opacity:1} 92%,100%{transform:scaleX(1);opacity:0} }
      .yaFora { animation: yaFora 6s ease infinite }
      @keyframes yaFora { 0%,30%{opacity:1} 42%,84%{opacity:.22} 100%{opacity:1} }"""
    return "".join(g), css


def camadas():
    nomes = [("INTERFACE", OURO_C), ("REGRAS DE NEGÓCIO", MARFIM), ("DADOS", ACO)]
    g = []
    for k, (n, cor) in enumerate(nomes):
        y = 18 + k * 58
        g.append(f'<rect x="54" y="{y}" width="200" height="40" rx="8" fill="#141319" stroke="{cor}" stroke-opacity=".45"/>')
        g.append(f'<rect class="cLuz" style="animation-delay:{[0,0.75,1.5][k]}s" x="54" y="{y}" width="200" height="40" rx="8" fill="{OURO}" fill-opacity=".1" stroke="{LUZ}"/>')
        g.append(T(n, MONO, 9, 154, y + 23.5, 2, "middle", fill=cor))
    g.append(f'<rect x="270" y="38" width="1" height="116" fill="{ACO}" opacity=".3"/>')
    g.append(f'<g class="cReq"><circle cx="270" cy="38" r="6" fill="{LUZ}" filter="url(#neonFino)"/><circle cx="270" cy="38" r="2.5" fill="#fff"/></g>')
    g.append(rot("CADA CAMADA COM SEU PAPEL", 154, 204, tam=7.5))
    css = """
      .cReq { animation: cReq 6s cubic-bezier(.5,0,.5,1) infinite }
      @keyframes cReq { 0%{transform:translateY(0)} 25%{transform:translateY(116px)} 30%{transform:translateY(116px)} 55%{transform:translateY(0)} 100%{transform:translateY(0)} }
      .cLuz { opacity:0; animation: cLuz 6s ease infinite }
      @keyframes cLuz { 0%{opacity:0} 4%{opacity:1} 16%{opacity:0} 100%{opacity:0} }"""
    return "".join(g), css


def falhe():
    xs = [34, 114, 194, 274]
    nomes = ["ENTRADA", "VALIDA", "PROCESSA", "SALVA"]
    g = [f'<path d="M34 90 H274" stroke="{ACO}" stroke-opacity=".3" stroke-dasharray="3 4"/>']
    for k, x in enumerate(xs):
        cor = OURO_C if k == 1 else ACO
        g.append(f'<circle cx="{x}" cy="90" r="16" fill="#141319" stroke="{cor}" stroke-opacity="{.8 if k < 2 else .35}"/>')
        g.append(rot(nomes[k], x, 126, cor, tam=7, op=".8" if k < 2 else ".4"))
    g.append(f'<circle class="fvBola" cx="34" cy="90" r="5" fill="{MARFIM}"/>')
    g.append(f'<g class="fvErro"><circle cx="114" cy="90" r="16" fill="{OURO}" fill-opacity=".2" stroke="{LUZ}" stroke-width="1.5"/>'
             f'<path d="M108 84 L120 96 M120 84 L108 96" stroke="{LUZ}" stroke-width="2" stroke-linecap="round"/></g>')
    g.append(f'<g class="fvMsg"><rect x="64" y="146" width="100" height="22" rx="11" fill="{OURO}" fill-opacity=".14" stroke="{OURO}" stroke-opacity=".6"/>'
             + rot("ERRO DETECTADO CEDO", 114, 160, OURO_C, tam=6.8) + "</g>")
    g.append(rot("PARE NO PRIMEIRO SINAL DE PROBLEMA", 154, 204, tam=7.5))
    css = """
      .fvBola { animation: fvBola 4.5s cubic-bezier(.5,0,.6,1) infinite }
      @keyframes fvBola { 0%{transform:translateX(0);opacity:1} 30%{transform:translateX(64px);opacity:1} 36%,100%{transform:translateX(64px);opacity:0} }
      .fvErro { opacity:0; animation: fvErro 4.5s ease infinite }
      @keyframes fvErro { 0%,30%{opacity:0} 34%,85%{opacity:1} 100%{opacity:0} }
      .fvMsg { opacity:0; animation: fvMsg 4.5s ease infinite }
      @keyframes fvMsg { 0%,36%{opacity:0;transform:translateY(6px)} 44%,85%{opacity:1;transform:translateY(0)} 100%{opacity:0} }"""
    return "".join(g), css


def aberto():
    g = [f'<rect x="114" y="54" width="80" height="80" rx="12" fill="#17151D" stroke="{OURO_C}"/>',
         f'<rect x="141" y="88" width="26" height="20" rx="3" fill="url(#ouro)"/>',
         f'<path d="M146 88 v-6 a8 8 0 0 1 16 0 v6" stroke="{OURO_C}" stroke-width="2.4" fill="none"/>',
         rot("NÚCLEO", 154, 150, OURO_C, tam=7.5),
         f'<rect x="108" y="84" width="6" height="20" rx="2" fill="{OURO_C}" opacity=".6"/>',
         f'<rect x="194" y="84" width="6" height="20" rx="2" fill="{OURO_C}" opacity=".6"/>']
    for lado, (x, dx) in enumerate([(30, -40), (214, 40)]):
        g.append(f'<g class="oExt" style="--dx:{dx}px;animation-delay:{lado*0.3}s">'
                 f'<rect x="{x}" y="70" width="64" height="48" rx="8" fill="#141319" stroke="{ACO}" stroke-dasharray="3 3"/>'
                 f'<rect x="{x+ (64 if lado==0 else -6)}" y="86" width="6" height="16" rx="2" fill="{ACO}"/>'
                 + rot("EXTENSÃO", x + 32, 98, ACO, tam=7) + "</g>")
    g.append(rot("ABERTO PARA EXTENSÃO, FECHADO PARA MUDANÇA", 154, 196, tam=7.2))
    css = """
      .oExt { animation: oExt 5s cubic-bezier(.5,0,.3,1) infinite }
      @keyframes oExt { 0%,10%{transform:translateX(var(--dx));opacity:0} 30%,80%{transform:translateX(0);opacity:1} 95%,100%{transform:translateX(var(--dx));opacity:0} }"""
    return "".join(g), css


# ═══════════════════════ CONTEÚDO ═══════════════════════
DESIGN = [
    ("LEI DE FITTS", fitts,
     "O tempo para alcançar um alvo depende da distância até ele e do seu tamanho.",
     "Ações importantes: grandes e perto de onde o olhar e o cursor já estão."),
    ("LEI DE HICK", hick,
     "Quanto mais opções, mais tempo a pessoa leva para decidir.",
     "Reduza escolhas por tela e destaque o caminho recomendado."),
    ("LEI DE JAKOB", jakob,
     "As pessoas passam a maior parte do tempo em outros sites e esperam que o seu funcione igual.",
     "Inove na experiência, não nos padrões que todo mundo já aprendeu."),
    ("LEI DE MILLER", miller,
     "A memória de curto prazo guarda poucos itens de uma vez, em torno de sete.",
     "Agrupe informações em blocos: telefones, cartões, menus, etapas."),
    ("EFEITO VON RESTORFF", restorff,
     "Entre itens parecidos, o que é diferente é o que fica na memória.",
     "Use o destaque com parcimônia: se tudo brilha, nada brilha."),
    ("LEI DA PROXIMIDADE", proximidade,
     "Elementos próximos uns dos outros são percebidos como um grupo.",
     "Espaçamento é informação: aproxime o que é relacionado."),
    ("LIMIAR DE DOHERTY", doherty,
     "A produtividade dispara quando o sistema responde em menos de 400 ms.",
     "Dê feedback imediato e use estados otimistas enquanto o servidor trabalha."),
]
ENG = [
    ("RESPONSABILIDADE ÚNICA", srp,
     "Cada módulo deve ter um, e apenas um, motivo para mudar.",
     "Separe autenticação, persistência e notificação em peças distintas."),
    ("DRY", dry,
     "Don't Repeat Yourself: cada conhecimento tem uma única representação no sistema.",
     "Extraia o que se repete para uma função ou componente compartilhado."),
    ("KISS", kiss,
     "Keep It Simple: a solução mais simples que resolve o problema costuma ser a melhor.",
     "Código claro hoje é manutenção barata amanhã."),
    ("YAGNI", yagni,
     "You Aren't Gonna Need It: não construa o que ainda não é necessário.",
     "Entregue o essencial, meça, e só então expanda."),
    ("SEPARAÇÃO DE CAMADAS", camadas,
     "Interface, regras de negócio e dados vivem em camadas com papéis bem definidos.",
     "Trocar o banco ou o framework não deveria reescrever o sistema inteiro."),
    ("FALHE RÁPIDO", falhe,
     "Detecte erros o mais cedo possível, perto de onde eles nascem.",
     "Valide na entrada e interrompa antes que o dado ruim se espalhe."),
    ("ABERTO / FECHADO", aberto,
     "Entidades devem estar abertas para extensão e fechadas para modificação.",
     "Adicione comportamento com novas peças, sem mexer no núcleo estável."),
]
TODOS = [x for par in zip(DESIGN, ENG) for x in par]   # alterna design / engenharia


def quebrar(texto, estilo, tam, largura):
    linhas, atual = [], ""
    for p in texto.split():
        t = (atual + " " + p).strip()
        if T.medir(t, estilo, tam, 0.1) > largura and atual:
            linhas.append(atual); atual = p
        else:
            atual = t
    return linhas + [atual]


def gerar(indice):
    titulo, arte, desc, pratica = TODOS[indice]
    design = indice % 2 == 0
    cat, cor = ("DESIGN", OURO_C) if design else ("ENGENHARIA", ACO)
    a = []
    L = 52
    a.append(losango(L + 4, 56, 4, OURO_C))
    a.append(T("PRINCÍPIO DO DIA", MONO, 10.5, L + 18, 60, 3.4, fill=OURO_C))
    cw = T.medir(cat, MONO, 9, 2.4) + 22
    a.append(f'<rect x="{L+196}" y="45" width="{cw:.0f}" height="20" rx="10" fill="{cor}" fill-opacity=".1" stroke="{cor}" stroke-opacity=".55"/>')
    a.append(T(cat, MONO, 9, L + 196 + cw / 2, 58.5, 2.4, "middle", fill=cor))
    a.append(T(AGORA.strftime("%d.%m.%Y"), MONO_R, 9.5, 600, 60, 1.6, "end", fill=SUAVE))
    tam = 34
    while T.medir(titulo, SERIF, tam, 1.2) > 540:
        tam -= 1
    a.append(em_ouro(T(titulo, SERIF, tam, L, 112, 1.2), L - 2, 112 - tam, 560, tam + 10, p="q"))
    a.append(f'<rect class="cresce" x="{L}" y="128" width="56" height="2" rx="1" fill="url(#ouro)"/>')
    y = 160
    for l in quebrar(desc, SANS, 16, 540):
        a.append(T(l, SANS, 16, L, y, 0.1, fill=MARFIM, extra=' fill-opacity=".9"'))
        y += 23
    y += 8
    a.append(f'<rect x="{L}" y="{y-12}" width="2" height="{len(quebrar(pratica, SANS, 13.5, 510))*20}" fill="{cor}" opacity=".7"/>')
    for l in quebrar(pratica, SANS, 13.5, 510):
        a.append(T(l, SANS, 13.5, L + 14, y, 0.1, fill=SUAVE))
        y += 20
    a.append(f'<circle class="pisca" cx="{L+3}" cy="{H-33}" r="2.4" fill="{OURO_C}"/>')
    a.append(T(f"ATUALIZADO AUTOMATICAMENTE TODA MADRUGADA  ·  {indice+1:02d}/{len(TODOS)}",
               MONO_R, 8.5, L + 14, H - 30, 1.8, fill=SUAVE, extra=' fill-opacity=".7"'))

    arte_svg, arte_css = arte()
    box = (f'<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="14" fill="#0E0D12" stroke="{OURO}" stroke-opacity=".18"/>'
           f'<rect x="{BX+30}" y="{BY}" width="{BW-60}" height="1" fill="url(#fioTopo)"/>'
           f'<g transform="translate({BX} {BY})">{arte_svg}</g>')
    css = arte_css + """
      .cresce { transform-box:fill-box; transform-origin:left; animation: cresce 1.1s cubic-bezier(.2,.7,.3,1) .4s both }
      @keyframes cresce { from{transform:scaleX(0)} to{transform:scaleX(1)} }"""
    corpo = f'''<g clip-path="url(#card)">
  {fundo_vidro(W, H, grade=.1, luz=(250, 120, 360, 200))}
  <g class="sobe">{"".join(a)}</g>
  <g class="surge" style="animation-delay:.3s">{box}</g>
  {borda_vidro(W, H)}
</g>'''
    label = f"Princípio do dia ({cat.lower()}): {titulo.title()}. {desc} Na prática: {pratica}"
    return svg(W, H, label, defs_vidro(W, H) + T.defs(), corpo, css)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        idx = int(sys.argv[1]) % len(TODOS)
    else:
        idx = AGORA.date().toordinal() % len(TODOS)
    gravar("principio.svg", gerar(idx))
    print("princípio:", TODOS[idx][0])
