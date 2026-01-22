# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
# AGPL-3.0 License - 商业用途需购买许可
# 详见 LICENSE 和 COMMERCIAL-LICENSE.txt

"""
字符串函数库

提供字符串处理相关的内置函数。
"""

import re
import unicodedata
from collections.abc import Callable, Iterable
from typing import Any

from .base import FunctionCategory, FunctionDefinition


def _to_str(value: Any) -> str:
    """转换为字符串"""
    if value is None:
        return ""
    return str(value)


# ============================================================
# 大小写转换
# ============================================================


def expr_upper(value: Any) -> str:
    """转换为大写"""
    return _to_str(value).upper()


def expr_lower(value: Any) -> str:
    """转换为小写"""
    return _to_str(value).lower()


def expr_title(value: Any) -> str:
    """每个单词首字母大写"""
    return _to_str(value).title()


def expr_capitalize(value: Any) -> str:
    """首字母大写"""
    return _to_str(value).capitalize()


def expr_swapcase(value: Any) -> str:
    """大小写互换"""
    return _to_str(value).swapcase()


# ============================================================
# 空白处理
# ============================================================


def expr_trim(value: Any) -> str:
    """去除两端空白"""
    return _to_str(value).strip()


def expr_ltrim(value: Any) -> str:
    """去除左侧空白"""
    return _to_str(value).lstrip()


def expr_rtrim(value: Any) -> str:
    """去除右侧空白"""
    return _to_str(value).rstrip()


def expr_strip(value: Any, chars: str | None = None) -> str:
    """去除两端指定字符"""
    return _to_str(value).strip(chars)


def expr_normalize_space(value: Any) -> str:
    """规范化空白（连续空白变为单个空格）"""
    return " ".join(_to_str(value).split())


# ============================================================
# 字符串操作
# ============================================================


def expr_concat(*values: Any) -> str:
    """连接字符串"""
    return "".join(_to_str(v) for v in values)


def expr_join(values: Iterable, separator: str = "") -> str:
    """使用分隔符连接"""
    return separator.join(_to_str(v) for v in values)


def expr_split(value: Any, separator: str | None = None, maxsplit: int = -1) -> list[str]:
    """分割字符串"""
    return _to_str(value).split(separator, maxsplit)


def expr_substring(value: Any, start: int, end: int | None = None) -> str:
    """获取子串"""
    s = _to_str(value)
    if end is None:
        return s[start:]
    return s[start:end]


def expr_left(value: Any, length: int) -> str:
    """获取左侧 n 个字符"""
    return _to_str(value)[:length]


def expr_right(value: Any, length: int) -> str:
    """获取右侧 n 个字符"""
    return _to_str(value)[-length:] if length > 0 else ""


def expr_mid(value: Any, start: int, length: int) -> str:
    """获取中间子串"""
    s = _to_str(value)
    return s[start:start + length]


def expr_replace(value: Any, old: str, new: str, count: int = -1) -> str:
    """替换字符串"""
    return _to_str(value).replace(old, new, count if count >= 0 else -1)


def expr_repeat(value: Any, times: int) -> str:
    """重复字符串"""
    return _to_str(value) * times


def expr_reverse(value: Any) -> str:
    """反转字符串"""
    return _to_str(value)[::-1]


# ============================================================
# 查找和匹配
# ============================================================


def expr_contains(value: Any, substring: str) -> bool:
    """检查是否包含子串"""
    return substring in _to_str(value)


def expr_starts_with(value: Any, prefix: str) -> bool:
    """检查是否以指定前缀开头"""
    return _to_str(value).startswith(prefix)


def expr_ends_with(value: Any, suffix: str) -> bool:
    """检查是否以指定后缀结尾"""
    return _to_str(value).endswith(suffix)


def expr_find(value: Any, substring: str, start: int = 0) -> int:
    """查找子串位置（未找到返回 -1）"""
    return _to_str(value).find(substring, start)


def expr_index(value: Any, substring: str, start: int = 0) -> int:
    """查找子串位置（未找到抛出异常）"""
    return _to_str(value).index(substring, start)


def expr_count(value: Any, substring: str) -> int:
    """统计子串出现次数"""
    return _to_str(value).count(substring)


def expr_match(value: Any, pattern: str) -> bool:
    """正则匹配（是否匹配）"""
    return bool(re.search(pattern, _to_str(value)))


