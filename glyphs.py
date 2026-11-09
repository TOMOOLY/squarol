"""Squarol glyph drawings. Design rule ("leaf corners"): convex corners on the
top-left / bottom-right diagonal are rounded, the other two stay sharp."""
from geom import *

# ---- metrics ---------------------------------------------------------------
CAP, XH, ASC, DSC = 700, 530, 740, -190
S, T = 150, 126          # cap vertical / horizontal stems
s, t = 140, 112          # lowercase stems
R, r = 200, 64           # cap outer / inner corner radius
Rl, rl = 160, 50         # lowercase radii
SB = 46                  # default sidebearing

G = {}                   # name -> (path, lsb, rsb) or callable


def glyph(name, lsb=SB, rsb=SB):
    def deco(fn):
        G[name] = (fn, lsb, rsb)
        return fn
    return deco


# ---- building blocks ---------------------------------------------------------
def ring(x0, y0, x1, y1, tl=0, tr=0, br=0, bl=0, sv=S, sh=T, ri=None):
    """Rounded-rect frame. Inner radius follows outer (0 stays 0)."""
    def inn(o):
        if not o:
            return 0
        return ri if ri is not None else max(o - (sv + sh) / 2.0, 30)
    outer = rrect(x0, y0, x1, y1, tl, tr, br, bl)
    inner = rrect(x0 + sv, y0 + sh, x1 - sv, y1 - sh, inn(tl), inn(tr), inn(br), inn(bl))
    return D(outer, inner)


def diag(x_bot, y_bot, x_top, y_top, w):
    """Stroke whose horizontal cross-section is w wide, centre line given."""
    return quad(x_bot - w / 2, x_bot + w / 2, y_bot, x_top - w / 2, x_top + w / 2, y_top)


def clipbox(p, x0, y0, x1, y1):
    return I(p, rect(x0, y0, x1, y1))


def dw(sv, dx, dy):
    """Horizontal width of a diagonal stroke so its true thickness ~ sv."""
    import math
    L = math.hypot(dx, dy)
    return sv * L / abs(dy) if dy else sv


# =============================================================================
# UPPERCASE
# =============================================================================
@glyph("O")
def _O():
    return ring(0, 0, 640, CAP, tl=R, br=R)


@glyph("Q")
def _Q():
    w = 640
    tail = diag(w - 40, -70, w - 230, 190, 150)
    return U(ring(0, 0, w, CAP, tl=R, br=R), clipbox(tail, w - 330, -90, w + 40, 230))


@glyph("C")
def _C():
    w = 610
    return D(ring(0, 0, w, CAP, tl=R, br=R), rect(w - S - 1, T + 70, w + 1, CAP - T))


@glyph("G")
def _G():
    w = 640
    bar_top = 380
    body = D(ring(0, 0, w, CAP, tl=R, br=R), rect(w - S - 1, bar_top, w + 1, CAP - T))
    return U(body, rect(w * 0.47, bar_top - T, w, bar_top))


@glyph("D")
def _D():
    return ring(0, 0, 630, CAP, tr=R * 0.6, br=R)


@glyph("B")
def _B():
    w = 620
    mid = 395
    up = ring(0, mid - T, w - 40, CAP, tr=110, br=110)
    lo = ring(0, 0, w, mid, br=R * 0.85, tr=110)
    return U(up, lo)


@glyph("E")
def _E():
    w = 560
    body = D(rrect(0, 0, w, CAP, tl=R), rrect(S, T, w + 1, CAP - T, tl=r))
    return U(body, rect(0, CAP / 2 - T / 2, w - 50, CAP / 2 + T / 2))


@glyph("F")
def _F():
    w = 550
    body = D(rrect(0, 0, w, CAP, tl=R), rrect(S, -1, w + 1, CAP - T, tl=r))
    return U(body, rect(0, CAP / 2 - T / 2 - 20, w - 60, CAP / 2 + T / 2 - 20))


