import random
from statistics import mean, median, stdev
import matplotlib.pyplot as plt
import numpy as np

population = 101
half_of_population = population // 2

def trend(count):
    if len(count) <= 1:
        return 0
    return count[-1] - count[0]

def get_mirror_image(half_of_population, attendance):
    return half_of_population - abs(half_of_population - attendance)

def generate_strategies(memory):
    if not memory:
        return {i: half_of_population for i in range(15)}
    strategies = {
        0: lambda c: c[-1],
        1: lambda c: mean(c[-3:]) if len(c) >= 3 else half_of_population,
        2: lambda c: trend(c[-4:]) + c[-1] if len(c) >= 4 else half_of_population,
        3: lambda c: random.randint(0, population),
        4: lambda c: mean(c[-5:]) if len(c) >= 5 else half_of_population,
        5: lambda c: get_mirror_image(half_of_population, c[-1]),
        6: lambda c: median(c[-3:]) if len(c) >= 3 else half_of_population,
        7: lambda c: half_of_population,
        8: lambda c: stdev(c[-4:]) if len(c) >= 5 else half_of_population,
        9: lambda c: c[-1] - mean(c[-4:]) + c[-1] if len(c) >= 4 else half_of_population,
        10: lambda c: half_of_population if c[-1] % 2 == 0 else half_of_population + 10,
        11: lambda c: sum(c[-4:]) / len(c[-4:]) if len(c) >= 4 else half_of_population,
        12: lambda c: min(c[-4:]) if len(c) >= 4 else half_of_population,
        13: lambda c: max(c[-4:]) if len(c) >= 4 else half_of_population,
        14: lambda c: trend(c[-6:]) + c[-1] if len(c) >= 6 else half_of_population,
        15: lambda c: get_mirror_image(half_of_population, mean(c[-2:])) if len(c) >= 2 else half_of_population,
        16: lambda c: get_mirror_image(half_of_population, median(c[-4:])) if len(c) >= 4 else half_of_population,
        17: lambda c: get_mirror_image(half_of_population, min(c[-4:])) if len(c) >= 4 else half_of_population,
        18: lambda c: get_mirror_image(half_of_population, max(c[-4:])) if len(c) >= 4 else half_of_population,
        19: lambda c: get_mirror_image(half_of_population, stdev(c[-4:])) if len(c) >= 5 else half_of_population,
        20: lambda c: half_of_population + (c[-1] - half_of_population) * 0.5 if c else half_of_population,
        21: lambda c: half_of_population - trend(c[-3:]) if len(c) >= 3 else half_of_population,
        22: lambda c: half_of_population * 0.9 if c[-1] > half_of_population else half_of_population * 1.1,
        23: lambda c: get_mirror_image(half_of_population, mean(c[-2:])) + 5 if len(c) >= 2 else half_of_population,
        24: lambda c: half_of_population if mean(c[-4:]) == half_of_population else (mean(c[-4:]) + median(c[-4:])) / 2 if len(c) >= 4 else half_of_population,
    }
    strategies_actions = {key: strategy(memory) for key, strategy in strategies.items()}
    return strategies_actions

# Update strategy values with AIMD approach
def update_strategy_value(strategy, predicted, actual, strategySet, increase_factor, decrease_factor):
    error_magnitude = abs(predicted - actual) / population
    current_score = strategySet.get(strategy, 0.5)
    acceptable_error = 0.1
    
    if error_magnitude <= acceptable_error:
        new_score = current_score + increase_factor
    else:
        new_score = current_score * decrease_factor
    
    new_score = min(max(new_score, 0), 1)
    strategySet[strategy] = new_score

# Simulation function

def run_simulation(increase_factor, decrease_factor, iterations=300, plot=False):
    memory = []
    strategySet = {x: 0.5 for x in range(25)}  # Adjust for your strategies
    agents = {agent: [random.randint(0, 24) for _ in range(5)] for agent in range(population)}
    total_payoffs = []

    for _ in range(iterations):
        strategy_actions = generate_strategies(memory)
        attendance = 0
        agent_decisions = []
        
        for agent, strategies in agents.items():
            chosen_strategy = max(strategies, key=lambda x: strategySet[x])
            predicted_attendance = strategy_actions[chosen_strategy]
            decide_to_go = predicted_attendance < half_of_population
            agent_decisions.append((agent, decide_to_go))
            if decide_to_go:
                attendance += 1
        
        memory.append(attendance)
        actual_attendance = attendance
        
        # Calculate pay-offs based on decisions and actual attendance
        payoffs = [(1 if decide_to_go and actual_attendance < half_of_population else -1 if decide_to_go else 0) for _, decide_to_go in agent_decisions]
        total_payoffs.extend(payoffs)
        
        for strategy, action in strategy_actions.items():
            update_strategy_value(strategy, action, actual_attendance, strategySet, increase_factor, decrease_factor)
    
    average_payoff = mean(total_payoffs)
    
    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(memory, label='Attendance')
        plt.axhline(y=half_of_population, color='r', linestyle='--', label='Optimal attendance threshold')
        plt.title('El Farol Bar Attendance Over Time')
        plt.xlabel('Iteration')
        plt.ylabel('Attendance')
        plt.legend()
        plt.show()
    
    return average_payoff, memory

increase_factors = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15]
decrease_factors = [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
performances = np.zeros((len(increase_factors), len(decrease_factors)))
best_performance = float('inf')
best_factors = None
best_memory = []

for i, inc in enumerate(increase_factors):
    for j, dec in enumerate(decrease_factors):
        performance, memory = run_simulation(inc, dec)
        performances[i, j] = performance
        if performance < best_performance:
            best_performance = performance
            best_factors = (inc, dec)
            best_memory = memory

# Plot the best simulation
_, _ = run_simulation(best_factors[0], best_factors[1], plot=True)

# Plot performance heatmap
plt.figure(figsize=(8, 6))
plt.imshow(performances, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.xlabel('Decrease Factor')
plt.ylabel('Increase Factor')
plt.xticks(np.arange(len(decrease_factors)), labels=[str(df) for df in decrease_factors])
plt.yticks(np.arange(len(increase_factors)), labels=[str(if_) for if_ in increase_factors])
plt.title('Performance Heatmap\n(Lower is Better)')
plt.show()