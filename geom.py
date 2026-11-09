"""Geometry helpers for Squarol: boolean ops on paths via skia-pathops."""
import pathops

K = 0.5523


def _new():
    return pathops.Path()


def rrect(x0, y0, x1, y1, tl=0, tr=0, br=0, bl=0):
    """Rounded rect, independent corner radii."""
    w, h = x1 - x0, y1 - y0
    m = min(w, h) / 2.0
    tl, tr, br, bl = [min(r, m) for r in (tl, tr, br, bl)]
    p = _new()
    p.moveTo(x0 + bl, y0)
    p.lineTo(x1 - br, y0)
    if br:
        p.cubicTo(x1 - br + br * K, y0, x1, y0 + br - br * K, x1, y0 + br)
    p.lineTo(x1, y1 - tr)
    if tr:
        p.cubicTo(x1, y1 - tr + tr * K, x1 - tr + tr * K, y1, x1 - tr, y1)
    p.lineTo(x0 + tl, y1)
    if tl:
        p.cubicTo(x0 + tl - tl * K, y1, x0, y1 - tl + tl * K, x0, y1 - tl)
    p.lineTo(x0, y0 + bl)
    if bl:
        p.cubicTo(x0, y0 + bl - bl * K, x0 + bl - bl * K, y0, x0 + bl, y0)
    p.close()
    return p


def rect(x0, y0, x1, y1):
    return rrect(x0, y0, x1, y1)


def poly(pts):
    p = _new()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    return p


def quad(xb0, xb1, yb, xt0, xt1, yt):
    """Slanted strip: bottom edge xb0..xb1 at yb, top edge xt0..xt1 at yt."""
    return poly([(xb0, yb), (xb1, yb), (xt1, yt), (xt0, yt)])


def ellipse(cx, cy, rx, ry):
    return rrect(cx - rx, cy - ry, cx + rx, cy + ry, rx, rx, rx, rx) if rx == ry else _ell(cx, cy, rx, ry)


def _ell(cx, cy, rx, ry):
    p = _new()
    p.moveTo(cx + rx, cy)
    p.cubicTo(cx + rx, cy + ry * K, cx + rx * K, cy + ry, cx, cy + ry)
    p.cubicTo(cx - rx * K, cy + ry, cx - rx, cy + ry * K, cx - rx, cy)
    p.cubicTo(cx - rx, cy - ry * K, cx - rx * K, cy - ry, cx, cy - ry)
    p.cubicTo(cx + rx * K, cy - ry, cx + rx, cy - ry * K, cx + rx, cy)
    p.close()
    return p


def U(*paths):
    out = _new()
    for p in paths:
        if p is None:
            continue
        out = pathops.op(out, p, pathops.PathOp.UNION)
    return out


def D(a, *bs):
    for b in bs:
        a = pathops.op(a, b, pathops.PathOp.DIFFERENCE)
    return a


def I(a, b):
    return pathops.op(a, b, pathops.PathOp.INTERSECTION)


def X(a, b):
    return pathops.op(a, b, pathops.PathOp.XOR)


def shift(p, dx, dy=0):
    out = _new()
    pen = out.getPen()
    from fontTools.pens.transformPen import TransformPen
    p.draw(TransformPen(pen, (1, 0, 0, 1, dx, dy)))
    return out


def transform(p, m):
    out = _new()
    from fontTools.pens.transformPen import TransformPen
    p.draw(TransformPen(out.getPen(), m))
    return out


def bounds(p):
    return p.bounds  # (xmin, ymin, xmax, ymax)


def clean(p):
    p = U(p)
    p.simplify(fix_winding=True, keep_starting_points=False, clockwise=False)
    return p
