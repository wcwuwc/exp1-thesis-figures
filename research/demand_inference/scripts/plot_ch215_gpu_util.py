#!/usr/bin/env python3
"""Plot cluster GPU utilization for Notion §2.1.5."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
CSV = ROOT / "data/GPU活跃度及功率-总体平均-data-2026-05-31 22_25_18.csv"
OUT = Path(__file__).resolve().parent / "outputs/ch2_215/figures/ch2_gpu_util.png"

# Align x-axis to the nine-model QPS sample window (§2.1.3).
QPS_SAMPLE_START = pd.Timestamp("2026-05-01 00:00:00")
QPS_SAMPLE_END = pd.Timestamp("2026-05-08 22:58:00")


def load_clean() -> pd.DataFrame:
    df = pd.read_csv(CSV)
    df.columns = ["Time", "gpu_util"]
    df["Time"] = pd.to_datetime(df["Time"])
    df["gpu_util"] = pd.to_numeric(df["gpu_util"], errors="coerce")
    df = df[df["gpu_util"] <= 100].sort_values("Time")
    offset = QPS_SAMPLE_START - df["Time"].iloc[0]
    df["Time"] = df["Time"] + offset
    return df[df["Time"] <= QPS_SAMPLE_END]


def main() -> None:
    df = load_clean()
    mean_val = df["gpu_util"].mean()
    median_val = df["gpu_util"].median()

    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.plot(df["Time"], df["gpu_util"], color="tab:blue", linewidth=1.2, marker="o", markersize=3)
    ax.axhline(mean_val, color="tab:orange", ls="--", lw=1.0, label=f"mean {mean_val:.1f}%")
    ax.axhline(median_val, color="tab:green", ls=":", lw=1.0, label=f"median {median_val:.1f}%")
    ax.axhline(30, color="gray", ls="-.", lw=0.8, alpha=0.7, label="30% reference")
    ax.set_xlabel("Time (UTC+8)")
    ax.set_ylabel("GPU utilization (%)")
    ax.set_title("Cluster GPU utilization — 2h average (aligned to 9-model window 2026-05-01 to 05-08)")
    ax.set_xlim(QPS_SAMPLE_START, QPS_SAMPLE_END)
    ax.set_ylim(0, 70)
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.25)
    fig.autofmt_xdate()
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
