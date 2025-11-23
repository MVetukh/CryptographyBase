import random
from typing import Optional

def gcd(a: int, b: int) -> int:
    """
    Вычисляет наибольший общий делитель (НОД) двух целых чисел
    с использованием алгоритма Евклида.

    Args:
        a: Первое целое число
        b: Второе целое число

    Returns:
        Наибольший общий делитель чисел a и b

    Raises:
        ValueError: Если оба числа равны 0
    """
    # Обработка нулевых значений
    if a == 0 and b == 0:
        raise ValueError("НОД(0, 0) не определен")

    # Алгоритм Евклида
    while b != 0:
        a, b = b, a % b
    return abs(a)  # НОД всегда неотрицательный

def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Расширенный алгоритм Евклида.
    Находит НОД(a, b) и коэффициенты x, y такие, что:
        a*x + b*y = НОД(a, b)

    Args:
        a: Первое целое число
        b: Второе целое число

    Returns:
        Кортеж (x, y, gcd): коэффициенты Безу и НОД

    Raises:
        ValueError: Если оба числа равны 0
    """
    if a == 0 and b == 0:
        raise ValueError("НОД(0, 0) не определен")

    # Инициализация матрицы преобразования
    # [x  xx]   представляющая коэффициенты для a и b
    # [y  yy]
    x, xx = 1, 0  # коэффициенты для a
    y, yy = 0, 1  # коэффициенты для b

    # Сохраняем знаки для корректного возврата коэффициентов
    sign_a = 1 if a >= 0 else -1
    sign_b = 1 if b >= 0 else -1
    a, b = abs(a), abs(b)

    while b != 0:
        # Вычисляем частное и остаток
        quotient = a // b
        a, b = b, a % b

        # Обновляем коэффициенты
        x, xx = xx, x - quotient * xx
        y, yy = yy, y - quotient * yy

    # Корректируем знаки коэффициентов
    x *= sign_a
    y *= sign_b

    return (x, y, a)

def mod_inverse(a: int, modulus: int) -> int:
    """
    Вычисляет мультипликативно обратный элемент a^(-1) mod modulus.

    Args:
        a: Число, для которого ищется обратный элемент
        modulus: Модуль, должен быть > 1

    Returns:
        Обратный элемент a^(-1) mod modulus

    Raises:
        ValueError: Если modulus ≤ 1 или обратный элемент не существует
        TypeError: Если аргументы не целые числа

    Note:
        Обратный элемент существует только когда gcd(a, modulus) = 1
    """
    # Проверка входных данных
    if not isinstance(a, int) or not isinstance(modulus, int):
        raise TypeError("Аргументы должны быть целыми числами")

    if modulus <= 1:
        raise ValueError(f"Модуль должен быть > 1, получено {modulus}")

    # Обработка отрицательного a
    a = a % modulus
    if a < 0:
        a += modulus

    # Специальные случаи
    if a == 0:
        raise ValueError("Обратный элемент к 0 не существует")
    if a == 1:
        return 1  # 1^(-1) ≡ 1 mod m

    # Используем расширенный алгоритм Евклида
    x, y, gcd_val = extended_gcd(a, modulus)

    if gcd_val != 1:
        raise ValueError(
            f"Обратный элемент к {a} по модулю {modulus} не существует, "
            f"так как НОД({a}, {modulus}) = {gcd_val} ≠ 1"
        )

    # Нормализуем результат к диапазону [0, modulus-1]
    inverse = x % modulus
    if inverse < 0:
        inverse += modulus

    # Проверка корректности (для отладки)
    assert (a * inverse) % modulus == 1, "Некорректный обратный элемент"

    return inverse

def batch_mod_inverse(numbers: list[int], modulus: int) -> list[int]:
    """
    Вычисляет обратные элементы для списка чисел за O(n + log m) операций.

    Args:
        numbers: Список чисел для инвертирования
        modulus: Модуль

    Returns:
        Список обратных элементов

    Note:
        Все числа должны быть обратимы по модулю modulus
    """
    n = len(numbers)
    if n == 0:
        return []
    # Предвычисление префиксных произведений
    prefix = [1] * (n + 1)
    for i in range(n):
        prefix[i + 1] = (prefix[i] * numbers[i]) % modulus
    # Вычисление обратного к общему произведению
    total_inverse = mod_inverse(prefix[n], modulus)
    # Обратный проход для вычисления отдельных обратных элементов
    inverses = [1] * n
    suffix_product = 1
    for i in range(n - 1, -1, -1):
        inverses[i] = (prefix[i] * total_inverse) % modulus
        total_inverse = (total_inverse * numbers[i]) % modulus

    return inverses

def solve_linear_congruence(a: int, b: int, modulus: int) -> list[int]:
    """
    Решает линейное сравнение a*x ≡ b (mod modulus).
    Args:
        a: Коэффициент при x
        b: Свободный член
        modulus: Модуль сравнения

    Returns:
        Список всех решений в диапазоне [0, modulus-1] или пустой список, если решений нет

    Raises:
        ValueError: Если modulus ≤ 1
        TypeError: Если аргументы не целые числа

    Note:
        Сравнение a*x ≡ b (mod m) имеет решения тогда и только тогда,
        когда gcd(a, m) делит b
    """
    # Проверка входных данных
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(modulus, int):
        raise TypeError("Все аргументы должны быть целыми числами")

    if modulus <= 1:
        raise ValueError(f"Модуль должен быть > 1, получено {modulus}")

    # Нормализация a и b
    a = a % modulus
    if a < 0:
        a += modulus

    b = b % modulus
    if b < 0:
        b += modulus

    # Специальные случаи
    if a == 0:
        # Уравнение 0*x ≡ b (mod m)
        return [0] if b == 0 else []

    if a == 1:
        # Уравнение x ≡ b (mod m)
        return [b]

    # Находим НОД(a, modulus)
    d = gcd(a, modulus)

    # Проверяем существование решений
    if b % d != 0:
        return []  # Решений нет

    # Приводим уравнение к виду с взаимно простыми коэффициентами
    a_reduced = a // d
    b_reduced = b // d
    modulus_reduced = modulus // d

    if a_reduced == 1:
        # После сокращения получили x ≡ b_reduced (mod modulus_reduced)
        base_solution = b_reduced % modulus_reduced
    else:
        # Находим частное решение приведенного уравнения
        x0, _, _ = extended_gcd(a_reduced, modulus_reduced)
        base_solution = (x0 * b_reduced) % modulus_reduced
        if base_solution < 0:
            base_solution += modulus_reduced

    # Генерируем все решения
    solutions = []
    for k in range(d):
        solution = base_solution + k * modulus_reduced
        solutions.append(solution)

    return solutions

def solve_linear_congruence_system(equations: list[tuple[int, int, int]]) -> list[int]:
    """
    Решает систему линейных сравнений методом Китайской теоремы об остатках.

    Args:
        equations: Список кортежей (a, b, m) для уравнений a*x ≡ b (mod m)

    Returns:
        Список решений системы

    Note:
        Все модули должны быть попарно взаимно простыми
    """
    if not equations:
        return []

    # Проверяем взаимную простоту модулей
    moduli = [m for _, _, m in equations]
    total_modulus = 1
    for m in moduli:
        if gcd(total_modulus, m) != 1:
            raise ValueError("Модули должны быть попарно взаимно простыми")
        total_modulus *= m

    # Решаем каждое уравнение отдельно
    solutions = []
    for a, b, m in equations:
        sols = solve_linear_congruence(a, b, m)
        if not sols:
            return []  # Система не имеет решений
        solutions.append(sols[0])  # Берем первое решение

    # Собираем решение по Китайской теореме
    result = 0
    for i, (a, b, m) in enumerate(equations):
        Mi = total_modulus // m
        yi = mod_inverse(Mi, m)
        result = (result + solutions[i] * Mi * yi) % total_modulus

    return [result]

def miller_rabin_test(n: int, k: Optional[int] = None, /, bases: Optional[list[int]] = None) -> bool:
    """
    Тест Миллера-Рабина на простоту числа.

    Вероятностный тест, который определяет, является ли число составным или,
    вероятно, простым. Используется в криптографии для генерации простых чисел
    в RSA, DSA, Diffie-Hellman и других алгоритмах.

    Args:
        n: Число для проверки на простоту (n > 3, нечетное)
        k: Количество раундов тестирования (точность теста)
           Если не указано, выбирается автоматически на основе размера n
        bases: Специфичный набор баз для тестирования. Если указан,
               тест становится детерминированным для n < 2^64

    Returns:
        True если число вероятно простое, False если составное

    Raises:
        ValueError: Если n ≤ 3 или четное
        TypeError: Если n не целое число

    Note:
        - Вероятность ошибки: 4^(-k)
        - Для n < 2^64 существует детерминированный набор баз
        - В криптографии обычно используют k=40-100
    """
    # Проверка входных данных
    if not isinstance(n, int):
        raise TypeError(f"n должно быть целым числом, получено {type(n)}")

    if n <= 3:
        raise ValueError(f"n должно быть > 3, получено {n}")
    if n % 2 == 0:
        return False  # Четные числа > 2 составные

    # Автоматический выбор k если не указан
    if k is None:
        k = _recommended_rounds(n)

    # Предварительные проверки для маленьких чисел
    if n < 10_000:
        return _is_small_prime(n)

    # Разложение n-1 = 2^s * d
    s, d = _factor_powers_of_two(n - 1)

    # Если указаны базы, используем их (детерминированный вариант)
    if bases is not None:
        return _miller_rabin_deterministic(n, s, d, bases)

    # Вероятностный тест с k раундами
    for _ in range(k):
        a = random.randint(2, n - 2)
        if not _miller_rabin_witness(n, s, d, a):
            return False

    return True

def _factor_powers_of_two(n: int) -> tuple[int, int]:
    """
    Разлагает n на вид n = 2^s * d, где d - нечетное.

    Args:
        n: Четное число для разложения

    Returns:
        Кортеж (s, d) где s - степень двойки, d - нечетное число
    """
    s = 0
    d = n
    while d % 2 == 0:
        s += 1
        d //= 2
    return s, d

def _miller_rabin_witness(n: int, s: int, d: int, a: int) -> bool:
    """
    Проверяет один свидетель простоты для теста Миллера-Рабина.

    Args:
        n: Проверяемое число
        s: Из разложения n-1 = 2^s * d
        d: Из разложения n-1 = 2^s * d
        a: Случайное основание (2 ≤ a ≤ n-2)

    Returns:
        True если a не является свидетелем составности n
    """
    # Вычисляем a^d mod n
    x = pow(a, d, n)

    # Если x ≡ 1 или x ≡ n-1 (mod n), то a не свидетель
    if x == 1 or x == n - 1:
        return True

    # Проверяем последовательные возведения в квадрат
    for _ in range(s - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
        if x == 1:
            return False

    return False

def _recommended_rounds(n: int) -> int:
    """
    Рекомендует количество раундов тестирования на основе размера числа.

    Args:
        n: Проверяемое число

    Returns:
        Рекомендуемое количество раундов
    """
    bit_length = n.bit_length()

    if bit_length < 100:
        return 40
    elif bit_length < 256:
        return 56
    elif bit_length < 512:
        return 64
    elif bit_length < 1024:
        return 80
    else:
        return 100

def _is_small_prime(n: int) -> bool:
    """
    Проверяет простоту маленьких чисел с помощью пробного деления.

    Args:
        n: Число для проверки (n < 10,000)

    Returns:
        True если число простое
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Проверяем делимость на нечетные числа до sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def _miller_rabin_deterministic(n: int, s: int, d: int, bases: list[int]) -> bool:
    """
    Детерминированная версия теста Миллера-Рабина для n < 2^64.

    Args:
        n: Проверяемое число
        s: Из разложения n-1 = 2^s * d
        d: Из разложения n-1 = 2^s * d
        bases: Набор баз для детерминированного тестирования

    Returns:
        True если число простое
    """
    for a in bases:
        if a % n == 0:
            continue
        if not _miller_rabin_witness(n, s, d, a):
            return False
    return True