@glyph("H")
def _H():
    w = 630
    return U(rect(0, 0, S, CAP), rect(w - S, 0, w, CAP), rect(0, CAP / 2 - T / 2, w, CAP / 2 + T / 2))


@glyph("I")
def _I():
    return rect(0, 0, S, CAP)


@glyph("J")
def _J():
    w = 560
    return D(rrect(0, 0, w, CAP, br=R), rrect(-1, T, w - S, CAP + 1, br=r), rect(-1, 250, S + 1, CAP + 1))


@glyph("K")
def _K():
    w = 610
    dwid = dw(S * 1.02, w - S, CAP / 2)
    up = diag(S + 40, CAP / 2 - 60, w - dwid / 2, CAP, dwid)
    dn = diag(w - dwid / 2, 0, S + 40, CAP / 2 + 60, dwid)
    arms = clipbox(U(up, dn), S - 10, 0, w, CAP)
    return U(rect(0, 0, S, CAP), arms)


@glyph("L")
def _L():
    w = 520
    return D(rrect(0, 0, w, CAP, br=0), rect(S, T, w + 1, CAP + 1))


@glyph("M")
def _M():
    w = 800
    body = D(rrect(0, 0, w, CAP, tl=R), rrect(S, -1, w - S, CAP - T, tl=r))
    return U(body, rect(w / 2 - S / 2, 0, w / 2 + S / 2, CAP - 1))


@glyph("N")
def _N():
    w = 650
    d = dw(S * 1.05, w - 2 * S, CAP)
    dg = clipbox(diag(S + d / 2 - 20, CAP, w - S - d / 2 + 20, 0, d), S - 5, 0, w - S + 5, CAP)
    return U(rect(0, 0, S, CAP), rect(w - S, 0, w, CAP), dg)


@glyph("P")
def _P():
    w = 610
    bowl_bot = 270
    return U(ring(0, bowl_bot, w, CAP, tl=R, br=R * 0.8), rect(0, 0, S, CAP - R))


@glyph("R")
def _R():
    w = 630
    bowl_bot = 300
    bowl = ring(0, bowl_bot, w, CAP, tl=R, br=R * 0.8)
    d = dw(S * 1.05, w - S - 120, bowl_bot + T)
    leg = clipbox(diag(w - d / 2, 0, S + 120, bowl_bot + T, d), S, 0, w, bowl_bot + 1)
    return U(bowl, rect(0, 0, S, CAP - R), leg)



@glyph("S")
def _S():
    w = 600
    m = CAP / 2
    up = D(rrect(0, m - T / 2, w, CAP, tl=R), rrect(S, m + T / 2, w + 1, CAP - T, tl=r))
    lo = D(rrect(0, 0, w, m + T / 2, br=R), rrect(-1, T, w - S, m - T / 2, br=r))
    return U(up, lo)


@glyph("T")
def _T():
    w = 600
    return U(rect(0, CAP - T, w, CAP), rect(w / 2 - S / 2, 0, w / 2 + S / 2, CAP))


@glyph("U")
def _U():
    w = 630
    return D(rrect(0, 0, w, CAP, br=R), rrect(S, T, w - S, CAP + 1, br=r))


def _vshape(w, h, sv, y0=0, apex=None):
    apex = w / 2 if apex is None else apex
    d = dw(sv, w / 2, h)
    left = diag(apex, y0, d / 2, y0 + h, d)
    right = diag(apex, y0, w - d / 2, y0 + h, d)
    return clipbox(U(left, right), 0, y0, w, y0 + h)


@glyph("V")
def _V():
    return _vshape(660, CAP, S)


@glyph("W")
def _W():
    w = 940
    a = _vshape(w / 2 + 70, CAP, S * 0.95)
    b = shift(_vshape(w / 2 + 70, CAP, S * 0.95), w / 2 - 70)
    return U(a, b)


