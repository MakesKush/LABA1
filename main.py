from pathlib import Path

from colors import invert_intensity_in_rgb, rgb_to_hsi, split_rgb_channels
from helpers import ensure_output_dir, load_rgb_image, normalize_input_path, save_gray_image, save_rgb_image
from sampling import decimate, rational_resample_one_pass, rational_resample_two_pass, upsample


def ask_int(prompt, default):
    while True:
        raw = input(f'{prompt} [{default}]: ').strip()
        if raw == '':
            return default
        try:
            value = int(raw)
            if value > 0:
                return value
        except ValueError:
            pass
        print('Введите положительное целое число.')


def ask_method(default='bilinear'):
    while True:
        raw = input(f'Метод интерполяции (nearest/bilinear) [{default}]: ').strip().lower()
        if raw == '':
            return default
        if raw in {'nearest', 'bilinear'}:
            return raw
        print('Введите nearest или bilinear.')


def ask_input_image():
    default_path = Path('input_demo.png')
    while True:
        raw = input(f'Путь к изображению [{default_path}]: ')
        value = normalize_input_path(raw)
        if value == '':
            return default_path
        path = Path(value).expanduser()
        if path.exists() and path.is_file():
            return path
        print('Файл не найден. Проверь путь и попробуй ещё раз.')


def run():
    print('Лабораторная работа №1: Цветовые модели и передискретизация')
    print('Если на первом вопросе нажать Enter, будет использовано input_demo.png')
    print()

    input_path = ask_input_image()
    out_dir = ensure_output_dir(input('Папка для результатов [out]: ').strip() or 'out')
    m = ask_int('Во сколько раз растянуть изображение (M)', 2)
    n = ask_int('Во сколько раз сжать изображение (N)', 3)
    method = ask_method('bilinear')

    rgb = load_rgb_image(input_path)
    save_rgb_image(out_dir / '01_original.png', rgb)

    r, g, b = split_rgb_channels(rgb)
    save_rgb_image(out_dir / '02_r_channel.png', r)
    save_rgb_image(out_dir / '03_g_channel.png', g)
    save_rgb_image(out_dir / '04_b_channel.png', b)

    _, _, intensity = rgb_to_hsi(rgb)
    save_gray_image(out_dir / '05_hsi_intensity.png', (intensity * 255.0).round())

    _, inverted_rgb = invert_intensity_in_rgb(rgb)
    save_rgb_image(out_dir / '06_inverted_intensity.png', inverted_rgb)

    save_rgb_image(out_dir / f'07_upsample_x{m}_{method}.png', upsample(rgb, m, method))
    save_rgb_image(out_dir / f'08_decimate_x{n}.png', decimate(rgb, n))
    save_rgb_image(out_dir / f'09_resample_two_pass_{m}over{n}_{method}.png', rational_resample_two_pass(rgb, m, n, method))
    save_rgb_image(out_dir / f'10_resample_one_pass_{m}over{n}_{method}.png', rational_resample_one_pass(rgb, m, n, method))

    print()
    print('Готово. Результаты сохранены в:')
    print(out_dir.resolve())


if __name__ == '__main__':
    run()
