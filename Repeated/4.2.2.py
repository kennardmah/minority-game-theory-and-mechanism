import random
from statistics import mean, median, median_high, median_low
import matplotlib.pyplot as plt

def trend(count):
    if len(count) <= 1:
        return 0
    return count[-1] - count[0]

def get_mirror_image(capacity, attendance):
    return abs(capacity - attendance)

def generate_strategies(memory, capacity):
    if not memory:
        return {i: 0 for i in range(26)}
    strategies = {
        0: memory[-1],
        1: memory[-2] if len(memory) >= 2 else 0,
        2: memory[-3] if len(memory) >= 3 else 0,
        3: memory[-4] if len(memory) >= 4 else 0,
        4: min(memory),
        5: min(memory[-4:]) if len(memory) >= 4 else min(memory),
        6: min(memory[-8:-4]) if len(memory) >= 8 else min(memory),
        7: min(memory[-12:-8]) if len(memory) >= 12 else min(memory),
        8: int(mean(memory[-3:])) if len(memory) >= 3 else int(mean(memory)),
        9: int(mean(memory[-4:])) if len(memory) >= 4 else int(mean(memory)),
        10: int(mean(memory[-8:-4])) if len(memory) >= 8 else int(mean(memory)),
        11: int(mean(memory[-12:-8])) if len(memory) >= 12 else int(mean(memory)),
        12: int(mean(memory)),
        13: int(median(memory)),
        14: median_high(memory),
        15: median_low(memory),
        16: trend(memory[-4:]) if len(memory) >= 4 else 0,
        17: trend(memory[-8:-4]) if len(memory) >= 8 else 0,
        18: trend(memory[-12:-8]) if len(memory) >= 12 else 0,
        19: get_mirror_image(capacity, memory[-1]),
        20: get_mirror_image(capacity, memory[-2]) if len(memory) >= 2 else get_mirror_image(capacity, 0),
        21: get_mirror_image(capacity, memory[-3]) if len(memory) >= 3 else get_mirror_image(capacity, 0),
        22: get_mirror_image(capacity, memory[-4]) if len(memory) >= 4 else get_mirror_image(capacity, 0),
        23: get_mirror_image(capacity, mean(memory[-4:])) if len(memory) >= 4 else get_mirror_image(capacity, mean(memory)),
        24: get_mirror_image(capacity, mean(memory[-8:-4])) if len(memory) >= 8 else get_mirror_image(capacity, mean(memory)),
        25: get_mirror_image(capacity, mean(memory[-12:-8])) if len(memory) >= 12 else get_mirror_image(capacity, mean(memory)),
    }
    return strategies

population = 101
capacity = 60
memory = []
iterations = 300

# Initialize the strategy set and agents
strategy_to_actions = generate_strategies(memory, capacity)
strategySet = {x: 0 for x in range(len(strategy_to_actions))}
agents = {agent: [random.randint(0, len(strategy_to_actions)-1) for _ in range(5)] for agent in range(1, population+1)}

for _ in range(iterations):
    attendance = 0

    # Each agent decides whether to go based on their strategy
    for agent_id, strategies in agents.items():
        strategy_scores = [(strategy, strategySet[strategy]) for strategy in strategies]
        best_strategies = [s for s, score in strategy_scores if score == max(strategy_scores, key=lambda x: x[1])[1]]
        chosen_strategy = random.choice(best_strategies)
        if strategy_to_actions[chosen_strategy] < capacity:
            attendance += 1
        # print(agent_id, strategy_scores, '\n', chosen_strategy, attendance)
    
    memory.append(attendance)

    # Update strategy values (refined in 4.2.3)
    for strategy, value in strategySet.items():
        if attendance >= capacity:
            if value >= capacity:
                strategySet[strategy] += 1
        else:
            if value < capacity:
                strategySet[strategy] += 1
    
    # Regenerate strategies with updated attendance history
    strategy_to_actions = generate_strategies(memory, capacity)

# Plot the simulation results
plt.figure(figsize=(10, 6))
plt.plot(range(1, 301), memory, label='Attendance', color = 'tan')
plt.ylim(0, population)
plt.axhline(y=capacity, color='brown', linestyle='--', label='Optimal attendance threshold')
plt.title('El Farol Bar Attendance Over 300 Weeks')
plt.xlabel('Week')
plt.ylabel('Attendance')
plt.legend()
plt.show()
