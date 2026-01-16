"""
表达式求值器

提供安全的表达式求值能力，包括：
- 基于 simpleeval 的安全求值
- 表达式预编译和缓存
- 自定义函数注册
- 上下文变量绑定
"""

import ast
import hashlib
import threading
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from .exceptions import (
    ExpressionEvalError,
    ExpressionParseError,
    UndefinedFunctionError,
    UndefinedVariableError,
)
from .functions.base import (
    FunctionRegistry,
)
from .functions.math_funcs import MATH_FUNCTIONS
from .functions.string_funcs import STRING_FUNCTIONS
from .functions.datetime_funcs import DATETIME_FUNCTIONS
from .functions.logic_funcs import LOGIC_FUNCTIONS
from .functions.list_funcs import LIST_FUNCTIONS
from .sandbox import Sandbox, SandboxConfig


# ============================================================
# 表达式缓存
# ============================================================


class LRUCache:
    """LRU 缓存

    线程安全的 LRU 缓存实现。
    """

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._cache: OrderedDict[str, Any] = OrderedDict()
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> tuple[bool, Any]:
        """获取缓存值

        Returns:
            (是否命中, 值)
        """
        with self._lock:
            if key in self._cache:
                # 移动到末尾（最近使用）
                self._cache.move_to_end(key)
                self._hits += 1
                return True, self._cache[key]
            self._misses += 1
            return False, None

    def put(self, key: str, value: Any) -> None:
        """存入缓存"""
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            else:
                if len(self._cache) >= self.max_size:
                    # 移除最老的项
                    self._cache.popitem(last=False)
                self._cache[key] = value

    def clear(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    @property
    def stats(self) -> dict:
        """获取统计信息"""
        total = self._hits + self._misses
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": self._hits / total if total > 0 else 0,
        }


@dataclass
class CompiledExpression:
    """编译后的表达式"""

    expression: str  # 原始表达式
    ast_node: ast.Expression  # AST 节点
    code: Any  # 编译后的代码对象
    variables: list[str] = field(default_factory=list)  # 变量列表
    functions: list[str] = field(default_factory=list)  # 函数列表

    @classmethod
    def compile(cls, expression: str) -> "CompiledExpression":
        """编译表达式"""
        try:
            tree = ast.parse(expression, mode="eval")
            code = compile(tree, "<expression>", "eval")
            return cls(
                expression=expression,
                ast_node=tree,
                code=code,
            )
        except SyntaxError as e:
            raise ExpressionParseError(expression, f"语法错误: {e.msg}", e.offset)

    def evaluate(self, context: dict[str, Any] | None = None) -> Any:
        """执行编译后的表达式

        Args:
            context: 上下文变量

        Returns:
            计算结果
        """
        context = context or {}
        evaluator = SafeEvaluator(names=context)
        return evaluator.eval(self.expression)


class ExpressionCache:
    """表达式缓存管理器

    缓存编译后的表达式以提高性能。
    """

    def __init__(self, max_size: int = 1000):
        self._cache = LRUCache(max_size)

    def get_or_compile(self, expression: str) -> CompiledExpression:
        """获取或编译表达式

        Args:
            expression: 表达式字符串

        Returns:
            编译后的表达式
        """
        cache_key = self._make_key(expression)
        hit, compiled = self._cache.get(cache_key)
        if hit:
            return compiled

        compiled = CompiledExpression.compile(expression)
        self._cache.put(cache_key, compiled)
        return compiled

    def _make_key(self, expression: str) -> str:
        """生成缓存键"""
        return hashlib.md5(expression.encode()).hexdigest()

    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()

    @property
    def stats(self) -> dict:
        """获取统计信息"""
        return self._cache.stats


# ============================================================
# 安全求值器
# ============================================================


