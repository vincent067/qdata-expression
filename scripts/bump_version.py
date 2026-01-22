#!/usr/bin/env python3
"""
版本管理工具

自动化版本号更新和发布准备。
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


class Colors:
    """终端颜色"""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_info(msg: str) -> None:
    """打印信息"""
    print(f"{Colors.OKBLUE}ℹ {msg}{Colors.ENDC}")


def print_success(msg: str) -> None:
    """打印成功信息"""
    print(f"{Colors.OKGREEN}✓ {msg}{Colors.ENDC}")


def print_error(msg: str) -> None:
    """打印错误信息"""
    print(f"{Colors.FAIL}✗ {msg}{Colors.ENDC}", file=sys.stderr)


def print_warning(msg: str) -> None:
    """打印警告信息"""
    print(f"{Colors.WARNING}⚠ {msg}{Colors.ENDC}")


def get_root_dir() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.parent


def get_current_version() -> str:
    """获取当前版本号"""
    version_file = get_root_dir() / "src" / "qdata_expr" / "_version.py"
    content = version_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("无法找到版本号")
    return match.group(1)


def parse_version(version: str) -> tuple[int, int, int]:
    """解析版本号"""
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"无效的版本号格式: {version}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def bump_version(current: str, part: str) -> str:
    """递增版本号"""
    major, minor, patch = parse_version(current)

    if part == "major":
        return f"{major + 1}.0.0"
    elif part == "minor":
        return f"{major}.{minor + 1}.0"
    elif part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"无效的版本部分: {part}")


def update_version_file(new_version: str) -> None:
    """更新 _version.py 文件"""
    version_file = get_root_dir() / "src" / "qdata_expr" / "_version.py"
    content = version_file.read_text()

    # 更新版本号
    content = re.sub(
        r'__version__\s*=\s*["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        content,
    )

    version_file.write_text(content)
    print_success(f"已更新 {version_file.relative_to(get_root_dir())}")


def update_pyproject_toml(new_version: str) -> None:
    """更新 pyproject.toml 文件"""
    pyproject_file = get_root_dir() / "pyproject.toml"
    content = pyproject_file.read_text()

    # 更新版本号
    content = re.sub(
        r'version\s*=\s*["\'][^"\']+["\']',
        f'version = "{new_version}"',
        content,
        count=1,
    )

    pyproject_file.write_text(content)
    print_success(f"已更新 {pyproject_file.relative_to(get_root_dir())}")


def update_changelog(new_version: str) -> None:
    """更新 CHANGELOG.md"""
    changelog_file = get_root_dir() / "CHANGELOG.md"

    if not changelog_file.exists():
        print_warning("CHANGELOG.md 不存在，跳过更新")
        return

    content = changelog_file.read_text()
    today = date.today().isoformat()

    # 在 ## [Unreleased] 后添加新版本
    new_section = f"\n## [{new_version}] - {today}\n\n### Added\n\n### Changed\n\n### Fixed\n\n"

    if "## [Unreleased]" in content:
        content = content.replace("## [Unreleased]", f"## [Unreleased]\n{new_section}")
    else:
        # 如果没有 Unreleased 部分，在文件开头添加
        lines = content.split("\n")
        # 找到第一个 ## 标题的位置
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("## "):
                insert_idx = i
                break

        lines.insert(insert_idx, new_section)
        content = "\n".join(lines)

    changelog_file.write_text(content)
    print_success(f"已更新 {changelog_file.relative_to(get_root_dir())}")
    print_warning(f"请手动编辑 CHANGELOG.md 添加版本更新内容")


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """运行命令"""
    print_info(f"执行: {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def git_status_clean() -> bool:
    """检查 Git 工作区是否干净"""
    result = run_command(["git", "status", "--porcelain"], check=False)
    return len(result.stdout.strip()) == 0


def create_git_tag(version: str, message: str) -> None:
    """创建 Git tag"""
    tag_name = f"v{version}"
    run_command(["git", "tag", "-a", tag_name, "-m", message])
    print_success(f"已创建 tag: {tag_name}")


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="版本管理工具")
    parser.add_argument(
        "action",
        choices=["bump", "show", "tag"],
        help="操作: bump (递增版本), show (显示当前版本), tag (创建 Git tag)",
    )
    parser.add_argument(
        "part",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="要递增的版本部分 (用于 bump)",
    )
    parser.add_argument(
        "--version",
        help="指定版本号 (用于 tag)",
    )
    parser.add_argument(
        "--message",
        "-m",
        help="Tag 消息 (用于 tag)",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="自动提交版本更改",
    )

    args = parser.parse_args()

    try:
        if args.action == "show":
            current = get_current_version()
            print(f"{Colors.BOLD}当前版本: {Colors.OKGREEN}{current}{Colors.ENDC}")

        elif args.action == "bump":
            if not args.part:
                print_error("bump 操作需要指定版本部分 (major/minor/patch)")
                sys.exit(1)

            if not git_status_clean():
                print_error("Git 工作区不干净，请先提交或暂存更改")
                sys.exit(1)

            current = get_current_version()
            new_version = bump_version(current, args.part)

            print_info(f"版本号: {current} → {new_version}")

            # 更新文件
            update_version_file(new_version)
            update_pyproject_toml(new_version)
            update_changelog(new_version)

            print_success(f"版本号已更新到 {new_version}")

            if args.commit:
                # Git 提交
                run_command(["git", "add", "."])
                run_command(
                    ["git", "commit", "-m", f"chore: bump version to {new_version}"]
                )
                print_success("已提交版本更改")

            print_info("\n后续步骤:")
            print("  1. 检查并编辑 CHANGELOG.md")
            if not args.commit:
                print("  2. git add .")
                print(f"  3. git commit -m 'chore: bump version to {new_version}'")
            print(f"  4. git tag -a v{new_version} -m 'Release v{new_version}'")
            print("  5. git push origin main --tags")

        elif args.action == "tag":
            version = args.version or get_current_version()
            message = args.message or f"Release v{version}"

            if not git_status_clean():
                print_error("Git 工作区不干净，请先提交或暂存更改")
                sys.exit(1)

            create_git_tag(version, message)

            print_info("\n后续步骤:")
            print(f"  git push origin v{version}")

    except Exception as e:
        print_error(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
