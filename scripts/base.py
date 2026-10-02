"""Base compartilhada de todas as peças do README de Erick Silva.

- paleta (tirada do .ai do logo)
- Texto: converte texto em vetor reaproveitando cada letra (<use>), para os
  arquivos ficarem leves mesmo com muito texto
- moldura de vidro (card) e CSS comum
"""
import os, re
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen

AQUI = os.path.dirname(os.path.abspath(__file__))
# funciona tanto em build/ (desenvolvimento) quanto em scripts/ (dentro do repositório)
FONTES = os.path.join(AQUI, "fonts") if os.path.isdir(os.path.join(AQUI, "fonts")) else os.path.join(AQUI, "..", "fonts")
ICONES = os.path.join(AQUI, "icons") if os.path.isdir(os.path.join(AQUI, "icons")) else os.path.join(AQUI, "..", "icons")
SAIDA = (os.path.join(AQUI, "..", "assets") if os.path.basename(AQUI) == "scripts"
         else os.path.join(AQUI, "..", "repo", "assets"))

# ── paleta ───────────────────────────────────────────────
OBS = "#0A0A0C"
OBS2 = "#121116"
FIO = "#2A2722"
OURO_E = "#BA8529"
OURO = "#D4A24C"
OURO_C = "#E2AE61"
LUZ = "#F5D79A"
MARFIM = "#F5F1E8"
SUAVE = "#A8A6A0"
ACO = "#7FA6C9"
ACO_E = "#4F6F8F"

SERIF = ("Cinzel", 700)
SERIF_R = ("Cinzel", 500)
SANS = ("Jost", 400)
SANS_M = ("Jost", 500)
SANS_B = ("Jost", 600)
MONO = ("JetBrainsMono", 500)
MONO_R = ("JetBrainsMono", 400)

_fontes = {}


def _fonte(nome, peso):
    k = (nome, peso)
    if k not in _fontes:
        f = TTFont(os.path.join(FONTES, nome + ".ttf"))
        if "fvar" in f:
            f = instancer.instantiateVariableFont(f, {"wght": peso})
        _fontes[k] = f
    return _fontes[k]


class Texto:
    """Banco de letras de UMA peça. Cada letra vira um <path> em <defs> uma vez só;
    o texto é feito de <use>. Chamar .defs() no fim para emitir as letras."""

    def __init__(self, prefixo="g"):
        self.p = prefixo
        self.glifos = {}  # (fonte, peso, glyph) -> (id, d)

    def _id(self, fonte, peso, g):
        k = (fonte, peso, g)
        if k not in self.glifos:
            f = _fonte(fonte, peso)
            pen = SVGPathPen(f.getGlyphSet(), ntos=lambda v: str(int(round(v))))
            f.getGlyphSet()[g].draw(pen)
            gid = f"{self.p}{len(self.glifos):x}"
            self.glifos[k] = (gid, pen.getCommands())
        return self.glifos[k][0]

    def medir(self, s, estilo, tam, esp=0.0):
        f = _fonte(*estilo)
        cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
        gs = [cmap.get(ord(c)) or cmap.get(ord("?")) for c in s]
        return sum(hmtx[g][0] for g in gs) * tam / upm + esp * (len(s) - 1)

    def __call__(self, s, estilo, tam, x, y, esp=0.0, ancora="start", fill=None, extra=""):
        """Devolve um <g> com o texto. esp = espaçamento entre letras em px."""
        fonte, peso = estilo
        f = _fonte(fonte, peso)
        cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
        k = tam / upm
        gs = [cmap.get(ord(c)) or cmap.get(ord("?")) for c in s]
        larg = sum(hmtx[g][0] for g in gs) * k + esp * (len(s) - 1)
        x0 = x - larg / 2 if ancora == "middle" else x - larg if ancora == "end" else x
        uses, cx = [], 0.0
        esp_u = esp / k
        for c, g in zip(s, gs):
            if c != " ":
                uses.append(f'<use href="#{self._id(fonte, peso, g)}" x="{int(round(cx))}"/>')
            cx += hmtx[g][0] + esp_u
        fl = f' fill="{fill}"' if fill else ""
        return (f'<g transform="translate({x0:.1f} {y:.1f}) scale({k:.5f} -{k:.5f})"{fl}{extra}>'
                + "".join(uses) + "</g>")

    def defs(self):
        return "".join(f'<path id="{i}" d="{d}"/>' for i, d in self.glifos.values())


def icone(nome, x, y, tam, fill, extra=""):
    """Ícone monocromático (simple-icons, viewBox 24)."""
    svg = open(os.path.join(ICONES, nome + ".svg")).read()
    d = re.search(r' d="([^"]+)"', svg).group(1)
    k = tam / 24
    fr = ' fill-rule="evenodd"' if 'evenodd' in svg else ""
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({k:.4f})" fill="{fill}"{fr} d="{d}"{extra}/>'


def losango(cx, cy, r, fill, extra=""):
    return (f'<path d="M{cx:.1f} {cy-r:.1f}L{cx+r:.1f} {cy:.1f}L{cx:.1f} {cy+r:.1f}L{cx-r:.1f} {cy:.1f}Z" '
            f'fill="{fill}"{extra}/>')


