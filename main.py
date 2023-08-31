import datetime as dt

FORMAT = '%H:%M:%S'
WEIGHT = 75  # Вес.
HEIGHT = 175  # Рост.
K_1 = 0.035  # Коэффициент для подсчета калорий.
K_2 = 0.029  # Коэффициент для подсчета калорий.
STEP_M = 0.65  # Длина шага в метрах.

storage_data = {}  # Словарь для хранения полученных данных.


def check_correct_data(data):
    """Проверка корректности полученного пакета."""
    # Если длина пакета отлична от 2
    # или один из элементов пакета имеет пустое значение -
    # функция вернет False, иначе - True.
    if len(data) != 2 or data[0] is None or data[1] is None:
        return False
    else:
        return True


def check_correct_time(time):
    """Проверка корректности параметра времени."""
    # Если словарь для хранения не пустой
    # и значение времени, полученное в аргументе,
    # меньше или равно самому большому значению ключа в словаре,
    # функция вернет False.
    # Иначе - True
    if storage_data is not None and time <= dt.datetime.strptime(str(max(storage_data, default='0:00:00')),
                                                                 FORMAT).time():
        return False
    else:
        return True


def get_step_day(steps):
    """Получить количество пройденных шагов за этот день."""

    summ = 0
    for step in storage_data.values():
        summ += step
    summ += steps
    return summ


def get_distance(steps):
    """Получить дистанцию пройденного пути в км."""

    dist = 0
    for step in storage_data.values():
        step *= 0.65
        dist += step
    dist += steps * 0.65
    dist = dist / 1000
    return dist


def get_spent_calories(dist, current_time):
    """Получить значения потраченных калорий."""

    time_in_hours = current_time.hour + current_time.minute / 60
    time_in_m = time_in_hours * 60
    mean_speed = dist / time_in_hours

    spent_calories = (K_1 * WEIGHT + (mean_speed ** 2 / HEIGHT) * K_2 * WEIGHT) * time_in_m
    return spent_calories


def get_achievement(dist):
    """Получить поздравления за пройденную дистанцию."""

    if dist >= 6.5:
        return 'Отличный результат! Цель достигнута.'
    elif dist >= 3.9:
        return 'Неплохо! День был продуктивный.'
    elif dist >= 2:
        return 'Завтра наверстаем!'
    else:
        return 'Лежать тоже полезно. Главное — участие, а не победа!'


def show_message(time, steps, dist, spent_cal, achievement):
    print(f'''
Время: {time}.
Количество шагов за сегодня: {steps}.
Дистанция составила {dist:.2f} км.
Вы сожгли {spent_cal:.2f} ккал.
{achievement}
''')


def accept_package(data):
    """Обработать пакет данных."""

    if not check_correct_data(data):
        return 'Некорректный пакет'

    pack_time = dt.datetime.strptime(data[0], FORMAT).time()

    if not check_correct_time(pack_time):
        return 'Некорректное значение времени'

    day_steps = get_step_day(data[1])
    dist = get_distance(data[1])
    spent_calories = get_spent_calories(dist, pack_time)
    achievement = get_achievement(dist)

    show_message(pack_time, day_steps, dist, spent_calories, achievement)

    storage_data[data[0]] = data[1]
    return storage_data


package_0 = ('2:00:01', 505)
package_1 = (None, 3211)
package_2 = ('9:36:02', 15000)
package_3 = ('9:36:02', 9000)
package_4 = ('8:01:02', 7600)
package_5 = ('16:23:45', 5000)

accept_package(package_0)
accept_package(package_1)
accept_package(package_2)
accept_package(package_3)
accept_package(package_4)
accept_package(package_5)