@glyph("X")
def _X():
    w = 640
    d = dw(S, w, CAP)
    return clipbox(U(diag(d / 2, 0, w - d / 2, CAP, d), diag(w - d / 2, 0, d / 2, CAP, d)), 0, 0, w, CAP)


@glyph("Y")
def _Y():
    w = 640
    top = _vshape(w, CAP - 300, S, y0=300)
    return U(top, rect(w / 2 - S / 2, 0, w / 2 + S / 2, 330))


@glyph("Z")
def _Z():
    w = 600
    d = dw(S, w, CAP - 2 * T)
    dg = clipbox(diag(d / 2, T - 5, w - d / 2, CAP - T + 5, d), 0, 0, w, CAP)
    return U(rect(0, CAP - T, w, CAP), rect(0, 0, w, T), dg)


@glyph("A")
def _A():
    w = 640
    bar = 250
    return D(rrect(0, 0, w, CAP, tl=R), rrect(S, bar + T, w - S, CAP - T, tl=r), rect(S, -1, w - S, bar))


# =============================================================================
# LOWERCASE
# =============================================================================
def lring(x0, y0, x1, y1, **k):
    return ring(x0, y0, x1, y1, sv=s, sh=t, **k)


W_l = 530


@glyph("o")
def _o():
    return lring(0, 0, W_l, XH, tl=Rl, br=Rl)


@glyph("c")
def _c():
    w = 500
    return D(lring(0, 0, w, XH, tl=Rl, br=Rl), rect(w - s - 1, t + 55, w + 1, XH - t))


@glyph("e")
def _e():
    w = W_l
    cut = 190
    body = D(lring(0, 0, w, XH, tl=Rl, br=Rl), rect(s, t, w + 1, cut))
    return U(body, rect(s - 1, cut, w, cut + t * 0.95))


@glyph("b")
def _b():
    return U(lring(0, 0, W_l, XH, tl=Rl, br=Rl), rect(0, 0, s, ASC))


@glyph("d")
def _d():
    return U(lring(0, 0, W_l, XH, tl=Rl, br=Rl), rect(W_l - s, 0, W_l, ASC))


@glyph("p")
def _p():
    return U(lring(0, 0, W_l, XH, tl=Rl, br=Rl), rect(0, DSC, s, XH))


@glyph("q")
def _q():
    return U(lring(0, 0, W_l, XH, tl=Rl, br=Rl), rect(W_l - s, DSC, W_l, XH))


@glyph("a")
def _a():
    w = 510
    mid = 300
    outer = rrect(0, 0, w, XH, tl=Rl)
    return D(outer, rect(-1, mid, w - s, XH - t), rrect(s, t, w - s, mid - t, tl=rl))


@glyph("g")
def _g():
    w = W_l
    hook = D(rrect(0, DSC, w, 40, br=Rl), rect(-1, DSC + t, w - s, 41))
    return U(lring(0, 0, w, XH, tl=Rl, br=0), hook)


def _arch(w, h=XH, stems=2):
    body = D(rrect(0, 0, w, h, tl=Rl), rrect(s, -1, w - s, h - t, tl=rl))
    return body


@glyph("n")
def _n():
    return _arch(W_l)


@glyph("h")
def _h():
    return U(_arch(W_l), rect(0, 0, s, ASC))


@glyph("m")
def _m():
    w = 800
    return U(_arch(w), rect(w / 2 - s / 2, 0, w / 2 + s / 2, XH - 1))


@glyph("r")
def _r():
    w = 380
    return D(rrect(0, 0, w, XH, tl=Rl), rrect(s, -1, w + 1, XH - t, tl=rl))


@glyph("u")
def _u():
    return D(rrect(0, 0, W_l, XH, br=Rl), rrect(s, t, W_l - s, XH + 1, br=rl))


@glyph("y")
def _y():
    w = W_l
    body = D(rrect(0, 0, w, XH, bl=0), rrect(s, t, w - s, XH + 1))
    body = D(rrect(0, 0, w, XH, tl=0), rect(s, t, w - s, XH + 1))
    hook = D(rrect(0, DSC, w, 40, br=Rl), rect(-1, DSC + t, w - s, 41))
    return U(body, hook)


