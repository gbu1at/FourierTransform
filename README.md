### **Идея преобразования Фурье**  

Код визуализирует процесс **намотки сигнала** (или **гибкого векторного представления**), который тесно связан с **преобразованием Фурье**.  

#### **1. Что делает код?**  
- Генерирует **сигнал**, состоящий из суммы синусоид с разными частотами и фазами. Частоту и фазы синусоид можно передавать в качестве аргументов в комнадной строке
- Визуализирует, как этот сигнал наматывается на комплексную плоскость с разными **частотами намотки** (аналогично комплексному экспоненциальному представлению в Фурье-анализе).
- Показывает **центр масс** намотанного сигнала, что аналогично нахождению коэффициентов Фурье.

---

### **2. Связь с преобразованием Фурье**  

#### **Намотка сигнала и интегралы Фурье**  
Преобразование Фурье для непрерывного сигнала $ f(t) $ записывается как:  

$$
F(w) = \int_{-\infty}^{\infty} f(t) e^{-i 2 \pi w t} dt
$$

Где $ F(w) $ — это коэффициенты, показывающие вклад каждой частоты $ w $ в общий сигнал.  
 

#### **Центр масс и коэффициенты Фурье**  
- В коде центр масс $( x_{cm}, y_{cm})$ вычисляется с помощью интегралов:  
  $$
  x_{cm} = \int f(t) \cos(2\pi f t) dt, \quad y_{cm} = \int f(t) \sin(2\pi f t) dt
  $$
  Это именно **вещественная и мнимая части коэффициентов Фурье** для данной частоты намотки. 
$$
F(w) = x_{cm} + i y_{cm}
$$ 
- График изменения $ x_{cm}, y_{cm} $ показывает, **какие частоты присутствуют** в сигнале.

---

### **3. Итог**
- Код **интуитивно показывает идею преобразования Фурье**, где сигнал **наматывается** на окружность с разными частотами.
- Центр масс намотки **соответствует коэффициентам Фурье**, показывая **основные частоты** в сигнале.
- Этот метод часто используется в **анимации, обработке сигналов и визуализации Фурье-анализа**.












# Документация кода

## Описание
Этот код выполняет визуализацию сигнала, наматываемого на окружность, с возможностью задания параметров сигнала через аргументы командной строки. Анимация демонстрирует исходный сигнал, его преобразование и вычисленный центр масс. Также реализована возможность перезапуска анимации с помощью кнопки.

## Зависимости
Для работы кода необходимо установить следующие библиотеки:
```sh
pip install numpy matplotlib scipy
```

## Аргументы командной строки
Программа поддерживает передачу параметров сигнала через командную строку:
- `--sampling_rate` (int) — частота дискретизации сигнала (по умолчанию 1000).
- `--frequencies` (str) — список частот через запятую (по умолчанию "2, 5, 8").
- `--shiftes` (str) — список фазовых сдвигов в градусах через запятую (по умолчанию "0, 0, 0").


## Основные функции

### `parse_args()`
Разбирает аргументы командной строки, преобразует строки в числовые списки и возвращает их.

### `wire_func(t, signal_func, winding_frequency)`
Вычисляет координаты точки на плоскости для намотанного сигнала.

### `compute_center_of_mass(signal_func, winding_frequency)`
Вычисляет координаты центра масс для намотанного сигнала с использованием численного интегрирования.

### `init()`
Инициализирует анимацию, обнуляя данные и сбрасывая графики.

### `update(frame)`
# Документация для анимации сигнала с вычислением центра масс

Этот код создает анимацию, которая показывает, как меняется "намотанный" сигнал с разной частотой намотки, а также визуализирует центр масс этого сигнала. Визуализация состоит из трех графиков, а также функции для перезапуска анимации.

## Описание

- **Исходный сигнал**: Представляет собой сумму синусоидальных волн с разными частотами и фазами.
- **Намотанный сигнал**: Это сигнал, который "наматывается" на спираль в плоскости XY, где амплитуда радиусного вектора зависит от значения исходного сигнала.
- **Центр масс**: Вычисляется для намотанного сигнала и отображается на графике.

## Структура

### 1. Импорт библиотек

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import quad
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button
```

### 2. Параметры сигнала

```python
sampling_rate = 1000
time_points = np.linspace(0, 5, sampling_rate, endpoint=False)