# ── defs comuns ──────────────────────────────────────────
def defs_vidro(W, H, rx=24, p=""):
    return f'''
    <linearGradient id="{p}fundo" x1="0" y1="0" x2=".35" y2="1">
      <stop offset="0" stop-color="{OBS2}"/><stop offset=".55" stop-color="{OBS}"/><stop offset="1" stop-color="#0D0C10"/>
    </linearGradient>
    <radialGradient id="{p}aco" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{ACO}" stop-opacity=".14"/><stop offset="1" stop-color="{ACO}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="{p}ouroAmb" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{OURO}" stop-opacity=".16"/><stop offset="1" stop-color="{OURO}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="{p}fioTopo" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="{LUZ}" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="{p}borda" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{OURO_C}" stop-opacity=".40"/><stop offset=".5" stop-color="{OURO}" stop-opacity=".07"/><stop offset="1" stop-color="{ACO}" stop-opacity=".28"/>
    </linearGradient>
    <linearGradient id="{p}ouro" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{OURO_E}"/><stop offset=".5" stop-color="{OURO_C}"/><stop offset=".65" stop-color="{LUZ}"/><stop offset="1" stop-color="{OURO}"/>
    </linearGradient>
    <linearGradient id="{p}reflexo" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <pattern id="{p}pontos" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r=".85" fill="{ACO}"/></pattern>
    <clipPath id="{p}card"><rect width="{W}" height="{H}" rx="{rx}"/></clipPath>
    <filter id="{p}neon" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>
    <filter id="{p}neonFino" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="2.2"/></filter>'''


def fundo_vidro(W, H, rx=24, p="", grade=.16, luz=None):
    """Camadas de fundo (dentro do clip). luz=(cx,cy,rx,ry) para um halo dourado."""
    halo = (f'<ellipse cx="{luz[0]}" cy="{luz[1]}" rx="{luz[2]}" ry="{luz[3]}" fill="url(#{p}ouroAmb)"/>' if luz else "")
    g = f'<rect width="{W}" height="{H}" fill="url(#{p}pontos)" opacity="{grade}"/>' if grade else ""
    return f'''<rect width="{W}" height="{H}" fill="url(#{p}fundo)"/>{g}
    <ellipse cx="{W*0.08:.0f}" cy="{H}" rx="{W*0.35:.0f}" ry="{H*0.5:.0f}" fill="url(#{p}aco)"/>
    <ellipse cx="{W*0.94:.0f}" cy="0" rx="{W*0.3:.0f}" ry="{H*0.45:.0f}" fill="url(#{p}aco)" opacity=".7"/>{halo}
    <path d="M{W*0.62:.0f} 0 L{W*0.74:.0f} 0 L{W*0.56:.0f} {H} L{W*0.44:.0f} {H} Z" fill="#fff" opacity=".016"/>'''


def borda_vidro(W, H, rx=24, p=""):
    return (f'<rect x="{W*0.08:.0f}" y="0" width="{W*0.84:.0f}" height="1.2" fill="url(#{p}fioTopo)"/>'
            f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{rx-1}" fill="none" stroke="url(#{p}borda)" stroke-width="1.5"/>')


CSS_COMUM = """
      .sobe { animation: sobe 1s cubic-bezier(.2,.7,.3,1) both }
      @keyframes sobe { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
      .surge { animation: surge 1.4s ease both }
      @keyframes surge { from{opacity:0} to{opacity:1} }
      .pisca { animation: pisca 2.6s ease-in-out infinite }
      @keyframes pisca { 0%,100%{opacity:.25} 50%{opacity:1} }
      @media (prefers-reduced-motion: reduce) { *{ animation:none !important } }"""


def svg(W, H, label, defs, corpo, css="", rx=24, p=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">\n'
            f'<defs>{defs}\n<style>{CSS_COMUM}{css}\n</style></defs>\n{corpo}\n</svg>\n')


def gravar(nome, conteudo):
    os.makedirs(SAIDA, exist_ok=True)
    caminho = os.path.join(SAIDA, nome)
    open(caminho, "w").write(conteudo)
    print(f"{nome}: {len(conteudo)/1024:.1f} KB")
    return caminho


_n_grad = [0]


def em_ouro(grupo_texto, x, y, w, h, grad="ouro", p=""):
    """Pinta um texto (vários <use>) com UM gradiente contínuo, via máscara."""
    _n_grad[0] += 1
    mid = f"{p}mo{_n_grad[0]}"
    return (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}">'
            f'<g fill="#fff">{grupo_texto}</g></mask>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{grad})" mask="url(#{mid})"/>')


def logo_pecas():
    """Peças vetoriais do logo (extraídas do .ai original), com precisão de 1 casa."""
    import json
    c = os.path.join(AQUI, "logo.json")
    if not os.path.exists(c):
        c = os.path.join(AQUI, "..", "logo", "pieces.json")
    P = json.load(open(c))
    for p in P:
        p["d"] = re.sub(r"\s+", " ", re.sub(r"-?\d+\.\d+", lambda m: f"{float(m.group(0)):.1f}".rstrip("0").rstrip("."), p["d"])).strip()
    return [P[i]["d"] for i in (10, 11, 12, 13, 5, 6, 8, 9, 4, 3, 1, 2, 0)]   # asas, coroa, águia+S, olho, E
