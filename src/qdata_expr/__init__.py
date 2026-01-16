"""
内置函数库

提供表达式引擎使用的内置函数。

函数分类：
- 数学函数 (math_funcs)
- 字符串函数 (string_funcs)
- 日期时间函数 (datetime_funcs)
- 逻辑函数 (logic_funcs)
- 列表函数 (list_funcs)
"""

from .base import (
    FunctionCategory,
    FunctionDefinition,
    FunctionRegistry,
    builtin_function,
    get_builtin_functions,
    get_all_builtin_functions,
)
from .datetime_funcs import DATETIME_FUNCTIONS
from .list_funcs import LIST_FUNCTIONS
from .logic_funcs import LOGIC_FUNCTIONS
from .math_funcs import MATH_FUNCTIONS
from .string_funcs import STRING_FUNCTIONS

__all__ = [
    # 基础类
    "FunctionCategory",
    "FunctionDefinition",
    "FunctionRegistry",
    "builtin_function",
    "get_builtin_functions",
    "get_all_builtin_functions",
    # 函数集
    "MATH_FUNCTIONS",
    "STRING_FUNCTIONS",
    "DATETIME_FUNCTIONS",
    "LOGIC_FUNCTIONS",
    "LIST_FUNCTIONS",
]
