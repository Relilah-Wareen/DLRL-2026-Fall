# Project 1

题目来源：[课程 project.pdf](https://yangwenhaosms.github.io/dlrl/project.pdf)，原件保存在 `project.pdf`。

- `report.pdf`：实验方法、6 张图及各图峰值；源文件为 `report.tex`。
- `experiment.py`：完整实验代码。
- `results/risks.csv`：三种信号强度 × 17 个 p × 20 次重复，共 1,020 条风险记录。
- `results/summary.csv`：每组风险的中位数和算术平均值。
- `results/signal_*_median.pdf`、`signal_*_mean.pdf`：6 张独立图。

在本目录运行（Python 3，依赖版本见 `requirements.txt`）：

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python experiment.py
pdflatex -interaction=nonstopmode -halt-on-error report.tex
```

固定随机种子为 `20260914`。每次重复重新生成训练矩阵、训练噪声和独立测试矩阵；不添加测试噪声。图的纵轴采用对数刻度，统计量在原始风险尺度上计算。
