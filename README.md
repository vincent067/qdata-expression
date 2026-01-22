# QData Expression

<p align="center">
  <strong>安全、可扩展的 Python 表达式引擎</strong>
</p>

<p align="center">
  由 <a href="https://www.qeasy.cloud">广东轻亿云软件科技有限公司</a> 开发<br>
  「轻易云数据集成平台」核心组件
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+"></a>
  <a href="https://www.gnu.org/licenses/agpl-3.0"><img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" alt="License: AGPL v3"></a>
  <a href="https://pypi.org/project/qdata-expression/"><img src="https://img.shields.io/pypi/v/qdata-expression.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/qdata-expression/"><img src="https://img.shields.io/pypi/dm/qdata-expression.svg" alt="Downloads"></a>
  <a href="https://github.com/qeasy/qdata-expression/actions/workflows/ci.yml"><img src="https://github.com/qeasy/qdata-expression/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://codecov.io/gh/qeasy/qdata-expression"><img src="https://codecov.io/gh/qeasy/qdata-expression/branch/main/graph/badge.svg" alt="Coverage"></a>
  <a href="https://jinja.palletsprojects.com/"><img src="https://img.shields.io/badge/Powered%20by-Jinja2-red.svg" alt="Jinja2"></a>
</p>

---

## 🌟 关于轻易云数据集成平台

> **数据集成，简单看得见**

轻易云是一款企业级数据集成平台，专注于帮助企业快速、高效地打通各类业务系统之间的数据通道。

<a href="https://www.qeasy.cloud">
  <img src="https://qcdn.qeasy.cloud/static/logo.svg" alt="轻易云" height="60">
</a>

### ✨ 平台亮点

- 🔌 **即插即用**：无需复杂开发，配置即连接，支持 500+ 主流应用系统对接
- 👁️ **全程可视**：数据流动、转换过程、执行状态一目了然，如同"物流跟踪"般清晰透明
- ⚡ **高性能引擎**：基于优化的执行引擎，轻松处理复杂表达式求值
- 🛡️ **企业级可靠**：完善的安全沙箱机制，防止代码注入和恶意操作
- 🧩 **灵活扩展**：插件化架构设计，支持自定义函数和过滤器扩展

### 🎯 适用场景

| 场景 | 描述 |
|------|------|
| **动态计算** | 业务规则引擎中的动态表达式求值 |
| **模板渲染** | 配置化的消息模板、报告生成 |
| **数据转换** | ETL 流程中的字段计算与转换 |
| **公式计算** | 用户自定义公式的安全执行 |

**QData Expression** 是轻易云数据集成平台的核心表达式引擎，现已开源，助力开发者构建安全、灵活的动态计算能力。

---

## 📖 目录

- [特性](#特性)
- [快速开始](#-快速开始)
- [核心概念](#核心概念)
- [使用指南](./docs/usage.md)
- [API 参考](./docs/api.md)
- [内置函数](./docs/functions.md)
- [示例](./examples/)
- [贡献](./CONTRIBUTING.md)
- [许可证](#-许可证)

---

## 特性

- 🛡️ **安全沙箱**：内置安全机制，防止代码注入和恶意操作
- 📝 **表达式求值**：支持复杂的数学和逻辑表达式
- 🎨 **模板引擎**：基于 Jinja2 的强大模板渲染
- 📦 **内置函数**：丰富的内置函数库（数学、字符串、日期、逻辑等）
- 🔧 **可扩展**：易于注册自定义函数和过滤器
- ⚡ **高性能**：表达式缓存和优化的执行引擎
- 🎯 **类型安全**：完整的类型提示支持

---

## 🚀 快速开始

### 安装

```bash
pip install qdata-expression
```

### 第一个表达式

```python
from qdata_expr import ExpressionEngine, evaluate, render_template

# 创建表达式引擎
engine = ExpressionEngine()

# 求值表达式
result = engine.evaluate("2 + 3 * 4")
print(result)  # 14

# 使用上下文变量
context = {"price": 100, "quantity": 5}
result = engine.evaluate("price * quantity", context)
print(result)  # 500

# 使用内置函数
result = engine.evaluate("abs(-5) + round(3.14, 1)")
print(result)  # 8.1

# 模板渲染
result = render_template("Hello, {{ name }}!", {"name": "World"})
print(result)  # Hello, World!
```

---

## 核心概念

| 概念 | 描述 |
|------|------|
| **表达式引擎 (ExpressionEngine)** | 安全求值数学和逻辑表达式 |
| **模板引擎 (TemplateEngine)** | 基于 Jinja2 的模板渲染 |
| **安全沙箱 (Sandbox)** | 防止不安全操作的保护层 |
| **上下文解析器 (ContextResolver)** | 嵌套路径的变量解析 |
| **函数注册表 (FunctionRegistry)** | 管理内置和自定义函数 |

---

## 📦 安装

```bash
# PyPI 安装
pip install qdata-expression

# 源码安装
git clone https://github.com/qeasy/qdata-expression.git
cd qdata-expression
pip install -e .

# 开发依赖
pip install -e ".[dev]"
```

---

## 示例与文档

- 完整用法示例请见 [`./examples/`](./examples/)
- 详细文档请见 [`./docs/`](./docs/)

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行带覆盖率测试
pytest --cov=qdata_expr --cov-report=html
```

---

## 📄 许可与商业政策

### 🔓 开源协议

本项目采用 **GNU Affero General Public License v3.0 (AGPL-3.0)** 开源协议。

- ✅ **个人学习/研究**：完全免费，无需授权
- ✅ **开源项目**：可自由使用，需遵守 AGPL-3.0 条款
- ✅ **修改与分发**：允许修改和重新分发，但必须保持开源

**重要**：如果你修改本软件并提供网络服务（包括内部使用），根据 AGPL-3.0 条款，你必须公开你的修改源代码。

### 💼 商业用途

任何**商业用途**必须单独购买商业许可，包括但不限于：

- ❌ 企业/公司在生产环境中使用
- ❌ 提供基于本软件的商业服务或 SaaS
- ❌ 集成到商业产品中销售
- ❌ 超过 5 个用户的组织使用
- ❌ 任何以盈利为目的的部署和使用

**商业许可咨询**：📧 vincent@qeasy.com

### 📋 许可文件

- **开源许可**：[LICENSE](LICENSE) - AGPL-3.0 完整条款
- **商业许可**：[COMMERCIAL-LICENSE.txt](COMMERCIAL-LICENSE.txt) - 商业授权详情

### ⚠️ 重要提示

**未经授权的商业使用将构成版权侵权，我们保留追究法律责任的权利。**

详细说明请查看：[COMMERCIAL-LICENSE.txt](COMMERCIAL-LICENSE.txt)

---

## 🏢 关于轻易云数据集成平台

**广东轻亿云软件科技有限公司**  
专注数据集成与处理，提供企业级 ETL/ELT 解决方案  
🌐 官网：[https://www.qeasy.cloud](https://www.qeasy.cloud)  
📧 开源项目：opensource@qeasy.cloud  
📧 商业咨询：vincent@qeasy.com

---

*Powered by [广东轻亿云软件科技有限公司](https://www.qeasy.cloud)*
