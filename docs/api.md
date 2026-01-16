# API 参考

本文档提供 QData Expression 的完整 API 参考。

## 核心类

### ExpressionEngine

表达式引擎，负责安全地求值表达式。

```python
from qdata_expr import ExpressionEngine
```

#### 构造函数

```python
ExpressionEngine(
    enable_cache: bool = True,
    enable_sandbox: bool = True,
    max_recursion_depth: int = 100,
    cache_size: int = 1000
)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `enable_cache` | `bool` | `True` | 是否启用表达式缓存 |
| `enable_sandbox` | `bool` | `True` | 是否启用安全沙箱 |
| `max_recursion_depth` | `int` | `100` | 最大递归深度 |
| `cache_size` | `int` | `1000` | LRU 缓存大小 |

#### 方法

##### evaluate

求值表达式。

```python
def evaluate(
    expression: str,
    context: dict[str, Any] | None = None
) -> Any
```

| 参数 | 类型 | 描述 |
|------|------|------|
| `expression` | `str` | 要求值的表达式 |
| `context` | `dict` | 上下文变量 |

**返回值**: 表达式求值结果

**异常**:
- `ExpressionParseError`: 表达式解析失败
- `ExpressionEvalError`: 表达式求值失败
- `SecurityViolationError`: 表达式存在安全问题

##### compile

预编译表达式。

```python
def compile(expression: str) -> CompiledExpression
```

##### register_function

注册自定义函数。

```python
def register_function(
    name: str,
    func: Callable,
    description: str = ""
) -> None
```

##### clear_cache

清空表达式缓存。

```python
def clear_cache() -> None
```

#### 属性

##### cache_stats

获取缓存统计信息。

```python
@property
def cache_stats(self) -> dict
```

返回:
```python
{
    "size": int,       # 当前缓存数量
    "max_size": int,   # 最大缓存数量
    "hits": int,       # 缓存命中次数
    "misses": int,     # 缓存未命中次数
    "hit_rate": float  # 命中率
}
```

---

### TemplateEngine

模板引擎，基于 Jinja2 实现。

```python
from qdata_expr import TemplateEngine
```

#### 构造函数

```python
TemplateEngine(
    strict_undefined: bool = False,
    autoescape: bool = False
)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `strict_undefined` | `bool` | `False` | 未定义变量是否抛出异常 |
| `autoescape` | `bool` | `False` | 是否自动转义 HTML |

#### 方法

##### render

渲染模板。

```python
def render(
    template: str,
    context: dict[str, Any] | None = None
) -> str
```

##### register_filter

注册自定义过滤器。

```python
def register_filter(name: str, func: Callable) -> None
```

##### register_global

注册全局变量。

```python
def register_global(name: str, value: Any) -> None
```

---

### Sandbox

安全沙箱。

```python
from qdata_expr import Sandbox, SandboxConfig
```

#### SandboxConfig

沙箱配置。

```python
SandboxConfig(
    strict_private_access: bool = True,
    max_execution_time: float = 5.0,
    max_recursion_depth: int = 100,
    max_string_length: int = 1000000,
    allowed_imports: list[str] | None = None,
    blocked_builtins: list[str] | None = None
)
```

#### 方法

##### is_safe

检查表达式是否安全。

```python
def is_safe(expression: str) -> bool
```

##### check_expression

获取表达式的安全问题列表。

```python
def check_expression(expression: str) -> list[str]
```

##### validate_expression

验证表达式，不安全时抛出异常。

```python
def validate_expression(expression: str) -> None
```

**异常**: `SecurityViolationError`

---

### ContextResolver

上下文解析器。

```python
from qdata_expr import ContextResolver
```

#### 方法

##### resolve

解析路径获取值。

```python
def resolve(
    path: str,
    context: dict[str, Any],
    default: Any = None
) -> Any
```

##### has

检查路径是否存在。

```python
def has(path: str, context: dict[str, Any]) -> bool
```

##### set

设置路径的值（返回新上下文）。

```python
def set(
    path: str,
    value: Any,
    context: dict[str, Any]
) -> dict[str, Any]
```

##### delete

删除路径（返回新上下文）。

```python
def delete(
    path: str,
    context: dict[str, Any]
) -> dict[str, Any]
```

##### merge

合并上下文。

```python
def merge(
    context: dict[str, Any],
    updates: dict[str, Any]
) -> dict[str, Any]
```

##### flatten

扁平化嵌套上下文。

```python
def flatten(context: dict[str, Any]) -> dict[str, Any]
```

##### unflatten

反扁平化上下文。

```python
def unflatten(flat: dict[str, Any]) -> dict[str, Any]
```

---

## 便捷函数

### evaluate

快速求值表达式。

```python
from qdata_expr import evaluate

result = evaluate(expression: str, context: dict | None = None) -> Any
```

### render_template

快速渲染模板。

```python
from qdata_expr import render_template

result = render_template(template: str, context: dict | None = None) -> str
```

### validate

验证表达式是否有效。

```python
from qdata_expr import validate

is_valid = validate(expression: str) -> bool
```

### resolve

快速解析路径。

```python
from qdata_expr import resolve

value = resolve(path: str, context: dict, default: Any = None) -> Any
```

### set_path

快速设置路径值。

```python
from qdata_expr import set_path

new_context = set_path(path: str, value: Any, context: dict) -> dict
```

### delete_path

快速删除路径。

```python
from qdata_expr import delete_path

new_context = delete_path(path: str, context: dict) -> dict
```

---

## 异常类

```python
from qdata_expr.exceptions import (
    ExpressionError,
    ExpressionParseError,
    ExpressionEvalError,
    UndefinedVariableError,
    UndefinedFunctionError,
    SecurityViolationError,
    TemplateError,
    TemplateRenderError,
)
```

| 异常类 | 描述 |
|--------|------|
| `ExpressionError` | 表达式错误基类 |
| `ExpressionParseError` | 表达式解析错误 |
| `ExpressionEvalError` | 表达式求值错误 |
| `UndefinedVariableError` | 未定义变量错误 |
| `UndefinedFunctionError` | 未定义函数错误 |
| `SecurityViolationError` | 安全违规错误 |
| `TemplateError` | 模板错误基类 |
| `TemplateRenderError` | 模板渲染错误 |

---

## 函数注册

### FunctionRegistry

函数注册表。

```python
from qdata_expr.functions import FunctionRegistry, FunctionCategory
```

### builtin_function 装饰器

```python
from qdata_expr import builtin_function

@builtin_function(
    name: str,
    category: FunctionCategory,
    description: str = "",
    signature: str = "",
    examples: list[str] | None = None
)
def my_function(...):
    ...
```

### FunctionCategory

函数分类枚举。

```python
class FunctionCategory(Enum):
    MATH = "math"
    STRING = "string"
    DATETIME = "datetime"
    LOGIC = "logic"
    LIST = "list"
    CUSTOM = "custom"
```
