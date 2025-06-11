# rl_agent.py (QLearningAgent_v2 with Epsilon Decay + Normalized Reward + Q-table plot)

import random
import numpy as np
from query_runner import apply_hint_indexes, run_query
import matplotlib.pyplot as plt

class QLearningAgent:
    def __init__(self, actions, states=None, epsilon=0.5, alpha=0.1, gamma=0.9, epsilon_decay=0.98, min_epsilon=0.05):
        self.actions = actions
        self.states = states or ['A', 'B', 'C', 'None']
        self.q_table = {s: {a: 0.0 for a in self.actions} for s in self.states}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.prev_state = 'None'
        self.prev_latency = None
        self.history = {a: [] for a in self.actions}
        self.latency_all = []
        self.q_table_trace = {s: {a: [] for a in self.actions} for s in self.states}  # For plotting Q-table trends

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return random.choice(self.actions)
        return min(self.q_table[state], key=self.q_table[state].get)

    def update_q(self, prev_state, action, reward, next_state):
        old_q = self.q_table[prev_state][action]
        next_best_q = min(self.q_table[next_state].values())
        new_q = old_q + self.alpha * (reward + self.gamma * next_best_q - old_q)
        self.q_table[prev_state][action] = new_q

        # Save Q value trace for plotting
        for a in self.actions:
            self.q_table_trace[prev_state][a].append(self.q_table[prev_state][a])

    def run(self, num_rounds=30, query=None, verbose=True):
        latency_window = []  # For moving average normalization

        for i in range(num_rounds):
            action = self.choose_action(self.prev_state)
            apply_hint_indexes(action)
            latency = run_query(query=query)

            latency_window.append(latency)
            if len(latency_window) > 20:  # Moving window size = 20
                latency_window.pop(0)

            # Normalized reward → latency / avg_latency
            avg_latency = np.mean(latency_window) if latency_window else latency
            reward = -(latency / avg_latency)  # 越快 reward 越大（> -1）

            next_state = action

            self.update_q(self.prev_state, action, reward, next_state)
            self.history[action].append(latency)
            self.latency_all.append(latency)

            if verbose:
                print(f"Round {i+1:02d}: Hint={action}, Latency={latency:.2f} ms, Reward={reward:.4f}, Epsilon={self.epsilon:.4f}")

            # 更新 state
            self.prev_state = next_state
            self.prev_latency = latency

            # Decay epsilon
            self.epsilon = max(self.epsilon * self.epsilon_decay, self.min_epsilon)

        return self.history, self.latency_all

    def print_summary(self):
        print("\n📊 [RL AutoSteer++] Average Latency per Hint:")
        for hint, times in self.history.items():
            avg = sum(times) / len(times) if times else 0
            print(f"Hint {hint}: {avg:.2f} ms over {len(times)} runs")

    def plot_q_table(self):
        """
        Plot Q value trends for each state-action pair
        """
        for state in self.states:
            plt.figure(figsize=(10, 5))
            for action in self.actions:
                plt.plot(self.q_table_trace[state][action], label=f'Q({state},{action})')
            plt.title(f'Q-value Trends from State "{state}"')
            plt.xlabel('Update Step')
            plt.ylabel('Q-value')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.4)
            plt.tight_layout()
            plt.show()
