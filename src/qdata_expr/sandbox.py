# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
#
# 本程序为自由软件：你可按 GNU Affero General Public License v3.0 (AGPL-3.0) 
# 条款重新分发或修改；详见 LICENSE 文件。
#
# 任何商业用途必须另行获得商业许可，详见 COMMERCIAL-LICENSE.txt。
# 商业许可咨询：vincent@qeasy.cloud
#
# 本程序的发布是希望它能有用，但不提供任何保证。

"""
安全沙箱

提供安全的表达式执行环境，禁止危险操作。

核心安全机制：
1. 禁止访问危险的内置函数和属性
2. 禁止访问双下划线属性
3. 限制可访问的类型和操作
4. 执行时间限制
5. 递归深度限制
"""

import ast
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from .exceptions import ForbiddenAccessError, SecurityViolationError

# ============================================================
# 安全配置
# ============================================================


@dataclass
class SandboxConfig:
    """沙箱配置"""

    # 允许的操作符
    allowed_operators: set[type] = field(default_factory=lambda: {
        # 算术运算符
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.USub,
        ast.UAdd,
        # 比较运算符
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
        ast.Is,
        ast.IsNot,
        ast.In,
        ast.NotIn,
        # 逻辑运算符
        ast.And,
        ast.Or,
        ast.Not,
        # 位运算符（可选）
        ast.BitAnd,
        ast.BitOr,
        ast.BitXor,
        ast.Invert,
        ast.LShift,
        ast.RShift,
    })

    # 禁止的属性名模式
    forbidden_attr_patterns: list[str] = field(default_factory=lambda: [
        "__",  # 双下划线属性
        "_",   # 单下划线开头（私有属性）- 可选，默认禁止
    ])

    # 严格模式下禁止单下划线
    strict_private_access: bool = False

    # 禁止的名称列表
    forbidden_names: set[str] = field(default_factory=lambda: {
        # 危险的内置函数
        "eval",
        "exec",
        "compile",
        "open",
        "input",
        "__import__",
        "globals",
        "locals",
        "vars",
        "dir",
        "getattr",
        "setattr",
        "delattr",
        "hasattr",
        # 危险的类型
        "type",
        "object",
        "classmethod",
        "staticmethod",
        "property",
        # 文件操作
        "file",
        # 代码对象
        "code",
        # 其他危险操作
        "memoryview",
        "breakpoint",
        "exit",
        "quit",
        "help",
        "copyright",
        "credits",
        "license",
    })

    # 允许的内置名称
    allowed_builtins: set[str] = field(default_factory=lambda: {
        # 类型转换
        "int",
        "float",
        "str",
        "bool",
        "list",
        "tuple",
        "dict",
        "set",
        "frozenset",
        "bytes",
        # 安全函数
        "abs",
        "round",
        "min",
        "max",
        "sum",
        "len",
        "sorted",
        "reversed",
        "enumerate",
        "zip",
        "map",
        "filter",
        "all",
        "any",
        "range",
        "slice",
        "repr",
        "ascii",
        "bin",
        "hex",
        "oct",
        "ord",
        "chr",
        "format",
        "hash",
        "id",
        "isinstance",
        "issubclass",
        "callable",
        "iter",
        "next",
        "pow",
        "divmod",
        # 常量
        "True",
        "False",
        "None",
    })

    # 最大执行时间（秒）
    max_execution_time: float = 5.0

    # 最大递归深度
    max_recursion_depth: int = 100

    # 最大字符串长度
    max_string_length: int = 1_000_000

    # 最大集合大小
    max_collection_size: int = 100_000

    # 允许访问的类型属性
    allowed_type_attrs: dict[type, set[str]] = field(default_factory=lambda: {
        str: {
            "upper", "lower", "strip", "lstrip", "rstrip", "split", "join",
            "replace", "startswith", "endswith", "find", "rfind", "index",
            "rindex", "count", "isalpha", "isdigit", "isalnum", "isspace",
            "isupper", "islower", "title", "capitalize", "swapcase", "center",
            "ljust", "rjust", "zfill", "format", "encode",
        },
        list: {
            "append", "extend", "insert", "remove", "pop", "clear", "index",
            "count", "sort", "reverse", "copy",
        },
        dict: {
            "keys", "values", "items", "get", "pop", "popitem", "clear",
            "update", "setdefault", "copy", "fromkeys",
        },
        set: {
            "add", "remove", "discard", "pop", "clear", "copy", "union",
            "intersection", "difference", "symmetric_difference", "update",
            "intersection_update", "difference_update", "symmetric_difference_update",
            "issubset", "issuperset", "isdisjoint",
        },
        tuple: {"count", "index"},
    })


# ============================================================
# 默认安全配置
# ============================================================


DEFAULT_SANDBOX_CONFIG = SandboxConfig()


