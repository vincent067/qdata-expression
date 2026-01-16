"""
逻辑函数库

提供逻辑判断和条件处理相关的内置函数。
"""

from collections.abc import Callable
from typing import Any

from .base import FunctionCategory, FunctionDefinition


# ============================================================
# 空值判断
# ============================================================


def expr_is_null(value: Any) -> bool:
    """判断是否为 None"""
    return value is None


def expr_is_not_null(value: Any) -> bool:
    """判断是否不为 None"""
    return value is not None


def expr_is_empty(value: Any) -> bool:
    """判断是否为空（None、空字符串、空列表等）"""
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) == 0
    return False


def expr_is_not_empty(value: Any) -> bool:
    """判断是否不为空"""
    return not expr_is_empty(value)


def expr_is_blank(value: Any) -> bool:
    """判断是否为空白（None、空字符串或只有空白的字符串）"""
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    return False


# ============================================================
# 条件函数
# ============================================================


def expr_if_else(condition: Any, true_value: Any, false_value: Any) -> Any:
    """条件判断，返回对应值"""
    return true_value if condition else false_value


def expr_if_null(value: Any, default: Any) -> Any:
    """如果为 None 则返回默认值"""
    return default if value is None else value


def expr_if_empty(value: Any, default: Any) -> Any:
    """如果为空则返回默认值"""
    return default if expr_is_empty(value) else value


def expr_coalesce(*values: Any) -> Any:
    """返回第一个非 None 的值"""
    for value in values:
        if value is not None:
            return value
    return None


def expr_nvl(value: Any, default: Any) -> Any:
    """NVL 函数（同 if_null）"""
    return default if value is None else value


def expr_nvl2(value: Any, not_null_value: Any, null_value: Any) -> Any:
    """NVL2 函数：非空返回第一个值，否则返回第二个值"""
    return not_null_value if value is not None else null_value


def expr_nullif(value1: Any, value2: Any) -> Any:
    """如果两个值相等则返回 None，否则返回第一个值"""
    return None if value1 == value2 else value1


def expr_case(value: Any, *pairs: Any, default: Any = None) -> Any:
    """
    CASE 表达式

    用法: case(value, condition1, result1, condition2, result2, ..., default=None)
    """
    for i in range(0, len(pairs), 2):
        if i + 1 < len(pairs):
            if value == pairs[i]:
                return pairs[i + 1]
    return default


def expr_switch(value: Any, cases: dict, default: Any = None) -> Any:
    """
    SWITCH 表达式

    用法: switch(value, {"a": 1, "b": 2}, default=0)
    """
    return cases.get(value, default)


# ============================================================
# 布尔运算
# ============================================================


def expr_and(*values: Any) -> bool:
    """逻辑与"""
    return all(values)


def expr_or(*values: Any) -> bool:
    """逻辑或"""
    return any(values)


def expr_not(value: Any) -> bool:
    """逻辑非"""
    return not value


def expr_xor(a: Any, b: Any) -> bool:
    """逻辑异或"""
    return bool(a) != bool(b)


# ============================================================
# 比较函数
# ============================================================


def expr_eq(a: Any, b: Any) -> bool:
    """等于"""
    return a == b


def expr_ne(a: Any, b: Any) -> bool:
    """不等于"""
    return a != b


def expr_gt(a: Any, b: Any) -> bool:
    """大于"""
    return a > b


def expr_ge(a: Any, b: Any) -> bool:
    """大于等于"""
    return a >= b


def expr_lt(a: Any, b: Any) -> bool:
    """小于"""
    return a < b


def expr_le(a: Any, b: Any) -> bool:
    """小于等于"""
    return a <= b


def expr_between(value: Any, low: Any, high: Any) -> bool:
    """判断值是否在范围内（包含边界）"""
    return low <= value <= high


def expr_in(value: Any, *items: Any) -> bool:
    """判断值是否在列表中"""
    if len(items) == 1 and isinstance(items[0], (list, tuple, set)):
        items = items[0]
    return value in items


def expr_not_in(value: Any, *items: Any) -> bool:
    """判断值是否不在列表中"""
    return not expr_in(value, *items)


# ============================================================
# 类型判断
# ============================================================


def expr_is_bool(value: Any) -> bool:
    """判断是否为布尔值"""
    return isinstance(value, bool)


def expr_is_int(value: Any) -> bool:
    """判断是否为整数"""
    return isinstance(value, int) and not isinstance(value, bool)


def expr_is_float(value: Any) -> bool:
    """判断是否为浮点数"""
    return isinstance(value, float)


def expr_is_number(value: Any) -> bool:
    """判断是否为数值"""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def expr_is_string(value: Any) -> bool:
    """判断是否为字符串"""
    return isinstance(value, str)


def expr_is_list(value: Any) -> bool:
    """判断是否为列表"""
    return isinstance(value, list)


def expr_is_dict(value: Any) -> bool:
    """判断是否为字典"""
    return isinstance(value, dict)


def expr_type_of(value: Any) -> str:
    """获取值的类型名称"""
    return type(value).__name__


# ============================================================
# 类型转换
# ============================================================


