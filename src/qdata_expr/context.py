# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
#
# 本程序为自由软件：你可按 GNU Affero General Public License v3.0 (AGPL-3.0) 
# 条款重新分发或修改；详见 LICENSE 文件。
#
# 任何商业用途必须另行获得商业许可，详见 COMMERCIAL-LICENSE.txt。
# 商业许可咨询：vincent@qeasy.com
#
# 本程序的发布是希望它能有用，但不提供任何保证。

"""
上下文解析器

提供上下文变量的路径访问能力：
- 点号路径访问 (user.name)
- 中括号路径访问 (items[0], data['key'])
- 嵌套路径访问 (users[0].address.city)
- 路径设置和删除
"""

import copy
import re
from typing import Any

from .exceptions import InvalidPathError

# ============================================================
# 路径解析
# ============================================================


class PathParser:
    """路径解析器

    解析路径字符串为路径部分列表。

    支持的路径格式：
    - 点号访问: user.name
    - 中括号索引: items[0]
    - 中括号字符串键: data['key'], data["key"]
    - 混合格式: users[0].address.city
    """

    # 路径部分匹配模式
    PATH_PATTERN = re.compile(
        r"""
        \.?([a-zA-Z_][a-zA-Z0-9_]*)  # .key 或 key
        |
        \[(\d+)\]                      # [index]
        |
        \['([^']+)'\]                  # ['key']
        |
        \["([^"]+)"\]                  # ["key"]
        """,
        re.VERBOSE,
    )

    @classmethod
    def parse(cls, path: str) -> list[str | int]:
        """解析路径为部分列表

        Args:
            path: 路径字符串

        Returns:
            路径部分列表

        Examples:
            >>> PathParser.parse("user.name")
            ['user', 'name']
            >>> PathParser.parse("items[0]")
            ['items', 0]
            >>> PathParser.parse("users[0].address.city")
            ['users', 0, 'address', 'city']
        """
        if not path:
            return []

        parts: list[str | int] = []
        for match in cls.PATH_PATTERN.finditer(path):
            if match.group(1):
                # 属性名
                parts.append(match.group(1))
            elif match.group(2):
                # 数字索引
                parts.append(int(match.group(2)))
            elif match.group(3):
                # 单引号字符串键
                parts.append(match.group(3))
            elif match.group(4):
                # 双引号字符串键
                parts.append(match.group(4))

        return parts

    @classmethod
    def build(cls, parts: list[str | int]) -> str:
        """从部分列表构建路径字符串

        Args:
            parts: 路径部分列表

        Returns:
            路径字符串
        """
        if not parts:
            return ""

        result = []
        for i, part in enumerate(parts):
            if isinstance(part, int):
                result.append(f"[{part}]")
            elif i == 0:
                result.append(part)
            else:
                result.append(f".{part}")

        return "".join(result)


# ============================================================
# 上下文解析器
# ============================================================


