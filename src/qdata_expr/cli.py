"""
命令行接口

提供 qdata-expr 命令行工具。

使用示例:
    # 求值表达式
    qdata-expr eval "2 + 3 * 4"

    # 使用上下文变量（JSON 格式）
    qdata-expr eval "price * quantity" --context '{"price": 100, "quantity": 5}'

    # 渲染模板
    qdata-expr render "Hello, {{ name }}!" --context '{"name": "World"}'

    # 验证表达式
    qdata-expr validate "2 + 3 * 4"

    # 列出所有内置函数
    qdata-expr functions

    # 显示版本
    qdata-expr version
"""

import argparse
import json
import sys
from typing import Any

from ._version import __version__
from .evaluator import ExpressionEngine
from .functions import FunctionCategory
from .template import render_template, validate_template


def cmd_eval(args: argparse.Namespace) -> int:
    """执行表达式求值命令"""
    expression = args.expression
    context: dict[str, Any] = {}

    if args.context:
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError as e:
            print(f"错误: 无法解析上下文 JSON - {e}", file=sys.stderr)
            return 1

    try:
        engine = ExpressionEngine(enable_sandbox=not args.unsafe)
        result = engine.evaluate(expression, context)

        if args.json:
            print(json.dumps({"result": result}, ensure_ascii=False, default=str))
        else:
            print(result)
        return 0
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


def cmd_render(args: argparse.Namespace) -> int:
    """执行模板渲染命令"""
    template = args.template
    context: dict[str, Any] = {}

    if args.context:
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError as e:
            print(f"错误: 无法解析上下文 JSON - {e}", file=sys.stderr)
            return 1

    try:
        result = render_template(template, context)
        print(result)
        return 0
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


def cmd_validate(args: argparse.Namespace) -> int:
    """执行验证命令"""
    expression = args.expression
    validate_type = args.type

    try:
        if validate_type == "expression":
            engine = ExpressionEngine()
            errors = engine.validate(expression)
        else:
            errors = validate_template(expression)

        if errors:
            for error in errors:
                print(f"错误: {error}", file=sys.stderr)
            return 1
        else:
            print("有效")
            return 0
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


def cmd_functions(args: argparse.Namespace) -> int:
    """列出所有内置函数"""
    engine = ExpressionEngine()

    if args.category:
        try:
            _ = FunctionCategory(args.category)  # Validate category
        except ValueError:
            print(f"错误: 未知分类 '{args.category}'", file=sys.stderr)
            print(f"可用分类: {', '.join(c.value for c in FunctionCategory)}", file=sys.stderr)
            return 1

    functions = engine.list_functions()

    if args.json:
        result = {"functions": functions}
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"内置函数 ({len(functions)} 个):")
        for name in sorted(functions):
            print(f"  - {name}")

    return 0


def cmd_version(args: argparse.Namespace) -> int:
    """显示版本信息"""
    print(f"qdata-expression {__version__}")
    return 0


def create_parser() -> argparse.ArgumentParser:
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        prog="qdata-expr",
        description="QData Expression - 安全、可扩展的 Python 表达式引擎",
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # eval 命令
    eval_parser = subparsers.add_parser("eval", help="求值表达式")
    eval_parser.add_argument("expression", help="要求值的表达式")
    eval_parser.add_argument(
        "-c", "--context", help="上下文变量（JSON 格式）", default=None
    )
    eval_parser.add_argument(
        "--json", action="store_true", help="以 JSON 格式输出结果"
    )
    eval_parser.add_argument(
        "--unsafe", action="store_true", help="禁用安全沙箱（不推荐）"
    )
    eval_parser.set_defaults(func=cmd_eval)

    # render 命令
    render_parser = subparsers.add_parser("render", help="渲染模板")
    render_parser.add_argument("template", help="要渲染的模板")
    render_parser.add_argument(
        "-c", "--context", help="上下文变量（JSON 格式）", default=None
    )
    render_parser.set_defaults(func=cmd_render)

    # validate 命令
    validate_parser = subparsers.add_parser("validate", help="验证表达式或模板")
    validate_parser.add_argument("expression", help="要验证的表达式或模板")
    validate_parser.add_argument(
        "-t", "--type",
        choices=["expression", "template"],
        default="expression",
        help="验证类型（默认: expression）"
    )
    validate_parser.set_defaults(func=cmd_validate)

    # functions 命令
    functions_parser = subparsers.add_parser("functions", help="列出所有内置函数")
    functions_parser.add_argument(
        "-c", "--category", help="按分类过滤", default=None
    )
    functions_parser.add_argument(
        "--json", action="store_true", help="以 JSON 格式输出"
    )
    functions_parser.set_defaults(func=cmd_functions)

    # version 命令
    version_parser = subparsers.add_parser("version", help="显示版本信息")
    version_parser.set_defaults(func=cmd_version)

    return parser


def main() -> int:
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
