"""Converte texto em <path> usando as fontes reais, para o SVG ficar idêntico em qualquer sistema."""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

_A = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(_A, "fonts") if os.path.isdir(os.path.join(_A, "fonts")) else os.path.join(_A, "..", "fonts")
_cache = {}


def font(name, wght):
    key = (name, wght)
    if key not in _cache:
        f = TTFont(os.path.join(FONTS, name + ".ttf"))
        if "fvar" in f:
            f = instancer.instantiateVariableFont(f, {"wght": wght})
        _cache[key] = f
    return _cache[key]


def _r(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def text(name, wght, s, size, x, y, tracking=0.0, anchor="middle"):
    """Devolve (d, largura). tracking em px entre letras."""
    f = font(name, wght)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = f["head"].unitsPerEm
    k = size / upm
    glyphs = [cmap.get(ord(c), cmap.get(ord("?"))) for c in s]
    width = sum(hmtx[g][0] * k for g in glyphs) + tracking * (len(s) - 1)
    if anchor == "middle":
        cx = x - width / 2
    elif anchor == "end":
        cx = x - width
    else:
        cx = x
    pen = SVGPathPen(gs, ntos=_r)
    for g in glyphs:
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, y)))
        cx += hmtx[g][0] * k + tracking
    return pen.getCommands(), width