class ContextResolver:
    """上下文解析器

    提供上下文变量的路径访问能力。

    使用示例：
        resolver = ContextResolver()

        context = {
            "user": {"name": "John", "age": 30},
            "items": [{"id": 1}, {"id": 2}],
        }

        # 获取值
        name = resolver.resolve("user.name", context)  # "John"
        item_id = resolver.resolve("items[0].id", context)  # 1

        # 检查路径是否存在
        exists = resolver.has("user.name", context)  # True

        # 设置值
        new_context = resolver.set("user.email", "john@example.com", context)
    """

    def __init__(self, path_parser: PathParser | None = None):
        self._parser = path_parser or PathParser()

    def resolve(
        self,
        path: str,
        context: dict[str, Any],
        default: Any = None,
    ) -> Any:
        """解析路径获取值

        Args:
            path: 路径字符串
            context: 上下文字典
            default: 默认值（路径不存在时返回）

        Returns:
            路径对应的值，未找到返回默认值
        """
        if not path:
            return context

        parts = self._parser.parse(path)
        if not parts:
            return default

        current = context
        for part in parts:
            if current is None:
                return default

            try:
                if isinstance(part, int):
                    # 数组索引
                    if isinstance(current, (list, tuple)):
                        if 0 <= part < len(current):
                            current = current[part]
                        else:
                            return default
                    else:
                        return default
                else:
                    # 字典键或对象属性
                    if isinstance(current, dict):
                        if part in current:
                            current = current[part]
                        else:
                            return default
                    elif hasattr(current, part):
                        current = getattr(current, part)
                    else:
                        return default
            except (KeyError, IndexError, TypeError, AttributeError):
                return default

        return current

    def has(self, path: str, context: dict[str, Any]) -> bool:
        """检查路径是否存在

        Args:
            path: 路径字符串
            context: 上下文字典

        Returns:
            是否存在
        """
        sentinel = object()
        return self.resolve(path, context, sentinel) is not sentinel

    def set(
        self,
        path: str,
        value: Any,
        context: dict[str, Any],
        create_missing: bool = True,
    ) -> dict[str, Any]:
        """设置路径的值

        Args:
            path: 路径字符串
            value: 要设置的值
            context: 上下文字典
            create_missing: 是否创建缺失的中间路径

        Returns:
            更新后的上下文（新字典）

        Raises:
            InvalidPathError: 路径无效时抛出
        """
        if not path:
            raise InvalidPathError(path, "路径不能为空")

        parts = self._parser.parse(path)
        if not parts:
            raise InvalidPathError(path, "无法解析路径")

        # 深拷贝以避免修改原字典
        result = copy.deepcopy(context)

        # 导航到父节点
        current = result
        for i, part in enumerate(parts[:-1]):
            if isinstance(part, int):
                # 数组索引
                if not isinstance(current, list):
                    raise InvalidPathError(
                        path,
                        f"期望列表，但得到 {type(current).__name__}",
                    )
                if part >= len(current):
                    if create_missing:
                        # 扩展列表
                        current.extend([None] * (part - len(current) + 1))
                    else:
                        raise InvalidPathError(path, f"索引 {part} 超出范围")
                if current[part] is None and create_missing:
                    # 根据下一个部分创建空容器
                    next_part = parts[i + 1]
                    current[part] = [] if isinstance(next_part, int) else {}
                current = current[part]
            else:
                # 字典键
                if not isinstance(current, dict):
                    raise InvalidPathError(
                        path,
                        f"期望字典，但得到 {type(current).__name__}",
                    )
                if part not in current:
                    if create_missing:
                        # 根据下一个部分创建空容器
                        next_part = parts[i + 1]
                        current[part] = [] if isinstance(next_part, int) else {}
                    else:
                        raise InvalidPathError(path, f"键 '{part}' 不存在")
                current = current[part]

        # 设置最后一个部分的值
        last_part = parts[-1]
        if isinstance(last_part, int):
            if not isinstance(current, list):
                raise InvalidPathError(
                    path,
                    f"期望列表，但得到 {type(current).__name__}",
                )
            if last_part >= len(current):
                if create_missing:
                    current.extend([None] * (last_part - len(current) + 1))
                else:
                    raise InvalidPathError(path, f"索引 {last_part} 超出范围")
            current[last_part] = value
        else:
            if not isinstance(current, dict):
                raise InvalidPathError(
                    path,
                    f"期望字典，但得到 {type(current).__name__}",
                )
            current[last_part] = value

        return result

    def delete(self, path: str, context: dict[str, Any]) -> dict[str, Any]:
        """删除路径

        Args:
            path: 路径字符串
            context: 上下文字典

        Returns:
            更新后的上下文（新字典）
        """
        if not path:
            raise InvalidPathError(path, "路径不能为空")

        parts = self._parser.parse(path)
        if not parts:
            raise InvalidPathError(path, "无法解析路径")

        # 深拷贝
        result = copy.deepcopy(context)

        # 导航到父节点
        current = result
        for part in parts[:-1]:
            if isinstance(part, int):
                if not isinstance(current, (list, tuple)) or part >= len(current):
                    return result  # 路径不存在，直接返回
                current = current[part]
            else:
                if not isinstance(current, dict) or part not in current:
                    return result
                current = current[part]

        # 删除最后一个部分
        last_part = parts[-1]
        if isinstance(last_part, int):
            if isinstance(current, list) and 0 <= last_part < len(current):
                del current[last_part]
        else:
            if isinstance(current, dict) and last_part in current:
                del current[last_part]

        return result

    def merge(
        self,
        context: dict[str, Any],
        updates: dict[str, Any],
        deep: bool = True,
    ) -> dict[str, Any]:
        """合并上下文

        Args:
            context: 原上下文
            updates: 更新内容
            deep: 是否深度合并

        Returns:
            合并后的上下文（新字典）
        """
        if not deep:
            return {**context, **updates}

        result = copy.deepcopy(context)
        self._deep_merge(result, updates)
        return result

    def _deep_merge(self, base: dict, updates: dict) -> None:
        """深度合并（就地修改）"""
        for key, value in updates.items():
            if (
                key in base
                and isinstance(base[key], dict)
                and isinstance(value, dict)
            ):
                self._deep_merge(base[key], value)
            else:
                base[key] = copy.deepcopy(value)

    def flatten(
        self,
        context: dict[str, Any],
        separator: str = ".",
        prefix: str = "",
    ) -> dict[str, Any]:
        """扁平化上下文

        Args:
            context: 上下文字典
            separator: 路径分隔符
            prefix: 路径前缀

        Returns:
            扁平化的字典

        Examples:
            >>> resolver.flatten({"user": {"name": "John"}})
            {"user.name": "John"}
        """
        result = {}

        for key, value in context.items():
            full_key = f"{prefix}{separator}{key}" if prefix else key

            if isinstance(value, dict):
                nested = self.flatten(value, separator, full_key)
                result.update(nested)
            else:
                result[full_key] = value

        return result

    def unflatten(
        self,
        data: dict[str, Any],
        separator: str = ".",
    ) -> dict[str, Any]:
        """反扁平化

        Args:
            data: 扁平化的字典
            separator: 路径分隔符

        Returns:
            嵌套的字典

        Examples:
            >>> resolver.unflatten({"user.name": "John"})
            {"user": {"name": "John"}}
        """
        result: dict[str, Any] = {}

        for key, value in data.items():
            parts = key.split(separator)
            current = result

            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            current[parts[-1]] = value

        return result