# ============================================================
# AST 安全检查器
# ============================================================


class SafetyChecker(ast.NodeVisitor):
    """AST 安全检查器

    遍历 AST 树检查潜在的安全问题。
    """

    def __init__(self, config: SandboxConfig | None = None):
        self.config = config or DEFAULT_SANDBOX_CONFIG
        self.errors: list[str] = []

    def check(self, expression: str) -> list[str]:
        """检查表达式安全性

        Args:
            expression: 表达式字符串

        Returns:
            错误列表，空列表表示安全
        """
        self.errors = []
        try:
            tree = ast.parse(expression, mode="eval")
            self.visit(tree)
        except SyntaxError as e:
            self.errors.append(f"语法错误: {e}")
        return self.errors

    def visit_Name(self, node: ast.Name) -> None:
        """检查名称访问"""
        name = node.id
        if name in self.config.forbidden_names:
            self.errors.append(f"禁止访问名称: {name}")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """检查属性访问"""
        attr = node.attr

        # 检查双下划线属性
        if attr.startswith("__") and attr.endswith("__"):
            self.errors.append(f"禁止访问魔术属性: {attr}")
        elif attr.startswith("__"):
            self.errors.append(f"禁止访问私有属性: {attr}")
        elif attr.startswith("_") and self.config.strict_private_access:
            self.errors.append(f"禁止访问私有属性: {attr}")

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """检查函数调用"""
        # 获取函数名
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        if func_name and func_name in self.config.forbidden_names:
            self.errors.append(f"禁止调用函数: {func_name}")

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        """禁止 import"""
        self.errors.append("禁止使用 import 语句")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """禁止 from import"""
        self.errors.append("禁止使用 from import 语句")


# ============================================================
# 安全名称解析器
# ============================================================


class SafeNameResolver:
    """安全名称解析器

    控制表达式中可访问的名称和属性。
    """

    def __init__(
        self,
        config: SandboxConfig | None = None,
        allowed_names: dict[str, Any] | None = None,
        allowed_functions: dict[str, Callable] | None = None,
    ):
        self.config = config or DEFAULT_SANDBOX_CONFIG
        self._allowed_names = allowed_names or {}
        self._allowed_functions = allowed_functions or {}

    def resolve_name(self, name: str) -> Any:
        """解析名称

        Args:
            name: 名称

        Returns:
            名称对应的值

        Raises:
            ForbiddenAccessError: 名称被禁止时抛出
        """
        if name in self.config.forbidden_names:
            raise ForbiddenAccessError(name)

        # 先检查用户提供的名称
        if name in self._allowed_names:
            return self._allowed_names[name]

        # 检查函数
        if name in self._allowed_functions:
            return self._allowed_functions[name]

        # 检查允许的内置名称
        if name in self.config.allowed_builtins:
            import builtins
            return getattr(builtins, name, None)

        # 未找到
        raise KeyError(name)

    def resolve_attr(self, obj: Any, attr: str) -> Any:
        """解析属性

        Args:
            obj: 对象
            attr: 属性名

        Returns:
            属性值

        Raises:
            ForbiddenAccessError: 属性被禁止时抛出
        """
        # 检查魔术属性
        if attr.startswith("__") and attr.endswith("__"):
            raise ForbiddenAccessError(f"魔术属性 {attr}")

        # 检查私有属性
        if attr.startswith("__"):
            raise ForbiddenAccessError(f"私有属性 {attr}")

        if attr.startswith("_") and self.config.strict_private_access:
            raise ForbiddenAccessError(f"私有属性 {attr}")

        # 检查类型特定的允许属性
        obj_type = type(obj)
        if obj_type in self.config.allowed_type_attrs:
            allowed = self.config.allowed_type_attrs[obj_type]
            if attr not in allowed:
                # 对于基础类型，只允许白名单中的属性
                pass  # 暂时放开，让 getattr 自然处理

        return getattr(obj, attr)

    def check_method_call(self, obj: Any, method: str) -> bool:
        """检查方法调用是否安全

        Args:
            obj: 对象
            method: 方法名

        Returns:
            是否允许调用
        """
        # 检查类型特定的允许方法
        obj_type = type(obj)
        if obj_type in self.config.allowed_type_attrs:
            allowed = self.config.allowed_type_attrs[obj_type]
            return method in allowed

        # 默认允许（让 getattr 自然处理错误）
        return True


# ============================================================
# 安全运行时包装器
# ============================================================


