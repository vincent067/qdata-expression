# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
# AGPL-3.0 License - 商业用途需购买许可
# 详见 LICENSE 和 COMMERCIAL-LICENSE.txt

"""
数学函数库

提供数学运算相关的内置函数。
"""

import math
from collections.abc import Callable
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Union

from .base import FunctionCategory, FunctionDefinition

# 类型别名
Number = Union[int, float, Decimal]


def _to_number(value: Any) -> Number:
    """转换为数值"""
    if isinstance(value, (int, float, Decimal)):
        return value
    if isinstance(value, str):
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
    raise TypeError(f"无法将 {type(value).__name__} 转换为数值")


# ============================================================
# 基础数学函数
# ============================================================


def expr_abs(value: Any) -> Number:
    """返回绝对值"""
    return abs(_to_number(value))


def expr_round(value: Any, digits: int = 0) -> Number:
    """四舍五入到指定位数"""
    num = _to_number(value)
    if digits == 0:
        return round(num)
    return round(num, digits)


def expr_round_half_up(value: Any, digits: int = 0) -> Decimal:
    """银行家舍入（四舍五入）"""
    num = Decimal(str(value))
    if digits == 0:
        return num.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    quantize_str = "0." + "0" * digits
    return num.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)


def expr_floor(value: Any) -> int:
    """向下取整"""
    return math.floor(_to_number(value))


def expr_ceil(value: Any) -> int:
    """向上取整"""
    return math.ceil(_to_number(value))


def expr_trunc(value: Any) -> int:
    """截断为整数"""
    return math.trunc(_to_number(value))


# ============================================================
# 聚合函数
# ============================================================


def expr_min(*values: Any) -> Number:
    """返回最小值"""
    if len(values) == 1 and hasattr(values[0], "__iter__"):
        values = tuple(values[0])
    nums = [_to_number(v) for v in values]
    return min(nums)


def expr_max(*values: Any) -> Number:
    """返回最大值"""
    if len(values) == 1 and hasattr(values[0], "__iter__"):
        values = tuple(values[0])
    nums = [_to_number(v) for v in values]
    return max(nums)


def expr_sum(*values: Any) -> Number:
    """求和"""
    if len(values) == 1 and hasattr(values[0], "__iter__"):
        values = tuple(values[0])
    nums = [_to_number(v) for v in values]
    return sum(nums)


def expr_avg(*values: Any) -> float:
    """计算平均值"""
    if len(values) == 1 and hasattr(values[0], "__iter__"):
        values = tuple(values[0])
    nums = [_to_number(v) for v in values]
    if not nums:
        return 0.0
    return sum(nums) / len(nums)


def expr_count(*values: Any) -> int:
    """计数"""
    if len(values) == 1 and hasattr(values[0], "__iter__"):
        return len(list(values[0]))
    return len(values)


# ============================================================
# 高级数学函数
# ============================================================


def expr_pow(base: Any, exp: Any) -> Number:
    """幂运算"""
    return pow(_to_number(base), _to_number(exp))


def expr_sqrt(value: Any) -> float:
    """平方根"""
    return math.sqrt(_to_number(value))


def expr_log(value: Any, base: Any = math.e) -> float:
    """对数"""
    return math.log(_to_number(value), _to_number(base))


def expr_log10(value: Any) -> float:
    """以 10 为底的对数"""
    return math.log10(_to_number(value))


def expr_exp(value: Any) -> float:
    """e 的幂"""
    return math.exp(_to_number(value))


def expr_mod(a: Any, b: Any) -> Number:
    """取模"""
    return _to_number(a) % _to_number(b)


def expr_div(a: Any, b: Any) -> float:
    """除法（返回浮点数）"""
    return _to_number(a) / _to_number(b)


def expr_divmod(a: Any, b: Any) -> tuple[int, Number]:
    """同时返回商和余数"""
    return divmod(_to_number(a), _to_number(b))


def expr_sign(value: Any) -> int:
    """返回符号（-1, 0, 1）"""
    num = _to_number(value)
    if num > 0:
        return 1
    elif num < 0:
        return -1
    return 0


# ============================================================
# 三角函数
# ============================================================


def expr_sin(value: Any) -> float:
    """正弦"""
    return math.sin(_to_number(value))


