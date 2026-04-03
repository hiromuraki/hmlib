# hmlib

[![Pytest](https://github.com/hiromuraki/hmlib/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/hiromuraki/hmlib/actions/workflows/pytest.yml)

`hmlib` 是一个基于 Python 的小型工具包，提供日期时间、动态对象、集合、文本处理和文件系统相关能力。

## 安装

从 Git 安装：

```bash
uv pip install "hmlib @ git+https://github.com/hiromuraki/hmlib.git"
```

本地开发：

```bash
git clone git@github.com:hiromuraki/hmlib.git
cd hmlib
uv sync --dev
```

## 使用

```python
from hmlib import DateTime, DynamicObject
from hmlib.io import LocalFile, LocalDirectory, TextFile
from hmlib.text import Json, Regex

now = DateTime.now()
data = DynamicObject({"name": "Ada"})
text = TextFile("notes.txt")

assert Regex.is_match(r"\d+", "123")
```

## 测试

```bash
uv run pytest test/
```

## 说明

- Python 版本要求：3.13+
- 当前仓库使用 `src` 布局
- CI 通过 GitHub Actions 自动运行 pytest
