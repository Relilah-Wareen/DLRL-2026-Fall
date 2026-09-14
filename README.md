# 深度学习与强化学习 · 2026 秋季

北京大学 SMS 00103335 — Deep Learning and Reinforcement Learning

- 课程主页：https://yangwenhaosms.github.io/dlrl.html
- 教师：Wenhao Yang
- 本页课程信息核对日期：2026-09-14；后续安排以课程主页为准。

## 目录

```text
assignments/       每次作业的题目、解答、代码及提交版本
  hw01/            第一次作业
  hw02/            第二次作业
projects/          项目代码、实验记录、报告及提交版本
notes/             课堂笔记与复习资料
materials/         讲义及其他课程资料
```

## 任务进度

| 任务 | 发布 / 更新日期 | 截止日期 | 状态 | 工作目录 | 题目链接 |
| --- | --- | --- | --- | --- | --- |
| Homework 1 | 2026-09-07 | 2026-09-23 | 已完成，未提交 | [hw01](assignments/hw01/) | [PDF](https://yangwenhaosms.github.io/dlrl/hw1.pdf) |
| Homework 2 | 2026-09-09 | 2026-09-23 | 已完成，未提交 | [hw02](assignments/hw02/) | [PDF](https://yangwenhaosms.github.io/dlrl/hw2.pdf) |
| Project 1 | 2026-09-07 | 期末考试前（具体日期待公布） | 已完成，未提交 | [pro01](projects/pro01/) | [PDF](https://yangwenhaosms.github.io/dlrl/project.pdf) |

## 解答与报告

- [HW1 解答](assignments/hw01/solution.pdf)：4 道题的全部小问；[LaTeX 源文件](assignments/hw01/solution.tex)。
- [HW2 解答](assignments/hw02/solution.pdf)：4 道题的完整推导，保留原题编号；[LaTeX 源文件](assignments/hw02/solution.tex)。
- [HW1 中文详解](assignments/hw01/solution_zh_detailed.pdf)：逐步计算与依据说明；[LaTeX 源文件](assignments/hw01/solution_zh_detailed.tex)。
- [HW2 中文详解](assignments/hw02/solution_zh_detailed.pdf)：逐步计算与依据说明；[LaTeX 源文件](assignments/hw02/solution_zh_detailed.tex)。
- [Project 1 报告](projects/pro01/report.pdf)：实验已实际运行，包含 6 张图及峰值；[代码与复现说明](projects/pro01/README.md)。

原始题目 PDF 已保存在各任务目录。作业解答使用英文，与原题一致。在各作业目录执行 `pdflatex -interaction=nonstopmode -halt-on-error solution.tex` 可重新生成解答 PDF。

中文详解是独立的学习版本，保留英文解答。在相应作业目录执行 `xelatex -interaction=nonstopmode -halt-on-error solution_zh_detailed.tex` 可重新生成中文 PDF。

## 课程资料

- [课程讲义（本地 PDF）](notes/lecture_note.pdf)：40 页，Lectures 1–2 with Probability Appendix；2026-09-14 下载，PDF 修改日期为 2026-09-08。[官网来源](https://yangwenhaosms.github.io/dlrl/lecture_note.pdf)。

## 使用约定

- 新作业按 `assignments/hw03/`、`assignments/hw04/` 顺序添加，同时更新任务进度。
- 每个项目使用 `projects/<项目名称>/`，按需要建立 `src/`、`experiments/`、`report/` 等子目录。
- 作业和项目的最终提交文件可放在各自目录的 `submission/` 中。
- 任务状态可使用：未开始、进行中、待检查、已提交。
- 代码、笔记和报告源文件纳入 Git；虚拟环境、缓存、数据集和模型权重不纳入 Git。
