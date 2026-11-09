"""Squarol: extended Latin letters, symbols, and marks."""
from geom import *
from glyphs import *
import glyphs as _g

ROT = lambda p: transform(p, (-1, 0, 0, -1, 0, 0))
MIRX = lambda p: transform(p, (-1, 0, 0, 1, 0, 0))

# ---------------------------------------------------------------- marks
# Marks are drawn centred on x=0. Top marks sit on y=0 upwards;
# bottom marks hang from y=0 downwards.
MT = 105  # mark stroke


def _acute():
    return quad(-100, 10, 0, 10, 120, 170)


MARKS = {
    "gravecomb": lambda: MIRX(_acute()),
    "acutecomb": _acute,
    "circumflexcomb": lambda: U(quad(-200, -200 + 130, 0, -55, 75, 160), quad(200 - 130, 200, 0, -75, 55, 160)),
    "caroncomb": lambda: U(quad(-55, 75, 0, -200, -70, 160), quad(-75, 55, 0, 70, 200, 160)),
    "brevecomb": lambda: D(rrect(-170, 0, 170, 160, br=70), rect(-170 + MT, MT * 0.85, 170 - MT, 161)),
    "dotaccentcomb": lambda: rect(-70, 0, 70, 140),
    "dieresiscomb": lambda: U(rect(-185, 0, -45, 140), rect(45, 0, 185, 140)),
    "ringcomb": lambda: ring(-130, 0, 130, 220, tl=80, br=80, sv=90, sh=80, ri=25),
    "tildecomb": lambda: U(rect(-190, 0, -100, 150), rect(-190, 70, 20, 150), rect(-20, 0, 190, 80), rect(100, 0, 190, 150)),
    "macroncomb": lambda: rect(-170, 0, 170, 100),
    "hungarumlautcomb": lambda: U(shift(_acute(), -95), shift(_acute(), 105)),
    "cedillacomb": lambda: U(rect(-50, -90, 50, 10), D(rrect(-150, -250, 50, -60, br=80), rect(-151, -250 + 90, -50, -59))),
    "ogonekcomb": lambda: D(rrect(-50, -240, 170, 10, bl=80), rect(50, -240 + 90, 171, 11)),
    "commaaccentcomb": lambda: poly([(-75, -260), (5, -260), (75, -110), (75, -40), (-65, -40), (-65, -110), (-20, -110)]),
    "caroncomb.alt": lambda: quad(0, 110, 0, 50, 160, 220),
}
TOPMARKS = ["gravecomb", "acutecomb", "circumflexcomb", "caroncomb", "brevecomb", "dotaccentcomb",
            "dieresiscomb", "ringcomb", "tildecomb", "macroncomb", "hungarumlautcomb"]
BOTMARKS = ["cedillacomb", "ogonekcomb", "commaaccentcomb"]

# ---------------------------------------------------------------- letters


@glyph("idotless")
def _idl():
    return rect(0, 0, s, XH)


@glyph("jdotless")
def _jdl():
    w = 300
    return D(rrect(0, DSC, w, XH, br=Rl), rect(-1, DSC + t, w - s, XH + 1))


@glyph("AE")
def _AE():
    a = D(rrect(0, 0, 900, CAP, tl=R), rrect(S, 250 + T, 1000, CAP - T, tl=r), rect(S, -1, 1000, 250))
    e = U(rect(470, 0, 470 + S, CAP), rect(470, 0, 900, T), rect(470, CAP / 2 - T / 2, 860, CAP / 2 + T / 2))
    return U(D(a, rect(470 + S, T, 901, CAP / 2 - T / 2), rect(470 + S, CAP / 2 + T / 2, 901, CAP - T)), e)


@glyph("ae")
def _ae():
    a = _g.G["a"][0]()
    e = shift(_g.G["e"][0](), 510 - s)
    return U(a, e)