def miller_rabin_deterministic_small(n: int) -> bool:
    """
    Детерминированный тест Миллера-Рабина для чисел < 2^64.

    Использует известные наборы баз, которые гарантируют правильный результат
    для всех чисел в указанном диапазоне.

    Args:
        n: Число для проверки (должно быть < 2^64)

    Returns:
        True если число простое, False если составное
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    s, d = _factor_powers_of_two(n - 1)

    # Известные наборы баз для детерминированного тестирования
    if n < 2_047:
        bases = [2]
    elif n < 1_373_653:
        bases = [2, 3]
    elif n < 9_080_191:
        bases = [31, 73]
    elif n < 25_326_001:
        bases = [2, 3, 5]
    elif n < 3_215_031_751:
        bases = [2, 3, 5, 7]
    elif n < 4_759_123_141:
        bases = [2, 7, 61]
    elif n < 1_122_004_669_633:
        bases = [2, 13, 23, 1662803]
    elif n < 2_152_302_898_747:
        bases = [2, 3, 5, 7, 11]
    elif n < 3_474_749_660_383:
        bases = [2, 3, 5, 7, 11, 13]
    elif n < 341_550_071_728_321:
        bases = [2, 3, 5, 7, 11, 13, 17]
    elif n < 3_825_123_056_546_413_051:
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    else:  # n < 2^64
        bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]

    return _miller_rabin_deterministic(n, s, d, bases)

def generate_probable_prime(bit_length: int, k: int = 100) -> int:
    """
    Генерирует вероятно простое число заданной битовой длины.

    Используется в криптографии для генерации ключей.

    Args:
        bit_length: Желаемая битовая длина простого числа
        k: Количество раундов теста Миллера-Рабина

    Returns:
        Вероятно простое число

    Raises:
        ValueError: Если bit_length < 2
    """
    if bit_length < 2:
        raise ValueError("Битовая длина должна быть ≥ 2")

    while True:
        # Генерируем случайное нечетное число
        candidate = random.getrandbits(bit_length)
        candidate |= (1 << (bit_length - 1)) | 1  # Устанавливаем старший и младший биты

        # Проверяем на простоту
        if miller_rabin_test(candidate, k):
            return candidate

def is_prime(n: int, method: str = "auto") -> bool:
    """
    Универсальная функция проверки простоты с выбором метода.

    Args:
        n: Число для проверки
        method: Метод проверки:
            - "auto": автоматический выбор оптимального метода
            - "miller-rabin": вероятностный тест Миллера-Рабина
            - "deterministic": детерминированный для n < 2^64
            - "trial-division": пробное деление для маленьких n

    Returns:
        True если число простое
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    if method == "auto":
        if n < 10_000:
            return _is_small_prime(n)
        elif n < (1 << 64):  # 2^64
            return miller_rabin_deterministic_small(n)
        else:
            return miller_rabin_test(n, k=50)

    elif method == "miller-rabin":
        return miller_rabin_test(n, k=50)

    elif method == "deterministic":
        if n < (1 << 64):
            return miller_rabin_deterministic_small(n)
        else:
            raise ValueError("Детерминированный метод работает только для n < 2^64")

    elif method == "trial-division":
        return _is_small_prime(n)

    else:
        raise ValueError(f"Неизвестный метод: {method}")




