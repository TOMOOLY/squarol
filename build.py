"""Build Squarol UFO from glyphs.py (+ composites.py if present)."""
import sys, importlib
import ufoLib2
from fontTools.agl import toUnicode
from geom import clean, shift
import glyphs as GL
import glyphs2  # registers extended glyphs

FAMILY = "Squarol"
VERSION = (1, 0)
OUT = "sources/Squarol-Regular.ufo"


def uni_for(name):
    special = {"nbspace": 0x00A0, "space": 0x20, "minus": 0x2212, "euro": 0x20AC,
               "periodcentered": 0x00B7, "idotaccent": None, "caroncomb.alt": None,
               "Germandbls": 0x1E9E, "guillemetleft": 0xAB, "guillemetright": 0xBB,
               "idotless": 0x131, "jdotless": 0x237, "Tcommaaccent": 0x21A, "tcommaaccent": 0x21B,
               "Scommaaccent": 0x218, "scommaaccent": 0x219}
    if name in special:
        return special[name]
    if "." in name:
        return None
    u = toUnicode(name)
    if len(u) == 1:
        return ord(u)
    return None


def make_font():
    f = ufoLib2.Font()
    i = f.info
    i.familyName = FAMILY
    i.styleName = "Regular"
    i.versionMajor, i.versionMinor = VERSION
    i.unitsPerEm = 1000
    i.capHeight = GL.CAP
    i.xHeight = GL.XH
    i.ascender = 950
    i.descender = -250
    i.copyright = "Copyright 2026 The Squarol Project Authors (https://github.com/TOMOOLY/squarol)"
    i.openTypeNameDesigner = "tom"
    i.openTypeNameLicense = ("This Font Software is licensed under the SIL Open Font License, Version 1.1. "
                             "This license is available with a FAQ at: https://openfontlicense.org")
    i.openTypeNameLicenseURL = "https://openfontlicense.org"
    i.openTypeOS2WeightClass = 400
    i.openTypeOS2VendorID = "NONE"
    i.openTypeOS2Type = []
    i.openTypeOS2TypoAscender = 950
    i.openTypeOS2TypoDescender = -250
    i.openTypeOS2TypoLineGap = 0
    i.openTypeHheaAscender = 950
    i.openTypeHheaDescender = -250
    i.openTypeHheaLineGap = 0
    i.openTypeOS2WinAscent = 1000
    i.openTypeOS2WinDescent = 300
    i.openTypeOS2Selection = [7]  # USE_TYPO_METRICS
    i.postscriptUnderlinePosition = -150
    i.postscriptUnderlineThickness = 80
    return f


def add_drawn(f):
    order = []
    for name, (fn, lsb, rsb) in GL.G.items():
        p = fn()
        g = f.newGlyph(name)
        if p is None:
            g.width = 260 if name == "space" else 500
        else:
            p = clean(p)
            xmin, ymin, xmax, ymax = p.bounds
            p = shift(p, lsb - xmin)
            p = clean(p)
            p.draw(g.getPen())
            g.width = round(xmax - xmin + lsb + rsb)
        u = uni_for(name)
        if u:
            g.unicodes = [u]
        order.append(name)
    return order


def main():
    f = make_font()
    order = add_drawn(f)
    try:
        comp = importlib.import_module("composites")
        order += comp.add(f, uni_for)
    except ModuleNotFoundError:
        pass
    f.glyphOrder = [".notdef"] + [n for n in order if n != ".notdef"] if ".notdef" in f else order
    f.save(OUT, overwrite=True)
    print("glyphs:", len(f))


if __name__ == "__main__":
    main()
