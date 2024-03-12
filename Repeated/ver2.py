import random
from statistics import mean, median, median_high, median_low
import matplotlib.pyplot as plt

def trend(count):
    if len(count) <= 1:
        return 0
    return count[-1] - count[0]

def get_mirror_image(half_of_population, attendance):
    return abs(half_of_population - attendance)

def generate_strategies(memory, half_of_population):
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
        19: get_mirror_image(half_of_population, memory[-1]),
        20: get_mirror_image(half_of_population, memory[-2]) if len(memory) >= 2 else get_mirror_image(half_of_population, 0),
        21: get_mirror_image(half_of_population, memory[-3]) if len(memory) >= 3 else get_mirror_image(half_of_population, 0),
        22: get_mirror_image(half_of_population, memory[-4]) if len(memory) >= 4 else get_mirror_image(half_of_population, 0),
        23: get_mirror_image(half_of_population, mean(memory[-4:])) if len(memory) >= 4 else get_mirror_image(half_of_population, mean(memory)),
        24: get_mirror_image(half_of_population, mean(memory[-8:-4])) if len(memory) >= 8 else get_mirror_image(half_of_population, mean(memory)),
        25: get_mirror_image(half_of_population, mean(memory[-12:-8])) if len(memory) >= 12 else get_mirror_image(half_of_population, mean(memory)),
    }
    return strategies

population = 100  # Define the population size
half_of_population = population // 2
memory = []  # Initialize the attendance list

# Initialize the strategy set and agents
strategy_to_actions = generate_strategies(memory, half_of_population)
strategySet = {x: 0 for x in range(len(strategy_to_actions))}
agents = {agent: [random.randint(0, len(strategy_to_actions)-1) for _ in range(5)] for agent in range(1, population+1)}

# Run the simulation for 300 iterations
for _ in range(300):
    attendance = 0

    # Each agent decides whether to go based on their strategy
    for agent_id, strategies in agents.items():
        strategy_scores = [(strategy, strategySet[strategy]) for strategy in strategies]
        best_strategies = [s for s, score in strategy_scores if score == max(strategy_scores, key=lambda x: x[1])[1]]
        chosen_strategy = random.choice(best_strategies)
        # Simplified decision: go if the chosen strategy's value is odd (just for demonstration)
        if chosen_strategy % 2 == 1:
            attendance += 1
        print(agent_id, strategy_scores, '\n', chosen_strategy, attendance)
    
    # Update attendance history
    memory.append(attendance)

    # Update strategy values (placeholder logic - adjust according to your strategy evaluation criteria)
    for strategy, value in strategySet.items():
        if random.random() > 0.5:  # Randomly decide if a strategy is successful
            strategySet[strategy] += 1  # Increase the value of successful strategies
    
    # Regenerate strategies with updated attendance history
    strategy_to_actions = generate_strategies(memory, half_of_population)

# Plot the simulation results
plt.figure(figsize=(10, 6))
plt.plot(range(1, 301), memory, label='Attendance')
plt.axhline(y=half_of_population, color='r', linestyle='--', label='Optimal attendance threshold')
plt.title('El Farol Bar Attendance Over 300 Weeks')
plt.xlabel('Week')
plt.ylabel('Attendance')
plt.legend()
plt.show()
