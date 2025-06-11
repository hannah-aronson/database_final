# plot_only.py

import json
import numpy as np
from visualization import (
    plot_boxen_comparison, plot_rl_vs_baseline,
    plot_hint_latency_trends, plot_top_n_latency
)

def compute_baseline_avg_round(baseline_history: dict) -> list:
    max_len = max(len(v) for v in baseline_history.values())
    baseline_avg_round = []
    for i in range(max_len):
        latencies = [
            baseline_history[hint][i]
            for hint in baseline_history
            if i < len(baseline_history[hint])
        ]
        if latencies:
            baseline_avg_round.append(np.mean(latencies))
    return baseline_avg_round

# 讀取 RL history
with open('./results/rl_history.json', 'r') as f:
    rl_history = json.load(f)

# 讀取 Baseline history
with open('./results/baseline_history.json', 'r') as f:
    baseline_history = json.load(f)

# 讀取 RL latency_all
with open('./results/rl_latency_all.json', 'r') as f:
    rl_latency_all = json.load(f)

# 計算 baseline_avg_round
baseline_avg_round = compute_baseline_avg_round(baseline_history)

print("\n📊 Plotting saved RL / Baseline data...")

# Boxenplot
plot_boxen_comparison(rl_history, baseline_history, save_path="./results/figures/boxenplot_latency_comparison.png")

# RL vs Baseline line plot
plot_rl_vs_baseline(
    rl_latency_all,
    baseline_avg_round,
    save_path="./results/figures/rl_vs_baseline_trend.png"
)

# RL Hint latency trends
plot_hint_latency_trends(rl_history, title="RL AutoSteer++ Latency Trend", save_path="./results/figures/rl_hint_latency_trend.png")

# Baseline Hint latency trends
plot_hint_latency_trends(baseline_history, title="Baseline Latency Trend", save_path="./results/figures/baseline_hint_latency_trend.png")

# Top-N latency (RL)
plot_top_n_latency(rl_history, n=10, title="Top-10 Fastest Latencies (RL)", save_path="./results/figures/top10_rl_latency.png")

# Top-N latency (Baseline)
plot_top_n_latency(baseline_history, n=10, title="Top-10 Fastest Latencies (Baseline)", save_path="./results/figures/top10_baseline_latency.png")

print("✅ 所有圖已畫完！可直接打開 results/figures 看圖。")
