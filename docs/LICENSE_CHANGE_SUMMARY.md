# 📋 许可证更新完成总结

## ✅ 已完成的工作

### 1. 许可证文件更新

#### 主许可证（AGPL-3.0）
- ✅ **[LICENSE](../LICENSE)** - 更新为 AGPL-3.0
  - 完整的 AGPL-3.0 许可声明
  - 清晰的双重许可说明
  - 中文友好的声明文本
  - 商业用途限制说明

#### 商业许可条款
- ✅ **[COMMERCIAL-LICENSE.txt](../COMMERCIAL-LICENSE.txt)** - 新增商业许可文件
  - 详细的商业用途定义
  - 授权流程说明
  - 法律责任条款
  - 常见问题解答
  - 联系方式：vincent@qeasy.com

### 2. 项目配置更新

#### pyproject.toml
- ✅ 许可证字段：`MIT` → `AGPL-3.0-or-later`
- ✅ 分类器更新：
  ```toml
  "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"
  ```

#### README.md
- ✅ 许可证徽章：MIT → AGPL v3
- ✅ 新增完整的"许可与商业政策"章节
  - 开源协议说明
  - 商业用途定义
  - 授权流程指引
  - 法律责任警告

### 3. 文档和工具

#### 文档
- ✅ **[docs/LICENSE_HEADERS.md](../docs/LICENSE_HEADERS.md)** - 文件头模板指南
  - Python 文件模板（标准、简化、完整）
  - 其他语言文件模板
  - 使用指南和 FAQ
  - 批量处理脚本示例

#### 自动化工具
- ✅ **[scripts/add_license_headers.py](../scripts/add_license_headers.py)** - 批量添加许可声明
  - 支持预览模式 (`--dry-run`)
  - 支持强制覆盖 (`--force`)
  - 智能识别核心模块
  - 自动处理 shebang

- ✅ **[scripts/check_license_headers.py](../scripts/check_license_headers.py)** - 检查许可声明合规性
  - 标准模式和严格模式
  - 详细的错误报告
  - 可集成到 CI/CD

---

## 🎯 许可证策略

### 双重许可模式

```
┌─────────────────────────────────────────────────────────────┐
│                     QData Expression                         │
│                    许可证策略架构                             │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │   QData Expr     │
                    │   Source Code    │
                    └──────────────────┘
                            │
                ┌───────────┴────────────┐
                │                        │
        ┌───────▼────────┐      ┌───────▼────────┐
        │  AGPL-3.0      │      │  Commercial    │
        │  开源许可       │      │  商业许可       │
        └────────────────┘      └────────────────┘
                │                        │
        ┌───────▼─────────┐      ┌──────▼───────┐
        │ 个人/学习/研究   │      │ 企业/生产     │
        │ 开源项目        │      │ 商业服务      │
        │ 非商业使用      │      │ SaaS 平台     │
        └─────────────────┘      └──────────────┘
                │                        │
        ┌───────▼─────────┐      ┌──────▼───────┐
        │ 免费使用         │      │ 购买许可      │
        │ 必须开源修改     │      │ 可闭源        │
        │ 网络服务开源     │      │ 技术支持      │
        └─────────────────┘      └──────────────┘
```

### 核心特点

#### ✅ AGPL-3.0 的优势

1. **防止云厂商白嫖**
   - 网络服务必须开源修改代码
   - 堵住"闭源托管"漏洞
   - SaaS 提供商必须开源或购买商业许可

2. **鼓励社区贡献**
   - 个人学习、研究完全免费
   - 开源项目可自由使用
   - 促进技术交流和改进

3. **商业化路径清晰**
   - 商业用途必须付费
   - 法律抓手明确
   - 保护版权方利益

#### ⚖️ 商业许可的价值

1. **灵活的商业模式**
   - 闭源商业产品可集成
   - 无需开源内部修改
   - 适合企业生产环境

2. **增值服务**
   - 优先技术支持
   - 定制开发
   - 企业培训

3. **合规保障**
   - 避免侵权风险
   - 正规授权协议
   - 法律文件支持

---

## 📊 对比分析

### MIT vs AGPL-3.0

| 特性 | MIT | AGPL-3.0 + 商业许可 |
|------|-----|---------------------|
| **个人使用** | ✅ 免费 | ✅ 免费 |
| **开源项目** | ✅ 免费 | ✅ 免费（需开源） |
| **商业闭源** | ✅ 允许 | ❌ 需购买许可 |
| **SaaS 服务** | ✅ 允许闭源 | ❌ 必须开源或购买许可 |
| **云厂商托管** | ✅ 可闭源托管 | ❌ 必须开源或购买许可 |
| **版权保护** | ❌ 弱 | ✅ 强 |
| **商业化** | ❌ 难以变现 | ✅ 清晰的商业模式 |
| **社区友好** | ✅ 极度友好 | ✅ 对非商业用户友好 |

### 适用场景

#### ✅ 适合 AGPL-3.0 的项目

- ✅ 希望防止云厂商白嫖的项目
- ✅ 有明确商业化需求的项目
- ✅ 需要强版权保护的项目
- ✅ 企业级产品开源版本
- ✅ 平台类、工具类产品