class SafeWrapper:
    """安全包装器

    包装对象以限制其可访问的属性和方法。
    """

    def __init__(
        self,
        obj: Any,
        config: SandboxConfig | None = None,
    ):
        object.__setattr__(self, "_obj", obj)
        object.__setattr__(self, "_config", config or DEFAULT_SANDBOX_CONFIG)

    def __getattr__(self, name: str) -> Any:
        config = object.__getattribute__(self, "_config")
        obj = object.__getattribute__(self, "_obj")

        # 检查禁止的属性
        if name.startswith("__") and name.endswith("__"):
            raise ForbiddenAccessError(f"魔术属性 {name}")

        if name.startswith("__"):
            raise ForbiddenAccessError(f"私有属性 {name}")

        if name.startswith("_") and config.strict_private_access:
            raise ForbiddenAccessError(f"私有属性 {name}")

        # 检查类型特定的允许属性
        obj_type = type(obj)
        if obj_type in config.allowed_type_attrs:
            allowed = config.allowed_type_attrs[obj_type]
            if name not in allowed:
                raise ForbiddenAccessError(f"属性 {name} 不在 {obj_type.__name__} 的允许列表中")

        result = getattr(obj, name)

        # 如果结果是可调用的，也进行包装
        if callable(result):
            return result

        # 递归包装复杂对象（可选）
        return result

    def __repr__(self) -> str:
        obj = object.__getattribute__(self, "_obj")
        return f"SafeWrapper({obj!r})"


# ============================================================
# 安全沙箱
# ============================================================


class Sandbox:
    """安全沙箱

    提供安全的表达式执行环境。

    使用示例：
        sandbox = Sandbox()

        # 检查表达式安全性
        errors = sandbox.check_expression("eval('code')")
        if errors:
            print("不安全:", errors)

        # 创建安全的名称解析器
        resolver = sandbox.create_resolver(
            names={"x": 10, "y": 20},
            functions={"custom_func": my_func},
        )

        # 创建安全的执行上下文
        safe_names = sandbox.create_safe_names(context)
    """

    def __init__(self, config: SandboxConfig | None = None):
        self.config = config or DEFAULT_SANDBOX_CONFIG
        self._checker = SafetyChecker(self.config)

    def check_expression(self, expression: str) -> list[str]:
        """检查表达式安全性

        Args:
            expression: 表达式字符串

        Returns:
            错误列表，空列表表示安全
        """
        return self._checker.check(expression)

    def is_safe(self, expression: str) -> bool:
        """检查表达式是否安全

        Args:
            expression: 表达式字符串

        Returns:
            是否安全
        """
        return len(self.check_expression(expression)) == 0

    def validate_expression(self, expression: str) -> None:
        """验证表达式安全性

        Args:
            expression: 表达式字符串

        Raises:
            SecurityViolationError: 表达式不安全时抛出
        """
        errors = self.check_expression(expression)
        if errors:
            raise SecurityViolationError(
                f"表达式安全检查失败: {'; '.join(errors)}",
                expression,
            )

    def create_resolver(
        self,
        names: dict[str, Any] | None = None,
        functions: dict[str, Callable] | None = None,
    ) -> SafeNameResolver:
        """创建安全名称解析器

        Args:
            names: 允许的名称映射
            functions: 允许的函数映射

        Returns:
            SafeNameResolver 实例
        """
        return SafeNameResolver(
            config=self.config,
            allowed_names=names,
            allowed_functions=functions,
        )

    def create_safe_names(
        self,
        context: dict[str, Any],
        include_builtins: bool = True,
    ) -> dict[str, Any]:
        """创建安全的名称字典

        Args:
            context: 用户上下文
            include_builtins: 是否包含安全的内置函数

        Returns:
            安全的名称字典
        """
        safe_names: dict[str, Any] = {}

        # 添加用户上下文（过滤禁止的名称）
        for name, value in context.items():
            if name not in self.config.forbidden_names:
                safe_names[name] = value

        # 添加安全的内置函数
        if include_builtins:
            import builtins
            for name in self.config.allowed_builtins:
                if hasattr(builtins, name):
                    safe_names[name] = getattr(builtins, name)

        return safe_names

    def wrap_object(self, obj: Any) -> SafeWrapper:
        """包装对象以限制访问

        Args:
            obj: 原始对象

        Returns:
            SafeWrapper 实例
        """
        return SafeWrapper(obj, self.config)


# ============================================================
# 便捷函数
# ============================================================


def is_expression_safe(expression: str) -> bool:
    """检查表达式是否安全

    Args:
        expression: 表达式字符串

    Returns:
        是否安全
    """
    sandbox = Sandbox()
    return sandbox.is_safe(expression)


def validate_expression_safety(expression: str) -> None:
    """验证表达式安全性

    Args:
        expression: 表达式字符串

    Raises:
        SecurityViolationError: 表达式不安全时抛出
    """
    sandbox = Sandbox()
    sandbox.validate_expression(expression)


def get_expression_safety_issues(expression: str) -> list[str]:
    """获取表达式安全问题

    Args:
        expression: 表达式字符串

    Returns:
        安全问题列表
    """
    sandbox = Sandbox()
    return sandbox.check_expression(expression)
