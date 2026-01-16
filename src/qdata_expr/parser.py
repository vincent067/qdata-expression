"""
表达式解析器

基于 simpleeval 的安全表达式解析器，提供：
- 表达式语法解析
- 变量提取
- 语法验证
"""

import ast
import re
from dataclasses import dataclass, field
from typing import Any

# ============================================================
# 解析结果
# ============================================================


@dataclass
class ParseResult:
    """解析结果"""

    expression: str  # 原始表达式
    ast_node: ast.AST | None = None  # AST 节点
    variables: list[str] = field(default_factory=list)  # 变量列表
    functions: list[str] = field(default_factory=list)  # 函数调用列表
    is_valid: bool = True  # 是否有效
    errors: list[str] = field(default_factory=list)  # 错误列表

    def to_dict(self) -> dict[str, Any]:
        return {
            "expression": self.expression,
            "variables": self.variables,
            "functions": self.functions,
            "is_valid": self.is_valid,
            "errors": self.errors,
        }


# ============================================================
# AST 分析器
# ============================================================


class ExpressionAnalyzer(ast.NodeVisitor):
    """表达式 AST 分析器

    遍历 AST 树，提取变量和函数调用。
    """

    def __init__(self, known_functions: set[str] | None = None):
        self.variables: set[str] = set()
        self.functions: set[str] = set()
        self.known_functions = known_functions or set()

    def visit_Name(self, node: ast.Name) -> None:
        """访问名称节点"""
        name = node.id
        # 排除 Python 关键字和内置常量
        if name not in ("True", "False", "None"):
            if name in self.known_functions:
                self.functions.add(name)
            else:
                self.variables.add(name)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """访问函数调用节点"""
        # 获取函数名
        if isinstance(node.func, ast.Name):
            self.functions.add(node.func.id)
            # 从变量集中移除（如果存在）
            self.variables.discard(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            # 方法调用，如 obj.method()
            self.functions.add(node.func.attr)
        self.generic_visit(node)

    def analyze(self, tree: ast.AST) -> tuple[list[str], list[str]]:
        """分析 AST 树

        Returns:
            (变量列表, 函数列表)
        """
        self.variables = set()
        self.functions = set()
        self.visit(tree)
        return sorted(self.variables), sorted(self.functions)


# ============================================================
# 表达式解析器
# ============================================================


class ExpressionParser:
    """表达式解析器

    解析表达式字符串，提取变量和函数，验证语法。

    使用示例：
        parser = ExpressionParser()

        # 解析表达式
        result = parser.parse("x + y * 2")
        print(result.variables)  # ['x', 'y']

        # 验证语法
        is_valid = parser.validate("x + y")

        # 提取变量
        variables = parser.extract_variables("a + b + c")
    """

    # 表达式语法标记
    EXPR_PREFIX = "${"
    EXPR_SUFFIX = "}"

    # 支持的操作符
    BINARY_OPERATORS = {"+", "-", "*", "/", "//", "%", "**", "==", "!=", "<", ">", "<=", ">=", "and", "or", "in"}
    UNARY_OPERATORS = {"not", "-", "+"}

    def __init__(self, known_functions: set[str] | None = None):
        """初始化解析器

        Args:
            known_functions: 已知函数名集合（用于区分变量和函数）
        """
        self.known_functions = known_functions or set()
        self._analyzer = ExpressionAnalyzer(self.known_functions)

    def parse(self, expression: str) -> ParseResult:
        """解析表达式

        Args:
            expression: 表达式字符串

        Returns:
            ParseResult 解析结果
        """
        result = ParseResult(expression=expression)

        if not expression or not expression.strip():
            result.is_valid = False
            result.errors.append("表达式为空")
            return result

        try:
            # 解析为 AST
            tree = ast.parse(expression, mode="eval")
            result.ast_node = tree

            # 分析变量和函数
            self._analyzer.known_functions = self.known_functions
            variables, functions = self._analyzer.analyze(tree)
            result.variables = variables
            result.functions = functions

        except SyntaxError as e:
            result.is_valid = False
            result.errors.append(f"语法错误: {e.msg} (行 {e.lineno}, 列 {e.offset})")
        except Exception as e:
            result.is_valid = False
            result.errors.append(f"解析错误: {e}")

        return result

    def validate(self, expression: str) -> bool:
        """验证表达式语法

        Args:
            expression: 表达式字符串

        Returns:
            是否有效
        """
        result = self.parse(expression)
        return result.is_valid

    def extract_variables(self, expression: str) -> list[str]:
        """提取表达式中的变量

        Args:
            expression: 表达式字符串

        Returns:
            变量名列表
        """
        result = self.parse(expression)
        return result.variables

    def extract_functions(self, expression: str) -> list[str]:
        """提取表达式中的函数调用

        Args:
            expression: 表达式字符串

        Returns:
            函数名列表
        """
        result = self.parse(expression)
        return result.functions

    def get_errors(self, expression: str) -> list[str]:
        """获取表达式的错误

        Args:
            expression: 表达式字符串

        Returns:
            错误列表
        """
        result = self.parse(expression)
        return result.errors

    @classmethod
    def is_expression_string(cls, value: str) -> bool:
        """检查字符串是否包含表达式标记

        Args:
            value: 字符串

        Returns:
            是否包含表达式
        """
        return cls.EXPR_PREFIX in value and cls.EXPR_SUFFIX in value

    @classmethod
    def extract_expressions(cls, value: str) -> list[str]:
        """从字符串中提取所有表达式

        Args:
            value: 包含表达式的字符串

        Returns:
            表达式列表
        """
        pattern = r'\$\{([^}]+)\}'
        return re.findall(pattern, value)

    @classmethod
    def unwrap_expression(cls, value: str) -> str:
        """解包表达式（移除 ${ } 标记）

        Args:
            value: 表达式字符串

        Returns:
            解包后的表达式
        """
        value = value.strip()
        if value.startswith(cls.EXPR_PREFIX) and value.endswith(cls.EXPR_SUFFIX):
            return value[len(cls.EXPR_PREFIX):-len(cls.EXPR_SUFFIX)]
        return value


# ============================================================
# 表达式构建器
# ============================================================


class ExpressionBuilder:
    """表达式构建器

    用于程序化构建表达式字符串。

    使用示例：
        builder = ExpressionBuilder()
        expr = (
            builder
            .var("price")
            .multiply()
            .var("quantity")
            .build()
        )
        # 结果: "price * quantity"
    """

    def __init__(self):
        self._parts: list[str] = []

    def var(self, name: str) -> "ExpressionBuilder":
        """添加变量"""
        self._parts.append(name)
        return self

    def literal(self, value: Any) -> "ExpressionBuilder":
        """添加字面值"""
        if isinstance(value, str):
            self._parts.append(f'"{value}"')
        elif value is None:
            self._parts.append("None")
        elif isinstance(value, bool):
            self._parts.append("True" if value else "False")
        else:
            self._parts.append(str(value))
        return self

    def func(self, name: str, *args: Any) -> "ExpressionBuilder":
        """添加函数调用"""
        args_str = ", ".join(str(a) for a in args)
        self._parts.append(f"{name}({args_str})")
        return self

    def add(self) -> "ExpressionBuilder":
        """加法"""
        self._parts.append(" + ")
        return self

    def subtract(self) -> "ExpressionBuilder":
        """减法"""
        self._parts.append(" - ")
        return self

    def multiply(self) -> "ExpressionBuilder":
        """乘法"""
        self._parts.append(" * ")
        return self

    def divide(self) -> "ExpressionBuilder":
        """除法"""
        self._parts.append(" / ")
        return self

    def eq(self) -> "ExpressionBuilder":
        """等于"""
        self._parts.append(" == ")
        return self

    def ne(self) -> "ExpressionBuilder":
        """不等于"""
        self._parts.append(" != ")
        return self

    def gt(self) -> "ExpressionBuilder":
        """大于"""
        self._parts.append(" > ")
        return self

    def ge(self) -> "ExpressionBuilder":
        """大于等于"""
        self._parts.append(" >= ")
        return self

    def lt(self) -> "ExpressionBuilder":
        """小于"""
        self._parts.append(" < ")
        return self

    def le(self) -> "ExpressionBuilder":
        """小于等于"""
        self._parts.append(" <= ")
        return self

    def and_(self) -> "ExpressionBuilder":
        """逻辑与"""
        self._parts.append(" and ")
        return self

    def or_(self) -> "ExpressionBuilder":
        """逻辑或"""
        self._parts.append(" or ")
        return self

    def not_(self) -> "ExpressionBuilder":
        """逻辑非"""
        self._parts.append("not ")
        return self

    def group(self, inner: "ExpressionBuilder") -> "ExpressionBuilder":
        """括号分组"""
        self._parts.append(f"({inner.build()})")
        return self

    def raw(self, text: str) -> "ExpressionBuilder":
        """原始文本"""
        self._parts.append(text)
        return self

    def build(self) -> str:
        """构建表达式字符串"""
        return "".join(self._parts)

    def wrap(self) -> str:
        """构建并包装为 ${expr} 格式"""
        return f"${{{self.build()}}}"

    def clear(self) -> "ExpressionBuilder":
        """清空"""
        self._parts = []
        return self


# ============================================================
# 便捷函数
# ============================================================


def parse_expression(expression: str) -> ParseResult:
    """解析表达式"""
    parser = ExpressionParser()
    return parser.parse(expression)


def validate_expression(expression: str) -> bool:
    """验证表达式语法"""
    parser = ExpressionParser()
    return parser.validate(expression)


def extract_variables(expression: str) -> list[str]:
    """提取表达式中的变量"""
    parser = ExpressionParser()
    return parser.extract_variables(expression)


def is_expression(value: str) -> bool:
    """检查字符串是否为表达式"""
    return ExpressionParser.is_expression_string(value)
