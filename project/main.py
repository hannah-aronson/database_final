from rl_agent import QLearningAgent
from baseline_eval import run_baseline, summarize_baseline
from visualization import (
    plot_boxen_comparison, plot_rl_vs_baseline,
    plot_hint_latency_trends, plot_top_n_latency
)
from config import QUERY_DEFAULT
from query_runner import reset_hint_cache
import numpy as np
import json
import os

def compute_baseline_avg_round(baseline_history: dict) -> list:
    """
    計算 Baseline 每 round 的平均 latency。
    """
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

def run_all(rounds=30):
    print("\n🚀 執行 RL AutoSteer++")
    agent = QLearningAgent(actions=['A', 'B', 'C'])
    rl_history, rl_latency_all = agent.run(num_rounds=rounds, query=QUERY_DEFAULT)
    agent.print_summary()
    agent.plot_q_table()

    print("\n🚀 執行 Baseline 測試")
    baseline_history = run_baseline(rounds=rounds, query=QUERY_DEFAULT)
    summarize_baseline(baseline_history)

    print("\n📊 畫圖中...")

    # 計算 baseline_avg_round 先算好
    baseline_avg_round = compute_baseline_avg_round(baseline_history)

    # Boxenplot
    plot_boxen_comparison(rl_history, baseline_history, save_path="./results/figures/boxenplot_latency_comparison.png")

    # RL vs Baseline line plot
    plot_rl_vs_baseline(rl_latency_all, baseline_avg_round, save_path="./results/figures/rl_vs_baseline_trend.png")

    # RL Hint latency trends
    plot_hint_latency_trends(rl_history, title="RL AutoSteer++ Latency Trend", save_path="./results/figures/rl_hint_latency_trend.png")

    # Baseline Hint latency trends
    plot_hint_latency_trends(baseline_history, title="Baseline Latency Trend", save_path="./results/figures/baseline_hint_latency_trend.png")

    # Top-N latency (RL)
    plot_top_n_latency(rl_history, n=10, title="Top-10 Fastest Latencies (RL)", save_path="./results/figures/top10_rl_latency.png")

    # Top-N latency (Baseline)
    plot_top_n_latency(baseline_history, n=10, title="Top-10 Fastest Latencies (Baseline)", save_path="./results/figures/top10_baseline_latency.png")

    os.makedirs('./results', exist_ok=True)

    # 儲存 RL history
    with open('./results/rl_history.json', 'w') as f:
        json.dump(rl_history, f)

    # 儲存 Baseline history
    with open('./results/baseline_history.json', 'w') as f:
        json.dump(baseline_history, f)

    # 儲存 RL latency_all
    with open('./results/rl_latency_all.json', 'w') as f:
        json.dump(rl_latency_all, f)

    print("✅ RL / Baseline 歷史已儲存為 JSON，可以直接用 plot_only.py 畫圖！")

if __name__ == "__main__":
    reset_hint_cache()
    run_all(rounds=30)