@glyph("i")
def _i():
    return U(rect(0, 0, s, XH), rect(0, XH + 70, s, XH + 70 + s))


@glyph("j")
def _j():
    w = 300
    hook = D(rrect(0, DSC, w, XH, br=Rl), rect(-1, DSC + t, w - s, XH + 1))
    return U(hook, rect(w - s, XH + 70, w, XH + 70 + s))


@glyph("l")
def _l():
    return rect(0, 0, s, ASC)


@glyph("k")
def _k():
    w = 500
    d = dw(s * 1.02, w - s, XH / 2)
    up = diag(s + 30, XH / 2 - 50, w - d / 2, XH, d)
    dn = diag(w - d / 2, 0, s + 30, XH / 2 + 50, d)
    return U(rect(0, 0, s, ASC), clipbox(U(up, dn), s - 10, 0, w, XH))


@glyph("f")
def _f():
    w = 400
    body = D(rrect(70, 0, w, ASC, tl=Rl), rrect(70 + s, -1, w + 1, ASC - t, tl=rl))
    return U(body, rect(0, XH - t, w - 30, XH))


@glyph("t")
def _t():
    w = 400
    body = D(rrect(70, 0, w, 680, br=0, bl=0), rect(70 + s, t, w + 1, 681))
    body = D(rrect(70, 0, w, 680, bl=Rl * 0.0), rect(70 + s, t, w + 1, 681))
    return U(body, rect(0, XH - t, w, XH))


@glyph("s")
def _s():
    w = 500
    m = XH / 2
    up = D(rrect(0, m - t / 2, w, XH, tl=Rl), rrect(s, m + t / 2, w + 1, XH - t, tl=rl))
    lo = D(rrect(0, 0, w, m + t / 2, br=Rl), rrect(-1, t, w - s, m - t / 2, br=rl))
    return U(up, lo)


@glyph("v")
def _v():
    return _vshape(560, XH, s)


@glyph("w")
def _w():
    w = 820
    a = _vshape(w / 2 + 60, XH, s * 0.95)
    return U(a, shift(_vshape(w / 2 + 60, XH, s * 0.95), w / 2 - 60))


@glyph("x")
def _x():
    w = 540
    d = dw(s, w, XH)
    return clipbox(U(diag(d / 2, 0, w - d / 2, XH, d), diag(w - d / 2, 0, d / 2, XH, d)), 0, 0, w, XH)


@glyph("z")
def _z():
    w = 500
    d = dw(s, w, XH - 2 * t)
    dg = clipbox(diag(d / 2, t - 5, w - d / 2, XH - t + 5, d), 0, 0, w, XH)
    return U(rect(0, XH - t, w, XH), rect(0, 0, w, t), dg)


# =============================================================================
# FIGURES
# =============================================================================
FW = 560  # tabular-ish figure body width


@glyph("zero")
def _0():
    return ring(0, 0, FW, CAP, tl=R, br=R)


@glyph("one")
def _1():
    return U(rect(FW / 2 - S / 2 + 40, 0, FW / 2 + S / 2 + 40, CAP),
             D(rrect(FW / 2 - 170 + 40, CAP - T - 70, FW / 2 + 40, CAP, tl=110), rect(0, -1, 1, 1)))


@glyph("two")
def _2():
    w = FW
    m = CAP / 2 + 20
    up = D(rrect(0, m - T / 2, w, CAP, tr=0, tl=0), rect(-1, m + T / 2, w - S, CAP - T))
    up = D(rrect(0, m - T / 2, w, CAP, tl=0), rect(-1, m + T / 2, w - S, CAP - T))
    lo = D(rrect(0, 0, w, m + T / 2, bl=0), rect(S, T, w + 1, m - T / 2))
    return U(up, lo)


