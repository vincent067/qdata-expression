"""
列表函数库

提供列表和集合处理相关的内置函数。
"""

from collections.abc import Callable, Iterable
from typing import Any

from .base import FunctionCategory, FunctionDefinition


def _to_list(value: Any) -> list:
    """转换为列表"""
    if isinstance(value, list):
        return value
    if isinstance(value, (tuple, set, frozenset)):
        return list(value)
    if isinstance(value, dict):
        return list(value.items())
    if isinstance(value, str):
        return [value]  # 不拆分字符串
    if hasattr(value, "__iter__"):
        return list(value)
    return [value]


# ============================================================
# 基础操作
# ============================================================


def expr_length(value: Any) -> int:
    """获取长度"""
    return len(value) if hasattr(value, "__len__") else 0


def expr_first(value: Any, default: Any = None) -> Any:
    """获取第一个元素"""
    lst = _to_list(value)
    return lst[0] if lst else default


def expr_last(value: Any, default: Any = None) -> Any:
    """获取最后一个元素"""
    lst = _to_list(value)
    return lst[-1] if lst else default


def expr_nth(value: Any, index: int, default: Any = None) -> Any:
    """获取第 n 个元素（从 0 开始）"""
    lst = _to_list(value)
    try:
        return lst[index]
    except IndexError:
        return default


def expr_take(value: Any, count: int) -> list:
    """获取前 n 个元素"""
    return _to_list(value)[:count]


def expr_skip(value: Any, count: int) -> list:
    """跳过前 n 个元素"""
    return _to_list(value)[count:]


def expr_slice(value: Any, start: int, end: int | None = None, step: int = 1) -> list:
    """切片"""
    return _to_list(value)[start:end:step]


def expr_reverse_list(value: Any) -> list:
    """反转列表"""
    return _to_list(value)[::-1]


# ============================================================
# 查找和判断
# ============================================================


def expr_contains_item(value: Any, item: Any) -> bool:
    """检查是否包含元素"""
    return item in _to_list(value)


def expr_index_of(value: Any, item: Any) -> int:
    """查找元素位置（未找到返回 -1）"""
    lst = _to_list(value)
    try:
        return lst.index(item)
    except ValueError:
        return -1


def expr_last_index_of(value: Any, item: Any) -> int:
    """查找元素最后出现的位置（未找到返回 -1）"""
    lst = _to_list(value)
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] == item:
            return i
    return -1


def expr_count_item(value: Any, item: Any) -> int:
    """统计元素出现次数"""
    return _to_list(value).count(item)


def expr_all_match(value: Any, condition: Callable | None = None) -> bool:
    """检查所有元素是否满足条件"""
    lst = _to_list(value)
    if condition is None:
        return all(lst)
    return all(condition(item) for item in lst)


def expr_any_match(value: Any, condition: Callable | None = None) -> bool:
    """检查是否有元素满足条件"""
    lst = _to_list(value)
    if condition is None:
        return any(lst)
    return any(condition(item) for item in lst)


def expr_none_match(value: Any, condition: Callable | None = None) -> bool:
    """检查是否没有元素满足条件"""
    return not expr_any_match(value, condition)


# ============================================================
# 转换操作
# ============================================================


def expr_map(value: Any, func: Callable) -> list:
    """对每个元素应用函数"""
    return [func(item) for item in _to_list(value)]


def expr_filter_list(value: Any, condition: Callable) -> list:
    """过滤元素"""
    return [item for item in _to_list(value) if condition(item)]


def expr_reject(value: Any, condition: Callable) -> list:
    """排除满足条件的元素"""
    return [item for item in _to_list(value) if not condition(item)]


def expr_reduce(value: Any, func: Callable, initial: Any = None) -> Any:
    """归约"""
    from functools import reduce
    lst = _to_list(value)
    if initial is not None:
        return reduce(func, lst, initial)
    return reduce(func, lst) if lst else initial


def expr_flat(value: Any) -> list:
    """扁平化一层"""
    result = []
    for item in _to_list(value):
        if isinstance(item, (list, tuple)):
            result.extend(item)
        else:
            result.append(item)
    return result


def expr_flatten(value: Any, depth: int = -1) -> list:
    """深度扁平化"""
    def _flatten(lst: list, current_depth: int) -> list:
        result = []
        for item in lst:
            if isinstance(item, (list, tuple)) and (depth == -1 or current_depth < depth):
                result.extend(_flatten(list(item), current_depth + 1))
            else:
                result.append(item)
        return result
    return _flatten(_to_list(value), 0)


