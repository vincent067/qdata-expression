# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
#
# 本程序为自由软件：你可按 GNU Affero General Public License v3.0 (AGPL-3.0) 
# 条款重新分发或修改；详见 LICENSE 文件。
#
# 任何商业用途必须另行获得商业许可，详见 COMMERCIAL-LICENSE.txt。
# 商业许可咨询：vincent@qeasy.com
#
# 本程序的发布是希望它能有用，但不提供任何保证。

"""
模板引擎

基于 Jinja2 的模板渲染引擎，提供：
- 模板解析和渲染
- 自定义过滤器
- 与表达式引擎的集成
"""

from collections.abc import Callable
from typing import Any

from .exceptions import TemplateParseError, TemplateRenderError

# ============================================================
# Jinja2 兼容层
# ============================================================

# 尝试导入 Jinja2，如果不可用则使用简化实现
try:
    from jinja2 import (
        BaseLoader,
        Environment,
        StrictUndefined,
        TemplateSyntaxError,
        UndefinedError,
        meta,
    )

    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False
    Environment = None  # type: ignore
    BaseLoader = None  # type: ignore
    StrictUndefined = None  # type: ignore
    TemplateSyntaxError = Exception  # type: ignore
    UndefinedError = Exception  # type: ignore
    meta = None  # type: ignore


# ============================================================
# 简化模板引擎（无 Jinja2 依赖）
# ============================================================


class SimpleTemplateEngine:
    """简化模板引擎

    当 Jinja2 不可用时的降级实现。
    仅支持基本的变量替换 {{ variable }}。
    """

    import re as _re

    VARIABLE_PATTERN = _re.compile(r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*\}\}')

    def __init__(self) -> None:
        self._filters: dict[str, Callable] = {}

    def render(self, template: str, context: dict[str, Any] | None = None) -> str:
        """渲染模板"""
        import re
        context = context or {}

        def replace(match: re.Match) -> str:  # type: ignore[type-arg]
            path = match.group(1)
            parts = path.split(".")
            value = context
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part, "")
                else:
                    value = getattr(value, part, "")
                if value is None:
                    return ""
            return str(value)

        return self.VARIABLE_PATTERN.sub(replace, template)

    def validate(self, template: str) -> list[str]:
        """验证模板语法"""
        # 简化实现总是有效
        return []

    def get_variables(self, template: str) -> list[str]:
        """获取模板中的变量"""
        return self.VARIABLE_PATTERN.findall(template)

    def register_filter(self, name: str, func: Callable) -> None:
        """注册过滤器（简化实现不支持）"""
        self._filters[name] = func


# ============================================================
# Jinja2 模板引擎
# ============================================================


