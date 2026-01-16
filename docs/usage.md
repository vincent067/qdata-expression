# 使用指南

本指南将帮助您快速上手 QData Expression 表达式引擎。

## 安装

```bash
pip install qdata-expression
```

## 基本用法

### 表达式求值

```python
from qdata_expr import ExpressionEngine, evaluate

# 创建引擎
engine = ExpressionEngine()

# 基本算术
result = engine.evaluate("2 + 3 * 4")  # 14

# 使用便捷函数
result = evaluate("10 / 2 + 1")  # 6.0
```

### 使用上下文变量

```python
context = {"price": 100, "quantity": 5, "discount": 0.1}

# 简单变量
result = engine.evaluate("price * quantity", context)  # 500

# 计算表达式
result = engine.evaluate("price * quantity * (1 - discount)", context)  # 450.0
```

### 嵌套数据访问

```python
context = {
    "user": {
        "name": "Alice",
        "profile": {"age": 30}
    },
    "items": [
        {"name": "Apple", "price": 5},
        {"name": "Banana", "price": 3}
    ]
}

# 访问嵌套属性
result = engine.evaluate("user.profile.age", context)  # 30

# 访问数组元素
result = engine.evaluate("items[0].price", context)  # 5
```

## 模板引擎

### 基本模板

```python
from qdata_expr import TemplateEngine, render_template

engine = TemplateEngine()

# 变量替换
result = engine.render("Hello, {{ name }}!", {"name": "World"})
# "Hello, World!"

# 使用便捷函数
result = render_template("Total: {{ price * quantity }}", {"price": 10, "quantity": 3})
# "Total: 30"
```

### 条件渲染

```python
template = """
{% if score >= 60 %}
恭喜，您通过了考试！
{% else %}
很遗憾，请继续努力。
{% endif %}
"""

result = engine.render(template, {"score": 75})
```

### 循环渲染

```python
template = """
购物清单：
{% for item in items %}
- {{ item.name }}: ¥{{ item.price }}
{% endfor %}
"""

context = {
    "items": [
        {"name": "苹果", "price": 5},
        {"name": "香蕉", "price": 3}
    ]
}
result = engine.render(template, context)
```

### 过滤器

```python
# 内置过滤器
result = engine.render("{{ name | upper }}", {"name": "alice"})  # "ALICE"
result = engine.render("{{ text | trim }}", {"text": "  hello  "})  # "hello"

# 注册自定义过滤器
def currency(value):
    return f"¥{value:.2f}"

engine.register_filter("currency", currency)
result = engine.render("{{ price | currency }}", {"price": 99.9})  # "¥99.90"
```

## 安全沙箱

### 基本安全检查

```python
from qdata_expr import Sandbox, SandboxConfig

config = SandboxConfig(
    strict_private_access=True,
    max_execution_time=5.0,
    max_recursion_depth=100
)

sandbox = Sandbox(config)

# 检查表达式是否安全
if sandbox.is_safe("2 + 3"):
    print("安全的表达式")

# 验证表达式（不安全时抛出异常）
try:
    sandbox.validate_expression("__import__('os').system('rm -rf /')")
except Exception as e:
    print(f"不安全: {e}")
```

### 危险操作检测

```python
# 获取安全问题列表
errors = sandbox.check_expression("eval(user_input)")
if errors:
    for error in errors:
        print(f"安全问题: {error}")
```

## 自定义函数

### 注册函数

```python
def calculate_tax(amount, rate=0.1):
    """计算税费"""
    return amount * rate

engine.register_function("tax", calculate_tax)

result = engine.evaluate("price + tax(price, 0.08)", {"price": 100})
# 108.0
```

### 使用装饰器

```python
from qdata_expr import builtin_function
from qdata_expr.functions import FunctionCategory

@builtin_function(
    name="discount",
    category=FunctionCategory.MATH,
    description="计算折扣价格"
)
def discount(price, rate):
    return price * (1 - rate)
```

## 上下文解析器

### 路径解析

```python
from qdata_expr import ContextResolver, resolve

resolver = ContextResolver()

context = {
    "user": {"name": "Alice", "addresses": [{"city": "Beijing"}]}
}

# 解析路径
result = resolver.resolve("user.addresses[0].city", context)  # "Beijing"

# 便捷函数
result = resolve("user.name", context)  # "Alice"
```

### 路径操作

```python
from qdata_expr import set_path, delete_path

# 设置值
new_context = set_path("user.email", "alice@example.com", context)

# 删除路径
new_context = delete_path("user.addresses", context)
```

## 性能优化

### 启用缓存

```python
engine = ExpressionEngine(enable_cache=True)

# 相同表达式的后续调用会使用缓存
for i in range(1000):
    result = engine.evaluate("a * b + c", {"a": i, "b": 2, "c": 10})

# 查看缓存统计
print(engine.cache_stats)
```

### 预编译表达式

```python
# 预编译常用表达式
compiled = engine.compile("price * quantity * (1 + tax_rate)")

# 多次使用
for order in orders:
    total = compiled.evaluate(order)
```

## 错误处理

```python
from qdata_expr.exceptions import (
    ExpressionError,
    ExpressionParseError,
    ExpressionEvalError,
    SecurityViolationError
)

try:
    result = engine.evaluate("invalid syntax ///")
except ExpressionParseError as e:
    print(f"解析错误: {e}")
except ExpressionEvalError as e:
    print(f"求值错误: {e}")
except SecurityViolationError as e:
    print(f"安全错误: {e}")
except ExpressionError as e:
    print(f"表达式错误: {e}")
```

## 下一步

- 查看 [API 参考](api.md) 了解完整 API
- 查看 [内置函数](functions.md) 了解所有可用函数
- 查看 [示例代码](../examples/) 获取更多用例
