import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# 確保 /results/figures 目錄存在
RESULTS_DIR = "./results/figures"
os.makedirs(RESULTS_DIR, exist_ok=True)

def plot_boxen_comparison(rl_history, baseline_history, save_path=None):
    """
    使用 boxenplot 比較 RL vs Baseline 在不同 Hint 策略下的 latency 分布
    """
    data = []

    for hint, latencies in rl_history.items():
        for latency in latencies:
            data.append({'Hint': hint, 'Latency (ms)': latency, 'Mode': 'RL AutoSteer++'})

    for hint, latencies in baseline_history.items():
        for latency in latencies:
            data.append({'Hint': hint, 'Latency (ms)': latency, 'Mode': 'Baseline'})

    df = pd.DataFrame(data)

    plt.figure(figsize=(12, 6))
    sns.boxenplot(x='Hint', y='Latency (ms)', hue='Mode', data=df, palette='Set2')

    plt.title('Latency Distribution per Hint Strategy')
    plt.xlabel('Hint Strategy')
    plt.ylabel('Query Latency (ms)')
    plt.legend(title='Strategy Mode')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"📄 Saved boxenplot to {save_path}")
    else:
        plt.show()

    plt.close()


def plot_rl_vs_baseline(rl_latency_all, baseline_avg_round, save_path=None):
    """
    比較 RL 每輪 latency vs baseline 平均 latency（線圖）
    """
    plt.figure(figsize=(12, 5))

    rounds = list(range(1, len(rl_latency_all) + 1))

    plt.plot(rounds, rl_latency_all, marker='o', label='RL AutoSteer++', color='blue')
    plt.plot(rounds, baseline_avg_round, marker='x', label='Baseline (Avg)', color='orange')

    plt.axhline(np.mean(rl_latency_all), linestyle='--', color='blue', alpha=0.5,
                label=f'RL Avg: {np.mean(rl_latency_all):.2f} ms')
    plt.axhline(np.mean(baseline_avg_round), linestyle='--', color='orange', alpha=0.5,
                label=f'Baseline Avg: {np.mean(baseline_avg_round):.2f} ms')

    plt.title('Latency per Round: RL AutoSteer++ vs Baseline')
    plt.xlabel('Round')
    plt.ylabel('Latency (ms)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"📄 Saved RL vs Baseline line plot to {save_path}")
    else:
        plt.show()

    plt.close()


def plot_hint_latency_trends(history_dict, title='Latency Trend per Hint', save_path=None):
    """
    一鍵畫出所有 hint latency 時序圖（Line by Hint）
    支援 history_dict = RL or Baseline 都可
    """
    plt.figure(figsize=(12, 6))
    for hint, latencies in history_dict.items():
        plt.plot(range(1, len(latencies) + 1), latencies, marker='o', label=f"Hint {hint}")

    plt.title(title)
    plt.xlabel('Round')
    plt.ylabel('Latency (ms)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"📄 Saved Hint Latency Trend plot to {save_path}")
    else:
        plt.show()

    plt.close()


def plot_top_n_latency(history_dict, n=10, title='Top-N Fastest Latencies per Hint', save_path=None):
    """
    產生 PDF 報告摘要圖，顯示 Top-N latency per Hint
    """
    data = []

    for hint, latencies in history_dict.items():
        top_n_latencies = sorted(latencies)[:n]
        for latency in top_n_latencies:
            data.append({'Hint': hint, 'Latency (ms)': latency})

    df = pd.DataFrame(data)

    plt.figure(figsize=(10, 5))
    sns.barplot(x='Hint', y='Latency (ms)', data=df, ci=None, palette='Set3')

    plt.title(f'{title} (Top-{n} per Hint)')
    plt.xlabel('Hint Strategy')
    plt.ylabel('Latency (ms)')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"📄 Saved Top-N Latency plot to {save_path}")
    else:
        plt.show()

    plt.close()
