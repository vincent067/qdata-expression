#!/usr/bin/env python3
"""
检查源代码文件是否包含许可声明

用法:
    python scripts/check_license_headers.py [--strict]

退出码:
    0 - 所有文件都包含许可声明
    1 - 有文件缺少许可声明
"""

import argparse
from pathlib import Path
import sys


def check_license_header(file_path: Path, strict: bool = False) -> tuple[bool, str]:
    """检查文件是否包含许可声明
    
    Args:
        file_path: 文件路径
        strict: 严格模式，检查是否包含 AGPL-3.0
    
    Returns:
        (is_valid, message)
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"无法读取文件: {e}"
    
    first_lines = content[:1000]
    
    # 基本检查
    has_copyright = 'Copyright' in first_lines
    has_company = '广东轻亿云软件科技有限公司' in first_lines or 'qeasy' in first_lines.lower()
    
    if not has_copyright:
        return False, "缺少 Copyright 声明"
    
    if not has_company:
        return False, "缺少公司名称"
    
    # 严格模式：检查 AGPL-3.0
    if strict:
        has_agpl = 'AGPL' in first_lines or 'GNU Affero General Public License' in first_lines
        has_commercial_notice = 'COMMERCIAL-LICENSE' in first_lines or '商业' in first_lines
        
        if not has_agpl:
            return False, "缺少 AGPL-3.0 许可声明"
        
        if not has_commercial_notice:
            return False, "缺少商业许可提示"
    
    return True, "OK"


def check_directory(directory: Path, strict: bool = False) -> tuple[list, list]:
    """检查目录中的所有 Python 文件
    
    Returns:
        (valid_files, invalid_files)
    """
    valid_files = []
    invalid_files = []
    
    for py_file in directory.rglob('*.py'):
        # 跳过特殊目录
        if any(part in py_file.parts for part in ['__pycache__', '.venv', 'venv', 'build', 'dist']):
            continue
        
        is_valid, message = check_license_header(py_file, strict)
        
        if is_valid:
            valid_files.append(py_file)
        else:
            invalid_files.append((py_file, message))
    
    return valid_files, invalid_files


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='检查源代码文件是否包含许可声明',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 基本检查
  python scripts/check_license_headers.py
  
  # 严格检查（确保包含 AGPL-3.0 声明）
  python scripts/check_license_headers.py --strict
        '''
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='严格模式：检查是否包含完整的 AGPL-3.0 许可声明'
    )
    
    args = parser.parse_args()
    
    # 获取项目根目录
    root_dir = Path(__file__).parent.parent
    src_dir = root_dir / 'src' / 'qdata_expr'
    
    if not src_dir.exists():
        print(f"❌ 源代码目录不存在: {src_dir}")
        return 1
    
    print("=" * 60)
    print("检查许可声明")
    print("=" * 60)
    print(f"目录: {src_dir}")
    print(f"模式: {'严格模式' if args.strict else '标准模式'}")
    print("=" * 60)
    print()
    
    # 检查文件
    valid_files, invalid_files = check_directory(src_dir, args.strict)
    
    # 显示结果
    if invalid_files:
        print(f"❌ 发现 {len(invalid_files)} 个文件缺少许可声明：")
        print()
        for file_path, message in invalid_files:
            rel_path = file_path.relative_to(root_dir)
            print(f"  ❌ {rel_path}")
            print(f"     原因: {message}")
        print()
        print("=" * 60)
        print(f"✅ 合规: {len(valid_files)} 个文件")
        print(f"❌ 不合规: {len(invalid_files)} 个文件")
        print("=" * 60)
        print()
        print("💡 运行以下命令自动添加许可声明：")
        print("   python scripts/add_license_headers.py")
        return 1
    else:
        print("✅ 所有文件都包含许可声明！")
        print()
        print("=" * 60)
        print(f"检查通过: {len(valid_files)} 个文件")
        print("=" * 60)
        return 0


if __name__ == '__main__':
    sys.exit(main())