#### ❌ 不适合 AGPL-3.0 的项目

- ❌ 纯公益开源项目
- ❌ 希望被广泛商业采用的基础库
- ❌ 不关心商业变现的项目
- ❌ 希望最大化开源影响力的项目

---

## 🚀 下一步行动

### 立即执行

1. **检查现有文件**
   ```bash
   python scripts/check_license_headers.py --strict
   ```

2. **添加许可声明**
   ```bash
   # 预览
   python scripts/add_license_headers.py --dry-run
   
   # 执行
   python scripts/add_license_headers.py
   ```

3. **提交更改**
   ```bash
   git add LICENSE COMMERCIAL-LICENSE.txt pyproject.toml README.md
   git add docs/LICENSE_HEADERS.md
   git add scripts/add_license_headers.py scripts/check_license_headers.py
   git commit -m "chore: update license to AGPL-3.0 with dual licensing"
   ```

### 持续维护

1. **CI/CD 集成**
   - 在 `.github/workflows/ci.yml` 中添加许可声明检查
   - 确保所有新增文件都包含许可声明

2. **文档更新**
   - 更新发布文档提及许可证变更
   - 在 CHANGELOG.md 中记录许可证更新

3. **社区沟通**
   - 发布 Release Notes 说明许可证变更
   - 在 README 显著位置说明新许可
   - 回答社区关于许可证的疑问

### 法律准备

1. **商业许可模板**
   - 准备正式的商业许可协议模板
   - 咨询法律顾问完善条款
   - 确定定价策略

2. **侵权监测**
   - 定期搜索公开部署实例
   - 监控商业使用情况
   - 准备维权流程

---

## 📚 参考资源

### AGPL-3.0 相关

- 📖 [GNU AGPL-3.0 官方文档](https://www.gnu.org/licenses/agpl-3.0.html)
- 📖 [AGPL-3.0 中文解读](https://www.gnu.org/licenses/agpl-3.0.zh-cn.html)
- 📖 [AGPL vs GPL 区别](https://www.gnu.org/licenses/why-affero-gpl.html)

### 双重许可案例

成功采用双重许可的开源项目：

- **MySQL** - GPL + 商业许可
- **Qt** - LGPL + 商业许可
- **MongoDB** - SSPL（类似 AGPL）
- **GitLab** - MIT(社区版) + 商业版
- **Sentry** - BSL（Business Source License）

### 最佳实践

- 📖 [Open Source Licensing Guide](https://opensource.guide/legal/)
- 📖 [Dual Licensing Best Practices](https://en.wikipedia.org/wiki/Multi-licensing)
- 📖 [How to Choose a License](https://choosealicense.com/)

---

## ❓ 常见问题

### Q1: 为什么选择 AGPL-3.0 而不是 GPL？

**A:** AGPL-3.0 的关键区别在于"网络服务条款"。GPL 允许闭源提供网络服务，而 AGPL-3.0 要求即使是网络服务也必须开源。这对于现代 SaaS 和云服务至关重要。

### Q2: 现有的 MIT 用户怎么办？

**A:** 许可证变更通常不具有追溯效力。已经在 MIT 下获得代码的用户可以继续使用那个版本。新版本采用 AGPL-3.0。

### Q3: 如何处理已有的商业用户？

**A:** 建议：
1. 通知现有用户许可证变更
2. 给予过渡期（如 6-12 个月）
3. 提供优惠的商业许可升级方案

### Q4: 个人开发者用于学习需要付费吗？

**A:** 不需要。AGPL-3.0 允许个人学习、研究、非商业项目免费使用。

### Q5: 我的开源项目可以使用吗？

**A:** 可以。只要你的项目也采用 AGPL-3.0 或兼容的开源许可即可。

### Q6: 如何界定"商业用途"？

**A:** 详见 `COMMERCIAL-LICENSE.txt`。简单判断：
- ✅ 个人学习项目 → 非商业
- ✅ 开源社区项目 → 非商业
- ❌ 公司内部使用 → 商业
- ❌ 对外提供服务 → 商业

### Q7: 违反许可证的后果？

**A:** 根据 `COMMERCIAL-LICENSE.txt`：
- 立即停止侵权
- 支付 3-10 倍赔偿
- 承担律师费用
- 可能面临诉讼

---

## 📞 联系方式

### 许可相关

- **开源问题**：vincent@qeasy.com
- **商业咨询**：vincent@qeasy.com
- **法律事务**：legal@qeasy.com（待设立）

### 技术支持

- **GitHub Issues**: https://github.com/qeasy/qdata-expression/issues
- **官方网站**: https://www.qeasy.cloud

---

## 📝 版本历史

- **v1.0** (2026-01-22) - 初始 AGPL-3.0 + 商业双重许可模式
- **v0.1.0** (2024) - 原 MIT 许可证

---

**许可证更新完成！**

祝你的开源项目既能保持社区活力，又能实现商业价值！🎉

---

*文档维护：广东轻亿云软件科技有限公司*  
*最后更新：2026年1月22日*