def expr_chunk(value: Any, size: int) -> list[list]:
    """分块"""
    lst = _to_list(value)
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def expr_zip_lists(*lists: Any) -> list[tuple]:
    """压缩多个列表"""
    return list(zip(*[_to_list(lst) for lst in lists]))


# ============================================================
# 排序
# ============================================================


def expr_sort(value: Any, reverse: bool = False) -> list:
    """排序"""
    return sorted(_to_list(value), reverse=reverse)


def expr_sort_by(value: Any, key: str | Callable, reverse: bool = False) -> list:
    """按键排序"""
    lst = _to_list(value)
    if isinstance(key, str):
        # 按字典键或对象属性排序
        def get_key(item: Any) -> Any:
            if isinstance(item, dict):
                return item.get(key)
            return getattr(item, key, None)
        return sorted(lst, key=get_key, reverse=reverse)
    return sorted(lst, key=key, reverse=reverse)


# ============================================================
# 去重和集合操作
# ============================================================


def expr_unique(value: Any) -> list:
    """去重（保持顺序）"""
    seen = set()
    result = []
    for item in _to_list(value):
        # 尝试将 item 转为可哈希类型
        try:
            if item not in seen:
                seen.add(item)
                result.append(item)
        except TypeError:
            # 不可哈希的类型，使用慢路径
            if item not in result:
                result.append(item)
    return result


def expr_unique_by(value: Any, key: str | Callable) -> list:
    """按键去重（保持顺序）"""
    seen = set()
    result = []
    for item in _to_list(value):
        if isinstance(key, str):
            k = item.get(key) if isinstance(item, dict) else getattr(item, key, None)
        else:
            k = key(item)
        try:
            if k not in seen:
                seen.add(k)
                result.append(item)
        except TypeError:
            if k not in [
                (item.get(key) if isinstance(item, dict) else getattr(item, key, None))
                if isinstance(key, str) else key(item)
                for item in result
            ]:
                result.append(item)
    return result


def expr_union(*lists: Any) -> list:
    """并集（保持顺序）"""
    result = []
    seen = set()
    for lst in lists:
        for item in _to_list(lst):
            try:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            except TypeError:
                if item not in result:
                    result.append(item)
    return result


def expr_intersection(*lists: Any) -> list:
    """交集"""
    if not lists:
        return []
    lists = [_to_list(lst) for lst in lists]
    result = lists[0]
    for lst in lists[1:]:
        result = [item for item in result if item in lst]
    return result


def expr_difference(list1: Any, list2: Any) -> list:
    """差集（在 list1 中但不在 list2 中）"""
    lst1 = _to_list(list1)
    lst2 = _to_list(list2)
    return [item for item in lst1 if item not in lst2]


# ============================================================
# 聚合
# ============================================================


def expr_group_by(value: Any, key: str | Callable) -> dict:
    """分组"""
    result: dict = {}
    for item in _to_list(value):
        if isinstance(key, str):
            k = item.get(key) if isinstance(item, dict) else getattr(item, key, None)
        else:
            k = key(item)
        if k not in result:
            result[k] = []
        result[k].append(item)
    return result


def expr_count_by(value: Any, key: str | Callable) -> dict:
    """按键计数"""
    result: dict = {}
    for item in _to_list(value):
        if isinstance(key, str):
            k = item.get(key) if isinstance(item, dict) else getattr(item, key, None)
        else:
            k = key(item)
        result[k] = result.get(k, 0) + 1
    return result


def expr_sum_by(value: Any, key: str | Callable) -> float:
    """按键求和"""
    total = 0
    for item in _to_list(value):
        if isinstance(key, str):
            v = item.get(key, 0) if isinstance(item, dict) else getattr(item, key, 0)
        else:
            v = key(item)
        total += v or 0
    return total


# ============================================================
# 构造
# ============================================================


def expr_range(start: int, end: int | None = None, step: int = 1) -> list:
    """生成数字范围"""
    if end is None:
        return list(range(start))
    return list(range(start, end, step))


def expr_repeat_item(item: Any, times: int) -> list:
    """重复元素"""
    return [item] * times


