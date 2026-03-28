# 代码与命令

## 行内代码

使用 `pip install mkdocs-material` 安装依赖。

## 代码块

```python
def build_docs():
    """构建文档站点。"""
    return "mkdocs build"
```

## 终端命令

```bash
cd docs
mkdocs serve -a 127.0.0.1:8000
```

## 带语法标注的代码块

```yaml
# mkdocs.yml 片段
nav:
  - 首页: index.md
  - 示例合集:
      - 概述: examples/index.md
```
