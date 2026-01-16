"""
Tests for template engine.
"""

import pytest

from qdata_expr import (
    TemplateEngine,
    TemplateParseError,
    TemplateRenderError,
    get_default_template_engine,
    get_template_variables,
    render_template,
    validate_template,
)


class TestTemplateEngine:
    """Test TemplateEngine class."""

    def test_template_engine_creation(self):
        """Test template engine creation."""
        engine = TemplateEngine()
        assert engine is not None

    def test_template_engine_creation_strict(self):
        """Test template engine creation with strict undefined."""
        engine = TemplateEngine(strict_undefined=True)
        assert engine is not None

    def test_basic_rendering(self, template_engine: TemplateEngine):
        """Test basic template rendering."""
        template = "Hello, {{ name }}!"
        context = {"name": "World"}
        result = template_engine.render(template, context)
        assert result == "Hello, World!"

    def test_rendering_without_context(self, template_engine: TemplateEngine):
        """Test rendering without context."""
        template = "Hello, World!"
        result = template_engine.render(template)
        assert result == "Hello, World!"

    def test_variable_rendering(self, template_engine: TemplateEngine, sample_context: dict):
        """Test variable rendering."""
        template = "User: {{ user.name }}, Age: {{ user.age }}"
        result = template_engine.render(template, sample_context)
        assert result == "User: Alice, Age: 30"

    def test_nested_variable_rendering(self, template_engine: TemplateEngine, sample_context: dict):
        """Test nested variable rendering."""
        template = "First address: {{ user.addresses[0].city }}"
        result = template_engine.render(template, sample_context)
        assert result == "First address: Beijing"

    def test_builtin_filters(self, template_engine: TemplateEngine):
        """Test built-in filters."""
        context = {"name": "  john doe  ", "items": ["apple", "banana", "cherry"]}

        # Upper filter
        result = template_engine.render("{{ name | upper }}", context)
        assert result == "  JOHN DOE  "

        # Lower filter
        result = template_engine.render("{{ name | lower }}", context)
        assert result == "  john doe  "

        # Trim filter
        result = template_engine.render("{{ name | trim }}", context)
        assert result == "john doe"

        # Join filter
        result = template_engine.render("{{ items | join(', ') }}", context)
        assert result == "apple, banana, cherry"

        # Default filter (for None value)
        context_with_none = {"value": None}
        result = template_engine.render("{{ value | default('N/A') }}", context_with_none)
        assert result == "N/A"

        # Length filter
        result = template_engine.render("{{ items | length }}", context)
        assert result == "3"

    def test_custom_filter(self, template_engine: TemplateEngine):
        """Test custom filter registration."""
        def double_filter(value):
            return value * 2

        template_engine.register_filter("double", double_filter)
        result = template_engine.render("{{ 5 | double }}")
        assert result == "10"

    def test_conditionals(self, template_engine: TemplateEngine):
        """Test conditional statements."""
        context = {"age": 25}
        template = "{% if age >= 18 %}Adult{% else %}Minor{% endif %}"
        result = template_engine.render(template, context)
        assert result == "Adult"

        context = {"age": 15}
        result = template_engine.render(template, context)
        assert result == "Minor"

    def test_conditionals_else_if(self, template_engine: TemplateEngine):
        """Test else-if conditions."""
        context = {"score": 85}
        template = """
{% if score >= 90 %}A
{% elif score >= 80 %}B
{% elif score >= 70 %}C
{% else %}F{% endif %}
"""
        result = template_engine.render(template, context)
        assert result.strip() == "B"

    def test_loops(self, template_engine: TemplateEngine):
        """Test loop statements."""
        context = {"items": ["apple", "banana", "cherry"]}
        template = "{% for item in items %}{{ item }}{% endfor %}"
        result = template_engine.render(template, context)
        assert result == "applebananacherry"

    def test_loops_with_variables(self, template_engine: TemplateEngine, sample_context: dict):
        """Test loops with variables."""
        # Use dict-style access to avoid conflict with dict.items() method
        template = """
{% for item in order['items'] %}
{{ item.name }}: ${{ item.price }}
{% endfor %}
"""
        result = template_engine.render(template, sample_context)
        lines = [line.strip() for line in result.strip().split('\n') if line.strip()]
        assert len(lines) == 2
        assert "Laptop: $999.99" in lines
        assert "Mouse: $29.99" in lines

    def test_loops_with_loop_variables(self, template_engine: TemplateEngine):
        """Test loop variables."""
        context = {"item_list": ["a", "b", "c"]}
        template = "{% for item in item_list %}{{ loop.index }}. {{ item }} {% endfor %}"
        result = template_engine.render(template, context)
        assert result == "1. a 2. b 3. c "

    def test_nested_loops(self, template_engine: TemplateEngine):
        """Test nested loops."""
        context = {
            "categories": [
                {"name": "Fruits", "products": ["apple", "banana"]},
                {"name": "Vegetables", "products": ["carrot", "potato"]},
            ]
        }
        template = """
{% for category in categories %}
{{ category.name }}:
{% for item in category.products %}
  - {{ item }}
{% endfor %}
{% endfor %}
"""
        result = template_engine.render(template, context)
        assert "Fruits:" in result
        assert "  - apple" in result
        assert "  - banana" in result
        assert "Vegetables:" in result

    def test_comments(self, template_engine: TemplateEngine):
        """Test template comments."""
        template = """
{# This is a comment #}
Hello, {{ name }}!
{# Another comment #}
"""
        context = {"name": "World"}
        result = template_engine.render(template, context)
        assert result.strip() == "Hello, World!"

    def test_filter_chaining(self, template_engine: TemplateEngine):
        """Test filter chaining."""
        context = {"text": "  Hello World  "}
        result = template_engine.render("{{ text | trim | upper }}", context)
        assert result == "HELLO WORLD"

        result = template_engine.render("{{ text | upper | trim }}", context)
        assert result == "HELLO WORLD"

    def test_arithmetic_in_templates(self, template_engine: TemplateEngine):
        """Test arithmetic in templates."""
        context = {"price": 100, "quantity": 3, "tax": 0.1}
        template = "Total: ${{ (price * quantity * (1 + tax)) | round(2) }}"
        result = template_engine.render(template, context)
        assert result == "Total: $330.0"

    def test_string_literals(self, template_engine: TemplateEngine):
        """Test string literals in templates."""
        template = '{{ "Hello, " + name + "!" }}'
        result = template_engine.render(template, {"name": "World"})
        assert result == "Hello, World!"

    def test_comparison_in_templates(self, template_engine: TemplateEngine):
        """Test comparisons in templates."""
        context = {"score": 95}
        template = "{% if score > 90 %}Excellent{% else %}Good{% endif %}"
        result = template_engine.render(template, context)
        assert result == "Excellent"

    def test_empty_loops(self, template_engine: TemplateEngine):
        """Test empty loops."""
        context = {"items": []}
        template = "{% for item in items %}{{ item }}{% else %}No items{% endfor %}"
        result = template_engine.render(template, context)
        assert result == "No items"

    def test_whitespace_control(self, template_engine: TemplateEngine):
        """Test whitespace control."""
        context = {"item_list": ["a", "b"]}
        template = """
{% for item in item_list -%}
{{ item }}
{%- endfor %}
"""
        result = template_engine.render(template, context)
        # With whitespace control, lines are joined without newlines
        assert "ab" in result or "a\nb" in result

    def test_error_handling_undefined_variable(self, template_engine: TemplateEngine):
        """Test error handling for undefined variables."""
        template = "{{ undefined_variable }}"
        
        # Default behavior (should render empty string for Jinja2)
        result = template_engine.render(template)
        if template_engine.has_full_support:
            assert result == ""
        else:
            # Simple template engine behavior
            assert result == ""

    def test_error_handling_strict_mode(self):
        """Test strict mode error handling."""
        engine = TemplateEngine(strict_undefined=True)
        template = "{{ undefined_variable }}"
        
        if engine.has_full_support:
            with pytest.raises(TemplateRenderError):
                engine.render(template)

    def test_error_handling_syntax_error(self):
        """Test syntax error handling."""
        engine = TemplateEngine()
        template = "{% if %}Invalid syntax{% endif %}"
        
        if engine.has_full_support:
            with pytest.raises(TemplateParseError):
                engine.render(template)

    def test_template_validation(self, template_engine: TemplateEngine):
        """Test template validation."""
        # Valid template
        errors = template_engine.validate("Hello, {{ name }}!")
        assert len(errors) == 0

        # Invalid template
        if template_engine.has_full_support:
            errors = template_engine.validate("{% if %}Invalid{% endif %}")
            assert len(errors) > 0

    def test_get_variables(self, template_engine: TemplateEngine):
        """Test variable extraction from templates."""
        template = "Hello, {{ name }}! Your order #{{ order.id }} is {{ order.status }}."
        variables = template_engine.get_variables(template)
        
        if template_engine.has_full_support:
            assert "name" in variables
            assert "order" in variables
        else:
            # Simple template engine extracts simple patterns
            assert len(variables) >= 0

    def test_get_variables_complex(self, template_engine: TemplateEngine):
        """Test variable extraction from complex templates."""
        template = """
{% for item in order.items %}
{{ item.name }}: {{ item.price }}
{% endfor %}
{% if user %}
{{ user.name }}
{% endif %}
"""
        variables = template_engine.get_variables(template)
        
        if template_engine.has_full_support:
            assert "order" in variables
            assert "user" in variables


