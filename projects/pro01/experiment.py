"""Run Problem 1 exactly as specified; write all risks, summaries, and six plots."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)
    rng = np.random.default_rng(20260914)
    n, n_test, repeats = 200, 2000, 20
    dimensions = [20, 40, 60, 80, 100, 120, 140, 160, 180,
                  199, 200, 220, 240, 260, 300, 400, 600]
    records, summaries = [], []
    for signal in (5, 2, 1):
        risks = np.empty((len(dimensions), repeats))
        for i, p in enumerate(dimensions):
            beta = np.zeros(p)
            beta[0] = np.sqrt(signal)
            for repetition in range(repeats):
                x = rng.standard_normal((n, p))
                y = x @ beta + rng.standard_normal(n)
                beta_hat = np.linalg.lstsq(x, y, rcond=None)[0]
                x_test = rng.standard_normal((n_test, p))
                error = x_test @ (beta_hat - beta)
                risk = float(error @ error / n_test)
                risks[i, repetition] = risk
                records.append((signal, p, repetition + 1, risk))
            print(f"signal={signal}, p={p}: finished {repeats} repetitions",
                  flush=True)

        medians = np.median(risks, axis=1)
        means = np.mean(risks, axis=1)
        summaries.extend((signal, p, median, mean)
                         for p, median, mean in zip(dimensions, medians, means))
        for name, values in (("median", medians), ("mean", means)):
            peak = int(np.argmax(values))
            fig, ax = plt.subplots(figsize=(6.4, 4.2), layout="constrained")
            ax.plot(dimensions, values, "o-", markersize=3)
            ax.axvline(n, color="gray", linestyle="--", linewidth=1,
                       label="Interpolation threshold: p = 200")
            ax.plot(dimensions[peak], values[peak], "ro", markersize=5,
                    label=f"Peak: p = {dimensions[peak]}")
            ax.set(xlabel="Number of features p", ylabel=f"{name.title()} risk R",
                   yscale="log", title=rf"$\|\beta\|^2 = {signal}$: {name} of 20 repetitions")
            ax.grid(alpha=0.25)
            ax.legend(fontsize=8)
            fig.savefig(output / f"signal_{signal}_{name}.pdf")
            plt.close(fig)
            print(f"  {name} peak: p={dimensions[peak]}, R={values[peak]:.6g}",
                  flush=True)

    np.savetxt(output / "risks.csv", records, delimiter=",",
               header="signal_squared,p,repetition,risk", comments="",
               fmt=["%d", "%d", "%d", "%.17g"])
    np.savetxt(output / "summary.csv", summaries, delimiter=",",
               header="signal_squared,p,median_risk,mean_risk", comments="",
               fmt=["%d", "%d", "%.17g", "%.17g"])


if __name__ == "__main__":
    main()