# ============================================================
# 便捷函数
# ============================================================


# 默认解析器
_default_resolver = ContextResolver()


def resolve(path: str, context: dict[str, Any], default: Any = None) -> Any:
    """解析路径获取值"""
    return _default_resolver.resolve(path, context, default)


def has_path(path: str, context: dict[str, Any]) -> bool:
    """检查路径是否存在"""
    return _default_resolver.has(path, context)


def set_path(
    path: str,
    value: Any,
    context: dict[str, Any],
    create_missing: bool = True,
) -> dict[str, Any]:
    """设置路径的值"""
    return _default_resolver.set(path, value, context, create_missing)


def delete_path(path: str, context: dict[str, Any]) -> dict[str, Any]:
    """删除路径"""
    return _default_resolver.delete(path, context)


def merge_context(
    context: dict[str, Any],
    updates: dict[str, Any],
    deep: bool = True,
) -> dict[str, Any]:
    """合并上下文"""
    return _default_resolver.merge(context, updates, deep)


def flatten_context(
    context: dict[str, Any],
    separator: str = ".",
) -> dict[str, Any]:
    """扁平化上下文"""
    return _default_resolver.flatten(context, separator)


def unflatten_context(
    data: dict[str, Any],
    separator: str = ".",
) -> dict[str, Any]:
    """反扁平化"""
    return _default_resolver.unflatten(data, separator)