@glyph("three")
def _3():
    w = FW
    m = CAP / 2
    return U(D(rrect(0, 0, w, CAP, br=R), rrect(-1, T, w - S, CAP - T, br=r)),
             rect(110, m - T / 2, w - 1, m + T / 2))


@glyph("four")
def _4():
    w = FW
    bar = 220
    return U(D(rrect(0, bar, w - 60, CAP, br=0), rect(S, bar + T, w, CAP + 1)),
             rect(w - S - 60, 0, w - 60, CAP), rect(0, bar, w, bar + T))


@glyph("five")
def _5():
    w = FW
    m = CAP / 2 + 30
    up = D(rect(0, m - T / 2, w, CAP), rect(S, m + T / 2, w + 1, CAP - T))
    lo = D(rrect(0, 0, w, m + T / 2, br=R), rrect(-1, T, w - S, m - T / 2, br=r))
    return U(up, lo)


@glyph("six")
def _6():
    w = FW
    m = 410
    lo = ring(0, 0, w, m, br=R * 0.8, tl=0)
    up = D(rrect(0, 0, w, CAP, tl=R), rrect(S, -1, w + 1, CAP - T, tl=r))
    return U(lo, up)


@glyph("seven")
def _7():
    w = FW
    return U(D(rrect(0, 0, w, CAP), rect(-1, -1, w - S, CAP - T)))


@glyph("eight")
def _8():
    w = FW
    m = 380
    return U(ring(30, m - T, w - 30, CAP, tl=150, br=110), ring(0, 0, w, m, tl=110, br=R * 0.85))


@glyph("nine")
def _9():
    w = FW
    m = CAP - 410
    up = ring(0, m, w, CAP, tl=R * 0.8)
    lo = D(rrect(0, 0, w, CAP, br=R), rrect(-1, T, w - S, CAP + 1, br=r))
    return U(up, lo)


# =============================================================================
# PUNCTUATION (basic)
# =============================================================================
DOT = 150


@glyph("period")
def _period():
    return rect(0, 0, DOT, DOT)


@glyph("comma")
def _comma():
    return U(rect(0, 0, DOT, DOT), quad(40, DOT, 0, 40, DOT, 0) if False else poly([(0, -130), (70, -130), (DOT, 0), (DOT, DOT), (40, DOT), (40, 0)]))


@glyph("colon")
def _colon():
    return U(rect(0, 0, DOT, DOT), rect(0, XH - DOT, DOT, XH))


@glyph("semicolon")
def _semicolon():
    return U(_comma(), rect(0, XH - DOT, DOT, XH))


@glyph("exclam")
def _exclam():
    return U(rect(0, 0, DOT, DOT), rect(0, 230, DOT, CAP))


@glyph("question")
def _question():
    w = 520
    top = D(rrect(0, 300, w, CAP, br=R * 0.7), rrect(-1, 300 + T, w - S, CAP - T, br=r))
    return U(top, rect(w / 2 - DOT / 2 - 40, 230, w / 2 + DOT / 2 - 40, 300 + T), rect(w / 2 - DOT / 2 - 40, 0, w / 2 + DOT / 2 - 40, DOT))


@glyph("hyphen")
def _hyphen():
    return rect(0, 270, 330, 270 + T)


@glyph("endash")
def _endash():
    return rect(0, 270, 500, 270 + T)


@glyph("emdash")
def _emdash():
    return rect(0, 270, 1000, 270 + T)


@glyph("underscore")
def _underscore():
    return rect(0, -150, 560, -150 + T)


@glyph("quotesingle")
def _qs():
    return rect(0, CAP - 260, DOT - 10, CAP)


@glyph("quotedbl")
def _qd():
    return U(rect(0, CAP - 260, DOT - 10, CAP), rect(DOT + 60, CAP - 260, 2 * DOT + 50, CAP))


@glyph("slash")
def _slash():
    d = dw(S * 0.9, 380, CAP + 120)
    return clipbox(diag(d / 2, -60, 420 - d / 2, CAP + 60, d), 0, -60, 420, CAP + 60)