frequencies = [2, 5, 8]
shiftes = [np.pi/2, 0, 0]
```

- `sampling_rate`: Частота дискретизации.
- `time_points`: Массив временных точек для сигнала.
- `frequencies`: Частоты синусоид, составляющих исходный сигнал.
- `shiftes`: Фазы этих синусоид.

Эти параметры можно менять и будет получаться различные графики
Конечно можно передавать в качестве аргументов

### 3. Функции

- **`signal_func`**: Функция для генерации исходного сигнала на основе частот и фаз.
- **`wire_func`**: Функция, преобразующая временные точки сигнала в координаты на плоскости XY, моделируя "намотку".
- **`compute_center_of_mass`**: Функция для вычисления центра масс сигнала на основе интегралов по времени.

### 4. Настройка графиков

Код использует `matplotlib` для создания трех графиков:

1. **Исходный сигнал** (верхний левый).
2. **Намотанный сигнал** (верхний правый).
3. **Центр масс** (нижний график, показывающий изменение координат центра масс по частоте намотки).

### 5. Анимация

Анимация создается с помощью функции `FuncAnimation` из библиотеки `matplotlib.animation`. Время анимации регулируется с помощью переменной `frame`.

### 6. Функции анимации

- **`init`**: Функция инициализации, которая устанавливает начальные значения для всех графиков.
- **`update`**: Функция обновления кадров анимации, которая рассчитывает новые координаты для "намотанного" сигнала и обновляет значения центра масс.

### 7. Кнопка перезапуска

Для перезапуска анимации добавлена кнопка с помощью `matplotlib.widgets.Button`. При нажатии на кнопку анимация останавливается и начинается заново.

```python
def restart(event):
    global ani
    ani.event_source.stop()
    ani = FuncAnimation(fig, update, frames=np.linspace(0, 10, 200), init_func=init, blit=True, interval=50, repeat=False)
    plt.draw()
```

## Запуск

1. Код создаст окно с графиками, отображающими исходный сигнал, намотанный сигнал и координаты центра масс.
2. Частота намотки будет изменяться, и вы сможете увидеть, как меняется поведение центра масс сигнала.
3. Для перезапуска анимации нужно нажать кнопку "Restart".

## Требования

- `numpy`
- `matplotlib`
- `scipy`

## Примечания

- Код использует численное интегрирование с помощью функции `quad` из библиотеки `scipy` для вычисления центра масс.
- Анимация обновляется с интервалом 50 миллисекунд, что позволяет наблюдать плавное изменение сигнала.

---

Это описание поможет вам лучше понять структуру и функциональность кода. Вы можете адаптировать или расширить его для своих нужд.

Обновляет состояние анимации, вычисляет новые координаты сигнала, центра масс и обновляет графики.

### `restart(event)`
Перезапускает анимацию при нажатии кнопки "Restart".

## Визуализация

### Основные графики
- **ax1 (Исходный сигнал)** — временная зависимость амплитуды сигнала.
- **ax2 (Намотанный сигнал)** — сигнал, преобразованный в систему координат с угловым перемещением.
- **ax3 (Центр масс)** — графики зависимости координат центра масс от частоты намотки.

### Анимация
Анимация выполняется с использованием `FuncAnimation` из `matplotlib`, изменяя частоту намотки сигнала.

### Кнопка перезапуска
Добавляется кнопка `Restart`, позволяющая сбросить и запустить анимацию заново.

## Итог
Код позволяет визуализировать процесс преобразования сигнала, исследовать его центр масс и экспериментировать с параметрами. С его помощью можно изучать поведение различных сигналов и их спектральные свойства.




### Пример запуска с параметрами:
```sh
python script.py --sampling_rate 2000 --frequencies "3,6,9" --shiftes "30,60,90"
```





---

## метод LSB‑стеганографии
#### Это немного не касается преобразования Фурье, просто мне стало любопытно

1. Представление аудиосигнала в цифровой форме

Частота дискретизации — это количество измерений аудиосигнала в единицу времени

(Это может быть измерение давления возле динамика например)

Если представить аудиосигнал как непрерывную волну, то при цифровой записи его нужно разбить на дискретные точки — сэмплы. Чем больше таких сэмплов в секунду, тем точнее цифровое представление сигнала.

Поэтому аудиофайл в цифровом виде представляет собой массив дискретных значений.

Часто для хранения аудио используют формат int16, где каждый сэмпл (одно измерение аудиосигнала) — это 16-битное целое число

Поэтому в аудио сигнал можно закодировать сообщение, изменив первый бит числа сэмпла
Давление воздуха измениться не очень значительно, поэтому в аудио сигнал можно кодировать другое аудио или текст

Декодирование происходит по тому же принципу
