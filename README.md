# Лабораторная работа №1

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Данные для ввода

- путь к изображению;
- папку для результатов;
- коэффициент растяжения `M`;
- коэффициент сжатия `N`;
- метод интерполяции: `nearest` или `bilinear`.

Если на первом вопросе просто нажать `Enter`, программа сама создаст demo-изображение `input_demo.png`.

## Результат

Все результаты сохраняются в папку `out` или в ту, которую укажет пользователь.


## Исходное изображение

![01_original.png](out/01_original.png)

---

### 1.1 Компоненты R, G, B

Компоненты сохранены как **отдельные изображения с выделением соответствующего цветового канала**.

| Красный канал | Зелёный канал | Синий канал |
|:------------:|:-------------:|:-----------:|
|![02_r_channel.png](out/02_r_channel.png) | ![03_g_channel.png](out/03_g_channel.png) | ![04_b_channel.png](out/04_b_channel.png) |

### 1.2 Яркостная компонента HSI

![05_hsi_intensity.png](out/05_hsi_intensity.png)

### 1.3 Инвертирование яркостной компоненты

| Исходное изображение | С инвертированной яркостью |
|:--------------------:|:--------------------------:|
| ![01_original.png](out/01_original.png) | ![06_inverted_intensity.png](out/06_inverted_intensity.png) |



---

## 2. Передискретизация 

### 2.1 Растяжение в M=2 раз (билинейная интерполяция)

| Исходное | Растянутое |
|:--------:|:----------:|
| ![01_original.png](out/01_original.png) | ![07_upsample_x2_bilinear.png](out/07_upsample_x2_bilinear.png) |

![07_upsample_x2_bilinear.png](out/07_upsample_x2_bilinear.png)

### 2.2 Сжатие в N=3 раз (децимация / прореживание)

| Исходное | Сжатое |
|:--------:|:------:|
| ![01_original.png](out/01_original.png) | ![08_decimate_x3.png](out/08_decimate_x3.png)|

![08_decimate_x3.png](out/08_decimate_x3.png)

### 2.3 Двухпроходная передискретизация (растяжение + сжатие)

Сначала растяжение в `M=2` раз, затем децимация в `N=3` раз.

| Исходное | Результат двух проходов |
|:--------:|:------------------------:|
| ![01_original.png](out/01_original.png) | ![09_resample_two_pass_2over3_bilinear.png](out/09_resample_two_pass_2over3_bilinear.png) |

![09_resample_two_pass_2over3_bilinear.png](out/09_resample_two_pass_2over3_bilinear.png)

### 2.4 Однопроходная передискретизация (прямое масштабирование в K раз)

Передискретизация выполняется за один проход с коэффициентом `K=M/N=2/3`.

| Исходное | Результат одного прохода |
|:--------:|:------------------------:|
| ![01_original.png](out/01_original.png) | ![10_resample_one_pass_2over3_bilinear.png](out/10_resample_one_pass_2over3_bilinear.png)|

![10_resample_one_pass_2over3_bilinear.png](out/10_resample_one_pass_2over3_bilinear.png)
---

## Результаты выполнения
| Операция | Размер изображения |
|:--|--:|
| Исходное изображение | 1000×563 |
| Растяжение (M=2) | 2000×1126 |
| Сжатие (N=3) | 334×188 |
| Двухпроходная (×2, затем ÷3) | 667×376 |
| Однопроходная (K=2/3) | 667×375 |

---

#
