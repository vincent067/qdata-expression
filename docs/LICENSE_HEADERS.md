# 代码文件头许可声明模板

本文档提供统一的代码文件头许可声明模板，用于所有源代码文件。

---

## Python 文件模板

### 标准模板（推荐）

```python
# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
#
# 本程序为自由软件：你可按 GNU Affero General Public License v3.0 (AGPL-3.0) 
# 条款重新分发或修改；详见 LICENSE 文件。
#
# 任何商业用途必须另行获得商业许可，详见 COMMERCIAL-LICENSE.txt。
# 商业许可咨询：vincent@qeasy.com
#
# 本程序的发布是希望它能有用，但不提供任何保证。
```

### 简化模板（适用于简单文件）

```python
# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
# AGPL-3.0 License - 商业用途需购买许可
# 详见 LICENSE 和 COMMERCIAL-LICENSE.txt
```

### 完整模板（适用于核心模块）

```python
# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
# All rights reserved.
#
# 本文件是 QData Expression 项目的一部分。
#
# 本程序为自由软件：你可按 GNU Affero General Public License v3.0 (AGPL-3.0) 
# 条款重新分发或修改；详见项目根目录的 LICENSE 文件。
#
# 本程序的发布是希望它能有用，但不提供任何保证，甚至不提供针对特定用途的
# 适销性或适用性的暗示保证。详见 GNU Affero General Public License。
#
# 你应该已经随本程序收到了一份 GNU Affero General Public License 的副本。
# 如果没有，请访问 <https://www.gnu.org/licenses/>。
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 商业用途声明
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 
# 任何以盈利为目的的使用、托管、二次分发、SaaS 对外服务，均需另行签署
# 《商业许可协议》并支付费用。详见 COMMERCIAL-LICENSE.txt 文件。
#
# 未获得书面商业许可前，禁止任何商业实体在生产环境部署本软件。
# 违反上述条款即构成版权侵权，作者可依法追责并索赔。
#
# 商业许可咨询：vincent@qeasy.com
# 项目主页：https://github.com/qeasy/qdata-expression
```

---

## Markdown 文件模板

```markdown
<!--
Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
AGPL-3.0 License - 商业用途需购买许可
详见 LICENSE 和 COMMERCIAL-LICENSE.txt
-->
```

---

## YAML/TOML 配置文件模板

```yaml
# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
# AGPL-3.0 License - 商业用途需购买许可
# 详见 LICENSE 和 COMMERCIAL-LICENSE.txt
```

---

## JavaScript/TypeScript 文件模板

```javascript
/**
 * Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
 * 
 * 本程序为自由软件：你可按 GNU Affero General Public License v3.0 (AGPL-3.0) 
 * 条款重新分发或修改；详见 LICENSE 文件。
 * 
 * 任何商业用途必须另行获得商业许可，详见 COMMERCIAL-LICENSE.txt。
 * 商业许可咨询：vincent@qeasy.com
 */
```

---

## Shell 脚本模板

```bash
#!/bin/bash
# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
# AGPL-3.0 License - 商业用途需购买许可
# 详见 LICENSE 和 COMMERCIAL-LICENSE.txt
```

---

## 使用指南

### 1. 新文件创建

所有新创建的源代码文件都应该在文件顶部添加许可声明：

- **核心模块**（evaluator, parser, sandbox 等）：使用完整模板
- **功能模块**（functions, utils 等）：使用标准模板
- **测试文件**：使用简化模板
- **配置文件**：使用简化模板
- **文档文件**：使用 Markdown 模板

### 2. 现有文件更新

对于现有文件，建议逐步更新：

```bash
# 批量更新 Python 文件示例（谨慎使用）
find src/qdata_expr -name "*.py" -type f -exec sed -i.bak '1i\
# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司\
# AGPL-3.0 License - 商业用途需购买许可\
# 详见 LICENSE 和 COMMERCIAL-LICENSE.txt\
' {} \;
```

### 3. 文件顶部位置

许可声明应该：

- 位于文件的**最顶部**
- 在 shebang (`#!/usr/bin/env python`) 之后（如果有）
- 在 module docstring 之前
- 在 import 语句之前

示例：

