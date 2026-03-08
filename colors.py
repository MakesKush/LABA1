import numpy as np

_EPS = 1e-12


def split_rgb_channels(rgb):
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError('Ожидается RGB-изображение (H, W, 3).')

    r = np.zeros_like(rgb)
    g = np.zeros_like(rgb)
    b = np.zeros_like(rgb)

    r[:, :, 0] = rgb[:, :, 0]
    g[:, :, 1] = rgb[:, :, 1]
    b[:, :, 2] = rgb[:, :, 2]
    return r, g, b


def rgb_to_hsi(rgb):
    rgb = rgb.astype(np.float64) / 255.0
    r = rgb[:, :, 0]
    g = rgb[:, :, 1]
    b = rgb[:, :, 2]

    intensity = (r + g + b) / 3.0
    min_rgb = np.minimum(np.minimum(r, g), b)
    saturation = 1.0 - (3.0 * min_rgb) / (r + g + b + _EPS)
    saturation = np.where((r + g + b) > _EPS, saturation, 0.0)
    saturation = np.clip(saturation, 0.0, 1.0)

    num = 0.5 * ((r - g) + (r - b))
    den = np.sqrt((r - g) ** 2 + (r - b) * (g - b)) + _EPS
    theta = np.degrees(np.arccos(np.clip(num / den, -1.0, 1.0)))
    hue = np.where(b <= g, theta, 360.0 - theta)
    hue = np.where(saturation <= _EPS, 0.0, hue)
    return hue, saturation, intensity


def hsi_to_rgb(h, s, i):
    h = np.asarray(h, dtype=np.float64) % 360.0
    s = np.clip(np.asarray(s, dtype=np.float64), 0.0, 1.0)
    i = np.clip(np.asarray(i, dtype=np.float64), 0.0, 1.0)

    r = np.zeros_like(i)
    g = np.zeros_like(i)
    b = np.zeros_like(i)

    mask1 = (h >= 0.0) & (h < 120.0)
    mask2 = (h >= 120.0) & (h < 240.0)
    mask3 = ~(mask1 | mask2)

    h1 = np.deg2rad(h[mask1])
    b[mask1] = i[mask1] * (1.0 - s[mask1])
    r[mask1] = i[mask1] * (1.0 + (s[mask1] * np.cos(h1)) / (np.cos(np.deg2rad(60.0) - h1) + _EPS))
    g[mask1] = 3.0 * i[mask1] - (r[mask1] + b[mask1])

    h2 = np.deg2rad(h[mask2] - 120.0)
    r[mask2] = i[mask2] * (1.0 - s[mask2])
    g[mask2] = i[mask2] * (1.0 + (s[mask2] * np.cos(h2)) / (np.cos(np.deg2rad(60.0) - h2) + _EPS))
    b[mask2] = 3.0 * i[mask2] - (r[mask2] + g[mask2])

    h3 = np.deg2rad(h[mask3] - 240.0)
    g[mask3] = i[mask3] * (1.0 - s[mask3])
    b[mask3] = i[mask3] * (1.0 + (s[mask3] * np.cos(h3)) / (np.cos(np.deg2rad(60.0) - h3) + _EPS))
    r[mask3] = 3.0 * i[mask3] - (g[mask3] + b[mask3])

    out = np.stack([r, g, b], axis=2)
    return np.clip(np.round(out * 255.0), 0, 255).astype(np.uint8)


def intensity_to_gray(intensity):
    return np.clip(np.round(intensity * 255.0), 0, 255).astype(np.uint8)


def invert_intensity_in_rgb(rgb):
    h, s, i = rgb_to_hsi(rgb)
    inverted = 1.0 - i
    return intensity_to_gray(i), hsi_to_rgb(h, s, inverted)