def expr_to_set(value: Any) -> set:
    """转换为集合"""
    return set(_to_list(value))


def expr_to_list(value: Any) -> list:
    """转换为列表"""
    return _to_list(value)


# ============================================================
# 字典相关
# ============================================================


def expr_keys(value: dict) -> list:
    """获取字典的键"""
    if isinstance(value, dict):
        return list(value.keys())
    return []


def expr_values(value: dict) -> list:
    """获取字典的值"""
    if isinstance(value, dict):
        return list(value.values())
    return []


def expr_items(value: dict) -> list[tuple]:
    """获取字典的键值对"""
    if isinstance(value, dict):
        return list(value.items())
    return []


def expr_get(value: Any, key: str | int, default: Any = None) -> Any:
    """获取字典或列表的值"""
    if isinstance(value, dict):
        return value.get(key, default)
    if isinstance(value, (list, tuple)):
        try:
            return value[key]
        except (IndexError, TypeError):
            return default
    return default


def expr_pluck(value: Any, key: str) -> list:
    """从对象列表中提取指定键的值"""
    result = []
    for item in _to_list(value):
        if isinstance(item, dict):
            result.append(item.get(key))
        else:
            result.append(getattr(item, key, None))
    return result


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
        category=FunctionCategory.LIST,
        description=description,
        signature=signature,
        examples=examples,
        min_args=min_args,
        max_args=max_args,
    )


