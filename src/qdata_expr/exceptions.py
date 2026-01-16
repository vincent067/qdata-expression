"""
表达式引擎异常定义

定义表达式解析、求值、模板渲染过程中可能出现的异常。
"""

from typing import Any


class ExpressionError(Exception):
    """表达式引擎基础异常类"""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} - {self.details}"
        return self.message


class ExpressionParseError(ExpressionError):
    """表达式解析错误

    当表达式语法无效时抛出。
    """

    def __init__(
        self,
        expression: str,
        message: str | None = None,
        position: int | None = None,
    ):
        self.expression = expression
        self.position = position
        msg = message or f"无法解析表达式: {expression}"
        if position is not None:
            msg += f" (位置: {position})"
        super().__init__(msg, details={"expression": expression, "position": position})


class ExpressionEvalError(ExpressionError):
    """表达式求值错误

    当表达式求值失败时抛出。
    """

    def __init__(
        self,
        expression: str,
        message: str | None = None,
        cause: Exception | None = None,
    ):
        self.expression = expression
        self.cause = cause
        msg = message or f"表达式求值失败: {expression}"
        if cause:
            msg += f" - {cause}"
        super().__init__(msg, details={"expression": expression})


class UndefinedVariableError(ExpressionEvalError):
    """未定义变量错误

    当表达式中引用了未定义的变量时抛出。
    """

    def __init__(
        self,
        variable: str,
        expression: str | None = None,
    ):
        self.variable = variable
        msg = f"未定义的变量: {variable}"
        super().__init__(
            expression or "",
            msg,
        )
        self.details["variable"] = variable


class UndefinedFunctionError(ExpressionEvalError):
    """未定义函数错误

    当表达式中调用了未定义的函数时抛出。
    """

    def __init__(
        self,
        function: str,
        expression: str | None = None,
    ):
        self.function = function
        msg = f"未定义的函数: {function}"
        super().__init__(
            expression or "",
            msg,
        )
        self.details["function"] = function


class InvalidOperationError(ExpressionEvalError):
    """无效操作错误

    当表达式中的操作无效时抛出（如类型不匹配的操作）。
    """

    def __init__(
        self,
        operation: str,
        expression: str | None = None,
        reason: str | None = None,
    ):
        self.operation = operation
        self.reason = reason
        msg = f"无效的操作: {operation}"
        if reason:
            msg += f" - {reason}"
        super().__init__(
            expression or "",
            msg,
        )
        self.details["operation"] = operation
        if reason:
            self.details["reason"] = reason


class SecurityViolationError(ExpressionError):
    """安全违规错误

    当表达式尝试执行不安全的操作时抛出。
    """

    def __init__(
        self,
        violation: str,
        expression: str | None = None,
    ):
        self.violation = violation
        msg = f"安全违规: {violation}"
        super().__init__(
            msg,
            details={"violation": violation, "expression": expression},
        )


class ForbiddenAccessError(SecurityViolationError):
    """禁止访问错误

    当表达式尝试访问禁止的属性或方法时抛出。
    """

    def __init__(
        self,
        accessed: str,
        expression: str | None = None,
    ):
        self.accessed = accessed
        msg = f"禁止访问: {accessed}"
        super().__init__(msg, expression)
        self.details["accessed"] = accessed


class TemplateError(ExpressionError):
    """模板引擎基础异常"""

    pass


class TemplateParseError(TemplateError):
    """模板解析错误

    当模板语法无效时抛出。
    """

    def __init__(
        self,
        template: str,
        message: str | None = None,
        line: int | None = None,
    ):
        self.template = template
        self.line = line
        msg = message or "模板语法错误"
        if line is not None:
            msg += f" (行: {line})"
        super().__init__(msg, details={"template": template[:100], "line": line})


class TemplateRenderError(TemplateError):
    """模板渲染错误

    当模板渲染失败时抛出。
    """

    def __init__(
        self,
        template: str,
        message: str | None = None,
        cause: Exception | None = None,
    ):
        self.template = template
        self.cause = cause
        msg = message or "模板渲染失败"
        if cause:
            msg += f" - {cause}"
        super().__init__(msg, details={"template": template[:100]})


class ContextError(ExpressionError):
    """上下文错误"""

    pass


class InvalidPathError(ContextError):
    """无效路径错误

    当上下文路径无效时抛出。
    """

    def __init__(
        self,
        path: str,
        reason: str | None = None,
    ):
        self.path = path
        msg = f"无效的路径: {path}"
        if reason:
            msg += f" - {reason}"
        super().__init__(msg, details={"path": path, "reason": reason})


class FunctionRegistrationError(ExpressionError):
    """函数注册错误

    当函数注册失败时抛出。
    """

    def __init__(
        self,
        function_name: str,
        reason: str | None = None,
    ):
        self.function_name = function_name
        msg = f"函数注册失败: {function_name}"
        if reason:
            msg += f" - {reason}"
        super().__init__(msg, details={"function_name": function_name, "reason": reason})


class ExpressionTimeoutError(ExpressionError):
    """表达式超时错误

    当表达式执行超时时抛出。
    """

    def __init__(
        self,
        expression: str,
        timeout: float,
    ):
        self.expression = expression
        self.timeout = timeout
        msg = f"表达式执行超时 ({timeout}秒): {expression[:50]}..."
        super().__init__(msg, details={"expression": expression, "timeout": timeout})


class RecursionLimitError(ExpressionError):
    """递归限制错误

    当表达式递归深度超过限制时抛出。
    """

    def __init__(
        self,
        expression: str,
        limit: int,
    ):
        self.expression = expression
        self.limit = limit
        msg = f"表达式递归深度超过限制 ({limit}): {expression[:50]}..."
        super().__init__(msg, details={"expression": expression, "limit": limit})