@glyph("backslash")
def _backslash():
    d = dw(S * 0.9, 380, CAP + 120)
    return clipbox(diag(420 - d / 2, -60, d / 2, CAP + 60, d), 0, -60, 420, CAP + 60)


@glyph("parenleft")
def _pl():
    return D(rrect(0, -120, 280, CAP + 80, tl=180, bl=180), rrect(S - 10, -120 + T - 10, 281, CAP + 80 - T + 10, tl=70, bl=70))


@glyph("parenright")
def _pr():
    return D(rrect(0, -120, 280, CAP + 80, tr=180, br=180), rrect(-1, -120 + T - 10, 280 - S + 10, CAP + 80 - T + 10, tr=70, br=70))


@glyph("bracketleft")
def _bl():
    return D(rect(0, -120, 260, CAP + 80), rect(S - 10, -120 + T - 10, 261, CAP + 80 - T + 10))


@glyph("bracketright")
def _br():
    return D(rect(0, -120, 260, CAP + 80), rect(-1, -120 + T - 10, 260 - S + 10, CAP + 80 - T + 10))


@glyph("ampersand")
def _amp():
    w = 680
    m = 400
    up = ring(40, m - T, w - 210, CAP, tl=150)
    lo = D(ring(0, 0, w - 110, m, br=R * 0.8), rect(w - 110 - S - 1, T + 90, w, m + 1))
    arm = rect(w - 300, T + 90, w, T + 90 + T)
    return U(up, lo, arm)



@glyph("plus")
def _plus():
    c = 300
    return U(rect(0, c - T / 2, 2 * c - 40, c + T / 2), rect(c - 20 - S / 2, 40, c - 20 + S / 2, 2 * c - 40))


@glyph("equal")
def _equal():
    return U(rect(0, 180, 520, 180 + T), rect(0, 380, 520, 380 + T))


@glyph("asterisk")
def _ast():
    import math
    cx, cy, L, wd = 0, 0, 190, 105
    paths = []
    for ang in (90, 30, 150):
        a = math.radians(ang)
        ex, ey = L * math.cos(a), L * math.sin(a)
        nx, ny = -math.sin(a) * wd / 2, math.cos(a) * wd / 2
        paths.append(poly([(-ex - nx, -ey - ny), (-ex + nx, -ey + ny), (ex + nx, ey + ny), (ex - nx, ey - ny)]))
    return shift(clipbox(U(*paths), -L, -L, L, L), 0, CAP - L)



@glyph("numbersign")
def _hash():
    w = 640
    v = U(rect(150, 0, 150 + S * 0.85, CAP), rect(w - 150 - S * 0.85, 0, w - 150, CAP))
    h = U(rect(0, 200, w, 200 + T * 0.9), rect(0, CAP - 200 - T * 0.9, w, CAP - 200))
    return U(v, h)


@glyph("at")
def _at():
    w = 820
    sv, sh = 110, 100
    outer = D(ring(0, -140, w, CAP, tl=R, sv=sv, sh=sh), rect(w * 0.55, -141, w + 1, 140))
    inner = ring(230, 140, w, CAP - 220, tl=110, sv=sv + 10, sh=sh)
    return U(outer, inner)



@glyph("dollar")
def _dollar():
    sg = _S()
    return U(sg, rect(300 - S / 2 + 20, -90, 300 + S / 2 - 20, CAP + 90))


@glyph("percent")
def _percent():
    a = ring(0, CAP - 300, 240, CAP, tl=90, sv=90, sh=80)
    b = ring(460, 0, 700, 300, br=90, sv=90, sh=80)
    d = dw(S * 0.85, 500, CAP)
    sl = clipbox(diag(100 + d / 2, 0, 600 - d / 2, CAP, d), 100, 0, 600, CAP)
    return U(a, b, sl)


@glyph("space")
def _space():
    return None
