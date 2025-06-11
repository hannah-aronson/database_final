import random
from typing import Dict, List
from query_runner import apply_hint_indexes, run_query

def run_baseline(hints: List[str] = ['A', 'B', 'C'], rounds: int = 30, query: str = None, verbose: bool = True):
    """
    執行每個 hint 固定策略的 baseline 測試。
    傳回每個 hint 對應的 latency list（字典）。
    """
    history = {hint: [] for hint in hints}

    for hint in hints:
        if verbose:
            print(f"\n▶ Baseline Testing for Hint: {hint}")
        for i in range(rounds):
            apply_hint_indexes(hint)
            latency = run_query(query=query)
            history[hint].append(latency)
            if verbose:
                print(f"[Baseline] Round {i+1:02d}: Hint={hint}, Latency={latency:.2f} ms")

    return history

def summarize_baseline(history: Dict[str, List[float]]):
    """
    顯示每個 Hint 的平均 latency 統計。
    """
    print("\n📊 [Baseline] Average Latency per Hint:")
    for hint, times in history.items():
        avg = sum(times) / len(times) if times else 0
        print(f"Hint {hint}: {avg:.2f} ms over {len(times)} runs")