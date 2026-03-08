import numpy as np


def _resample_by_scale(image, scale, method='bilinear'):
    if scale <= 0:
        raise ValueError('Коэффициент должен быть положительным.')

    h, w = image.shape[:2]
    out_w = max(1, int(round(w * scale)))
    out_h = max(1, int(round(h * scale)))

    x = (np.arange(out_w, dtype=np.float64) + 0.5) / scale - 0.5
    y = (np.arange(out_h, dtype=np.float64) + 0.5) / scale - 0.5

    if method == 'nearest':
        xi = np.clip(np.rint(x).astype(np.int64), 0, w - 1)
        yi = np.clip(np.rint(y).astype(np.int64), 0, h - 1)
        return image[np.ix_(yi, xi)].copy()

    if method != 'bilinear':
        raise ValueError('Метод должен быть nearest или bilinear.')

    x = np.clip(x, 0.0, w - 1.0)
    y = np.clip(y, 0.0, h - 1.0)
    x0 = np.floor(x).astype(np.int64)
    y0 = np.floor(y).astype(np.int64)
    x1 = np.clip(x0 + 1, 0, w - 1)
    y1 = np.clip(y0 + 1, 0, h - 1)

    dx = (x - x0).reshape(1, out_w, 1)
    dy = (y - y0).reshape(out_h, 1, 1)

    tl = image[np.ix_(y0, x0)].astype(np.float64)
    tr = image[np.ix_(y0, x1)].astype(np.float64)
    bl = image[np.ix_(y1, x0)].astype(np.float64)
    br = image[np.ix_(y1, x1)].astype(np.float64)

    top = (1.0 - dx) * tl + dx * tr
    bottom = (1.0 - dx) * bl + dx * br
    out = (1.0 - dy) * top + dy * bottom
    return np.clip(np.rint(out), 0, 255).astype(np.uint8)


def upsample(image, m, method='bilinear'):
    return _resample_by_scale(image, float(m), method)


def decimate(image, n):
    return image[::n, ::n].copy()


def rational_resample_two_pass(image, m, n, method='bilinear'):
    return decimate(upsample(image, m, method), n)


def rational_resample_one_pass(image, m, n, method='bilinear'):
    return _resample_by_scale(image, m / n, method)