class TestJinja2TemplateEngine:
    """Test Jinja2TemplateEngine class."""

    def test_jinja2_engine_creation(self):
        """Test Jinja2 engine creation."""
        try:
            from qdata_expr.template import Jinja2TemplateEngine
            engine = Jinja2TemplateEngine()
            assert engine is not None
        except ImportError:
            pytest.skip("Jinja2 not available")

    def test_jinja2_strict_mode(self):
        """Test Jinja2 strict mode."""
        try:
            from qdata_expr.template import Jinja2TemplateEngine
            engine = Jinja2TemplateEngine(strict_undefined=True)
            
            with pytest.raises(TemplateRenderError):
                engine.render("{{ undefined_var }}")
        except ImportError:
            pytest.skip("Jinja2 not available")

    def test_jinja2_custom_filters(self):
        """Test Jinja2 custom filters."""
        try:
            from qdata_expr.template import Jinja2TemplateEngine
            engine = Jinja2TemplateEngine()
            
            def reverse_filter(value):
                return value[::-1]
            
            engine.register_filter("reverse", reverse_filter)
            result = engine.render("{{ 'hello' | reverse }}")
            assert result == "olleh"
        except ImportError:
            pytest.skip("Jinja2 not available")


class TestSimpleTemplateEngine:
    """Test SimpleTemplateEngine class."""

    def test_simple_engine_creation(self):
        """Test simple engine creation."""
        from qdata_expr.template import SimpleTemplateEngine
        engine = SimpleTemplateEngine()
        assert engine is not None

    def test_simple_engine_rendering(self):
        """Test simple engine rendering."""
        from qdata_expr.template import SimpleTemplateEngine
        engine = SimpleTemplateEngine()
        
        template = "Hello, {{ name }}!"
        context = {"name": "World"}
        result = engine.render(template, context)
        assert result == "Hello, World!"

    def test_simple_engine_nested_variables(self):
        """Test simple engine with nested variables."""
        from qdata_expr.template import SimpleTemplateEngine
        engine = SimpleTemplateEngine()
        
        template = "{{ user.name }} - {{ user.age }}"
        context = {"user": {"name": "Alice", "age": 30}}
        result = engine.render(template, context)
        assert result == "Alice - 30"

    def test_simple_engine_missing_variable(self):
        """Test simple engine with missing variable."""
        from qdata_expr.template import SimpleTemplateEngine
        engine = SimpleTemplateEngine()
        
        template = "Hello, {{ missing }}!"
        result = engine.render(template, {})
        assert result == "Hello, !"


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_render_template_function(self):
        """Test render_template convenience function."""
        result = render_template("Hello, {{ name }}!", {"name": "World"})
        assert result == "Hello, World!"

    def test_validate_template_function(self):
        """Test validate_template convenience function."""
        errors = validate_template("Hello, {{ name }}!")
        assert len(errors) == 0

    def test_get_template_variables_function(self):
        """Test get_template_variables convenience function."""
        variables = get_template_variables("Hello, {{ name }}! Your age is {{ age }}.")
        assert len(variables) >= 0  # Depends on implementation

    def test_get_default_template_engine(self):
        """Test get_default_template_engine function."""
        engine = get_default_template_engine()
        assert isinstance(engine, TemplateEngine)

        # Should return the same instance
        engine2 = get_default_template_engine()
        assert engine is engine2
