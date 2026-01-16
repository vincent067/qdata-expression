"""
QData Expression - 安全、可扩展的 Python 表达式引擎

这是轻易云数据集成平台的核心表达式引擎组件，提供：
- 安全的表达式求值（基于 AST 解析）
- 强大的模板渲染（基于 Jinja2）
- 丰富的内置函数库
- 灵活的上下文管理
- 完善的安全沙箱机制

使用示例:
    >>> from qdata_expr import ExpressionEngine, evaluate, render_template
    >>>
    >>> # 表达式求值
    >>> engine = ExpressionEngine()
    >>> result = engine.evaluate("2 + 3 * 4")  # 14
    >>>
    >>> # 使用上下文变量
    >>> result = engine.evaluate("price * quantity", {"price": 100, "quantity": 5})
    >>>
    >>> # 模板渲染
    >>> result = render_template("Hello, {{ name }}!", {"name": "World"})

作者: 广东轻亿云软件科技有限公司
官网: https://www.qeasy.cloud
"""

from ._version import __version__, __version_info__

# 核心异常类
from .exceptions import (
    ExpressionError,
    ExpressionEvalError,
    ExpressionParseError,
    UndefinedFunctionError,
    UndefinedVariableError,
    InvalidOperationError,
    SecurityViolationError,
    ForbiddenAccessError,
    TemplateError,
    TemplateParseError,
    TemplateRenderError,
    ContextError,
    InvalidPathError,
    FunctionRegistrationError,
    ExpressionTimeoutError,
    RecursionLimitError,
)

# 表达式引擎
from .evaluator import (
    ExpressionEngine,
    SafeEvaluator,
    CompiledExpression,
    ExpressionCache,
    LRUCache,
    evaluate,
    validate,
    register_function,
    get_default_engine,
)

# 模板引擎
from .template import (
    TemplateEngine,
    Jinja2TemplateEngine,
    SimpleTemplateEngine,
    render_template,
    validate_template,
    get_template_variables,
    get_default_template_engine,
)

# 上下文解析
from .context import (
    ContextResolver,
    PathParser,
    resolve,
    has_path,
    set_path,
    delete_path,
    merge_context,
    flatten_context,
    unflatten_context,
)

# 表达式解析
from .parser import (
    ExpressionParser,
    ExpressionAnalyzer,
    ExpressionBuilder,
    ParseResult,
    parse_expression,
    validate_expression,
    extract_variables,
    is_expression,
)

# 安全沙箱
from .sandbox import (
    Sandbox,
    SandboxConfig,
    SafetyChecker,
    SafeNameResolver,
    SafeWrapper,
    is_expression_safe,
    validate_expression_safety,
    get_expression_safety_issues,
)

# 函数注册
from .functions import (
    FunctionCategory,
    FunctionDefinition,
    FunctionRegistry,
    builtin_function,
    get_builtin_functions,
    get_all_builtin_functions,
    MATH_FUNCTIONS,
    STRING_FUNCTIONS,
    DATETIME_FUNCTIONS,
    LOGIC_FUNCTIONS,
    LIST_FUNCTIONS,
)

__all__ = [
    # 版本信息
    "__version__",
    "__version_info__",
    # 核心异常
    "ExpressionError",
    "ExpressionEvalError",
    "ExpressionParseError",
    "UndefinedFunctionError",
    "UndefinedVariableError",
    "InvalidOperationError",
    "SecurityViolationError",
    "ForbiddenAccessError",
    "TemplateError",
    "TemplateParseError",
    "TemplateRenderError",
    "ContextError",
    "InvalidPathError",
    "FunctionRegistrationError",
    "ExpressionTimeoutError",
    "RecursionLimitError",
    # 表达式引擎
    "ExpressionEngine",
    "SafeEvaluator",
    "CompiledExpression",
    "ExpressionCache",
    "LRUCache",
    "evaluate",
    "validate",
    "register_function",
    "get_default_engine",
    # 模板引擎
    "TemplateEngine",
    "Jinja2TemplateEngine",
    "SimpleTemplateEngine",
    "render_template",
    "validate_template",
    "get_template_variables",
    "get_default_template_engine",
    # 上下文解析
    "ContextResolver",
    "PathParser",
    "resolve",
    "has_path",
    "set_path",
    "delete_path",
    "merge_context",
    "flatten_context",
    "unflatten_context",
    # 表达式解析
    "ExpressionParser",
    "ExpressionAnalyzer",
    "ExpressionBuilder",
    "ParseResult",
    "parse_expression",
    "validate_expression",
    "extract_variables",
    "is_expression",
    # 安全沙箱
    "Sandbox",
    "SandboxConfig",
    "SafetyChecker",
    "SafeNameResolver",
    "SafeWrapper",
    "is_expression_safe",
    "validate_expression_safety",
    "get_expression_safety_issues",
    # 函数注册
    "FunctionCategory",
    "FunctionDefinition",
    "FunctionRegistry",
    "builtin_function",
    "get_builtin_functions",
    "get_all_builtin_functions",
    "MATH_FUNCTIONS",
    "STRING_FUNCTIONS",
    "DATETIME_FUNCTIONS",
    "LOGIC_FUNCTIONS",
    "LIST_FUNCTIONS",
]