def expr_cos(value: Any) -> float:
    """余弦"""
    return math.cos(_to_number(value))


def expr_tan(value: Any) -> float:
    """正切"""
    return math.tan(_to_number(value))


def expr_radians(degrees: Any) -> float:
    """角度转弧度"""
    return math.radians(_to_number(degrees))


def expr_degrees(radians: Any) -> float:
    """弧度转角度"""
    return math.degrees(_to_number(radians))


# ============================================================
# 随机数函数（用于数据生成）
# ============================================================


def expr_random() -> float:
    """返回 0-1 之间的随机数"""
    import random
    return random.random()


def expr_random_int(a: int, b: int) -> int:
    """返回 a-b 之间的随机整数"""
    import random
    return random.randint(int(a), int(b))


# ============================================================
# 函数注册
# ============================================================


def _create_function_definition(
    name: str,
    func: Callable,
    description: str,
    signature: str,
    examples: list[str],
    min_args: int = 0,
    max_args: int | None = None,
    aliases: list[str] | None = None,
) -> FunctionDefinition:
    """创建函数定义"""
    return FunctionDefinition(
        name=name,
        func=func,
        category=FunctionCategory.MATH,
        description=description,
        signature=signature,
        examples=examples,
        min_args=min_args,
        max_args=max_args,
    )


