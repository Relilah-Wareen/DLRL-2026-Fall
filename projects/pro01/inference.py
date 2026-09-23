"""Problem 2: averaged-SGD intervals from 500 independent online streams."""

import csv
from pathlib import Path

import matplotlib
import numpy as np
from numba import njit

matplotlib.use("Agg")
import matplotlib.pyplot as plt


CHECKPOINTS = (500, 1000, 2000, 5000, 10000)
BURN_IN = 200
BOOTSTRAPS = 200
REPLICATIONS = 500
SEED = 20260923
TRUTH = -1.0 / np.sqrt(5.0)


@njit
def sigmoid(u):
    if u >= 0:
        return 1.0 / (1.0 + np.exp(-u))
    z = np.exp(u)
    return z / (1.0 + z)


@njit
def linear_quantile(sorted_values, p):
    index = p * (len(sorted_values) - 1)
    left = int(index)
    fraction = index - left
    if left + 1 == len(sorted_values):
        return sorted_values[left]
    return (1.0 - fraction) * sorted_values[left] + fraction * sorted_values[left + 1]


@njit
def one_replication(seed):
    np.random.seed(seed)
    c0, c1 = 1.0 / np.sqrt(5.0), 2.0 / np.sqrt(5.0)
    theta0 = theta1 = 0.0
    boot = np.zeros((BOOTSTRAPS, 2), dtype=np.float64)
    boot_contrast_sums = np.zeros(BOOTSTRAPS, dtype=np.float64)
    contrast_sum = 0.0
    prefix_square_sum = prefix_weighted_sum = weight_square_sum = 0.0
    h00 = h01 = h11 = s00 = s01 = s11 = 0.0
    intervals = np.empty((len(CHECKPOINTS), 3, 2), dtype=np.float64)
    checkpoint_index = 0

    for t in range(1, CHECKPOINTS[-1] + 1):
        # Fresh correlated Gaussian covariate and correctly specified response.
        x0 = np.random.randn()
        x1 = 0.4 * x0 + np.sqrt(0.84) * np.random.randn()
        y = 1.0 if np.random.random() < sigmoid(x0 - x1) else 0.0
        eta = 1.6 * (t + 10.0) ** (-0.6)

        probability = sigmoid(x0 * theta0 + x1 * theta1)
        residual = probability - y
        g0, g1 = residual * x0, residual * x1
        if t > BURN_IN:
            curvature = probability * (1.0 - probability)
            h00 += curvature * x0 * x0
            h01 += curvature * x0 * x1
            h11 += curvature * x1 * x1
            s00 += g0 * g0
            s01 += g0 * g1
            s11 += g1 * g1

        theta0 -= eta * g0
        theta1 -= eta * g1

        for b in range(BOOTSTRAPS):
            boot_probability = sigmoid(x0 * boot[b, 0] + x1 * boot[b, 1])
            multiplier = np.random.exponential(1.0)
            step = eta * multiplier * (boot_probability - y)
            boot[b, 0] -= step * x0
            boot[b, 1] -= step * x1
            if t > BURN_IN:
                boot_contrast_sums[b] += c0 * boot[b, 0] + c1 * boot[b, 1]

        if t > BURN_IN:
            n = t - BURN_IN
            contrast_sum += c0 * theta0 + c1 * theta1
            prefix_square_sum += contrast_sum * contrast_sum
            prefix_weighted_sum += n * contrast_sum
            weight_square_sum += n * n

        if t == CHECKPOINTS[checkpoint_index]:
            n = t - BURN_IN
            psi = contrast_sum / n
            # Solve H w = c, then c^T H^{-1} S H^{-1} c = w^T S w.
            det = h00 * h11 - h01 * h01
            w0 = n * (h11 * c0 - h01 * c1) / det
            w1 = n * (h00 * c1 - h01 * c0) / det
            variance = (w0 * w0 * s00 + 2.0 * w0 * w1 * s01
                        + w1 * w1 * s11) / n
            pi_radius = 1.96 * np.sqrt(variance / n)
            intervals[checkpoint_index, 0, 0] = psi - pi_radius
            intervals[checkpoint_index, 0, 1] = psi + pi_radius

            deviations = np.empty(BOOTSTRAPS, dtype=np.float64)
            for b in range(BOOTSTRAPS):
                deviations[b] = (boot_contrast_sums[b] / n - psi) * np.sqrt(n)
            deviations.sort()
            intervals[checkpoint_index, 1, 0] = psi - linear_quantile(deviations, 0.975) / np.sqrt(n)
            intervals[checkpoint_index, 1, 1] = psi - linear_quantile(deviations, 0.025) / np.sqrt(n)

            scaling = (prefix_square_sum - 2.0 * psi * prefix_weighted_sum
                       + psi * psi * weight_square_sum) / (n * n)
            rs_radius = 6.747 * np.sqrt(max(scaling, 0.0) / n)
            intervals[checkpoint_index, 2, 0] = psi - rs_radius
            intervals[checkpoint_index, 2, 1] = psi + rs_radius
            checkpoint_index += 1
            if checkpoint_index == len(CHECKPOINTS):
                break

    return intervals