def expr_regex_find(value: Any, pattern: str) -> str | None:
    """正则查找（返回第一个匹配）"""
    match = re.search(pattern, _to_str(value))
    return match.group(0) if match else None


def expr_regex_findall(value: Any, pattern: str) -> list[str]:
    """正则查找所有匹配"""
    return re.findall(pattern, _to_str(value))


def expr_regex_replace(value: Any, pattern: str, replacement: str) -> str:
    """正则替换"""
    return re.sub(pattern, replacement, _to_str(value))


# ============================================================
# 填充和对齐
# ============================================================


def expr_pad_left(value: Any, width: int, char: str = " ") -> str:
    """左侧填充"""
    return _to_str(value).rjust(width, char[0] if char else " ")


def expr_pad_right(value: Any, width: int, char: str = " ") -> str:
    """右侧填充"""
    return _to_str(value).ljust(width, char[0] if char else " ")


def expr_pad_center(value: Any, width: int, char: str = " ") -> str:
    """居中填充"""
    return _to_str(value).center(width, char[0] if char else " ")


def expr_zfill(value: Any, width: int) -> str:
    """零填充"""
    return _to_str(value).zfill(width)


# ============================================================
# 类型检查
# ============================================================


def expr_is_alpha(value: Any) -> bool:
    """是否全为字母"""
    s = _to_str(value)
    return s.isalpha() if s else False


def expr_is_digit(value: Any) -> bool:
    """是否全为数字"""
    s = _to_str(value)
    return s.isdigit() if s else False


def expr_is_alnum(value: Any) -> bool:
    """是否全为字母或数字"""
    s = _to_str(value)
    return s.isalnum() if s else False


def expr_is_space(value: Any) -> bool:
    """是否全为空白"""
    s = _to_str(value)
    return s.isspace() if s else False


def expr_is_upper(value: Any) -> bool:
    """是否全为大写"""
    s = _to_str(value)
    return s.isupper() if s else False


def expr_is_lower(value: Any) -> bool:
    """是否全为小写"""
    s = _to_str(value)
    return s.islower() if s else False


def expr_is_numeric(value: Any) -> bool:
    """是否为数值字符串"""
    s = _to_str(value).strip()
    if not s:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False


# ============================================================
# 长度和格式
# ============================================================


def expr_len(value: Any) -> int:
    """获取长度

    对于字符串，返回字符数；对于列表、元组、字典等，返回元素个数。
    """
    if hasattr(value, "__len__"):
        return len(value)
    return len(_to_str(value))


def expr_format(template: str, *args: Any, **kwargs: Any) -> str:
    """格式化字符串"""
    return template.format(*args, **kwargs)


def expr_truncate(value: Any, length: int, suffix: str = "...") -> str:
    """截断字符串"""
    s = _to_str(value)
    if len(s) <= length:
        return s
    return s[:length - len(suffix)] + suffix


def expr_normalize(value: Any, form: str = "NFC") -> str:
    """Unicode 规范化"""
    return unicodedata.normalize(form, _to_str(value))


# ============================================================
# 编码转换
# ============================================================


def expr_encode(value: Any, encoding: str = "utf-8") -> bytes:
    """编码为字节"""
    return _to_str(value).encode(encoding)


def expr_decode(value: bytes, encoding: str = "utf-8") -> str:
    """解码字节为字符串"""
    if isinstance(value, bytes):
        return value.decode(encoding)
    return str(value)


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
        category=FunctionCategory.STRING,
        description=description,
        signature=signature,
        examples=examples,
        min_args=min_args,
        max_args=max_args,
    )


