import enum
from math import sin, cos, e


class Function(enum.Enum):
    sin_mult = 1
    sin_exp = 2
    sin_div = 3


def func_1(x: float) -> float:
    return 10 * sin(x)


def func_2(x: float) -> float:
    return 10 * sin((2 ** x + e ** (cos(abs(x)))))


def func_3(x: float) -> float:
    return 10 / sin(x)


def calculate_func(func: Function, start, end, num) -> list:
    functions_dict = {Function.sin_mult: func_1, Function.sin_exp: func_2, Function.sin_div: func_3}
    values_list = []

    step = (end - start) / (num - 1)
    for _ in range(num):
        values_list.append(functions_dict[func](start))
        start += step

    return values_list
