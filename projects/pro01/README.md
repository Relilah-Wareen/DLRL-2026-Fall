# Projects: Problems 1 and 2

题目来源：[课程 project.pdf](https://yangwenhaosms.github.io/dlrl/project.pdf)，原件保存在 `project.pdf`。官网于 2026-09-21 更新，增加 Problem 2；2026-09-23 已下载并核对。截止时间为期末考试前（具体日期待公布）。

- `report.pdf`：两道题的证明、实验方法、结果和图；源文件为 `report.tex`。
- `experiment.py`：Problem 1 的实验代码。
- `inference.py`：Problem 2 的平均 SGD 推断实验代码。
- `results/risks.csv`：三种信号强度 × 17 个 p × 20 次重复，共 1,020 条风险记录。
- `results/summary.csv`：每组风险的中位数和算术平均值。
- `results/signal_*_median.pdf`、`signal_*_mean.pdf`：6 张独立图。
- `results/inference_intervals.csv`：500 次重复 × 5 个检查点 × 3 种方法的全部区间、覆盖指示和长度。
- `results/inference_summary.csv`：各检查点的覆盖率和平均区间长度。
- `results/inference_coverage.pdf`：三种方法的覆盖率曲线、标称水平及 Monte Carlo 参考带。

在本目录运行（Python 3，依赖版本见 `requirements.txt`）：

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python experiment.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python inference.py
pdflatex -interaction=nonstopmode -halt-on-error report.tex
```

固定随机种子为 `20260914`。每次重复重新生成训练矩阵、训练噪声和独立测试矩阵；不添加测试噪声。图的纵轴采用对数刻度，统计量在原始风险尺度上计算。

Problem 2 的第 `r` 次外层重复固定随机种子为 `20260923 + r - 1`，每次重复使用单一数据流运行至 `T=10000`，并在同一数据流上运行 200 条独立乘子路径。三种置信区间按原题公式计算；保存 7,500 条区间记录。`inference.py` 使用 Numba 加速，首次运行会有编译时间。