@glyph("OE")
def _OE():
    o = D(rrect(0, 0, 560, CAP, tl=R), rrect(S, T, 560 - S + 1, CAP - T, tl=r))
    e = U(rect(410, 0, 900, T), rect(410, CAP - T, 900, CAP), rect(410, CAP / 2 - T / 2, 860, CAP / 2 + T / 2), rect(410, 0, 410 + S, CAP))
    return U(o, e)


@glyph("oe")
def _oe():
    o = _g.G["o"][0]()
    e = shift(_g.G["e"][0](), W_l - s)
    return U(o, e)


@glyph("Oslash")
def _Oslash():
    w = 640
    d = dw(S * 0.7, w + 60, CAP + 80)
    sl = clipbox(diag(-30 + d / 2, -40, w + 30 - d / 2, CAP + 40, d), -30, -40, w + 30, CAP + 40)
    return U(ring(0, 0, w, CAP, tl=R, br=R), sl)


@glyph("oslash")
def _oslash():
    w = W_l
    d = dw(s * 0.7, w + 60, XH + 60)
    sl = clipbox(diag(-30 + d / 2, -30, w + 30 - d / 2, XH + 30, d), -30, -30, w + 30, XH + 30)
    return U(_g.G["o"][0](), sl)


def _crossbar(x0, x1, y, th=None):
    th = th or T * 0.85
    return rect(x0, y - th / 2, x1, y + th / 2)


@glyph("Eth")
def _Eth():
    return U(shift(_g.G["D"][0](), 70), _crossbar(0, 300, CAP / 2))


@glyph("Dcroat", 46, 46)
def _Dcroat():
    return _Eth()


@glyph("dcroat")
def _dcroat():
    return U(_g.G["d"][0](), _crossbar(W_l - s - 120, W_l + 60, ASC - 90, t * 0.8))


@glyph("Hbar")
def _Hbar():
    return U(shift(_g.G["H"][0](), 50), _crossbar(0, 730, CAP - 150))


@glyph("hbar")
def _hbar():
    return U(shift(_g.G["h"][0](), 60), _crossbar(0, 60 + s + 160, ASC - 100, t * 0.8))


@glyph("Lslash")
def _Lslash():
    L = shift(_g.G["L"][0](), 70)
    d = dw(T * 0.8, 260, 220)
    return U(L, clipbox(diag(d / 2, 260, 330 - d / 2, 480, d), 0, 260, 330, 480))


@glyph("lslash")
def _lslash():
    l = shift(rect(0, 0, s, ASC), 110)
    d = dw(t * 0.8, 260, 220)
    return U(l, clipbox(diag(d / 2, 260, 360 - d / 2, 480, d), 0, 260, 360, 480))


@glyph("Thorn")
def _Thorn():
    w = 610
    return U(ring(0, 140, w, CAP - 140, tl=0, br=R * 0.7), rect(0, 0, S, CAP))


@glyph("thorn")
def _thorn():
    return U(lring(0, 0, W_l, XH, tl=Rl, br=Rl), rect(0, DSC, s, ASC))


@glyph("eth")
def _eth():
    o = lring(0, 0, W_l, XH + 60, tl=Rl, br=Rl)
    stem = rect(W_l - s, 0, W_l, ASC)
    bar = _crossbar(W_l - s - 140, W_l + 40, ASC - 110, t * 0.8)
    return D(U(o, stem, bar), rect(-1, XH + 60 - t + 1, W_l - s, XH + 61), rect(-1, XH - 100, s, XH + 61))


@glyph("germandbls")
def _gdbl():
    w = 540
    body = D(rrect(0, 0, w, ASC, tl=Rl), rrect(s, -1, w + 1, ASC - t, tl=rl))
    up = ring(0, 330, w - 40, ASC, tr=0, br=100, sv=s, sh=t)
    lo = D(rrect(0, 0, w, 330 + t, br=Rl), rrect(-1, t, w - s, 330, br=rl))
    return U(rect(0, 0, s, ASC - Rl), D(U(up, lo), rect(-1, -1, s, ASC + 1)), D(rrect(0, 0, w - 40, ASC, tl=Rl), rect(s, -1, w, ASC - t)))


