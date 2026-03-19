from __future__ import annotations

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

from .config import AppConfig


def _evaluate_and_plot(search_results: pd.DataFrame, subtitle: str) -> None:
    accuracy = (search_results["prediction_1"] == search_results["validated"]).mean() * 100
    print(
        f"In {round(accuracy, 1)}% of cases the predicted code matched the validated code."
    )

    thresholds = np.arange(0, 1.05, 0.01)
    results = []

    for threshold in thresholds:
        covered = search_results.loc[search_results["score"] > threshold]
        coverage = len(covered) / len(search_results)
        accuracy = (covered["validated"] == covered["prediction_1"]).mean()
        results.append({"threshold": threshold, "coverage": coverage, "accuracy": accuracy})

    results_df = pd.DataFrame(results)

    x = results_df["coverage"]
    y = results_df["accuracy"]
    z = results_df["threshold"]
    xs = np.sort(x)
    ys = np.array(y)[np.argsort(x)]
    zs = np.array(z)[np.argsort(x)]
    x0 = 0.5
    x1 = 0.8
    y0 = np.interp(x0, xs, ys)
    y1 = np.interp(x1, xs, ys)
    z0 = np.interp(x0, xs, zs)
    z1 = np.interp(x1, xs, zs)

    sns.set_style("whitegrid", {"axes.grid": False})
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="coverage", y="accuracy", data=results_df, color="#212121")
    plt.axvline(x=x0, color="#cab2d6", ls=":", lw=2, alpha=0.8)
    plt.axvline(x=x1, color="#6a3d9a", ls=":", lw=2, alpha=0.8)
    plt.axhline(y=y0, color="#cab2d6", ls=":", lw=2, alpha=0.8)
    plt.axhline(y=y1, color="#6a3d9a", ls=":", lw=2, alpha=0.8)
    plt.plot(x0, y0, marker="o", color="#cab2d6")
    plt.plot(x1, y1, marker="o", color="#6a3d9a")
    plt.title(
        "Coverage vs. Accuracy for Different Similarity Thresholds",
        fontsize=14,
        weight="bold",
        y=1.055,
        loc="left",
    )
    plt.gcf().text(0.125, 0.9, subtitle, fontsize=9, color="#666")
    plt.xlabel("Coverage")
    plt.ylabel("Accuracy")
    plt.text(
        0.02,
        0.04,
        f"cov≈0.50> (thr={z0:.2f})\ncov≈0.80> (thr={z1:.2f})",
        transform=plt.gca().transAxes,
        fontsize=10,
        color="black",
        bbox=dict(facecolor="white", edgecolor="gray", boxstyle="round,pad=0.6"),
    )
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter("% 1.2f"))
    plt.gca().yaxis.set_ticks_position("none")
    plt.gca().yaxis.tick_right()
    plt.gca().yaxis.set_label_position("right")
    plt.show()


def _coerce_results(search_results: pd.DataFrame) -> pd.DataFrame:
    coerced = search_results.copy()
    coerced["prediction_1"] = coerced["prediction_1"].astype(str)
    coerced["validated"] = coerced["validated"].astype(str)
    coerced["score"] = pd.to_numeric(coerced["score"], errors="coerce")
    return coerced


def evaluate_search_results(config: AppConfig) -> None:
    isco_results = _coerce_results(
        pd.read_csv(config.paths.search_results_isco_file)
    )
    _evaluate_and_plot(
        isco_results,
        f"ISCO Q2 2024 NLFS - ({config.model_name})",
    )

    isic_results = _coerce_results(
        pd.read_csv(config.paths.search_results_isic_file)
    )
    _evaluate_and_plot(
        isic_results,
        f"ISIC Q2 2024 NLFS - ({config.model_name})",
    )
