# 简易心理测试 — 5题

文件列表：

- index.html — 测试页面
- styles.css — 样式
- script.js — 交互与评分逻辑

本地预览：启动本地静态服务器，然后在浏览器或 VS Code 的 Simple Browser 打开 `http://127.0.0.1:8000`

说明：题库已扩展为 200 道占位题（`script.js` 中的 `questionPool`）。页面每次随机抽取 5 题显示。

下一步建议：
- 用真实题目替换 `script.js` 中 `questionPool` 的占位文本。
- 若需要记录答题历史或保存结果，可考虑后端或将结果存入 `localStorage`。
