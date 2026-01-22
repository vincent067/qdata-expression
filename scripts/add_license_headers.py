#!/usr/bin/env python3
"""
批量添加许可声明到源代码文件

用法:
    python scripts/add_license_headers.py [--dry-run] [--force]

选项:
    --dry-run  只显示将要修改的文件，不实际修改
    --force    强制覆盖已有的许可声明
"""

import argparse
from pathlib import Path
import sys

# 标准许可声明模板
LICENSE_HEADER_STANDARD = '''# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
# AGPL-3.0 License - 商业用途需购买许可
# 详见 LICENSE 和 COMMERCIAL-LICENSE.txt

'''

LICENSE_HEADER_FULL = '''# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
#
# 本程序为自由软件：你可按 GNU Affero General Public License v3.0 (AGPL-3.0) 
# 条款重新分发或修改；详见 LICENSE 文件。
#
# 任何商业用途必须另行获得商业许可，详见 COMMERCIAL-LICENSE.txt。
# 商业许可咨询：vincent@qeasy.cloud
#
# 本程序的发布是希望它能有用，但不提供任何保证。

'''

# 核心模块使用完整模板
CORE_MODULES = ['evaluator.py', 'parser.py', 'sandbox.py', 'context.py', 'template.py']


def has_license_header(content: str) -> bool:
    """检查是否已有许可声明"""
    first_lines = content[:1000]
    return 'Copyright' in first_lines and ('AGPL' in first_lines or 'MIT' in first_lines)


def get_license_header(file_path: Path) -> str:
    """根据文件类型获取合适的许可声明"""
    if file_path.name in CORE_MODULES:
        return LICENSE_HEADER_FULL
    return LICENSE_HEADER_STANDARD


def add_license_header(file_path: Path, dry_run: bool = False, force: bool = False) -> bool:
    """添加许可声明到文件
    
    Returns:
        True if file was modified (or would be in dry-run mode)
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ 无法读取文件 {file_path}: {e}")
        return False
    
    # 检查是否已有许可声明
    if has_license_header(content) and not force:
        print(f"⏭️  跳过（已有许可声明）: {file_path}")
        return False
    
    # 获取合适的许可声明
    license_header = get_license_header(file_path)
    
    # 处理文件内容
    lines = content.split('\n')
    
    # 如果是强制模式，移除旧的许可声明
    if force and has_license_header(content):
        # 简单处理：跳过前面的注释行
        start_idx = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('#'):
                start_idx = i
                break
        lines = lines[start_idx:]
        content = '\n'.join(lines)
    
    # 处理 shebang
    if lines and lines[0].startswith('#!'):
        new_content = lines[0] + '\n' + license_header + '\n'.join(lines[1:])
    else:
        new_content = license_header + content
    
    if dry_run:
        print(f"🔍 将要修改: {file_path}")
        return True
    
    # 写入文件
    try:
        file_path.write_text(new_content, encoding='utf-8')
        print(f"✅ 已添加许可声明: {file_path}")
        return True
    except Exception as e:
        print(f"❌ 无法写入文件 {file_path}: {e}")
        return False


def process_directory(directory: Path, dry_run: bool = False, force: bool = False) -> tuple[int, int]:
    """处理目录中的所有 Python 文件
    
    Returns:
        (modified_count, skipped_count)
    """
    modified = 0
    skipped = 0
    
    for py_file in directory.rglob('*.py'):
        # 跳过特殊目录
        if any(part in py_file.parts for part in ['__pycache__', '.venv', 'venv', 'build', 'dist']):
            continue
        
        if add_license_header(py_file, dry_run, force):
            modified += 1
        else:
            skipped += 1
    
    return modified, skipped


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='批量添加许可声明到源代码文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 预览将要修改的文件
  python scripts/add_license_headers.py --dry-run
  
  # 添加许可声明到所有文件
  python scripts/add_license_headers.py
  
  # 强制更新所有文件（包括已有许可声明的）
  python scripts/add_license_headers.py --force
        '''
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='只显示将要修改的文件，不实际修改'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='强制覆盖已有的许可声明'
    )
    
    args = parser.parse_args()
    
    # 获取项目根目录
    root_dir = Path(__file__).parent.parent
    src_dir = root_dir / 'src' / 'qdata_expr'
    
    if not src_dir.exists():
        print(f"❌ 源代码目录不存在: {src_dir}")
        return 1
    
    print("=" * 60)
    print("批量添加许可声明")
    print("=" * 60)
    print(f"目录: {src_dir}")
    print(f"模式: {'预览模式' if args.dry_run else '修改模式'}")
    if args.force:
        print("⚠️  强制模式：将覆盖已有许可声明")
    print("=" * 60)
    print()
    
    # 处理文件
    modified, skipped = process_directory(src_dir, args.dry_run, args.force)
    
    print()
    print("=" * 60)
    print("处理完成")
    print("=" * 60)
    print(f"{'将要修改' if args.dry_run else '已修改'}: {modified} 个文件")
    print(f"已跳过: {skipped} 个文件")
    
    if args.dry_run and modified > 0:
        print()
        print("💡 使用不带 --dry-run 参数运行以实际修改文件")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