class SafeEvaluator:
    """安全表达式求值器

    使用 AST 解释执行，避免使用 eval。
    """

    # 允许的操作符映射
    OPERATORS = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.FloorDiv: lambda a, b: a // b,
        ast.Mod: lambda a, b: a % b,
        ast.Pow: lambda a, b: a ** b,
        ast.USub: lambda a: -a,
        ast.UAdd: lambda a: +a,
        ast.Not: lambda a: not a,
        ast.Eq: lambda a, b: a == b,
        ast.NotEq: lambda a, b: a != b,
        ast.Lt: lambda a, b: a < b,
        ast.LtE: lambda a, b: a <= b,
        ast.Gt: lambda a, b: a > b,
        ast.GtE: lambda a, b: a >= b,
        ast.Is: lambda a, b: a is b,
        ast.IsNot: lambda a, b: a is not b,
        ast.In: lambda a, b: a in b,
        ast.NotIn: lambda a, b: a not in b,
        ast.BitAnd: lambda a, b: a & b,
        ast.BitOr: lambda a, b: a | b,
        ast.BitXor: lambda a, b: a ^ b,
        ast.Invert: lambda a: ~a,
        ast.LShift: lambda a, b: a << b,
        ast.RShift: lambda a, b: a >> b,
    }

    def __init__(
        self,
        names: dict[str, Any] | None = None,
        functions: dict[str, Callable] | None = None,
    ):
        self.names = names or {}
        self.functions = functions or {}

    def eval(self, expression: str) -> Any:
        """求值表达式

        Args:
            expression: 表达式字符串

        Returns:
            计算结果
        """
        try:
            tree = ast.parse(expression, mode="eval")
            return self._eval_node(tree.body)
        except Exception as e:
            raise ExpressionEvalError(expression, cause=e)

    def _eval_node(self, node: ast.AST) -> Any:
        """求值 AST 节点"""
        # 常量
        if isinstance(node, ast.Constant):
            return node.value

        # 名称（变量）
        if isinstance(node, ast.Name):
            name = node.id
            # 先检查函数
            if name in self.functions:
                return self.functions[name]
            # 再检查变量
            if name in self.names:
                return self.names[name]
            # 内置常量
            if name == "True":
                return True
            if name == "False":
                return False
            if name == "None":
                return None
            raise UndefinedVariableError(name)

        # 二元操作
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type in self.OPERATORS:
                return self.OPERATORS[op_type](left, right)
            raise ExpressionEvalError("", f"不支持的操作符: {op_type.__name__}")

        # 一元操作
        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in self.OPERATORS:
                return self.OPERATORS[op_type](operand)
            raise ExpressionEvalError("", f"不支持的操作符: {op_type.__name__}")

        # 比较操作
        if isinstance(node, ast.Compare):
            left = self._eval_node(node.left)
            for op, comparator in zip(node.ops, node.comparators, strict=False):
                right = self._eval_node(comparator)
                op_type = type(op)
                if op_type not in self.OPERATORS:
                    raise ExpressionEvalError("", f"不支持的比较操作符: {op_type.__name__}")
                if not self.OPERATORS[op_type](left, right):
                    return False
                left = right
            return True

        # 布尔操作
        if isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                for value in node.values:
                    if not self._eval_node(value):
                        return False
                return True
            if isinstance(node.op, ast.Or):
                for value in node.values:
                    if self._eval_node(value):
                        return True
                return False

        # 条件表达式 (a if b else c)
        if isinstance(node, ast.IfExp):
            if self._eval_node(node.test):
                return self._eval_node(node.body)
            return self._eval_node(node.orelse)

        # 函数调用
        if isinstance(node, ast.Call):
            # 获取函数
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name not in self.functions:
                    raise UndefinedFunctionError(func_name)
                func = self.functions[func_name]
            elif isinstance(node.func, ast.Attribute):
                # 方法调用
                obj = self._eval_node(node.func.value)
                func = getattr(obj, node.func.attr)
            else:
                raise ExpressionEvalError("", "不支持的函数调用形式")

            # 求值参数
            args = [self._eval_node(arg) for arg in node.args]
            kwargs = {kw.arg: self._eval_node(kw.value) for kw in node.keywords if kw.arg}

            return func(*args, **kwargs)

        # 属性访问
        if isinstance(node, ast.Attribute):
            obj = self._eval_node(node.value)
            attr = node.attr
            # 对于字典，使用键访问
            if isinstance(obj, dict):
                return obj.get(attr)
            return getattr(obj, attr)

        # 下标访问
        if isinstance(node, ast.Subscript):
            obj = self._eval_node(node.value)
            if isinstance(node.slice, ast.Constant):
                return obj[node.slice.value]
            if isinstance(node.slice, ast.Slice):
                return obj[
                    self._eval_node(node.slice.lower) if node.slice.lower else None:
                    self._eval_node(node.slice.upper) if node.slice.upper else None:
                    self._eval_node(node.slice.step) if node.slice.step else None
                ]
            return obj[self._eval_node(node.slice)]

        # 列表
        if isinstance(node, ast.List):
            return [self._eval_node(elt) for elt in node.elts]

        # 元组
        if isinstance(node, ast.Tuple):
            return tuple(self._eval_node(elt) for elt in node.elts)

        # 集合
        if isinstance(node, ast.Set):
            return {self._eval_node(elt) for elt in node.elts}

        # 字典
        if isinstance(node, ast.Dict):
            return {
                self._eval_node(k) if k else None: self._eval_node(v)
                for k, v in zip(node.keys, node.values, strict=False)
            }

        # 格式化字符串 (f-string)
        if isinstance(node, ast.JoinedStr):
            parts = []
            for value in node.values:
                if isinstance(value, ast.Constant):
                    parts.append(str(value.value))
                elif isinstance(value, ast.FormattedValue):
                    parts.append(str(self._eval_node(value.value)))
            return "".join(parts)

        # 列表推导式
        if isinstance(node, ast.ListComp):
            return self._eval_comprehension(node)

        # 集合推导式
        if isinstance(node, ast.SetComp):
            return set(self._eval_comprehension(node))

        # 字典推导式
        if isinstance(node, ast.DictComp):
            return self._eval_dict_comprehension(node)

        # 生成器表达式
        if isinstance(node, ast.GeneratorExp):
            return self._eval_comprehension(node)

        raise ExpressionEvalError("", f"不支持的表达式类型: {type(node).__name__}")

    def _eval_comprehension(
        self,
        node: ast.ListComp | ast.SetComp | ast.GeneratorExp,
    ) -> list:
        """求值列表/集合/生成器推导式"""
        # 保存当前 names
        saved_names = dict(self.names)

        result = []
        self._eval_generators(
            generators=node.generators,
            index=0,
            callback=lambda: result.append(self._eval_node(node.elt)),
        )

        # 恢复 names
        self.names = saved_names
        return result

    def _eval_dict_comprehension(self, node: ast.DictComp) -> dict:
        """求值字典推导式"""
        # 保存当前 names
        saved_names = dict(self.names)

        result = {}

        def add_item() -> None:
            key = self._eval_node(node.key)
            value = self._eval_node(node.value)
            result[key] = value

        self._eval_generators(
            generators=node.generators,
            index=0,
            callback=add_item,
        )

        # 恢复 names
        self.names = saved_names
        return result

    def _eval_generators(
        self,
        generators: list[ast.comprehension],
        index: int,
        callback: Callable[[], None],
    ) -> None:
        """递归求值推导式的生成器"""
        if index >= len(generators):
            callback()
            return

        comp = generators[index]
        iterable = self._eval_node(comp.iter)

        for item in iterable:
            # 设置迭代变量
            if isinstance(comp.target, ast.Name):
                self.names[comp.target.id] = item
            elif isinstance(comp.target, ast.Tuple):
                # 解包
                for i, elt in enumerate(comp.target.elts):
                    if isinstance(elt, ast.Name):
                        self.names[elt.id] = item[i]

            # 检查条件
            if all(self._eval_node(if_clause) for if_clause in comp.ifs):
                self._eval_generators(generators, index + 1, callback)


