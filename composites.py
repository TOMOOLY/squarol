"""Marks, anchors, and accented composites for Squarol."""
import unicodedata
from fontTools.agl import toUnicode
from geom import clean
import glyphs as GL
import glyphs2 as G2

CAP, XH, ASC = GL.CAP, GL.XH, GL.ASC
GAP = 70  # gap between letter and top mark

COMB = {0x300: "gravecomb", 0x301: "acutecomb", 0x302: "circumflexcomb", 0x303: "tildecomb",
        0x304: "macroncomb", 0x306: "brevecomb", 0x307: "dotaccentcomb", 0x308: "dieresiscomb",
        0x30A: "ringcomb", 0x30B: "hungarumlautcomb", 0x30C: "caroncomb", 0x326: "commaaccentcomb",
        0x327: "cedillacomb", 0x328: "ogonekcomb"}
SPACING = {"grave": ("gravecomb", 0x60), "acute": ("acutecomb", 0xB4), "circumflex": ("circumflexcomb", 0x2C6),
           "caron": ("caroncomb", 0x2C7), "breve": ("brevecomb", 0x2D8), "dotaccent": ("dotaccentcomb", 0x2D9),
           "ring": ("ringcomb", 0x2DA), "tilde": ("tildecomb", 0x2DC), "hungarumlaut": ("hungarumlautcomb", 0x2DD),
           "dieresis": ("dieresiscomb", 0xA8), "macron": ("macroncomb", 0xAF), "cedilla": ("cedillacomb", 0xB8),
           "ogonek": ("ogonekcomb", 0x2DB)}
COMB_UNI = {v: k for k, v in COMB.items()}
ASCENDER_LC = set("bdhklt") | {"thorn", "germandbls"}
CEDILLA_AS_COMMA = set("GKLNRgklnr")


def _bbox(f, name):
    g = f[name]
    return g.getBounds(f) if hasattr(g, "getBounds") else g.getControlBounds(f)


def add(f, uni_for):
    added = []
    # combining marks
    for name, fn in G2.MARKS.items():
        p = clean(fn())
        g = f.newGlyph(name)
        p.draw(g.getPen())
        g.width = 0
        if name in G2.BOTMARKS:
            g.appendAnchor({"name": "_bottom", "x": 0, "y": 0})
        else:
            g.appendAnchor({"name": "_top", "x": 0, "y": 0})
            g.appendAnchor({"name": "top", "x": 0, "y": (p.bounds[3] + GAP) if p.bounds else GAP})
        if name in COMB_UNI:
            g.unicodes = [COMB_UNI[name]]
        added.append(name)

    # anchors on base letters
    for name in list(f.keys()):
        if name in G2.MARKS or len(name) != 1 and name not in ("idotless", "jdotless", "AE", "ae", "OE", "oe"):
            continue
        b = _bbox(f, name)
        if b is None:
            continue
        cx = round((b.xMin + b.xMax) / 2)
        if name.isupper() or name in ("AE", "OE"):
            ty = CAP + GAP
        elif name in ASCENDER_LC and name != "t":
            ty = ASC + GAP
        else:
            ty = XH + GAP
        g = f[name]
        g.appendAnchor({"name": "top", "x": cx, "y": ty})
        g.appendAnchor({"name": "bottom", "x": cx, "y": 0})

    # spacing accents
    for name, (comb, u) in SPACING.items():
        m = f[comb]
        mb = m.getBounds(f)
        w = round(mb.xMax - mb.xMin + 80)
        g = f.newGlyph(name)
        y = 0 if comb in G2.BOTMARKS else XH + GAP
        g.components.append(_comp(comb, w / 2 - (mb.xMin + mb.xMax) / 2, y))
        g.width = w
        g.unicodes = [u]
        added.append(name)

    # nbspace
    g = f.newGlyph("nbspace")
    g.width = f["space"].width
    g.unicodes = [0xA0]
    added.append("nbspace")

    # composites from the GF Latin Core list
    core = [l.strip() for l in open("core.txt") if l.strip() and not l.startswith("#")]
    for name in core:
        if name in f:
            continue
        built = _composite(f, name, uni_for)
        if built:
            u = uni_for(name)
            if u:
                f[name].unicodes = [u]
            added.append(name)
    missing = [n for n in core if n not in f]
    print("missing from core:", missing)
    return added


def _comp(base, x=0, y=0, xx=1, yy=1):
    from ufoLib2.objects import Component
    return Component(baseGlyph=base, transformation=(xx, 0, 0, yy, round(x), round(y)))


def _anchor(f, gname, aname):
    for a in f[gname].anchors:
        if a.name == aname:
            return a.x, a.y
    return None


def _composite(f, name, uni_for):
    special = {"idotaccent": ("idotless", ["dotaccentcomb"]), "Idotaccent": ("I", ["dotaccentcomb"])}
    if name in special:
        base, marks = special[name]
    else:
        cp = uni_for(name)
        if not cp:
            return False
        nfd = unicodedata.normalize("NFD", chr(cp))
        if len(nfd) < 2:
            return False
        base = nfd[0]
        marks = []
        for ch in nfd[1:]:
            mk = COMB.get(ord(ch))
            if not mk:
                return False
            marks.append(mk)
        if base in "ij" and any(m not in G2.BOTMARKS for m in marks):
            base = {"i": "idotless", "j": "jdotless"}[base]
        if base == "i":
            base = "i"
    g = f.newGlyph(name)
    g.components.append(_comp(base))
    g.width = f[base].width
    bb = f[base].getBounds(f)
    stack_y = None
    for mk in marks:
        if mk == "caroncomb" and base in ("d", "l", "t", "L"):
            # vertical caron to the right of the stem
            if base == "L":
                x, y = bb.xMin + GL.S + 30, CAP - 220
            elif base == "t":
                x, y = bb.xMin + 70 + GL.s + 25, 680 - 220
            elif base == "d":
                x, y = bb.xMax + 40, ASC - 220
                g.width += 150
            else:
                x, y = bb.xMin + GL.s + 40, ASC - 220
                g.width += 150
            g.components.append(_comp("caroncomb.alt", x, y))
            continue
        if mk == "cedillacomb" and base in CEDILLA_AS_COMMA:
            if base == "g":
                ax, ay = _anchor(f, base, "top")
                g.components.append(_comp("commaaccentcomb", ax, ay - 240 + 20, -1, -1))
                continue
            mk = "commaaccentcomb"
        if mk == "ogonekcomb":
            g.components.append(_comp(mk, bb.xMax - 170, 0))
            continue
        if mk in G2.BOTMARKS:
            ax, ay = _anchor(f, base, "bottom")
            g.components.append(_comp(mk, ax, ay))
            continue
        ax, ay = _anchor(f, base, "top")
        if stack_y is not None:
            ay = stack_y
        g.components.append(_comp(mk, ax, ay))
        mb = f[mk].getBounds(f)
        stack_y = ay + mb.yMax + 40
    return True
