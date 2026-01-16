"""
内置函数库

提供表达式引擎使用的内置函数。

函数分类：
- 数学函数 (math_funcs): 数学运算和聚合函数
- 字符串函数 (string_funcs): 字符串处理和格式化
- 日期时间函数 (datetime_funcs): 日期时间处理和计算
- 逻辑函数 (logic_funcs): 逻辑判断和条件处理
- 列表函数 (list_funcs): 列表和集合操作

示例:
    >>> from qdata_expr.functions import MATH_FUNCTIONS, get_all_builtin_functions
    >>> 
    >>> # 获取所有数学函数
    >>> math_funcs = get_all_builtin_functions()
    >>> print(math_funcs.keys())
    
    >>> # 使用函数
    >>> from qdata_expr import evaluate
    >>> result = evaluate("abs(-5) + round(3.14, 1)")
    >>> print(result)  # 8.1
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