@glyph("Germandbls")
def _Gdbl():
    w = 640
    return U(rect(0, 0, S, CAP - R), D(rrect(0, 0, w, CAP, tl=R, br=R), rrect(S, T, w - S, CAP - T, tl=r, br=r), rect(-1, -1, S, CAP - R)),
             rect(S, 290, w - S, 290 + T))


@glyph("ordfeminine")
def _ordf():
    a = transform(_g.G["a"][0](), (0.62, 0, 0, 0.62, 0, 300))
    return U(a, rect(0, 220, 320, 220 + 70))


@glyph("ordmasculine")
def _ordm():
    o = transform(_g.G["o"][0](), (0.62, 0, 0, 0.62, 0, 300))
    return U(o, rect(0, 220, 330, 220 + 70))


# ---------------------------------------------------------------- symbols
@glyph("cent")
def _cent():
    c = _g.G["c"][0]()
    return U(c, rect(230, -90, 230 + s * 0.75, XH + 90))


@glyph("sterling")
def _sterling():
    w = 560
    body = D(rrect(60, 0, w, CAP, tl=R), rrect(60 + S, T, w + 1, CAP - T, tl=r))
    return U(body, rect(0, 300, 420, 300 + T * 0.9))


@glyph("yen")
def _yen():
    y = _g.G["Y"][0]()
    return U(y, rect(70, 180, 570, 180 + T * 0.8), rect(70, 330, 570, 330 + T * 0.8))


@glyph("euro")
def _euro():
    c = shift(_g.G["C"][0](), 80)
    return U(c, rect(0, 220, 470, 220 + T * 0.8), rect(0, 390, 470, 390 + T * 0.8))


@glyph("section")
def _section():
    w = 500
    a = transform(_g.G["S"][0](), (0.83, 0, 0, 0.62, 0, 300))
    b = transform(_g.G["S"][0](), (0.83, 0, 0, 0.62, 0, -40))
    return U(a, b)


@glyph("paragraph")
def _para():
    w = 560
    return U(rrect(0, 300, w - 120, CAP, tl=R * 0.8), rect(w - 250, -120, w - 250 + 110, CAP), rect(w - 110, -120, w, CAP), rect(w - 250, CAP - T, w, CAP))


def _circled(letter):
    w = 820
    outer = ring(0, -40, w, CAP + 40, tl=R + 40, br=R + 40, sv=80, sh=75)
    inner = transform(_g.G[letter][0](), (0.55, 0, 0, 0.55, 0, 0))
    xmin, ymin, xmax, ymax = inner.bounds
    inner = shift(inner, w / 2 - (xmin + xmax) / 2, (CAP / 2) - (ymin + ymax) / 2)
    return U(outer, inner)


@glyph("copyright")
def _copy():
    return _circled("C")


@glyph("registered")
def _reg():
    return transform(_circled("R"), (0.55, 0, 0, 0.55, 0, CAP * 0.45))


@glyph("trademark")
def _tm():
    tt = transform(_g.G["T"][0](), (0.45, 0, 0, 0.45, 0, CAP * 0.55))
    mm = transform(_g.G["M"][0](), (0.45, 0, 0, 0.45, 300, CAP * 0.55))
    return U(tt, mm)


@glyph("degree")
def _deg():
    return ring(0, CAP - 280, 280, CAP, tl=110, br=110, sv=95, sh=90, ri=30)


@glyph("multiply")
def _mul():
    w = 460
    d = dw(T, w, w)
    return clipbox(U(diag(d / 2, 60, w - d / 2, 60 + w, d), diag(w - d / 2, 60, d / 2, 60 + w, d)), 0, 60, w, 60 + w)


@glyph("divide")
def _div():
    return U(rect(0, 290 - T / 2 + 20, 520, 290 + T / 2 + 20), rect(190, 60, 330, 190), rect(190, 450, 330, 580))


@glyph("minus")
def _minus():
    return rect(0, 310 - T / 2, 520, 310 + T / 2)


