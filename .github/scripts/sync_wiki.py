#!/usr/bin/env python3
"""sync_wiki.py — 将课程内容同步到 GitHub Wiki
Sync course content from main repository to GitHub Wiki.

功能 | Features:
  1. 扫描已完成的课程 .md 文件，复制到 Wiki 仓库（保留目录结构）
  2. 转换目录链接为具体文件链接，确保 Wiki 内跳转正常
  3. 为每个页面添加导航面包屑
  4. 复制 assets/code 等资源目录
  5. 为无 README 的知识主题生成索引页
  6. 生成 Home.md（首页）、_Sidebar.md（侧边栏）、_Footer.md（页脚）

环境变量 | Environment Variables:
  MAIN_REPO_PATH    — 主仓库路径
  WIKI_REPO_PATH    — Wiki 仓库路径
  GITHUB_REPOSITORY — GitHub 仓库全名 (owner/repo)
"""

import os
import re
import shutil
from pathlib import Path
from collections import OrderedDict

# ---------------------------------------------------------------------------
# 常量 | Constants
# ---------------------------------------------------------------------------

STAGES = [
    '00_高中复习',
    '01_基础能力',
    '02_核心原理',
    '03_工程落地',
    '04_持续研究',
]

STAGE_META = {
    '00_高中复习': ('阶段 00：高中复习', '补齐进入人工智能前最必要的基础'),
    '01_基础能力': ('阶段 01：基础能力', '建立可持续学习的工具链与理论底座'),
    '02_核心原理': ('阶段 02：核心原理', '理解经典与现代 AI 的核心机制'),
    '03_工程落地': ('阶段 03：工程落地', '将模型训练、部署、监控串成系统'),
    '04_持续研究': ('阶段 04：持续研究', '建立持续更新知识与专业判断的能力'),
}

# ---------------------------------------------------------------------------
# 主入口 | Main
# ---------------------------------------------------------------------------


def main():
    main_repo = Path(os.environ['MAIN_REPO_PATH']).resolve()
    wiki_repo = Path(os.environ['WIKI_REPO_PATH']).resolve()
    github_repo = os.environ['GITHUB_REPOSITORY']

    syncer = WikiSyncer(main_repo, wiki_repo, github_repo)
    syncer.run()


# ---------------------------------------------------------------------------
# 核心同步类 | Core Syncer
# ---------------------------------------------------------------------------


