# AutoSteer++

## Introduction

**AutoSteer++** is a reinforcement learning (RL) experimentation framework designed to improve and analyze latency performance in autonomous steering systems.

The project enables:

- Running RL-based experiments to optimize steering latency
- Evaluating baseline (non-RL) performance
- Visualizing trends and comparisons via an interactive dashboard

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Example Outputs](#example-outputs)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation

1. Clone this repository:

```
git clone <your-repo-url>
cd <your-repo-folder>
```

2. Install required dependencies:

```
pip install -r requirements.txt
```

*Note: If `requirements.txt` is not present, you can manually install the following libraries:*

```
pip install matplotlib numpy pandas seaborn streamlit
```

## Usage

### Project

```
project/
├── app.py                # Streamlit Dashboard
├── main.py               # RL 主程式
├── rl_agent.py           # RL Agent
├── baseline_eval.py      # Baseline
├── visualization.py      # 畫圖 utils
├── query_runner.py       # apply_hint + run_query
├── data_import.py        # 匯入資料
├── config.py             # DB + Query_DEFAULT
├── results/              # 存 rl_history.json baseline_history.json rl_latency_all.json
README.md             
requirements.txt
```

### Run RL Experiment

```
python3 main.py
```

### Launch Dashboard

```
streamlit run app.py
```

## Features

- Execute **Reinforcement Learning** experiments to optimize system latency.
- Compute and log **baseline performance** for comparison.
- Visualize:
    - Q-value trends per state-action pair.
    - RL vs Baseline latency trends.
    - Distribution and trends of latency results.
- Interactive **Streamlit dashboard** for result exploration.
- Configurable experiment settings.

## Dependencies

- Dependencies are listed in [requirements.txt](requirements.txt).

## Configuration

Edit `config.py` to adjust parameters such as:

- RL hyperparameters
- Baseline evaluation settings
- Data import paths
- Plot configurations

## Example Outputs

Example results and figures are available in the `results/` directory:

- `rl_history.json`
- `baseline_history.json`
- `rl_latency_all.json`
- Visualizations:
    - `boxenplot_latency_comparison.png`
    - `rl_vs_baseline_trend.png`
    - `rl_hint_latency_trend.png`
    - `baseline_hint_latency_trend.png`
    - `top10_rl_latency.png`
    - `top10_baseline_latency.png`

## Troubleshooting

- If `streamlit run app.py` fails, verify Streamlit installation.
- If RL or baseline evaluation does not produce expected results, check `config.py` and ensure input data is available.

## Contributors

- 李若葳
- 程涵寧
- 蘇鈺琁
- 林立潔