def expr_to_bool(value: Any) -> bool:
    """转换为布尔值"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    return bool(value)


def expr_to_int(value: Any, default: int = 0) -> int:
    """转换为整数"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def expr_to_float(value: Any, default: float = 0.0) -> float:
    """转换为浮点数"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def expr_to_str(value: Any) -> str:
    """转换为字符串"""
    if value is None:
        return ""
    return str(value)


# ============================================================
# 断言函数
# ============================================================


def expr_assert(condition: Any, message: str = "Assertion failed") -> bool:
    """断言条件为真"""
    if not condition:
        raise AssertionError(message)
    return True


def expr_require(value: Any, message: str = "Required value is missing") -> Any:
    """要求值不为空"""
    if expr_is_empty(value):
        raise ValueError(message)
    return value


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
) -> FunctionDefinition:
    """创建函数定义"""
    return FunctionDefinition(
        name=name,
        func=func,
        category=FunctionCategory.LOGIC,
        description=description,
        signature=signature,
        examples=examples,
        min_args=min_args,
        max_args=max_args,
    )


# 逻辑函数集合
LOGIC_FUNCTIONS: dict[str, FunctionDefinition] = {
    # 空值判断
    "is_null": _create_function_definition(
        "is_null", expr_is_null, "判断是否为 None",
        "is_null(value) -> bool", ["is_null(None) = True", "is_null(0) = False"],
        min_args=1, max_args=1,
    ),
    "is_not_null": _create_function_definition(
        "is_not_null", expr_is_not_null, "判断是否不为 None",
        "is_not_null(value) -> bool", ["is_not_null(1) = True"],
        min_args=1, max_args=1,
    ),
    "is_empty": _create_function_definition(
        "is_empty", expr_is_empty, "判断是否为空",
        "is_empty(value) -> bool", ['is_empty("") = True', "is_empty([]) = True"],
        min_args=1, max_args=1,
    ),
    "is_not_empty": _create_function_definition(
        "is_not_empty", expr_is_not_empty, "判断是否不为空",
        "is_not_empty(value) -> bool", ['is_not_empty("hello") = True'],
        min_args=1, max_args=1,
    ),
    "is_blank": _create_function_definition(
        "is_blank", expr_is_blank, "判断是否为空白",
        "is_blank(value) -> bool", ['is_blank("  ") = True'],
        min_args=1, max_args=1,
    ),
    # 条件函数
    "if_else": _create_function_definition(
        "if_else", expr_if_else, "条件判断",
        "if_else(condition, true_value, false_value) -> any",
        ['if_else(True, "yes", "no") = "yes"'],
        min_args=3, max_args=3,
    ),
    "if_null": _create_function_definition(
        "if_null", expr_if_null, "如果为 None 则返回默认值",
        "if_null(value, default) -> any", ["if_null(None, 0) = 0"],
        min_args=2, max_args=2,
    ),
    "if_empty": _create_function_definition(
        "if_empty", expr_if_empty, "如果为空则返回默认值",
        "if_empty(value, default) -> any", ['if_empty("", "default") = "default"'],
        min_args=2, max_args=2,
    ),
    "coalesce": _create_function_definition(
        "coalesce", expr_coalesce, "返回第一个非 None 的值",
        "coalesce(*values) -> any", ['coalesce(None, "", "a") = ""'],
        min_args=1,
    ),
    "nvl": _create_function_definition(
        "nvl", expr_nvl, "NVL 函数",
        "nvl(value, default) -> any", ["nvl(None, 0) = 0"],
        min_args=2, max_args=2,
    ),
    "nvl2": _create_function_definition(
        "nvl2", expr_nvl2, "NVL2 函数",
        "nvl2(value, not_null_value, null_value) -> any",
        ['nvl2("x", "has value", "no value") = "has value"'],
        min_args=3, max_args=3,
    ),
    "nullif": _create_function_definition(
        "nullif", expr_nullif, "如果两个值相等则返回 None",
        "nullif(value1, value2) -> any", ["nullif(1, 1) = None", "nullif(1, 2) = 1"],
        min_args=2, max_args=2,
    ),
    "switch": _create_function_definition(
        "switch", expr_switch, "SWITCH 表达式",
        'switch(value, cases, default=None) -> any',
        ['switch("a", {"a": 1, "b": 2}, 0) = 1'],
        min_args=2, max_args=3,
    ),
    # 布尔运算
    "bool_and": _create_function_definition(
        "bool_and", expr_and, "逻辑与",
        "bool_and(*values) -> bool", ["bool_and(True, True) = True", "bool_and(True, False) = False"],
        min_args=1,
    ),
    "bool_or": _create_function_definition(
        "bool_or", expr_or, "逻辑或",
        "bool_or(*values) -> bool", ["bool_or(True, False) = True", "bool_or(False, False) = False"],
        min_args=1,
    ),
    "bool_not": _create_function_definition(
        "bool_not", expr_not, "逻辑非",
        "bool_not(value) -> bool", ["bool_not(True) = False", "bool_not(False) = True"],
        min_args=1, max_args=1,
    ),
    "xor": _create_function_definition(
        "xor", expr_xor, "逻辑异或",
        "xor(a, b) -> bool", ["xor(True, False) = True", "xor(True, True) = False"],
        min_args=2, max_args=2,
    ),
    # 比较函数
    "eq": _create_function_definition(
        "eq", expr_eq, "等于",
        "eq(a, b) -> bool", ["eq(1, 1) = True"],
        min_args=2, max_args=2,
    ),
    "ne": _create_function_definition(
        "ne", expr_ne, "不等于",
        "ne(a, b) -> bool", ["ne(1, 2) = True"],
        min_args=2, max_args=2,
    ),
    "gt": _create_function_definition(
        "gt", expr_gt, "大于",
        "gt(a, b) -> bool", ["gt(2, 1) = True"],
        min_args=2, max_args=2,
    ),
    "ge": _create_function_definition(
        "ge", expr_ge, "大于等于",
        "ge(a, b) -> bool", ["ge(1, 1) = True"],
        min_args=2, max_args=2,
    ),
    "lt": _create_function_definition(
        "lt", expr_lt, "小于",
        "lt(a, b) -> bool", ["lt(1, 2) = True"],
        min_args=2, max_args=2,
    ),
    "le": _create_function_definition(
        "le", expr_le, "小于等于",
        "le(a, b) -> bool", ["le(1, 1) = True"],
        min_args=2, max_args=2,
    ),
    "between": _create_function_definition(
        "between", expr_between, "判断值是否在范围内",
        "between(value, low, high) -> bool", ["between(5, 1, 10) = True"],
        min_args=3, max_args=3,
    ),
    "contains_value": _create_function_definition(
        "contains_value", expr_in, "判断值是否在列表中",
        "contains_value(value, *items) -> bool", ["contains_value(1, 1, 2, 3) = True", 'contains_value("a", ["a", "b"]) = True'],
        min_args=2,
    ),
    "not_in": _create_function_definition(
        "not_in", expr_not_in, "判断值是否不在列表中",
        "not_in(value, *items) -> bool", ["not_in(4, 1, 2, 3) = True"],
        min_args=2,
    ),
    # 类型判断
    "is_bool": _create_function_definition(
        "is_bool", expr_is_bool, "判断是否为布尔值",
        "is_bool(value) -> bool", ["is_bool(True) = True"],
        min_args=1, max_args=1,
    ),
    "is_int": _create_function_definition(
        "is_int", expr_is_int, "判断是否为整数",
        "is_int(value) -> bool", ["is_int(1) = True"],
        min_args=1, max_args=1,
    ),
    "is_float": _create_function_definition(
        "is_float", expr_is_float, "判断是否为浮点数",
        "is_float(value) -> bool", ["is_float(1.5) = True"],
        min_args=1, max_args=1,
    ),
    "is_number": _create_function_definition(
        "is_number", expr_is_number, "判断是否为数值",
        "is_number(value) -> bool", ["is_number(1.5) = True"],
        min_args=1, max_args=1,
    ),
    "is_string": _create_function_definition(
        "is_string", expr_is_string, "判断是否为字符串",
        "is_string(value) -> bool", ['is_string("hello") = True'],
        min_args=1, max_args=1,
    ),
    "is_list": _create_function_definition(
        "is_list", expr_is_list, "判断是否为列表",
        "is_list(value) -> bool", ["is_list([1, 2]) = True"],
        min_args=1, max_args=1,
    ),
    "is_dict": _create_function_definition(
        "is_dict", expr_is_dict, "判断是否为字典",
        "is_dict(value) -> bool", ['is_dict({"a": 1}) = True'],
        min_args=1, max_args=1,
    ),
    "type_of": _create_function_definition(
        "type_of", expr_type_of, "获取值的类型名称",
        "type_of(value) -> str", ['type_of(1) = "int"'],
        min_args=1, max_args=1,
    ),
    # 类型转换
    "to_bool": _create_function_definition(
        "to_bool", expr_to_bool, "转换为布尔值",
        "to_bool(value) -> bool", ['to_bool("true") = True'],
        min_args=1, max_args=1,
    ),
    "to_int": _create_function_definition(
        "to_int", expr_to_int, "转换为整数",
        "to_int(value, default=0) -> int", ['to_int("123") = 123'],
        min_args=1, max_args=2,
    ),
    "to_float": _create_function_definition(
        "to_float", expr_to_float, "转换为浮点数",
        "to_float(value, default=0.0) -> float", ['to_float("3.14") = 3.14'],
        min_args=1, max_args=2,
    ),
    "to_str": _create_function_definition(
        "to_str", expr_to_str, "转换为字符串",
        "to_str(value) -> str", ['to_str(123) = "123"'],
        min_args=1, max_args=1,
    ),
    # 断言
    "require": _create_function_definition(
        "require", expr_require, "要求值不为空",
        "require(value, message='...') -> any", ['require(name, "Name is required")'],
        min_args=1, max_args=2,
    ),
}


def get_logic_functions() -> dict[str, Callable]:
    """获取所有逻辑函数"""
    return {name: defn.func for name, defn in LOGIC_FUNCTIONS.items()}