class WikiSyncer:
    """Scans course content and syncs it to a GitHub Wiki repository."""

    def __init__(self, main_repo: Path, wiki_repo: Path, github_repo: str):
        self.main = main_repo
        self.wiki = wiki_repo
        self.repo_slug = github_repo
        # tree: stage_dir -> module_dir -> topic_dir -> {readme, points}
        self.tree: OrderedDict = OrderedDict()
        self.stats = {'pages': 0, 'points': 0, 'assets': 0}

    # ---------------------------------------------------------------
    # public
    # ---------------------------------------------------------------

    def run(self):
        print('🔄 Starting wiki sync …')
        self._clean()
        self._scan_and_copy()
        self._gen_topic_indexes()
        self._gen_home()
        self._gen_sidebar()
        self._gen_footer()
        print(
            f'\n✅ Done — {self.stats["pages"]} pages, '
            f'{self.stats["points"]} knowledge points, '
            f'{self.stats["assets"]} asset files'
        )

    # ---------------------------------------------------------------
    # 1. clean wiki (keep .git)
    # ---------------------------------------------------------------

    def _clean(self):
        """Remove everything in wiki repo except .git directory."""
        for p in self.wiki.iterdir():
            if p.name == '.git':
                continue
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()

    # ---------------------------------------------------------------
    # 2. scan & copy course content
    # ---------------------------------------------------------------

    def _scan_and_copy(self):
        """Walk the 4-level course tree; copy completed content to wiki."""
        print('📂 Scanning course content …')

        for stage_dir in STAGES:
            stage_path = self.main / stage_dir
            if not stage_path.is_dir():
                continue

            stage_data: OrderedDict = OrderedDict()

            for module_path in sorted(stage_path.iterdir()):
                if not module_path.is_dir():
                    continue

                module_data: OrderedDict = OrderedDict()

                for topic_path in sorted(module_path.iterdir()):
                    if not topic_path.is_dir():
                        continue

                    topic_data = {
                        'readme': None,
                        'points': OrderedDict(),
                    }

                    # --- topic README (level 3) ---
                    readme = topic_path / 'README.md'
                    if readme.is_file():
                        rel = self._copy_md(readme)
                        topic_data['readme'] = rel

                    # --- knowledge points (level 4) ---
                    for point_path in sorted(topic_path.iterdir()):
                        if not point_path.is_dir():
                            continue

                        course_file = point_path / f'{point_path.name}.md'
                        if not course_file.is_file():
                            continue  # empty placeholder (.gitkeep only)

                        rel = self._copy_md(course_file)
                        topic_data['points'][point_path.name] = rel
                        self.stats['points'] += 1

                        # copy resource sub-directories
                        for sub in sorted(point_path.iterdir()):
                            if sub.is_dir() and not sub.name.startswith('.'):
                                self._copy_dir(sub)

                        # copy extra .md files (sub-lectures)
                        for extra in sorted(point_path.glob('*.md')):
                            if extra.name != f'{point_path.name}.md':
                                self._copy_md(extra)

                    if topic_data['readme'] or topic_data['points']:
                        module_data[topic_path.name] = topic_data

                if module_data:
                    stage_data[module_path.name] = module_data

            self.tree[stage_dir] = stage_data

    # ---------------------------------------------------------------
    # helpers: copy files
    # ---------------------------------------------------------------

    def _copy_md(self, src: Path) -> str:
        """Copy an .md file to wiki with nav header + link transforms."""
        rel = src.relative_to(self.main)
        dest = self.wiki / rel
        dest.parent.mkdir(parents=True, exist_ok=True)

        content = src.read_text(encoding='utf-8')
        content = self._add_nav(content, rel)
        content = self._transform_links(content, rel)
        dest.write_text(content, encoding='utf-8')
        self.stats['pages'] += 1
        return str(rel)

    def _copy_dir(self, src: Path):
        """Copy a resource directory (assets/, code/, …) to wiki."""
        if not src.is_dir():
            return
        rel = src.relative_to(self.main)
        dest = self.wiki / rel
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        self.stats['assets'] += sum(1 for f in src.rglob('*') if f.is_file())

    # ---------------------------------------------------------------
    # 3. navigation header (breadcrumb)
    # ---------------------------------------------------------------

    def _add_nav(self, content: str, rel_path: Path) -> str:
        """Prepend a breadcrumb navigation bar to page content."""
        parts = rel_path.parts
        depth = len(parts) - 1  # directories above the file

        if depth > 0:
            up = '/'.join(['..'] * depth)
            home_link = f'[🏠 首页]({up}/Home)'
        else:
            home_link = '[🏠 首页](Home)'

        crumbs = ' / '.join(parts[:-1])
        if crumbs:
            header = f'> {home_link} · {crumbs}\n\n---\n\n'
        else:
            header = f'> {home_link}\n\n---\n\n'

        return header + content

    # ---------------------------------------------------------------
    # 4. link transformation
    # ---------------------------------------------------------------

    def _transform_links(self, content: str, file_rel_path: Path) -> str:
        """Transform directory-only links to point to concrete .md files."""
        file_dir = file_rel_path.parent

        def _replace(match):
            full = match.group(0)
            text = match.group(1)
            url = match.group(2)

            # skip external / anchor / data / mailto links
            if re.match(r'^(https?://|#|mailto:|data:)', url):
                return full

            # directory links (ending with /)
            if url.endswith('/'):
                resolved = (self.main / file_dir / url).resolve()
                if resolved.is_dir():
                    name = resolved.name
                    # prefer course main file, then README
                    if (resolved / f'{name}.md').is_file():
                        return f'[{text}]({url}{name}.md)'
                    if (resolved / 'README.md').is_file():
                        return f'[{text}]({url}README.md)'
                # leave as-is if target doesn't exist

            return full

        return re.sub(r'\[([^\]]*)\]\(([^)]+)\)', _replace, content)

    # ---------------------------------------------------------------
    # 5. generate topic index pages (for topics without README)
    # ---------------------------------------------------------------

    def _gen_topic_indexes(self):
        """Create index pages for topics that have points but no README."""
        print('📑 Generating topic index pages …')

        for stage_dir, stage_data in self.tree.items():
            for mod_name, mod_data in stage_data.items():
                for topic_name, topic_data in mod_data.items():
                    if topic_data['readme'] is not None:
                        continue  # already has a README
                    if not topic_data['points']:
                        continue  # no content to index

                    rel_dir = f'{stage_dir}/{mod_name}/{topic_name}'
                    idx_rel = f'{rel_dir}/README.md'
                    dest = self.wiki / idx_rel
                    dest.parent.mkdir(parents=True, exist_ok=True)

                    lines = [
                        f'# {topic_name}',
                        '',
                        f'> **所属路径**：`{rel_dir}`',
                        f'> **包含知识点**：{len(topic_data["points"])} 个',
                        '',
                        '---',
                        '',
                        '## 知识点列表',
                        '',
                    ]

                    for pt_name, pt_path in topic_data['points'].items():
                        # link relative to the README location
                        pt_file = f'./{pt_name}/{pt_name}.md'
                        lines.append(f'- [{pt_name}]({pt_file})')

                    lines.append('')

                    # add nav header
                    nav_content = '\n'.join(lines)
                    idx_path = Path(idx_rel)
                    nav_content = self._add_nav(nav_content, idx_path)

                    dest.write_text(nav_content, encoding='utf-8')
                    topic_data['readme'] = idx_rel
                    self.stats['pages'] += 1

    # ---------------------------------------------------------------
    # 6. Home.md
    # ---------------------------------------------------------------

    def _gen_home(self):
        """Generate the wiki landing page."""
        print('🏠 Generating Home.md …')
        repo_url = f'https://github.com/{self.repo_slug}'

        lines = [
            '# 🎓 人工智能中文教程',
            '',
            f'> 本 Wiki 自动同步自 **[主仓库]({repo_url})** 的课程内容，'
            '提供更友好的浏览体验。',
            f'> 如需修改内容，请在 [主仓库]({repo_url}) 提交 PR。',
            '',
            '---',
            '',
            '## 📖 课程导航',
            '',
            '本教程面向零基础学习者，从高中知识复习出发，'
            '系统构建人工智能完整知识体系。',
            '',
            '| 阶段 | 名称 | 核心任务 | 已完成知识点 |',
            '| :--: | ---- | -------- | :----------: |',
        ]

        # summary table
        for sd in STAGES:
            meta = STAGE_META[sd]
            sdata = self.tree.get(sd, {})
            count = sum(
                len(td['points'])
                for md in sdata.values()
                for td in md.values()
            )
            label = f'{count} 个' if count > 0 else '—'
            stage_num = sd[:2]
            lines.append(
                f'| {stage_num} | [{meta[0]}](#{_anchor(meta[0])}) '
                f'| {meta[1]} | {label} |'
            )

        lines.extend(['', '---', ''])

        # detailed sections
        for sd in STAGES:
            meta = STAGE_META[sd]
            sdata = self.tree.get(sd, {})

            lines.append(f'## {meta[0]}')
            lines.append('')

            if not sdata:
                lines.append('_暂无已完成的课程内容。_')
                lines.extend(['', '---', ''])
                continue

            for mod_name, mod_data in sdata.items():
                lines.append(f'### 📚 {mod_name}')
                lines.append('')

                for topic_name, topic_data in mod_data.items():
                    if topic_data['readme']:
                        lines.append(
                            f'<details><summary>'
                            f'<strong>📂 <a href="{topic_data["readme"]}">'
                            f'{topic_name}</a></strong> '
                            f'({len(topic_data["points"])} 个知识点)'
                            f'</summary>'
                        )
                    else:
                        lines.append(
                            f'<details><summary>'
                            f'<strong>📂 {topic_name}</strong> '
                            f'({len(topic_data["points"])} 个知识点)'
                            f'</summary>'
                        )
                    lines.append('')

                    for pt_name, pt_path in topic_data['points'].items():
                        lines.append(f'- [{pt_name}]({pt_path})')

                    lines.extend(['', '</details>', ''])

                lines.append('')

            lines.extend(['---', ''])

        # learning philosophy
        lines.extend([
            '## 📐 学习哲学',
            '',
            '1. 不从热点工具入门，而从底层能力出发',
            '2. 不把数学、编程、数据、模型割裂成彼此无关的学科',
            '3. 不把工程部署视为附加项，而把它视为专业能力的一部分',
            '4. 不把论文阅读和趋势判断留到最后，而是在理解原理后尽早介入',
            '5. 不把伦理、安全与产品思维当作附录，'
            '而把它们纳入完整的专业判断体系',
            '',
            '---',
            '',
            f'> 📖 详细课程体系说明请查看 '
            f'[主仓库 README]({repo_url}#readme)',
        ])

        (self.wiki / 'Home.md').write_text(
            '\n'.join(lines), encoding='utf-8'
        )

    # ---------------------------------------------------------------
    # 7. _Sidebar.md
    # ---------------------------------------------------------------

    def _gen_sidebar(self):
        """Generate the wiki sidebar with collapsible navigation."""
        print('📑 Generating _Sidebar.md …')

        lines = [
            '**[🏠 首页](Home)**',
            '',
            '---',
            '',
        ]

        for sd in STAGES:
            meta = STAGE_META[sd]
            sdata = self.tree.get(sd, {})
            has_content = any(
                td['points']
                for md in sdata.values()
                for td in md.values()
            )
            open_attr = ' open' if has_content else ''

            lines.append(f'<details{open_attr}>')
            lines.append(
                f'<summary><strong>{meta[0]}</strong></summary>'
            )
            lines.append('')

            if not has_content:
                lines.append('&emsp;_暂无课程_')
                lines.append('')
            else:
                for mod_name, mod_data in sdata.items():
                    lines.append('<details>')
                    lines.append(
                        f'<summary>&emsp;📚 {mod_name}</summary>'
                    )
                    lines.append('')

                    for topic_name, topic_data in mod_data.items():
                        if topic_data['readme']:
                            lines.append(
                                f'&emsp;&emsp;'
                                f'[{topic_name}]({topic_data["readme"]})'
                            )
                        else:
                            lines.append(
                                f'&emsp;&emsp;{topic_name}'
                            )
                        lines.append('')

                    lines.append('</details>')
                    lines.append('')

            lines.append('</details>')
            lines.append('')

        (self.wiki / '_Sidebar.md').write_text(
            '\n'.join(lines), encoding='utf-8'
        )

    # ---------------------------------------------------------------
    # 8. _Footer.md
    # ---------------------------------------------------------------

    def _gen_footer(self):
        """Generate the wiki footer."""
        print('📋 Generating _Footer.md …')
        repo_url = f'https://github.com/{self.repo_slug}'

        lines = [
            '---',
            f'📖 [主仓库]({repo_url}) · '
            f'🤝 [参与贡献]({repo_url}/blob/main/CONTRIBUTING.md) · '
            f'📜 [CC BY-NC-SA 4.0]({repo_url}/blob/main/LICENSE)',
            '',
            '> 本 Wiki 由 GitHub Actions 自动同步生成，'
            '请勿直接编辑。如需修改内容，请在主仓库提交 PR。',
        ]

        (self.wiki / '_Footer.md').write_text(
            '\n'.join(lines), encoding='utf-8'
        )


# ---------------------------------------------------------------------------
# 工具函数 | Utilities
# ---------------------------------------------------------------------------


def _anchor(text: str) -> str:
    """Convert heading text to GitHub-flavoured Markdown anchor id."""
    # GitHub strips punctuation except hyphens and lowercases everything
    anchor = text.lower()
    anchor = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', anchor)
    anchor = re.sub(r'\s+', '-', anchor.strip())
    return anchor


# ---------------------------------------------------------------------------

if __name__ == '__main__':
    main()