class Jinja2TemplateEngine:
    """Jinja2 模板引擎

    完整的 Jinja2 模板渲染能力。

    使用示例：
        engine = Jinja2TemplateEngine()

        # 基础渲染
        result = engine.render("Hello, {{ name }}!", {"name": "World"})

        # 循环
        template = '''
        {% for item in items %}
        - {{ item.name }}: {{ item.price }}
        {% endfor %}
        '''
        result = engine.render(template, {"items": [...]})

        # 条件
        template = "Status: {% if active %}Active{% else %}Inactive{% endif %}"
        result = engine.render(template, {"active": True})
    """

    def __init__(self, strict_undefined: bool = False):
        """初始化引擎

        Args:
            strict_undefined: 是否使用严格的未定义变量处理
        """
        if not HAS_JINJA2:
            raise ImportError("Jinja2 is required for Jinja2TemplateEngine")

        if strict_undefined:
            self._env = Environment(
                loader=BaseLoader(),
                autoescape=False,
                undefined=StrictUndefined,
            )
        else:
            self._env = Environment(
                loader=BaseLoader(),
                autoescape=False,
            )

        # 注册内置过滤器
        self._register_builtin_filters()

    def _register_builtin_filters(self) -> None:
        """注册内置过滤器"""
        import json

        self._env.filters.update({
            # JSON
            "json": lambda v: json.dumps(v, ensure_ascii=False, default=str),
            "json_pretty": lambda v: json.dumps(v, ensure_ascii=False, indent=2, default=str),

            # 默认值
            "default": lambda v, d="": d if v is None else v,
            "default_if_none": lambda v, d="": d if v is None else v,
            "default_if_empty": lambda v, d="": d if not v else v,

            # 字符串
            "truncate": lambda s, l, e="...": str(s)[:l - len(e)] + e if len(str(s)) > l else str(s),
            "upper": lambda s: str(s).upper(),
            "lower": lambda s: str(s).lower(),
            "title": lambda s: str(s).title(),
            "capitalize": lambda s: str(s).capitalize(),
            "strip": lambda s: str(s).strip(),

            # 格式化
            "number_format": lambda v, d=2: f"{float(v):,.{d}f}",
            "date_format": lambda d, f="%Y-%m-%d": d.strftime(f) if d else "",
        })

    def register_filter(self, name: str, func: Callable) -> None:
        """注册自定义过滤器

        Args:
            name: 过滤器名称
            func: 过滤器函数
        """
        self._env.filters[name] = func

    def render(self, template: str, context: dict[str, Any] | None = None) -> str:
        """渲染模板

        Args:
            template: 模板字符串
            context: 上下文变量

        Returns:
            渲染结果
        """
        context = context or {}

        try:
            tpl = self._env.from_string(template)
            return tpl.render(**context)
        except UndefinedError as e:
            raise TemplateRenderError(template, f"未定义的变量: {e}")
        except TemplateSyntaxError as e:
            raise TemplateParseError(template, e.message, e.lineno)
        except Exception as e:
            raise TemplateRenderError(template, str(e), e)

    def validate(self, template: str) -> list[str]:
        """验证模板语法

        Args:
            template: 模板字符串

        Returns:
            错误列表（空列表表示有效）
        """
        errors = []
        try:
            self._env.parse(template)
        except TemplateSyntaxError as e:
            errors.append(f"语法错误 (行 {e.lineno}): {e.message}")
        return errors

    def get_variables(self, template: str) -> list[str]:
        """获取模板中的变量

        Args:
            template: 模板字符串

        Returns:
            变量名列表
        """
        try:
            ast = self._env.parse(template)
            return sorted(meta.find_undeclared_variables(ast))
        except TemplateSyntaxError:
            return []


# ============================================================
# 统一模板引擎
# ============================================================


class TemplateEngine:
    """统一模板引擎

    自动选择可用的实现（Jinja2 或简化实现）。

    使用示例：
        engine = TemplateEngine()

        # 渲染
        result = engine.render("Hello, {{ name }}!", {"name": "World"})

        # 验证
        errors = engine.validate("{{ invalid }")

        # 获取变量
        variables = engine.get_variables("{{ a }} + {{ b }}")
    """

    def __init__(self, strict_undefined: bool = False):
        """初始化引擎

        Args:
            strict_undefined: 是否使用严格的未定义变量处理
        """
        if HAS_JINJA2:
            self._engine = Jinja2TemplateEngine(strict_undefined)
        else:
            self._engine = SimpleTemplateEngine()

    @property
    def has_full_support(self) -> bool:
        """是否有完整的 Jinja2 支持"""
        return HAS_JINJA2

    def render(self, template: str, context: dict[str, Any] | None = None) -> str:
        """渲染模板"""
        return self._engine.render(template, context)

    def validate(self, template: str) -> list[str]:
        """验证模板语法"""
        return self._engine.validate(template)

    def get_variables(self, template: str) -> list[str]:
        """获取模板中的变量"""
        return self._engine.get_variables(template)

    def register_filter(self, name: str, func: Callable) -> None:
        """注册自定义过滤器"""
        self._engine.register_filter(name, func)


# ============================================================
# 便捷函数
# ============================================================


# 默认引擎
_default_engine: TemplateEngine | None = None


def get_default_template_engine() -> TemplateEngine:
    """获取默认模板引擎"""
    global _default_engine
    if _default_engine is None:
        _default_engine = TemplateEngine()
    return _default_engine


def render_template(template: str, context: dict[str, Any] | None = None) -> str:
    """渲染模板（使用默认引擎）"""
    engine = get_default_template_engine()
    return engine.render(template, context)


def validate_template(template: str) -> list[str]:
    """验证模板语法（使用默认引擎）"""
    engine = get_default_template_engine()
    return engine.validate(template)


def get_template_variables(template: str) -> list[str]:
    """获取模板中的变量（使用默认引擎）"""
    engine = get_default_template_engine()
    return engine.get_variables(template)