# 数学函数集合
MATH_FUNCTIONS: dict[str, FunctionDefinition] = {
    # 基础函数
    "abs": _create_function_definition(
        "abs",
        expr_abs,
        "返回绝对值",
        "abs(value) -> number",
        ["abs(-5) = 5", "abs(3.14) = 3.14"],
        min_args=1,
        max_args=1,
    ),
    "round": _create_function_definition(
        "round",
        expr_round,
        "四舍五入到指定位数",
        "round(value, digits=0) -> number",
        ["round(3.14159, 2) = 3.14", "round(2.5) = 2"],
        min_args=1,
        max_args=2,
    ),
    "round_half_up": _create_function_definition(
        "round_half_up",
        expr_round_half_up,
        "银行家舍入（真正的四舍五入）",
        "round_half_up(value, digits=0) -> Decimal",
        ["round_half_up(2.5) = 3", "round_half_up(3.145, 2) = 3.15"],
        min_args=1,
        max_args=2,
    ),
    "floor": _create_function_definition(
        "floor",
        expr_floor,
        "向下取整",
        "floor(value) -> int",
        ["floor(3.7) = 3", "floor(-3.2) = -4"],
        min_args=1,
        max_args=1,
    ),
    "ceil": _create_function_definition(
        "ceil",
        expr_ceil,
        "向上取整",
        "ceil(value) -> int",
        ["ceil(3.2) = 4", "ceil(-3.7) = -3"],
        min_args=1,
        max_args=1,
    ),
    "trunc": _create_function_definition(
        "trunc",
        expr_trunc,
        "截断为整数（去掉小数部分）",
        "trunc(value) -> int",
        ["trunc(3.7) = 3", "trunc(-3.7) = -3"],
        min_args=1,
        max_args=1,
    ),
    # 聚合函数
    "min": _create_function_definition(
        "min",
        expr_min,
        "返回最小值",
        "min(*values) -> number",
        ["min(1, 2, 3) = 1", "min([5, 3, 8]) = 3"],
        min_args=1,
    ),
    "max": _create_function_definition(
        "max",
        expr_max,
        "返回最大值",
        "max(*values) -> number",
        ["max(1, 2, 3) = 3", "max([5, 3, 8]) = 8"],
        min_args=1,
    ),
    "sum": _create_function_definition(
        "sum",
        expr_sum,
        "求和",
        "sum(*values) -> number",
        ["sum(1, 2, 3) = 6", "sum([1, 2, 3, 4]) = 10"],
        min_args=1,
    ),
    "avg": _create_function_definition(
        "avg",
        expr_avg,
        "计算平均值",
        "avg(*values) -> float",
        ["avg(1, 2, 3, 4) = 2.5", "avg([10, 20, 30]) = 20.0"],
        min_args=1,
    ),
    "count": _create_function_definition(
        "count",
        expr_count,
        "计数",
        "count(*values) -> int",
        ["count(1, 2, 3) = 3", "count([1, 2, 3, 4, 5]) = 5"],
        min_args=1,
    ),
    # 高级数学函数
    "pow": _create_function_definition(
        "pow",
        expr_pow,
        "幂运算",
        "pow(base, exp) -> number",
        ["pow(2, 3) = 8", "pow(10, 2) = 100"],
        min_args=2,
        max_args=2,
    ),
    "sqrt": _create_function_definition(
        "sqrt",
        expr_sqrt,
        "平方根",
        "sqrt(value) -> float",
        ["sqrt(16) = 4.0", "sqrt(2) ≈ 1.414"],
        min_args=1,
        max_args=1,
    ),
    "log": _create_function_definition(
        "log",
        expr_log,
        "对数（默认自然对数）",
        "log(value, base=e) -> float",
        ["log(e) = 1.0", "log(100, 10) = 2.0"],
        min_args=1,
        max_args=2,
    ),
    "log10": _create_function_definition(
        "log10",
        expr_log10,
        "以 10 为底的对数",
        "log10(value) -> float",
        ["log10(100) = 2.0", "log10(1000) = 3.0"],
        min_args=1,
        max_args=1,
    ),
    "exp": _create_function_definition(
        "exp",
        expr_exp,
        "e 的幂",
        "exp(value) -> float",
        ["exp(0) = 1.0", "exp(1) ≈ 2.718"],
        min_args=1,
        max_args=1,
    ),
    "mod": _create_function_definition(
        "mod",
        expr_mod,
        "取模（求余数）",
        "mod(a, b) -> number",
        ["mod(10, 3) = 1", "mod(15, 4) = 3"],
        min_args=2,
        max_args=2,
    ),
    "div": _create_function_definition(
        "div",
        expr_div,
        "除法（返回浮点数）",
        "div(a, b) -> float",
        ["div(10, 3) = 3.333...", "div(15, 5) = 3.0"],
        min_args=2,
        max_args=2,
    ),
    "sign": _create_function_definition(
        "sign",
        expr_sign,
        "返回符号（-1, 0, 1）",
        "sign(value) -> int",
        ["sign(-5) = -1", "sign(0) = 0", "sign(10) = 1"],
        min_args=1,
        max_args=1,
    ),
    # 三角函数
    "sin": _create_function_definition(
        "sin",
        expr_sin,
        "正弦（弧度）",
        "sin(radians) -> float",
        ["sin(0) = 0.0", "sin(π/2) = 1.0"],
        min_args=1,
        max_args=1,
    ),
    "cos": _create_function_definition(
        "cos",
        expr_cos,
        "余弦（弧度）",
        "cos(radians) -> float",
        ["cos(0) = 1.0", "cos(π) = -1.0"],
        min_args=1,
        max_args=1,
    ),
    "tan": _create_function_definition(
        "tan",
        expr_tan,
        "正切（弧度）",
        "tan(radians) -> float",
        ["tan(0) = 0.0", "tan(π/4) = 1.0"],
        min_args=1,
        max_args=1,
    ),
    "radians": _create_function_definition(
        "radians",
        expr_radians,
        "角度转弧度",
        "radians(degrees) -> float",
        ["radians(180) ≈ 3.14159", "radians(90) ≈ 1.5708"],
        min_args=1,
        max_args=1,
    ),
    "degrees": _create_function_definition(
        "degrees",
        expr_degrees,
        "弧度转角度",
        "degrees(radians) -> float",
        ["degrees(π) ≈ 180", "degrees(π/2) ≈ 90"],
        min_args=1,
        max_args=1,
    ),
    # 随机数
    "random": _create_function_definition(
        "random",
        expr_random,
        "返回 0-1 之间的随机数",
        "random() -> float",
        ["random() = 0.123..."],
        min_args=0,
        max_args=0,
    ),
    "random_int": _create_function_definition(
        "random_int",
        expr_random_int,
        "返回 a-b 之间的随机整数",
        "random_int(a, b) -> int",
        ["random_int(1, 10) = 5"],
        min_args=2,
        max_args=2,
    ),
}


def get_math_functions() -> dict[str, Callable]:
    """获取所有数学函数"""
    return {name: defn.func for name, defn in MATH_FUNCTIONS.items()}