# 字符串函数集合
STRING_FUNCTIONS: dict[str, FunctionDefinition] = {
    # 大小写转换
    "upper": _create_function_definition(
        "upper", expr_upper, "转换为大写",
        "upper(value) -> str", ['upper("hello") = "HELLO"'],
        min_args=1, max_args=1,
    ),
    "lower": _create_function_definition(
        "lower", expr_lower, "转换为小写",
        "lower(value) -> str", ['lower("HELLO") = "hello"'],
        min_args=1, max_args=1,
    ),
    "title": _create_function_definition(
        "title", expr_title, "每个单词首字母大写",
        "title(value) -> str", ['title("hello world") = "Hello World"'],
        min_args=1, max_args=1,
    ),
    "capitalize": _create_function_definition(
        "capitalize", expr_capitalize, "首字母大写",
        "capitalize(value) -> str", ['capitalize("hello") = "Hello"'],
        min_args=1, max_args=1,
    ),
    "swapcase": _create_function_definition(
        "swapcase", expr_swapcase, "大小写互换",
        "swapcase(value) -> str", ['swapcase("HeLLo") = "hEllO"'],
        min_args=1, max_args=1,
    ),
    # 空白处理
    "trim": _create_function_definition(
        "trim", expr_trim, "去除两端空白",
        "trim(value) -> str", ['trim("  hello  ") = "hello"'],
        min_args=1, max_args=1,
    ),
    "ltrim": _create_function_definition(
        "ltrim", expr_ltrim, "去除左侧空白",
        "ltrim(value) -> str", ['ltrim("  hello") = "hello"'],
        min_args=1, max_args=1,
    ),
    "rtrim": _create_function_definition(
        "rtrim", expr_rtrim, "去除右侧空白",
        "rtrim(value) -> str", ['rtrim("hello  ") = "hello"'],
        min_args=1, max_args=1,
    ),
    "strip": _create_function_definition(
        "strip", expr_strip, "去除两端指定字符",
        "strip(value, chars=None) -> str", ['strip("##hello##", "#") = "hello"'],
        min_args=1, max_args=2,
    ),
    "normalize_space": _create_function_definition(
        "normalize_space", expr_normalize_space, "规范化空白",
        "normalize_space(value) -> str", ['normalize_space("hello   world") = "hello world"'],
        min_args=1, max_args=1,
    ),
    # 字符串操作
    "concat": _create_function_definition(
        "concat", expr_concat, "连接字符串",
        "concat(*values) -> str", ['concat("a", "b", "c") = "abc"'],
        min_args=1,
    ),
    "join": _create_function_definition(
        "join", expr_join, "使用分隔符连接",
        "join(values, separator='') -> str", ['join(["a", "b"], "-") = "a-b"'],
        min_args=1, max_args=2,
    ),
    "split": _create_function_definition(
        "split", expr_split, "分割字符串",
        "split(value, separator=None) -> list", ['split("a,b,c", ",") = ["a", "b", "c"]'],
        min_args=1, max_args=3,
    ),
    "substring": _create_function_definition(
        "substring", expr_substring, "获取子串",
        "substring(value, start, end=None) -> str", ['substring("hello", 1, 4) = "ell"'],
        min_args=2, max_args=3,
    ),
    "left": _create_function_definition(
        "left", expr_left, "获取左侧 n 个字符",
        "left(value, length) -> str", ['left("hello", 3) = "hel"'],
        min_args=2, max_args=2,
    ),
    "right": _create_function_definition(
        "right", expr_right, "获取右侧 n 个字符",
        "right(value, length) -> str", ['right("hello", 3) = "llo"'],
        min_args=2, max_args=2,
    ),
    "mid": _create_function_definition(
        "mid", expr_mid, "获取中间子串",
        "mid(value, start, length) -> str", ['mid("hello", 1, 3) = "ell"'],
        min_args=3, max_args=3,
    ),
    "replace": _create_function_definition(
        "replace", expr_replace, "替换字符串",
        "replace(value, old, new, count=-1) -> str", ['replace("hello", "l", "L") = "heLLo"'],
        min_args=3, max_args=4,
    ),
    "repeat": _create_function_definition(
        "repeat", expr_repeat, "重复字符串",
        "repeat(value, times) -> str", ['repeat("ab", 3) = "ababab"'],
        min_args=2, max_args=2,
    ),
    "reverse": _create_function_definition(
        "reverse", expr_reverse, "反转字符串",
        "reverse(value) -> str", ['reverse("hello") = "olleh"'],
        min_args=1, max_args=1,
    ),
    # 查找和匹配
    "contains": _create_function_definition(
        "contains", expr_contains, "检查是否包含子串",
        "contains(value, substring) -> bool", ['contains("hello", "ell") = True'],
        min_args=2, max_args=2,
    ),
    "starts_with": _create_function_definition(
        "starts_with", expr_starts_with, "检查是否以指定前缀开头",
        "starts_with(value, prefix) -> bool", ['starts_with("hello", "he") = True'],
        min_args=2, max_args=2,
    ),
    "ends_with": _create_function_definition(
        "ends_with", expr_ends_with, "检查是否以指定后缀结尾",
        "ends_with(value, suffix) -> bool", ['ends_with("hello", "lo") = True'],
        min_args=2, max_args=2,
    ),
    "find": _create_function_definition(
        "find", expr_find, "查找子串位置",
        "find(value, substring, start=0) -> int", ['find("hello", "l") = 2'],
        min_args=2, max_args=3,
    ),
    "str_count": _create_function_definition(
        "str_count", expr_count, "统计子串出现次数",
        "str_count(value, substring) -> int", ['str_count("hello", "l") = 2'],
        min_args=2, max_args=2,
    ),
    "match": _create_function_definition(
        "match", expr_match, "正则匹配",
        "match(value, pattern) -> bool", ['match("hello123", r"\\d+") = True'],
        min_args=2, max_args=2,
    ),
    "regex_find": _create_function_definition(
        "regex_find", expr_regex_find, "正则查找",
        "regex_find(value, pattern) -> str|None", ['regex_find("hello123", r"\\d+") = "123"'],
        min_args=2, max_args=2,
    ),
    "regex_findall": _create_function_definition(
        "regex_findall", expr_regex_findall, "正则查找所有匹配",
        "regex_findall(value, pattern) -> list", ['regex_findall("a1b2c3", r"\\d") = ["1","2","3"]'],
        min_args=2, max_args=2,
    ),
    "regex_replace": _create_function_definition(
        "regex_replace", expr_regex_replace, "正则替换",
        "regex_replace(value, pattern, replacement) -> str", ['regex_replace("a1b2", r"\\d", "X") = "aXbX"'],
        min_args=3, max_args=3,
    ),
    # 填充和对齐
    "pad_left": _create_function_definition(
        "pad_left", expr_pad_left, "左侧填充",
        "pad_left(value, width, char=' ') -> str", ['pad_left("5", 3, "0") = "005"'],
        min_args=2, max_args=3,
    ),
    "pad_right": _create_function_definition(
        "pad_right", expr_pad_right, "右侧填充",
        "pad_right(value, width, char=' ') -> str", ['pad_right("5", 3, "0") = "500"'],
        min_args=2, max_args=3,
    ),
    "pad_center": _create_function_definition(
        "pad_center", expr_pad_center, "居中填充",
        "pad_center(value, width, char=' ') -> str", ['pad_center("hi", 6, "-") = "--hi--"'],
        min_args=2, max_args=3,
    ),
    "zfill": _create_function_definition(
        "zfill", expr_zfill, "零填充",
        "zfill(value, width) -> str", ['zfill("42", 5) = "00042"'],
        min_args=2, max_args=2,
    ),
    # 类型检查
    "is_alpha": _create_function_definition(
        "is_alpha", expr_is_alpha, "是否全为字母",
        "is_alpha(value) -> bool", ['is_alpha("hello") = True'],
        min_args=1, max_args=1,
    ),
    "is_digit": _create_function_definition(
        "is_digit", expr_is_digit, "是否全为数字",
        "is_digit(value) -> bool", ['is_digit("123") = True'],
        min_args=1, max_args=1,
    ),
    "is_alnum": _create_function_definition(
        "is_alnum", expr_is_alnum, "是否全为字母或数字",
        "is_alnum(value) -> bool", ['is_alnum("abc123") = True'],
        min_args=1, max_args=1,
    ),
    "is_numeric": _create_function_definition(
        "is_numeric", expr_is_numeric, "是否为数值字符串",
        "is_numeric(value) -> bool", ['is_numeric("3.14") = True'],
        min_args=1, max_args=1,
    ),
    # 长度和格式
    "len": _create_function_definition(
        "len", expr_len, "获取长度",
        "len(value) -> int", ['len("hello") = 5'],
        min_args=1, max_args=1,
    ),
    "format": _create_function_definition(
        "format", expr_format, "格式化字符串",
        "format(template, *args, **kwargs) -> str", ['format("{} {}", "hello", "world") = "hello world"'],
        min_args=1,
    ),
    "truncate": _create_function_definition(
        "truncate", expr_truncate, "截断字符串",
        "truncate(value, length, suffix='...') -> str", ['truncate("hello world", 8) = "hello..."'],
        min_args=2, max_args=3,
    ),
}


def get_string_functions() -> dict[str, Callable]:
    """获取所有字符串函数"""
    return {name: defn.func for name, defn in STRING_FUNCTIONS.items()}
