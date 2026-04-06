# 贡献指南 | Contributing Guide

感谢你对 **人工智能中文教程** 项目的关注！🎉

无论你是修正一个错别字、改进一段解释、编写一节完整的课程，还是提出一个改进建议，你的每一份贡献都非常重要。

Thank you for your interest in the **Artificial Intelligence Tutorial (CN)** project! 🎉 Whether you're fixing a typo, improving an explanation, writing a full lesson, or suggesting an enhancement, every contribution matters.

---

## 📖 目录 | Table of Contents

- [行为准则 | Code of Conduct](#-行为准则--code-of-conduct)
- [如何贡献 | How to Contribute](#-如何贡献--how-to-contribute)
- [开发流程 | Development Workflow](#-开发流程--development-workflow)
- [目录与文件规范 | Directory & File Conventions](#-目录与文件规范--directory--file-conventions)
- [课程内容规范 | Content Standards](#-课程内容规范--content-standards)
- [Git 提交规范 | Commit Conventions](#-git-提交规范--commit-conventions)
- [Pull Request 流程 | Pull Request Process](#-pull-request-流程--pull-request-process)
- [Issue 指南 | Issue Guidelines](#-issue-指南--issue-guidelines)
- [参考资料引用规范 | Reference Citation Standards](#-参考资料引用规范--reference-citation-standards)
- [注意事项 | Important Notes](#-注意事项--important-notes)

---

## 📜 行为准则 | Code of Conduct

参与本项目即表示你同意遵守我们的 [行为准则](CODE_OF_CONDUCT.md)。请在贡献之前阅读。

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

---

## 🚀 如何贡献 | How to Contribute

我们欢迎以下类型的贡献：

We welcome the following types of contributions:

| 贡献类型 | 说明 | Type | Description |
| :--- | :--- | :--- | :--- |
| 📝 撰写课程 | 为空的知识点目录编写课程内容 | Write Lessons | Create content for empty knowledge point directories |
| 🔧 修正错误 | 修正已有课程中的文字、公式、代码错误 | Fix Errors | Correct text, formula, or code errors in existing lessons |
| 🎨 改进排版 | 优化 Markdown 排版、图表、代码格式 | Improve Formatting | Optimize Markdown layout, diagrams, and code format |
| 💡 提出建议 | 通过 Issue 提出内容改进或结构调整建议 | Suggest Improvements | Submit suggestions via Issues |
| 🐛 报告问题 | 报告课程中的技术错误、链接失效等 | Report Bugs | Report technical errors, broken links, etc. |

---

## 🔄 开发流程 | Development Workflow

### 1. Fork 仓库 | Fork the Repository

点击页面右上角的 **Fork** 按钮，将仓库复制到你的账号下。

Click the **Fork** button at the top-right corner to create a copy under your account.

### 2. 克隆到本地 | Clone Locally

```bash
git clone https://github.com/<你的用户名>/Artificial_Intelligence_Tutorial_CN.git
cd Artificial_Intelligence_Tutorial_CN
```

### 3. 创建分支 | Create a Branch

```bash
git checkout -b feature/你的功能描述
```

**分支命名建议 | Branch naming suggestions**：

| 前缀 | 用途 | Prefix | Purpose |
| :--- | :--- | :--- | :--- |
| `feature/` | 新增课程内容 | `feature/` | New lesson content |
| `fix/` | 修正错误 | `fix/` | Bug fixes |
| `improve/` | 改进排版或优化 | `improve/` | Formatting improvements |
| `docs/` | 文档更新 | `docs/` | Documentation updates |

### 4. 编写内容并提交 | Write Content and Commit

详见下方的 [目录与文件规范](#-目录与文件规范--directory--file-conventions) 和 [课程内容规范](#-课程内容规范--content-standards)。

See the [Directory & File Conventions](#-目录与文件规范--directory--file-conventions) and [Content Standards](#-课程内容规范--content-standards) sections below.

### 5. 推送并创建 Pull Request | Push and Create a Pull Request

```bash
git push origin feature/你的功能描述
```

然后在 GitHub 上创建 Pull Request。

Then create a Pull Request on GitHub.

---

## 📂 目录与文件规范 | Directory & File Conventions

本项目采用四级目录结构：

This project uses a four-level directory structure:

```
阶段 / 主题模块 / 知识主题 / 知识点
Stage / Topic Module / Knowledge Topic / Knowledge Point
```

### 知识点目录结构 | Knowledge Point Directory Structure

```
知识点目录/
├── 知识点名称.md        ← 课程主文件（必须）| Main course file (required)
├── 01_第一讲.md         ← 分讲文件（按需）| Sub-lectures (optional)
├── assets/              ← 图片、图表资源（按需）| Images & diagrams (optional)
├── code/                ← 示例代码文件（按需）| Example code (optional)
└── exercises/           ← 练习题与参考答案（按需）| Exercises (optional)
```

### ⚠️ 重要命名规则 | Important Naming Rules

- **课程主文件** 使用与知识点目录同名的 `.md` 文件，**不要使用 `README.md`**。
  - 例如：知识点目录为 `01_一元二次方程/`，则课程主文件为 `01_一元二次方程/01_一元二次方程.md`
- **知识主题概览页**（第三级目录）使用 `README.md` 作为概览和导航页。
- 所有目录和文件使用**中文命名**，通过**数字前缀**保持学习顺序。

- **Main course files** should use a `.md` file with the same name as the directory, **not `README.md`**.
  - Example: Directory `01_一元二次方程/` → main file `01_一元二次方程/01_一元二次方程.md`
- **Knowledge topic overview pages** (3rd-level directories) use `README.md` for navigation.
- All directories and files use **Chinese names** with **numeric prefixes** for ordering.

---

## 📝 课程内容规范 | Content Standards

每篇课程内容应包含以下章节：

Each lesson should contain the following sections:

| 章节 | 必须 | Section | Required |
| :--- | :---: | :--- | :---: |
| 前置知识 | ✅ | Prerequisites | ✅ |
| 学习目标 | ✅ | Learning Objectives | ✅ |
| 正文讲解 | ✅ | Main Content | ✅ |
| 动手实践 | ✅ | Hands-on Practice | ✅ |
| 典型误区 | ✅ | Common Misconceptions | ✅ |
| 练习题 | ✅ | Exercises | ✅ |
| 下一步学习 | ✅ | Next Steps | ✅ |
| 参考资料 | ✅ | References | ✅ |

### 教学策略 | Teaching Approach

- **叙事引导式教学**：像讲故事一样引出概念，不干巴巴地罗列定义。
- **先直觉后形式**：先用日常语言解释，再给出数学或技术定义。
- **先简单后复杂**：先展示最简单的例子，再逐步增加复杂度。
- **先具体后抽象**：先用具体数字演示，再抽象为通用公式。

- **Narrative-driven teaching**: Introduce concepts through storytelling, not dry definitions.
- **Intuition before formalism**: Explain in everyday language first, then provide formal definitions.
- **Simple before complex**: Start with the simplest examples, then gradually increase complexity.
- **Concrete before abstract**: Demonstrate with specific numbers first, then generalize.

### 代码要求 | Code Requirements

- 默认使用 **Python 3.10+** | Default language: **Python 3.10+**
- 所有代码必须可直接运行 | All code must be directly runnable
- 关键步骤必须有中文注释 | Key steps must have Chinese comments
- 注明依赖库及版本 | Specify dependency libraries and versions

### 数学公式要求 | Math Formula Requirements

- 使用 LaTeX 语法：行内 `$...$`，独立行 `$$...$$` | Use LaTeX: inline `$...$`, display `$$...$$`
- 行内公式前后各加一个空格 | Add a space before and after inline formulas
- 每个关键公式后附「直觉解读」| Add intuitive explanations after key formulas

### 术语规范 | Terminology Standards

- 首次出现使用中文全称，括号内标注英文全称和缩写。
- 示例：**梯度下降（Gradient Descent, GD）**
- 后续行文统一使用最常用的形式。

- First occurrence: Chinese full name with English in parentheses.
- Example: **梯度下降（Gradient Descent, GD）**
- Subsequent mentions: use the most common form consistently.

> 📖 完整的课程模板和质量检查清单请参阅 [AGENTS.MD](AGENTS.MD)。
>
> 📖 For the complete course template and quality checklist, see [AGENTS.MD](AGENTS.MD).

---

## 💬 Git 提交规范 | Commit Conventions

提交信息使用**中文**，格式如下：

Commit messages should be in **Chinese**, following this format:

```
[阶段编号/主题模块] 动作：知识点名称
```

**示例 | Examples**：

```
[00/数学基础] 新增：01_一元二次方程课程内容
[02/深度学习] 修正：03_优化器公式错误
[01/数据能力] 改进：02_数据清洗排版优化
```

**常用动作词 | Common action verbs**：

| 动作 | 用途 | Action | Purpose |
| :--- | :--- | :--- | :--- |
| 新增 | 创建新的课程内容 | New | Create new lesson content |
| 修正 | 修复错误 | Fix | Fix errors |
| 改进 | 优化排版或内容 | Improve | Optimize layout or content |
| 更新 | 更新已有内容 | Update | Update existing content |
| 删除 | 移除过时内容 | Remove | Remove outdated content |

### 其他注意事项 | Additional Notes

- 课程内容创建后，请删除对应的 `.gitkeep` 占位文件。
- Remove the corresponding `.gitkeep` placeholder file after creating lesson content.

---

## 🔀 Pull Request 流程 | Pull Request Process

### 提交前检查 | Pre-submission Checklist

请在提交 PR 前确认以下事项：

Please confirm the following before submitting a PR:

- [ ] 内容遵循课程模板结构 | Content follows the course template structure
- [ ] 代码可直接运行 | Code is directly runnable
- [ ] 数学公式格式正确 | Math formulas are correctly formatted
- [ ] 链接使用相对路径 | Links use relative paths
- [ ] 已删除对应的 `.gitkeep` 文件 | Corresponding `.gitkeep` files removed
- [ ] 提交信息符合规范 | Commit messages follow conventions

### 审查流程 | Review Process

1. 维护者将审查你的 PR，可能会提出修改建议。
2. 请在收到反馈后及时回应和更新。
3. PR 通过审查后将被合并到主分支。

1. Maintainers will review your PR and may suggest changes.
2. Please respond to feedback and update promptly.
3. Once approved, the PR will be merged into the main branch.

---

## 📋 Issue 指南 | Issue Guidelines

提交 Issue 时，请：

When submitting an Issue, please:

- 使用提供的 Issue 模板 | Use the provided Issue templates
- 清晰描述问题或建议 | Clearly describe the problem or suggestion
- 如果是内容错误，请注明具体的知识点路径和行号 | For content errors, specify the knowledge point path and line number
- 如果是功能建议，请说明预期效果和理由 | For feature suggestions, explain the expected outcome and rationale

---

## 📚 参考资料引用规范 | Reference Citation Standards

课程中的参考资料**只允许引用确定开源或公开可访问的资源**：

References in lessons **must only cite confirmed open-source or publicly accessible resources**:

### ✅ 允许引用 | Allowed

- 开源教材或 Creative Commons 许可的书籍 | Open-source textbooks or CC-licensed books
- 官方文档（如 Python、PyTorch 等） | Official documentation (e.g., Python, PyTorch)
- 作者公开发布的博客、视频或教程 | Publicly available blogs, videos, or tutorials
- 学术论文（arXiv 预印本或开放获取） | Academic papers (arXiv preprints or open access)
- 维基百科等公共知识库 | Public knowledge bases like Wikipedia

### ❌ 禁止引用 | Not Allowed

- 付费教材或版权受保护的书籍 | Paid textbooks or copyrighted books
- 需要登录或付费才能访问的内容 | Content requiring login or payment
- 版权归属不清晰的网络资源 | Web resources with unclear copyright

每条参考资料应注明其开放获取性质（如「开源教材」「官方文档」「CC BY 许可」等）。

Each reference should note its open-access nature (e.g., "open-source textbook", "official documentation", "CC BY license").

---

## ⚠️ 注意事项 | Important Notes

- 🚫 **请勿修改** `知识图谱可视化/` 目录下的文件（该模块独立维护）。
- 🚫 **请勿在课程中硬编码绝对路径**，链接应使用相对路径。
- 🚫 **请勿引入** 与教程无关的第三方框架依赖。
- 🚫 **请勿删除** 尚未被课程内容替代的 `.gitkeep` 文件。
- 🚫 **请勿在知识点目录中** 使用 `README.md` 作为课程主文件名。

- 🚫 **Do not modify** files under `知识图谱可视化/` (maintained independently).
- 🚫 **Do not hardcode absolute paths** in lessons; use relative paths.
- 🚫 **Do not introduce** third-party framework dependencies unrelated to the tutorial.
- 🚫 **Do not delete** `.gitkeep` files that haven't been replaced by lesson content.
- 🚫 **Do not use** `README.md` as the main course file name in knowledge point directories.

---

## 💬 需要帮助？ | Need Help?

如果你有任何疑问，欢迎：

If you have any questions, feel free to:

- 📧 在本仓库提交 [Issue](../../issues) | Submit an [Issue](../../issues)
- 💬 如需公开讨论，请在 Issue 中提供问题背景与相关上下文 | For public questions, please use Issues and include relevant background and context

---

再次感谢你的贡献！让我们一起构建高质量的中文人工智能学习资源。🚀

Thank you again for contributing! Let's build high-quality Chinese AI learning resources together. 🚀
