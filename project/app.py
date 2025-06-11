# app.py
import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 讀取資料
with open('./results/rl_history.json', 'r') as f:
    rl_history = json.load(f)

with open('./results/baseline_history.json', 'r') as f:
    baseline_history = json.load(f)

with open('./results/rl_latency_all.json', 'r') as f:
    rl_latency_all = json.load(f)

# 讀 Query → 你可以直接放進去
from config import QUERY_DEFAULT

# ---- Streamlit App ----

st.title("RL AutoSteer++ Dashboard")

# 顯示 Query
st.header("Current Query")
st.code(QUERY_DEFAULT, language='sql')

# Boxenplot RL vs Baseline
st.header("RL vs Baseline Latency Distribution (Boxenplot)")
df_box = []

for hint, times in rl_history.items():
    for latency in times:
        df_box.append({'Hint': hint, 'Latency': latency, 'Mode': 'RL AutoSteer++'})

for hint, times in baseline_history.items():
    for latency in times:
        df_box.append({'Hint': hint, 'Latency': latency, 'Mode': 'Baseline'})

df_box = pd.DataFrame(df_box)

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.boxenplot(x='Hint', y='Latency', hue='Mode', data=df_box, ax=ax1)
ax1.set_title('Latency Distribution per Hint (RL vs Baseline)')
st.pyplot(fig1)

# RL vs Baseline Trend
st.header("Latency per Round: RL AutoSteer++ vs Baseline")
# 計算 baseline_avg_round
min_len = min(len(latencies) for latencies in baseline_history.values())
baseline_avg_round = []
for i in range(min_len):
    avg_latency = np.mean([baseline_history[hint][i] for hint in baseline_history])
    baseline_avg_round.append(avg_latency)

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(rl_latency_all, label='RL AutoSteer++', marker='o')
ax2.plot(baseline_avg_round, label='Baseline (Avg)', marker='x')
ax2.axhline(np.mean(rl_latency_all), color='blue', linestyle='--', label=f'RL Avg: {np.mean(rl_latency_all):.2f} ms')
ax2.axhline(np.mean(baseline_avg_round), color='orange', linestyle='--', label=f'Baseline Avg: {np.mean(baseline_avg_round):.2f} ms')
ax2.set_xlabel('Round')
ax2.set_ylabel('Latency (ms)')
ax2.set_title('Latency per Round: RL AutoSteer++ vs Baseline')
ax2.legend()
st.pyplot(fig2)

# Top-10 Fastest Latency (RL)
st.header("Top-10 Fastest Latencies (RL) per Hint")
df_top10 = []

for hint, times in rl_history.items():
    top10 = sorted(times)[:10]
    for latency in top10:
        df_top10.append({'Hint': hint, 'Latency': latency})

df_top10 = pd.DataFrame(df_top10)

fig3, ax3 = plt.subplots(figsize=(8, 5))
sns.barplot(x='Hint', y='Latency', data=df_top10, ci=None, palette='pastel', ax=ax3)
ax3.set_title('Top-10 Fastest Latencies (RL)')
st.pyplot(fig3)

# Q-table evolution → 可加進去，如果你有存 Q-table → 目前先省略
# st.header("Q-table Evolution (Optional)")

# ---- Done ----


