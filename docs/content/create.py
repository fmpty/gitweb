#!/usr/bin/env python3
"""
遍历 posts/（结构：posts/YYYY-MM/文章目录/index.md），生成可粘贴进 mkdocs.yml 的 nav 片段。

排序：月份倒序（时间新的在前）；同月内文章目录名倒序。

在 docs/content 目录执行：
  python create.py

输出：同目录 mkdocs_nav_snippet.txt（UTF-8）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# 与 mkdocs.yml 中 docs 目录为根的路径一致（docs_dir 默认 docs）
PREFIX = "content/posts"

# 侧栏分组标题（可改）
SECTION_TITLE = "历史合集"

MONTH_DIR = re.compile(r"^\d{4}-\d{2}$")


def yaml_key(s: str) -> str:
    """MkDocs 导航键名；含冒号、引号等时加双引号。"""
    if not s:
        return '""'
    need = any(
        c in s
        for c in (
            ":",
            "#",
            "{",
            "}",
            "[",
            "]",
            ",",
            "&",
            "*",
            "!",
            "|",
            ">",
            "%",
            "@",
            "`",
        )
    ) or s.strip() != s
    if need or s[0] in "0123456789-%@":
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def collect_posts(posts_root: Path) -> list[tuple[str, list[str]]]:
    """返回 [(月份, [文章目录名, ...]), ...]。
    月份倒序（新的在前）；同一月内文章目录名倒序。"""
    if not posts_root.is_dir():
        raise FileNotFoundError(f"未找到目录: {posts_root}")

    months: list[tuple[str, list[str]]] = []
    for month_path in sorted(
        posts_root.iterdir(), key=lambda p: p.name, reverse=True
    ):
        if not month_path.is_dir() or not MONTH_DIR.match(month_path.name):
            continue
        articles: list[str] = []
        for art_path in sorted(
            month_path.iterdir(), key=lambda p: p.name, reverse=True
        ):
            if not art_path.is_dir():
                continue
            if (art_path / "index.md").is_file():
                articles.append(art_path.name)
        if articles:
            months.append((month_path.name, articles))
    return months


def render_snippet(months: list[tuple[str, list[str]]]) -> str:
    lines: list[str] = [
        "# 粘贴到 mkdocs.yml 的 nav: 下（保留缩进；与上下条目对齐）",
        f"  - {SECTION_TITLE}:",
    ]
    for month, articles in months:
        lines.append(f"    - {yaml_key(month)}:")
        for name in articles:
            rel = f"{PREFIX}/{month}/{name}/index.md"
            lines.append(f"      - {yaml_key(name)}: {rel}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    base = Path(__file__).resolve().parent
    posts = base / "posts"
    out = base / "mkdocs_nav_snippet.txt"

    try:
        data = collect_posts(posts)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1

    text = render_snippet(data)
    out.write_text(text, encoding="utf-8")
    print(f"已写入 {out}（{len(data)} 个月份）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