# ============================================================
# 表达式引擎
# ============================================================


class ExpressionEngine:
    """表达式引擎

    完整的表达式求值引擎，包括：
    - 内置函数库
    - 自定义函数注册
    - 表达式缓存
    - 安全沙箱

    使用示例：
        engine = ExpressionEngine()

        # 基础计算
        result = engine.evaluate("2 + 3 * 4")  # 14

        # 变量计算
        result = engine.evaluate("price * quantity", {
            "price": 100,
            "quantity": 5
        })  # 500

        # 内置函数
        result = engine.evaluate("round(price * 0.9, 2)", {"price": 99.99})

        # 注册自定义函数
        engine.register_function("tax", lambda amount: amount * 0.1)
        result = engine.evaluate("price + tax(price)", {"price": 100})
    """

    def __init__(
        self,
        enable_cache: bool = True,
        cache_size: int = 1000,
        enable_sandbox: bool = True,
        sandbox_config: SandboxConfig | None = None,
    ):
        """初始化引擎

        Args:
            enable_cache: 是否启用表达式缓存
            cache_size: 缓存大小
            enable_sandbox: 是否启用安全沙箱
            sandbox_config: 沙箱配置
        """
        self._function_registry = FunctionRegistry()
        self._cache = ExpressionCache(cache_size) if enable_cache else None
        self._sandbox = Sandbox(sandbox_config) if enable_sandbox else None

        # 注册内置函数
        self._register_builtin_functions()

    def _register_builtin_functions(self) -> None:
        """注册内置函数"""
        # 注册各类函数
        for name, definition in MATH_FUNCTIONS.items():
            self._function_registry.register_definition(definition)
        for name, definition in STRING_FUNCTIONS.items():
            self._function_registry.register_definition(definition)
        for name, definition in DATETIME_FUNCTIONS.items():
            self._function_registry.register_definition(definition)
        for name, definition in LOGIC_FUNCTIONS.items():
            self._function_registry.register_definition(definition)
        for name, definition in LIST_FUNCTIONS.items():
            self._function_registry.register_definition(definition)

    def register_function(
        self,
        name: str,
        func: Callable,
        description: str = "",
    ) -> None:
        """注册自定义函数

        Args:
            name: 函数名
            func: 函数对象
            description: 函数描述
        """
        from .functions.base import FunctionCategory
        self._function_registry.register(
            name=name,
            func=func,
            category=FunctionCategory.CUSTOM,
            description=description,
        )

    def unregister_function(self, name: str) -> bool:
        """注销函数

        Args:
            name: 函数名

        Returns:
            是否成功
        """
        return self._function_registry.unregister(name)

    def has_function(self, name: str) -> bool:
        """检查函数是否存在"""
        return self._function_registry.has(name)

    def list_functions(self) -> list[str]:
        """列出所有函数"""
        return self._function_registry.list_all()

    def evaluate(
        self,
        expression: str,
        context: dict[str, Any] | None = None,
    ) -> Any:
        """求值表达式

        Args:
            expression: 表达式字符串
            context: 上下文变量

        Returns:
            计算结果
        """
        context = context or {}

        # 添加数学常量
        context = self._add_math_constants(context)

        # 安全检查
        if self._sandbox:
            self._sandbox.validate_expression(expression)

        # 创建求值器
        functions = self._function_registry.get_all_callables()
        evaluator = SafeEvaluator(names=context, functions=functions)

        return evaluator.eval(expression)

    def _add_math_constants(self, context: dict[str, Any]) -> dict[str, Any]:
        """添加数学常量到上下文（如果未定义）

        Args:
            context: 原始上下文

        Returns:
            包含数学常量的上下文
        """
        import math
        result = dict(context)  # 复制，不修改原始上下文

        # 添加常用数学常量
        if "e" not in result:
            result["e"] = math.e
        if "pi" not in result:
            result["pi"] = math.pi
        if "inf" not in result:
            result["inf"] = math.inf
        if "nan" not in result:
            result["nan"] = math.nan

        return result

    def validate(self, expression: str) -> list[str]:
        """验证表达式

        Args:
            expression: 表达式字符串

        Returns:
            错误列表（空列表表示有效）
        """
        errors = []

        # 语法检查
        try:
            ast.parse(expression, mode="eval")
        except SyntaxError as e:
            errors.append(f"语法错误: {e.msg}")
            return errors

        # 安全检查
        if self._sandbox:
            sandbox_errors = self._sandbox.check_expression(expression)
            errors.extend(sandbox_errors)

        return errors

    def get_variables(self, expression: str) -> list[str]:
        """获取表达式中的变量

        Args:
            expression: 表达式字符串

        Returns:
            变量名列表
        """
        from .parser import ExpressionParser
        parser = ExpressionParser(self._function_registry.list_all())
        result = parser.parse(expression)
        return result.variables

    def clear_cache(self) -> None:
        """清空缓存"""
        if self._cache:
            self._cache.clear()

    @property
    def cache_stats(self) -> dict | None:
        """获取缓存统计"""
        if self._cache:
            return self._cache.stats
        return None


# ============================================================
# 便捷函数
# ============================================================


# 全局默认引擎
_default_engine: ExpressionEngine | None = None
_engine_lock = threading.Lock()


def get_default_engine() -> ExpressionEngine:
    """获取默认表达式引擎"""
    global _default_engine
    with _engine_lock:
        if _default_engine is None:
            _default_engine = ExpressionEngine()
        return _default_engine


def evaluate(expression: str, context: dict[str, Any] | None = None) -> Any:
    """求值表达式（使用默认引擎）

    Args:
        expression: 表达式字符串
        context: 上下文变量

    Returns:
        计算结果
    """
    engine = get_default_engine()
    return engine.evaluate(expression, context)


def validate(expression: str) -> list[str]:
    """验证表达式（使用默认引擎）

    Args:
        expression: 表达式字符串

    Returns:
        错误列表
    """
    engine = get_default_engine()
    return engine.validate(expression)


def register_function(name: str, func: Callable, description: str = "") -> None:
    """注册自定义函数到默认引擎"""
    engine = get_default_engine()
    engine.register_function(name, func, description)