# 列表函数集合
LIST_FUNCTIONS: dict[str, FunctionDefinition] = {
    # 基础操作
    "length": _create_function_definition(
        "length", expr_length, "获取长度",
        "length(value) -> int", ["length([1, 2, 3]) = 3"],
        min_args=1, max_args=1,
    ),
    "first": _create_function_definition(
        "first", expr_first, "获取第一个元素",
        "first(value, default=None) -> any", ["first([1, 2, 3]) = 1"],
        min_args=1, max_args=2,
    ),
    "last": _create_function_definition(
        "last", expr_last, "获取最后一个元素",
        "last(value, default=None) -> any", ["last([1, 2, 3]) = 3"],
        min_args=1, max_args=2,
    ),
    "nth": _create_function_definition(
        "nth", expr_nth, "获取第 n 个元素",
        "nth(value, index, default=None) -> any", ["nth([1, 2, 3], 1) = 2"],
        min_args=2, max_args=3,
    ),
    "take": _create_function_definition(
        "take", expr_take, "获取前 n 个元素",
        "take(value, count) -> list", ["take([1, 2, 3, 4], 2) = [1, 2]"],
        min_args=2, max_args=2,
    ),
    "skip": _create_function_definition(
        "skip", expr_skip, "跳过前 n 个元素",
        "skip(value, count) -> list", ["skip([1, 2, 3, 4], 2) = [3, 4]"],
        min_args=2, max_args=2,
    ),
    "slice": _create_function_definition(
        "slice", expr_slice, "切片",
        "slice(value, start, end=None, step=1) -> list",
        ["slice([1, 2, 3, 4], 1, 3) = [2, 3]"],
        min_args=2, max_args=4,
    ),
    "reverse_list": _create_function_definition(
        "reverse_list", expr_reverse_list, "反转列表",
        "reverse_list(value) -> list", ["reverse_list([1, 2, 3]) = [3, 2, 1]"],
        min_args=1, max_args=1,
    ),
    # 查找和判断
    "contains_item": _create_function_definition(
        "contains_item", expr_contains_item, "检查是否包含元素",
        "contains_item(value, item) -> bool", ["contains_item([1, 2, 3], 2) = True"],
        min_args=2, max_args=2,
    ),
    "index_of": _create_function_definition(
        "index_of", expr_index_of, "查找元素位置",
        "index_of(value, item) -> int", ["index_of([1, 2, 3], 2) = 1"],
        min_args=2, max_args=2,
    ),
    "count_item": _create_function_definition(
        "count_item", expr_count_item, "统计元素出现次数",
        "count_item(value, item) -> int", ["count_item([1, 2, 2, 3], 2) = 2"],
        min_args=2, max_args=2,
    ),
    # 排序
    "sort": _create_function_definition(
        "sort", expr_sort, "排序",
        "sort(value, reverse=False) -> list", ["sort([3, 1, 2]) = [1, 2, 3]"],
        min_args=1, max_args=2,
    ),
    "sort_by": _create_function_definition(
        "sort_by", expr_sort_by, "按键排序",
        "sort_by(value, key, reverse=False) -> list",
        ['sort_by([{"a": 2}, {"a": 1}], "a") = [{"a": 1}, {"a": 2}]'],
        min_args=2, max_args=3,
    ),
    # 去重和集合操作
    "unique": _create_function_definition(
        "unique", expr_unique, "去重",
        "unique(value) -> list", ["unique([1, 2, 2, 3]) = [1, 2, 3]"],
        min_args=1, max_args=1,
    ),
    "union": _create_function_definition(
        "union", expr_union, "并集",
        "union(*lists) -> list", ["union([1, 2], [2, 3]) = [1, 2, 3]"],
        min_args=1,
    ),
    "intersection": _create_function_definition(
        "intersection", expr_intersection, "交集",
        "intersection(*lists) -> list", ["intersection([1, 2, 3], [2, 3, 4]) = [2, 3]"],
        min_args=1,
    ),
    "difference": _create_function_definition(
        "difference", expr_difference, "差集",
        "difference(list1, list2) -> list", ["difference([1, 2, 3], [2]) = [1, 3]"],
        min_args=2, max_args=2,
    ),
    # 扁平化
    "flat": _create_function_definition(
        "flat", expr_flat, "扁平化一层",
        "flat(value) -> list", ["flat([[1, 2], [3, 4]]) = [1, 2, 3, 4]"],
        min_args=1, max_args=1,
    ),
    "flatten": _create_function_definition(
        "flatten", expr_flatten, "深度扁平化",
        "flatten(value, depth=-1) -> list",
        ["flatten([[1, [2, 3]], [4]]) = [1, 2, 3, 4]"],
        min_args=1, max_args=2,
    ),
    "chunk": _create_function_definition(
        "chunk", expr_chunk, "分块",
        "chunk(value, size) -> list", ["chunk([1, 2, 3, 4, 5], 2) = [[1, 2], [3, 4], [5]]"],
        min_args=2, max_args=2,
    ),
    # 聚合
    "group_by": _create_function_definition(
        "group_by", expr_group_by, "分组",
        'group_by(value, key) -> dict',
        ['group_by([{"type": "a", "v": 1}, {"type": "a", "v": 2}], "type")'],
        min_args=2, max_args=2,
    ),
    # 构造
    "range": _create_function_definition(
        "range", expr_range, "生成数字范围",
        "range(start, end=None, step=1) -> list",
        ["range(5) = [0, 1, 2, 3, 4]", "range(1, 5) = [1, 2, 3, 4]"],
        min_args=1, max_args=3,
    ),
    "repeat_item": _create_function_definition(
        "repeat_item", expr_repeat_item, "重复元素",
        "repeat_item(item, times) -> list", ['repeat_item("a", 3) = ["a", "a", "a"]'],
        min_args=2, max_args=2,
    ),
    # 字典相关
    "keys": _create_function_definition(
        "keys", expr_keys, "获取字典的键",
        "keys(value) -> list", ['keys({"a": 1, "b": 2}) = ["a", "b"]'],
        min_args=1, max_args=1,
    ),
    "values": _create_function_definition(
        "values", expr_values, "获取字典的值",
        "values(value) -> list", ['values({"a": 1, "b": 2}) = [1, 2]'],
        min_args=1, max_args=1,
    ),
    "items": _create_function_definition(
        "items", expr_items, "获取字典的键值对",
        "items(value) -> list", ['items({"a": 1}) = [("a", 1)]'],
        min_args=1, max_args=1,
    ),
    "get": _create_function_definition(
        "get", expr_get, "获取字典或列表的值",
        "get(value, key, default=None) -> any",
        ['get({"a": 1}, "a") = 1', "get([1, 2, 3], 0) = 1"],
        min_args=2, max_args=3,
    ),
    "pluck": _create_function_definition(
        "pluck", expr_pluck, "从对象列表中提取指定键的值",
        "pluck(value, key) -> list",
        ['pluck([{"name": "a"}, {"name": "b"}], "name") = ["a", "b"]'],
        min_args=2, max_args=2,
    ),
}


def get_list_functions() -> dict[str, Callable]:
    """获取所有列表函数"""
    return {name: defn.func for name, defn in LIST_FUNCTIONS.items()}
