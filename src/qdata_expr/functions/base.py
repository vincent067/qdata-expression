# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
# AGPL-3.0 License - 商业用途需购买许可
# 详见 LICENSE 和 COMMERCIAL-LICENSE.txt

"""
函数注册基类

提供函数注册和管理的基础设施。
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FunctionCategory(str, Enum):
    """函数分类"""

    MATH = "math"  # 数学函数
    STRING = "string"  # 字符串函数
    DATETIME = "datetime"  # 日期时间函数
    LOGIC = "logic"  # 逻辑函数
    LIST = "list"  # 列表函数
    TYPE = "type"  # 类型转换函数
    AGGREGATE = "aggregate"  # 聚合函数
    CUSTOM = "custom"  # 自定义函数


@dataclass
class FunctionDefinition:
    """函数定义

    描述一个可在表达式中调用的函数。
    """

    name: str  # 函数名
    func: Callable  # 实际函数
    category: FunctionCategory  # 分类
    description: str = ""  # 描述
    signature: str = ""  # 函数签名（用于文档）
    examples: list[str] = field(default_factory=list)  # 使用示例
    min_args: int = 0  # 最小参数数
    max_args: int | None = None  # 最大参数数（None 表示不限）
    safe: bool = True  # 是否安全（用于沙箱）

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """调用函数"""
        return self.func(*args, **kwargs)

    def validate_args(self, args: tuple) -> bool:
        """验证参数数量"""
        if len(args) < self.min_args:
            return False
        if self.max_args is not None and len(args) > self.max_args:
            return False
        return True


class FunctionRegistry:
    """函数注册表

    管理可在表达式中使用的函数。

    使用示例：
        registry = FunctionRegistry()

        # 注册函数
        registry.register("my_func", my_function, FunctionCategory.CUSTOM)

        # 获取函数
        func = registry.get("my_func")

        # 列出函数
        math_funcs = registry.list_by_category(FunctionCategory.MATH)
    """

    def __init__(self):
        self._functions: dict[str, FunctionDefinition] = {}
        self._aliases: dict[str, str] = {}  # 别名 -> 原名

    def register(
        self,
        name: str,
        func: Callable,
        category: FunctionCategory = FunctionCategory.CUSTOM,
        description: str = "",
        signature: str = "",
        examples: list[str] | None = None,
        min_args: int = 0,
        max_args: int | None = None,
        safe: bool = True,
        aliases: list[str] | None = None,
    ) -> None:
        """注册函数

        Args:
            name: 函数名
            func: 实际函数
            category: 分类
            description: 描述
            signature: 函数签名
            examples: 使用示例
            min_args: 最小参数数
            max_args: 最大参数数
            safe: 是否安全
            aliases: 别名列表
        """
        definition = FunctionDefinition(
            name=name,
            func=func,
            category=category,
            description=description,
            signature=signature,
            examples=examples or [],
            min_args=min_args,
            max_args=max_args,
            safe=safe,
        )
        self._functions[name] = definition

        # 注册别名
        if aliases:
            for alias in aliases:
                self._aliases[alias] = name

    def register_definition(self, definition: FunctionDefinition) -> None:
        """注册函数定义"""
        self._functions[definition.name] = definition

    def unregister(self, name: str) -> bool:
        """注销函数

        Args:
            name: 函数名

        Returns:
            是否成功注销
        """
        if name in self._functions:
            del self._functions[name]
            # 移除相关别名
            self._aliases = {
                alias: target
                for alias, target in self._aliases.items()
                if target != name
            }
            return True
        return False

    def get(self, name: str) -> FunctionDefinition | None:
        """获取函数定义

        Args:
            name: 函数名或别名

        Returns:
            函数定义，未找到返回 None
        """
        # 先检查别名
        if name in self._aliases:
            name = self._aliases[name]
        return self._functions.get(name)

    def get_callable(self, name: str) -> Callable | None:
        """获取可调用对象

        Args:
            name: 函数名或别名

        Returns:
            可调用对象，未找到返回 None
        """
        definition = self.get(name)
        if definition:
            return definition.func
        return None

    def has(self, name: str) -> bool:
        """检查函数是否存在

        Args:
            name: 函数名或别名

        Returns:
            是否存在
        """
        if name in self._aliases:
            name = self._aliases[name]
        return name in self._functions

    def list_all(self) -> list[str]:
        """列出所有函数名"""
        return list(self._functions.keys())

    def list_by_category(self, category: FunctionCategory) -> list[str]:
        """按分类列出函数名

        Args:
            category: 分类

        Returns:
            函数名列表
        """
        return [
            name
            for name, definition in self._functions.items()
            if definition.category == category
        ]

    def get_all_callables(self) -> dict[str, Callable]:
        """获取所有可调用对象

        Returns:
            名称到可调用对象的映射
        """
        callables = {}
        for name, definition in self._functions.items():
            callables[name] = definition.func
        # 添加别名
        for alias, target in self._aliases.items():
            if target in self._functions:
                callables[alias] = self._functions[target].func
        return callables

    def get_safe_callables(self) -> dict[str, Callable]:
        """获取安全的可调用对象

        Returns:
            名称到安全可调用对象的映射
        """
        return {
            name: definition.func
            for name, definition in self._functions.items()
            if definition.safe
        }

    def merge(self, other: "FunctionRegistry") -> None:
        """合并另一个注册表

        Args:
            other: 另一个注册表
        """
        for name, definition in other._functions.items():
            self._functions[name] = definition
        self._aliases.update(other._aliases)

    def to_documentation(self) -> dict[str, list[dict]]:
        """生成文档

        Returns:
            按分类组织的函数文档
        """
        docs: dict[str, list[dict]] = {}
        for definition in self._functions.values():
            category = definition.category.value
            if category not in docs:
                docs[category] = []
            docs[category].append({
                "name": definition.name,
                "description": definition.description,
                "signature": definition.signature,
                "examples": definition.examples,
            })
        return docs


# ============================================================
# 全局函数注册表
# ============================================================


_BUILTIN_REGISTRY = FunctionRegistry()


def builtin_function(
    name: str | None = None,
    category: FunctionCategory = FunctionCategory.CUSTOM,
    description: str = "",
    signature: str = "",
    examples: list[str] | None = None,
    min_args: int = 0,
    max_args: int | None = None,
    aliases: list[str] | None = None,
) -> Callable[[Callable], Callable]:
    """内置函数装饰器

    用于注册内置函数。

    使用示例：
        @builtin_function(
            name="my_sum",
            category=FunctionCategory.MATH,
            description="求和",
            signature="my_sum(*values) -> number",
            examples=["my_sum(1, 2, 3) = 6"],
        )
        def my_sum(*values):
            return sum(values)
    """
    def decorator(func: Callable) -> Callable:
        func_name = name or func.__name__
        _BUILTIN_REGISTRY.register(
            name=func_name,
            func=func,
            category=category,
            description=description or func.__doc__ or "",
            signature=signature,
            examples=examples,
            min_args=min_args,
            max_args=max_args,
            aliases=aliases,
        )
        return func

    return decorator


def get_builtin_functions() -> FunctionRegistry:
    """获取内置函数注册表"""
    return _BUILTIN_REGISTRY


def register_builtin_functions(registry: FunctionRegistry) -> None:
    """将内置函数注册到指定注册表"""
    registry.merge(_BUILTIN_REGISTRY)


def get_all_builtin_functions() -> dict[str, Callable]:
    """获取所有内置函数"""
    return _BUILTIN_REGISTRY.get_all_callables()
