# 简易心理测试 — 12题

文件列表：

- index.html — 测试页面
- styles.css — 样式
- script.js — 交互与评分逻辑
- tests/test_psych.py — Selenium 自动化测试
- requirements.txt — Python 依赖
- run_tests.py — 测试运行脚本
- .github/workflows/test.yml — GitHub Actions 自动测试配置

## 本地预览

启动本地静态服务器，然后在浏览器打开 `http://127.0.0.1:8000`

```bash
python -m http.server 8000
```

## 运行自动化测试

**前提条件：**
- 已安装 Python 3.8+
- 已安装 Chrome 浏览器

**运行测试：**

```bash
# 方式一：直接运行脚本（自动安装依赖）
python run_tests.py

# 方式二：手动安装依赖后用 pytest
pip install -r requirements.txt
pytest tests/test_psych.py -v
```

**测试覆盖：**
- 页面加载和标题
- 12 道题目正确显示
- 提交按钮状态（答完才可提交）
- 提交后结果显示（低/中/高三档）
- 重置功能
- 换题功能

## GitHub Actions 自动测试

本项目配置了 GitHub Actions，每次 push 代码会自动运行测试。

- 查看测试状态：仓库页面 → **Actions** 标签
- 测试报告：点击某次运行 → **Artifacts** → 下载 `test-report`

[![自动化测试](https://github.com/sherry1499/psych-test/actions/workflows/test.yml/badge.svg)](https://github.com/sherry1499/psych-test/actions/workflows/test.yml)

## 说明

题库已扩展为 200 道占位题（`script.js` 中的 `questionPool`）。页面每次随机抽取 12 题显示。

## 下一步建议

- 用真实题目替换 `script.js` 中 `questionPool` 的占位文本。
- 若需要记录答题历史或保存结果，可考虑后端或将结果存入 `localStorage`。