def plot_coverage(output, coverage):
    methods = ("PI", "Boot", "RS")
    fig, ax = plt.subplots(figsize=(7.0, 4.4), layout="constrained")
    for j, method in enumerate(methods):
        ax.plot(CHECKPOINTS, coverage[:, j], "o-", label=method)
    half_width = 1.96 * np.sqrt(0.95 * 0.05 / REPLICATIONS)
    ax.axhspan(0.95 - half_width, 0.95 + half_width, color="gray", alpha=0.16,
               label="95% Monte Carlo reference band")
    ax.axhline(0.95, color="black", linestyle="--", linewidth=1, label="Nominal 0.95")
    ax.set_xscale("log")
    ax.set(xlabel="Number of iterations T", ylabel="Empirical coverage rate",
           xticks=CHECKPOINTS, ylim=(0, 1))
    ax.set_xticklabels([str(t) for t in CHECKPOINTS])
    ax.grid(alpha=0.25)
    ax.legend()
    fig.savefig(output / "inference_coverage.pdf")
    plt.close(fig)


def main():
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)
    methods = ("PI", "Boot", "RS")
    all_intervals = np.empty((REPLICATIONS, len(CHECKPOINTS), len(methods), 2))
    for r in range(REPLICATIONS):
        all_intervals[r] = one_replication(SEED + r)
        if (r + 1) % 25 == 0:
            print(f"Problem 2: {r + 1}/{REPLICATIONS} replications", flush=True)

    with (output / "inference_intervals.csv").open("w", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(("replication", "T", "method", "lower", "upper", "covers", "length"))
        for r in range(REPLICATIONS):
            for i, t in enumerate(CHECKPOINTS):
                for j, method in enumerate(methods):
                    lower, upper = all_intervals[r, i, j]
                    writer.writerow((r + 1, t, method, format(lower, ".17g"),
                                     format(upper, ".17g"), int(lower <= TRUTH <= upper),
                                     format(upper - lower, ".17g")))

    coverage = ((all_intervals[..., 0] <= TRUTH) &
                (TRUTH <= all_intervals[..., 1])).mean(axis=0)
    mean_lengths = (all_intervals[..., 1] - all_intervals[..., 0]).mean(axis=0)
    with (output / "inference_summary.csv").open("w", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(("T", "method", "coverage", "mean_interval_length"))
        for i, t in enumerate(CHECKPOINTS):
            for j, method in enumerate(methods):
                writer.writerow((t, method, format(coverage[i, j], ".17g"),
                                 format(mean_lengths[i, j], ".17g")))

    plot_coverage(output, coverage)
    print("Coverage by checkpoint (PI, Boot, RS):")
    for t, values in zip(CHECKPOINTS, coverage):
        print(t, values)
    print("Mean interval lengths at T=10000:", mean_lengths[-1])


if __name__ == "__main__":
    main()
