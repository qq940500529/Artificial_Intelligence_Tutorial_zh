#!/usr/bin/env python3
"""sync_wiki.py — 将课程内容同步到 GitHub Wiki
Sync course content from main repository to GitHub Wiki.

功能 | Features:
  1. 扫描已完成的课程 .md 文件，扁平化复制到 Wiki 仓库根目录
     GitHub Wiki 使用扁平页面命名空间（按文件名索引，忽略目录结构），
     因此所有 .md 文件必须放在 Wiki 仓库根目录下。
  2. 将知识主题 README.md 重命名为 <主题名>.md 避免文件名冲突
  3. 转换所有内部链接为扁平 Wiki 页面名（不含 .md 后缀和目录路径）
  4. 为每个页面添加导航面包屑
  5. 复制 assets/code 等资源目录（以知识点名称为前缀避免冲突）
  6. 为无 README 的知识主题生成索引页
  7. 生成 Home.md（首页）、_Sidebar.md（侧边栏）、_Footer.md（页脚）

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

# Emoji prefix used for module headings in Home.md and _Sidebar.md
MODULE_EMOJI = '📚'

# ---------------------------------------------------------------------------
# 主入口 | Main
# ---------------------------------------------------------------------------


def main():
    required_vars = ['MAIN_REPO_PATH', 'WIKI_REPO_PATH', 'GITHUB_REPOSITORY']
    missing = [v for v in required_vars if v not in os.environ]
    if missing:
        print(
            f'❌ Missing required environment variable(s): {", ".join(missing)}\n'
            f'Usage:\n'
            f'  MAIN_REPO_PATH=/path/to/repo '
            f'WIKI_REPO_PATH=/path/to/wiki '
            f'GITHUB_REPOSITORY=owner/repo '
            f'python {__file__}'
        )
        raise SystemExit(1)

    main_repo = Path(os.environ['MAIN_REPO_PATH']).resolve()
    wiki_repo = Path(os.environ['WIKI_REPO_PATH']).resolve()
    github_repo = os.environ['GITHUB_REPOSITORY']

    syncer = WikiSyncer(main_repo, wiki_repo, github_repo)
    syncer.run()


# ---------------------------------------------------------------------------
# 核心同步类 | Core Syncer
# ---------------------------------------------------------------------------


class WikiSyncer:
    """Scans course content and syncs it to a GitHub Wiki repository.

    GitHub Wiki uses a flat page namespace: pages are indexed solely by
    filename (without .md extension), and subdirectory structure is ignored
    in the web UI.  Therefore this syncer copies all .md files to the wiki
    root directory and transforms all internal links to flat wiki page names.
    """

    def __init__(self, main_repo: Path, wiki_repo: Path, github_repo: str):
        self.main = main_repo
        self.wiki = wiki_repo
        self.repo_slug = github_repo
        # tree: stage_dir -> module_dir -> topic_dir -> {readme, points}
        self.tree: OrderedDict = OrderedDict()
        self.stats = {'pages': 0, 'points': 0, 'assets': 0}
        # Maps repo-relative .md path -> wiki page name (flat, no .md)
        # e.g. "00_高中复习/.../01_一元二次方程/01_一元二次方程.md"
        #      -> "01_一元二次方程"
        # e.g. "00_高中复习/.../01_代数与方程/README.md"
        #      -> "01_代数与方程"
        self._path_to_wiki: dict = {}
        # Maps repo-relative directory path -> wiki destination
        # for stage/module/topic/point directories.
        # Stage/module dirs → "Home#<anchor>" (section in Home.md)
        # Topic/point dirs → flat wiki page name
        self._dir_to_wiki: dict = {}

    # ---------------------------------------------------------------
    # public
    # ---------------------------------------------------------------

    def run(self):
        print('🔄 Starting wiki sync …')
        self._clean()
        self._scan()
        self._copy_all()
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
    # 2. scan course content (build tree + path mapping, no copy yet)
    # ---------------------------------------------------------------

    def _scan(self):
        """Walk the 4-level course tree and build the content tree."""
        print('📂 Scanning course content …')

        for stage_dir in STAGES:
            stage_path = self.main / stage_dir
            if not stage_path.is_dir():
                continue

            # Register stage directory → Home anchor
            meta = STAGE_META.get(stage_dir)
            if meta:
                stage_anchor = _anchor(meta[0])
                self._dir_to_wiki[stage_dir] = f'Home#{stage_anchor}'

            stage_data: OrderedDict = OrderedDict()

            for module_path in sorted(stage_path.iterdir()):
                if not module_path.is_dir():
                    continue

                # Register module directory → Home anchor
                mod_heading = f'{MODULE_EMOJI} {module_path.name}'
                mod_anchor = _anchor(mod_heading)
                mod_rel = str(
                    module_path.relative_to(self.main)
                )
                self._dir_to_wiki[mod_rel] = f'Home#{mod_anchor}'

                module_data: OrderedDict = OrderedDict()

                for topic_path in sorted(module_path.iterdir()):
                    if not topic_path.is_dir():
                        continue

                    topic_data = {
                        'readme': None,      # wiki page name (flat)
                        'readme_src': None,   # repo-relative path
                        'points': OrderedDict(),
                        'points_src': OrderedDict(),
                        'extra_md': [],       # (src_path, wiki_name)
                        'asset_dirs': [],     # (src_path, wiki_subdir)
                    }

                    # Register topic directory → topic wiki page
                    topic_rel = str(
                        topic_path.relative_to(self.main)
                    )
                    self._dir_to_wiki[topic_rel] = topic_path.name

                    # --- topic README (level 3) ---
                    readme = topic_path / 'README.md'
                    if readme.is_file():
                        wiki_name = topic_path.name
                        rel = str(readme.relative_to(self.main))
                        self._path_to_wiki[rel] = wiki_name
                        topic_data['readme'] = wiki_name
                        topic_data['readme_src'] = rel

                    # --- knowledge points (level 4) ---
                    for point_path in sorted(topic_path.iterdir()):
                        if not point_path.is_dir():
                            continue

                        course_file = point_path / f'{point_path.name}.md'
                        if not course_file.is_file():
                            continue  # empty placeholder (.gitkeep only)

                        wiki_name = point_path.name
                        rel = str(course_file.relative_to(self.main))
                        self._path_to_wiki[rel] = wiki_name
                        topic_data['points'][wiki_name] = wiki_name
                        topic_data['points_src'][wiki_name] = rel
                        self.stats['points'] += 1

                        # Register point directory → point wiki page
                        pt_rel = str(
                            point_path.relative_to(self.main)
                        )
                        self._dir_to_wiki[pt_rel] = wiki_name

                        # record resource sub-directories
                        for sub in sorted(point_path.iterdir()):
                            if sub.is_dir() and not sub.name.startswith('.'):
                                topic_data['asset_dirs'].append(
                                    (sub, wiki_name)
                                )

                        # record extra .md files (sub-lectures)
                        for extra in sorted(point_path.glob('*.md')):
                            if extra.name == f'{point_path.name}.md':
                                continue
                            extra_wiki = extra.stem
                            extra_rel = str(
                                extra.relative_to(self.main)
                            )
                            self._path_to_wiki[extra_rel] = extra_wiki
                            topic_data['extra_md'].append(
                                (extra, extra_wiki)
                            )

                    if topic_data['readme'] or topic_data['points']:
                        module_data[topic_path.name] = topic_data

                if module_data:
                    stage_data[module_path.name] = module_data

            self.tree[stage_dir] = stage_data

    # ---------------------------------------------------------------
    # 3. copy all content to wiki (flat structure)
    # ---------------------------------------------------------------

    def _copy_all(self):
        """Copy all scanned content to wiki root with flat naming."""
        print('📄 Copying content to wiki (flat) …')

        for stage_dir, stage_data in self.tree.items():
            for mod_name, mod_data in stage_data.items():
                for topic_name, topic_data in mod_data.items():
                    # Copy topic README as <topic_name>.md
                    if topic_data['readme_src']:
                        src = self.main / topic_data['readme_src']
                        wiki_name = topic_data['readme']
                        self._copy_md_flat(src, wiki_name, topic_data)

                    # Copy knowledge point files
                    for pt_name, pt_rel in (
                            topic_data['points_src'].items()):
                        src = self.main / pt_rel
                        self._copy_md_flat(src, pt_name, topic_data)

                    # Copy extra .md files
                    for extra_src, extra_wiki in topic_data['extra_md']:
                        self._copy_md_flat(
                            extra_src, extra_wiki, topic_data
                        )

                    # Copy asset directories
                    for asset_src, pt_name in topic_data['asset_dirs']:
                        self._copy_assets(asset_src, pt_name)

    # ---------------------------------------------------------------
    # helpers: copy files
    # ---------------------------------------------------------------

    def _copy_md_flat(self, src: Path, wiki_name: str,
                      topic_data: dict) -> None:
        """Copy a .md file to wiki root as <wiki_name>.md."""
        dest = self.wiki / f'{wiki_name}.md'

        try:
            content = src.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError) as exc:
            rel = src.relative_to(self.main)
            print(f'  ⚠️ Skipping {rel}: {exc}')
            return

        rel = src.relative_to(self.main)
        content = self._add_nav(content, rel)
        content = self._transform_links(content, rel)
        dest.write_text(content, encoding='utf-8')
        self.stats['pages'] += 1

    def _copy_assets(self, src: Path, point_name: str):
        """Copy a resource directory (assets/, code/, …) to wiki.

        Assets are stored under _assets/<point_name>/<dir_name>/
        to avoid collisions between knowledge points.
        """
        if not src.is_dir():
            return
        dir_name = src.name  # e.g. "assets", "code"
        dest = self.wiki / '_assets' / point_name / dir_name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        self.stats['assets'] += sum(
            1 for f in src.rglob('*') if f.is_file()
        )

    # ---------------------------------------------------------------
    # 3. navigation header (breadcrumb)
    # ---------------------------------------------------------------

    def _add_nav(self, content: str, src_rel_path: Path) -> str:
        """Prepend a breadcrumb navigation bar to page content.

        All pages are now at wiki root, so Home link is just 'Home'.
        """
        parts = src_rel_path.parts
        crumbs = ' / '.join(parts[:-1])
        home_link = '[🏠 首页](Home)'
        if crumbs:
            header = f'> {home_link} · {crumbs}\n\n---\n\n'
        else:
            header = f'> {home_link}\n\n---\n\n'
        return header + content

    # ---------------------------------------------------------------
    # 4. link transformation
    # ---------------------------------------------------------------

    def _transform_links(self, content: str, file_rel_path: Path) -> str:
        """Transform all internal links to flat wiki page names.

        - Resolve relative paths against the source file location
        - Map resolved repo paths to wiki page names
        - Strip .md extensions (GitHub Wiki convention)
        - Transform asset paths to use the _assets/ prefix
        """
        file_dir = file_rel_path.parent

        def _replace(match):
            full = match.group(0)
            text = match.group(1)
            url = match.group(2)

            # skip external / anchor / data / mailto links
            if re.match(r'^(https?://|#|mailto:|data:)', url):
                return full

            # Handle .md links (both file.md and dir/file.md)
            if url.endswith('.md') or '.md#' in url:
                # Split off any anchor
                if '#' in url:
                    url_path, anchor = url.rsplit('#', 1)
                    anchor = '#' + anchor
                else:
                    url_path = url
                    anchor = ''

                target_stem = Path(url_path).stem

                resolved = (
                    self.main / file_dir / url_path
                ).resolve()
                try:
                    repo_rel = str(resolved.relative_to(self.main))
                except ValueError:
                    # Path went above repo root; use filename fallback
                    if target_stem != 'README':
                        for wn in self._path_to_wiki.values():
                            if wn == target_stem:
                                return f'[{text}]({wn}{anchor})'
                    return f'[{text}]({target_stem}{anchor})'

                # Look up wiki page name by exact repo-relative path
                wiki_name = self._path_to_wiki.get(repo_rel)
                if wiki_name:
                    return f'[{text}]({wiki_name}{anchor})'

                # Fallback: match by filename stem (all knowledge
                # point and topic names are unique across the repo)
                if target_stem != 'README':
                    for wn in self._path_to_wiki.values():
                        if wn == target_stem:
                            return f'[{text}]({wn}{anchor})'

                # Try: directory link ending with /README.md
                # -> topic page
                if Path(repo_rel).name == 'README.md':
                    # Topic README -> wiki name is the topic dir name
                    topic_dir = Path(repo_rel).parent.name
                    for wn in self._path_to_wiki.values():
                        if wn == topic_dir:
                            return f'[{text}]({topic_dir}{anchor})'

                return full

            # Handle directory links (ending with /)
            if url.endswith('/'):
                # Extract the last meaningful directory component
                # from the URL (before the trailing /)
                url_clean = url.rstrip('/')
                dir_name = (url_clean.rsplit('/', 1)[-1]
                            if '/' in url_clean else url_clean)

                resolved = (self.main / file_dir / url).resolve()
                try:
                    dir_rel = str(resolved.relative_to(self.main))
                except ValueError:
                    # Path went above repo root; use fallback
                    for wn in self._path_to_wiki.values():
                        if wn == dir_name:
                            return f'[{text}]({wn})'
                    # Check _dir_to_wiki by directory name
                    for dk, dv in self._dir_to_wiki.items():
                        if Path(dk).name == dir_name:
                            return f'[{text}]({dv})'
                    return f'[{text}]({dir_name})'

                # Check _dir_to_wiki for stage/module/topic/point
                wiki_dest = self._dir_to_wiki.get(dir_rel)
                if wiki_dest:
                    return f'[{text}]({wiki_dest})'

                if resolved.is_dir():
                    # Check if this dir has a main course file
                    course_md = resolved / f'{dir_name}.md'
                    readme_md = resolved / 'README.md'

                    if course_md.is_file():
                        rel = str(course_md.relative_to(self.main))
                        wiki_name = self._path_to_wiki.get(
                            rel, dir_name
                        )
                        return f'[{text}]({wiki_name})'
                    if readme_md.is_file():
                        rel = str(readme_md.relative_to(self.main))
                        wiki_name = self._path_to_wiki.get(
                            rel, dir_name
                        )
                        return f'[{text}]({wiki_name})'

                # Fallback: match directory name against wiki pages
                # (handles broken relative paths in source files)
                for wn in self._path_to_wiki.values():
                    if wn == dir_name:
                        return f'[{text}]({wn})'

                # Check _dir_to_wiki by directory name (partial match)
                for dk, dv in self._dir_to_wiki.items():
                    if Path(dk).name == dir_name:
                        return f'[{text}]({dv})'

                # Final fallback: use the last path component as
                # wiki page name.  When the target course is created
                # and synced later, the link will automatically work.
                return f'[{text}]({dir_name})'

            return full

        # Transform markdown links [text](url)
        content = re.sub(
            r'\[([^\]]*)\]\(([^)]+)\)', _replace, content
        )

        # Transform image/asset references to use _assets/ prefix
        content = self._transform_asset_refs(content, file_rel_path)

        return content

    def _transform_asset_refs(self, content: str,
                              file_rel_path: Path) -> str:
        """Transform asset references (images etc.) to _assets/ paths."""
        # The source file's knowledge point name (parent dir of the file)
        point_name = file_rel_path.parent.name

        # Match image syntax ![alt](url)
        content = re.sub(
            r'(!\[[^\]]*\]\()([^)]+)',
            lambda m: _img_replace(m, point_name),
            content,
        )

        return content

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
                    wiki_name = topic_name

                    lines = [
                        f'# {topic_name}',
                        '',
                        f'> **所属路径**：`{rel_dir}`',
                        f'> **包含知识点**：'
                        f'{len(topic_data["points"])} 个',
                        '',
                        '---',
                        '',
                        '## 知识点列表',
                        '',
                    ]

                    for pt_name in topic_data['points']:
                        lines.append(f'- [{pt_name}]({pt_name})')

                    lines.append('')

                    # add nav header
                    nav_content = '\n'.join(lines)
                    crumbs = rel_dir.replace('/', ' / ')
                    header = (
                        f'> [🏠 首页](Home) · {crumbs}\n\n---\n\n'
                    )
                    nav_content = header + nav_content

                    dest = self.wiki / f'{wiki_name}.md'
                    dest.write_text(nav_content, encoding='utf-8')
                    topic_data['readme'] = wiki_name
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
                lines.append(f'### {MODULE_EMOJI} {mod_name}')
                lines.append('')

                for topic_name, topic_data in mod_data.items():
                    if topic_data['readme']:
                        lines.append(
                            f'<details><summary>'
                            f'<strong>📂 <a href="'
                            f'{topic_data["readme"]}'
                            f'">{topic_name}</a></strong> '
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

                    for pt_name in topic_data['points']:
                        lines.append(f'- [{pt_name}]({pt_name})')

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
                        f'<summary>&emsp;{MODULE_EMOJI} {mod_name}</summary>'
                    )
                    lines.append('')

                    for topic_name, topic_data in mod_data.items():
                        if topic_data['readme']:
                            lines.append(
                                f'&emsp;&emsp;'
                                f'[{topic_name}]'
                                f'({topic_data["readme"]})'
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
    anchor = re.sub(r'[^\w\s\u4e00-\u9fff\-]', '', anchor)
    anchor = re.sub(r'\s+', '-', anchor.strip())
    return anchor


def _img_replace(match, point_name: str) -> str:
    """Replace image asset paths with _assets/ prefix."""
    full = match.group(0)
    prefix = match.group(1)  # '!['...']('
    url = match.group(2)

    if re.match(r'^(https?://|#|mailto:|data:)', url):
        return full

    if url.startswith(('assets/', 'code/', './assets/', './code/')):
        clean_url = url.lstrip('./')
        new_url = f'_assets/{point_name}/{clean_url}'
        return f'{prefix}{new_url}'

    return full


# ---------------------------------------------------------------------------

if __name__ == '__main__':
    main()
