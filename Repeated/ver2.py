import random
from statistics import mean, median, median_high, median_low
import matplotlib.pyplot as plt

# Define the trend function for calculating trends in attendance
def trend(counts):
    if len(counts) <= 1:
        return 0
    return counts[-1] - counts[0]

# Define the get_mirror_image function for calculating the mirror image strategy
def get_mirror_image(half_of_population, attendance):
    return abs(half_of_population - attendance)

# Define a function to generate strategies based on past attendance
def generate_strategies(count, half_of_population):
    if not count:  # If count is empty, initialize with dummy values
        return {i: 0 for i in range(26)}
    strategies = {
        0: count[-1],  # Last week
        1: count[-2] if len(count) >= 2 else 0,  # Two weeks ago
        2: count[-3] if len(count) >= 3 else 0,  # Three weeks ago
        3: count[-4] if len(count) >= 4 else 0,  # Four weeks ago
        4: min(count),  # Minimum attendance
        5: min(count[-4:]) if len(count) >= 4 else min(count),  # Minimum month attendance
        6: min(count[-8:-4]) if len(count) >= 8 else min(count),  # Minimum two month attendance
        7: min(count[-12:-8]) if len(count) >= 12 else min(count),  # Minimum three month attendance
        8: int(mean(count[-3:])) if len(count) >= 3 else int(mean(count)),  # Three week average
        9: int(mean(count[-4:])) if len(count) >= 4 else int(mean(count)),  # Month average
        10: int(mean(count[-8:-4])) if len(count) >= 8 else int(mean(count)),  # Two month average
        11: int(mean(count[-12:-8])) if len(count) >= 12 else int(mean(count)),  # Three month average
        12: int(mean(count)),  # Total average
        13: int(median(count)),  # Median
        14: median_high(count),  # Median high
        15: median_low(count),  # Median low
        16: trend(count[-4:]) if len(count) >= 4 else 0,  # Month trend
        17: trend(count[-8:-4]) if len(count) >= 8 else 0,  # Two month trend
        18: trend(count[-12:-8]) if len(count) >= 12 else 0,  # Three month trend
        19: get_mirror_image(half_of_population, count[-1]),  # Mirror last week
        20: get_mirror_image(half_of_population, count[-2]) if len(count) >= 2 else get_mirror_image(half_of_population, 0),  # Mirror two weeks
        21: get_mirror_image(half_of_population, count[-3]) if len(count) >= 3 else get_mirror_image(half_of_population, 0),  # Mirror three weeks
        22: get_mirror_image(half_of_population, count[-4]) if len(count) >= 4 else get_mirror_image(half_of_population, 0),  # Mirror four weeks
        23: get_mirror_image(half_of_population, mean(count[-4:])) if len(count) >= 4 else get_mirror_image(half_of_population, mean(count)),  # Mirror month average
        24: get_mirror_image(half_of_population, mean(count[-8:-4])) if len(count) >= 8 else get_mirror_image(half_of_population, mean(count)),  # Mirror two month average
        25: get_mirror_image(half_of_population, mean(count[-12:-8])) if len(count) >= 12 else get_mirror_image(half_of_population, mean(count)),  # Mirror three month average
    }
    return strategies

population = 100  # Define the population size
half_of_population = population // 2
count = []  # Initialize the attendance list

# Initialize the strategy set and agents
strategy_to_actions = generate_strategies(count, half_of_population)
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
    count.append(attendance)

    # Update strategy values (placeholder logic - adjust according to your strategy evaluation criteria)
    for strategy, value in strategySet.items():
        if random.random() > 0.5:  # Randomly decide if a strategy is successful
            strategySet[strategy] += 1  # Increase the value of successful strategies
    
    # Regenerate strategies with updated attendance history
    strategy_to_actions = generate_strategies(count, half_of_population)

# Plot the simulation results
plt.figure(figsize=(10, 6))
plt.plot(range(1, 301), count, label='Attendance')
plt.axhline(y=half_of_population, color='r', linestyle='--', label='Optimal attendance threshold')
plt.title('El Farol Bar Attendance Over 300 Weeks')
plt.xlabel('Week')
plt.ylabel('Attendance')
plt.legend()
plt.show()