def _angle(w, h, y0, th):
    d = dw(th, w, h / 2)
    up = diag(d / 2, y0 + h / 2, w - d / 2, y0 + h, d)
    dn = diag(w - d / 2, y0, d / 2, y0 + h / 2, d)
    return clipbox(U(up, dn), 0, y0, w, y0 + h)


@glyph("less")
def _less():
    return _angle(470, 520, 50, T)


@glyph("greater")
def _greater():
    return MIRX(_angle(470, 520, 50, T))


@glyph("asciicircum")
def _circ():
    return U(quad(0, 140, 300, 170, 310, CAP), quad(480, 620, 300, 310, 450, CAP))


@glyph("asciitilde")
def _atilde():
    return shift(transform(MARKS["tildecomb"](), (1.4, 0, 0, 1, 0, 0)), 0, 230)


@glyph("bar")
def _bar():
    return rect(0, -180, S * 0.8, CAP + 120)


@glyph("braceleft")
def _bcl():
    w = 320
    top = D(rrect(100, 340, w, CAP + 80, tl=150), rrect(100 + S * 0.85, 340 - 1, w + 1, CAP + 80 - T, tl=50))
    bot = D(rrect(100, -120, w, 300, bl=150), rrect(100 + S * 0.85, -120 + T, w + 1, 301, bl=50))
    return U(top, bot, rect(0, 260, 100 + S * 0.85, 380))


@glyph("braceright")
def _bcr():
    return MIRX(_bcl())


@glyph("exclamdown")
def _exd():
    return shift(ROT(_g.G["exclam"][0]()), 0, XH)


@glyph("questiondown")
def _qd():
    return shift(ROT(_g.G["question"][0]()), 0, XH)


def _chev(w, h, th):
    return MIRX(_angle(w, h, 60, th))


@glyph("guilsinglleft")
def _gsl():
    return _angle(300, 400, 70, T * 0.9)


@glyph("guilsinglright")
def _gsr():
    return MIRX(_angle(300, 400, 70, T * 0.9))


@glyph("guillemetleft")
def _gl():
    return U(_angle(300, 400, 70, T * 0.9), shift(_angle(300, 400, 70, T * 0.9), 230))


@glyph("guillemetright")
def _gr():
    return MIRX(_gl())


def _qmark():
    return U(rect(0, CAP - 140, DOT, CAP), poly([(0, CAP - 140), (DOT, CAP - 140), (DOT, CAP - 140), (70, CAP - 270), (0, CAP - 270)]))


@glyph("quoteright")
def _qr():
    return _qmark()


@glyph("quoteleft")
def _ql():
    return shift(ROT(_qmark()), 0, 2 * CAP - 270)


@glyph("quotesinglbase")
def _qsb():
    return _g.G["comma"][0]()


@glyph("quotedblright")
def _qdr():
    return U(_qmark(), shift(_qmark(), DOT + 60))


@glyph("quotedblleft")
def _qdl():
    return U(_ql(), shift(_ql(), DOT + 60))


@glyph("quotedblbase")
def _qdb():
    c = _g.G["comma"][0]()
    return U(c, shift(c, DOT + 60))


@glyph("bullet")
def _bullet():
    return rrect(0, 200, 240, 440, tl=80, br=80)


@glyph("ellipsis")
def _ell():
    return U(rect(0, 0, DOT, DOT), rect(DOT + 90, 0, 2 * DOT + 90, DOT), rect(2 * DOT + 180, 0, 3 * DOT + 180, DOT))


@glyph("periodcentered")
def _pc():
    return rect(0, 250, DOT, 250 + DOT)


@glyph("periodcentered.loclCAT")
def _pccat():
    return rect(0, 250, DOT, 250 + DOT)


@glyph("periodcentered.loclCAT.case")
def _pccatc():
    return rect(0, 300, DOT, 300 + DOT)


@glyph(".notdef", 50, 50)
def _notdef():
    return D(rect(0, 0, 500, CAP), rect(70, 70, 430, CAP - 70))
