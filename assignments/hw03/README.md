# Homework 3

- [原题](hw3.pdf)：[官网来源](https://yangwenhaosms.github.io/dlrl/hw3.pdf)。
- 发布日期：2026-09-16；截止日期：2026-09-23。
- 下载与核对日期：2026-09-17。
- [英文解答](solution.pdf) / [LaTeX 源文件](solution.tex)。
- [中文逐步详解](solution_zh_detailed.pdf) / [LaTeX 源文件](solution_zh_detailed.tex)。

两道题的全部小问均为数学证明；内容包括四阶矩估计、概率阶、几乎处处收敛，以及凸 SGD 的平均误差界。

在本目录编译：

```bash
pdflatex -interaction=nonstopmode -halt-on-error solution.tex
xelatex -interaction=nonstopmode -halt-on-error solution_zh_detailed.tex
```
