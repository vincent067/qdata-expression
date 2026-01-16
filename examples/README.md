# 示例代码

本目录包含 QData Expression 的使用示例。

## 文件说明

| 文件 | 描述 |
|------|------|
| [basic_usage.py](basic_usage.py) | 基本用法示例，包括表达式求值、上下文变量、内置函数等 |
| [template_examples.py](template_examples.py) | 模板引擎示例，包括条件、循环、过滤器等 |
| [custom_functions.py](custom_functions.py) | 自定义函数注册和使用示例 |
| [security_examples.py](security_examples.py) | 安全沙箱功能示例 |
| [performance_benchmark.py](performance_benchmark.py) | 性能基准测试 |

## 运行示例

```bash
# 进入项目根目录
cd qdata-expression

# 安装项目
pip install -e .

# 运行基本示例
python examples/basic_usage.py

# 运行模板示例
python examples/template_examples.py

# 运行自定义函数示例
python examples/custom_functions.py

# 运行安全示例
python examples/security_examples.py

# 运行性能测试
python examples/performance_benchmark.py
```

## 快速开始

### 表达式求值

```python
from qdata_expr import ExpressionEngine, evaluate

# 创建引擎
engine = ExpressionEngine()

# 基本计算
result = engine.evaluate("2 + 3 * 4")  # 14

# 使用上下文
context = {"price": 100, "quantity": 5}
result = engine.evaluate("price * quantity", context)  # 500

# 便捷函数
result = evaluate("abs(-10) + round(3.14159, 2)")  # 13.14
```

### 模板渲染

```python
from qdata_expr import render_template

# 简单模板
result = render_template("Hello, {{ name }}!", {"name": "World"})
# "Hello, World!"

# 条件模板
template = "{% if age >= 18 %}Adult{% else %}Minor{% endif %}"
result = render_template(template, {"age": 25})
# "Adult"
```

### 安全沙箱

```python
from qdata_expr import Sandbox

sandbox = Sandbox()

# 检查表达式安全性
if sandbox.is_safe("2 + 3"):
    print("安全")

# 获取安全问题
issues = sandbox.check_expression("eval('hack')")
# ['不允许使用 eval 函数']
```

## 更多信息

- [使用指南](../docs/usage.md)
- [API 参考](../docs/api.md)
- [内置函数](../docs/functions.md)