```python
#!/usr/bin/env python3
# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
# AGPL-3.0 License - 商业用途需购买许可
# 详见 LICENSE 和 COMMERCIAL-LICENSE.txt

"""
模块说明文档
"""

import sys
import os
```

### 4. 版权年份更新

- 首次创建文件：使用当前年份 `2026`
- 修改现有文件：保持原创建年份，添加修改年份 `2024-2026`
- 跨年度维护：更新结束年份 `2024-2027`

---

## 批量添加脚本

创建一个 Python 脚本来批量添加许可声明：

```python
#!/usr/bin/env python3
"""
批量添加许可声明到 Python 文件
"""

import os
from pathlib import Path

LICENSE_HEADER = '''# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
# AGPL-3.0 License - 商业用途需购买许可
# 详见 LICENSE 和 COMMERCIAL-LICENSE.txt

'''

def add_license_header(file_path: Path) -> None:
    """添加许可声明到文件"""
    content = file_path.read_text(encoding='utf-8')
    
    # 跳过已有许可声明的文件
    if 'Copyright' in content[:500]:
        print(f"跳过（已有许可声明）: {file_path}")
        return
    
    # 处理 shebang
    lines = content.split('\n')
    if lines[0].startswith('#!'):
        new_content = lines[0] + '\n' + LICENSE_HEADER + '\n'.join(lines[1:])
    else:
        new_content = LICENSE_HEADER + content
    
    file_path.write_text(new_content, encoding='utf-8')
    print(f"已添加许可声明: {file_path}")

def main():
    """主函数"""
    src_dir = Path('src/qdata_expr')
    
    for py_file in src_dir.rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        add_license_header(py_file)

if __name__ == '__main__':
    main()
```

使用方法：

```bash
# 保存为 scripts/add_license_headers.py
python scripts/add_license_headers.py
```

---

## 检查合规性

创建检查脚本验证所有文件是否包含许可声明：

```python
#!/usr/bin/env python3
"""
检查源代码文件是否包含许可声明
"""

from pathlib import Path

def check_license_header(file_path: Path) -> bool:
    """检查文件是否包含许可声明"""
    try:
        content = file_path.read_text(encoding='utf-8')
        return 'Copyright' in content[:500] and 'AGPL' in content[:500]
    except Exception:
        return False

def main():
    """主函数"""
    src_dir = Path('src/qdata_expr')
    missing = []
    
    for py_file in src_dir.rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        if not check_license_header(py_file):
            missing.append(py_file)
    
    if missing:
        print("以下文件缺少许可声明：")
        for file in missing:
            print(f"  - {file}")
        return 1
    else:
        print("✓ 所有文件都包含许可声明")
        return 0

if __name__ == '__main__':
    exit(main())
```

集成到 CI/CD：

```yaml
# .github/workflows/ci.yml
- name: Check License Headers
  run: python scripts/check_license_headers.py
```

---

## Pre-commit Hook

添加 pre-commit 钩子自动检查：

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-license-headers
        name: Check license headers
        entry: python scripts/check_license_headers.py
        language: system
        types: [python]
        pass_filenames: false
```

---

## FAQ

### Q1: 我需要在每个文件都添加吗？

A: 建议在所有源代码文件（.py, .js, .ts 等）中添加。配置文件和文档可以使用简化模板。

### Q2: 测试文件也需要吗？

A: 是的。测试代码也是项目的一部分，应当包含许可声明。可以使用简化模板。

### Q3: 第三方库的文件怎么办？

A: 不要修改第三方库的许可声明。只对自己编写的代码添加。

### Q4: 我fork了这个项目，需要改动吗？

A: 根据 AGPL-3.0，你需要保留原有的许可声明，可以在下方添加你的修改说明：

```python
# Copyright (c) 2024-2026 广东轻亿云软件科技有限公司
# Modified by [Your Name/Company] in 2026
# AGPL-3.0 License - 商业用途需购买许可
```

### Q5: 我可以移除许可声明吗？

A: 不可以。根据 AGPL-3.0 和商业许可条款，移除或篡改许可声明是违法的。

---

## 模板维护

模板更新由版权方维护：

- 年份需要定期更新
- 联系方式变更需要同步
- 新的文件类型需要添加相应模板

---

**最后更新：2026年1月22日**  
**维护者：广东轻亿云软件科技有限公司**
