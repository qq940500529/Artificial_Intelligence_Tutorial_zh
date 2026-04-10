# 安全策略 | Security Policy

感谢你帮助我们维护 **人工智能中文教程** 项目的安全。本文档说明了如何报告安全漏洞以及我们的响应流程。

Thank you for helping keep the **Artificial Intelligence Tutorial (zh)** project safe. This document describes how to report security vulnerabilities and our response process.

---

## 📋 支持的版本 | Supported Versions

本项目为教育类开源内容项目，始终以主分支（`main`）的最新版本为准。

This is an educational open-source content project. The latest version on the `main` branch is always the supported version.

| 版本 / Version | 支持状态 / Status |
| :--- | :--- |
| `main` 分支最新版 / Latest on `main` | ✅ 支持 / Supported |
| 其他分支 / Other branches | ❌ 不支持 / Not supported |

---

## 🔒 报告安全问题 | Reporting a Vulnerability

如果你发现了安全问题（包括但不限于以下情况），请**不要**在公开的 Issue 中报告，而是通过私密方式联系我们：

If you discover a security issue (including but not limited to the following), please **do not** report it in a public Issue. Instead, contact us privately:

### 安全问题类型 | Types of Security Issues

- 🔑 仓库中意外泄露了敏感信息（密钥、令牌、个人数据等）
- 🔗 课程内容中包含指向恶意网站的链接
- 💻 示例代码中存在可能被利用的安全漏洞
- 📦 依赖库中存在已知的安全漏洞
- 🛡️ GitHub Actions 工作流中的安全配置问题

- 🔑 Accidental exposure of sensitive information (keys, tokens, personal data, etc.)
- 🔗 Links to malicious websites in course content
- 💻 Exploitable security vulnerabilities in example code
- 📦 Known security vulnerabilities in dependencies
- 🛡️ Security configuration issues in GitHub Actions workflows

### 报告方式 | How to Report

1. **唯一报告方式 | Only reporting method**：请通过 [GitHub Security Advisories](../../security/advisories/new) 提交私密安全报告。

   Please submit private security reports only through [GitHub Security Advisories](../../security/advisories/new).

如无法使用上述链接，请在仓库的 **Security** 选项卡中创建私密安全报告；请不要通过公开 Issue 报告安全问题。

If the link above is unavailable, use the repository's **Security** tab to create a private security report; please do not report security issues in a public Issue.

### 报告内容 | What to Include

请在报告中尽量包含以下信息：

Please include the following information in your report:

- 📝 问题的详细描述 | Detailed description of the issue
- 📍 受影响的文件路径或 URL | Affected file paths or URLs
- 🔄 复现步骤（如适用）| Steps to reproduce (if applicable)
- 💥 潜在影响的评估 | Assessment of potential impact
- 💡 建议的修复方案（如有） | Suggested fix (if any)

---

## ⏱️ 响应流程 | Response Process

我们承诺按照以下时间线处理安全报告：

We commit to the following timeline for handling security reports:

| 阶段 | 时间 | Phase | Timeline |
| :--- | :--- | :--- | :--- |
| 确认收到报告 | 48 小时内 | Acknowledge receipt | Within 48 hours |
| 初步评估 | 5 个工作日内 | Initial assessment | Within 5 business days |
| 修复发布 | 根据严重程度尽快处理 | Fix release | As soon as possible based on severity |
| 公开披露 | 修复后协商决定 | Public disclosure | Coordinated after fix |

---

## 🙏 致谢 | Acknowledgments

我们感谢所有负责任地报告安全问题的贡献者。在修复发布后，我们将在适当的位置感谢报告者（如报告者同意）。

We appreciate all contributors who responsibly report security issues. After a fix is released, we will acknowledge the reporter (with their consent) in the appropriate location.

---

## 📜 免责声明 | Disclaimer

本项目的示例代码仅用于教学目的。在将任何示例代码应用到生产环境之前，请务必进行充分的安全审查和测试。

The example code in this project is for educational purposes only. Please conduct thorough security reviews and testing before applying any example code to production environments.
