# -----------------------------------------------------------------------------
# El Farol Bar Attendance Simulation
# Authors: Ken Mah, Felix Brochier
# Date: March 8th, 2024
# 
# This simulation models the decision-making process of individuals attempting
# to attend a bar based on past attendance records, utilizing various predictive
# strategies to avoid overcrowding.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
#                              import stuff
# -----------------------------------------------------------------------------

import random
from statistics import mean, median, stdev
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
#                              initialise strategies
# -----------------------------------------------------------------------------

def trend(counts):
    if len(counts) <= 1:
        return 0
    return counts[-1] - counts[0]

def get_mirror_image(half_of_population, attendance):
    return half_of_population - abs(half_of_population - attendance)

def generate_strategies(count, half_of_population):
    if not count:  # If count is empty, default to predicting half_of_population
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
    strategies_actions = {key: strategy(count) for key, strategy in strategies.items()}
    return strategies_actions

# -----------------------------------------------------------------------------
#                              define parameters
# -----------------------------------------------------------------------------

population = 101
half_of_population = population // 2
count = []

strategy_to_actions = generate_strategies(count, half_of_population)
strategySet = {x: 0 for x in range(len(strategy_to_actions))}
agents = {agent: [random.randint(0, len(strategy_to_actions)-1) for _ in range(5)] for agent in range(1, population+1)}

# -----------------------------------------------------------------------------
#            update active strategies (weighted benefits/penalties)
# -----------------------------------------------------------------------------

def update_strategy_value(strategy, predicted, actual, strategySet, alpha=0.1):
    error_magnitude = abs(predicted - actual) / population
    current_score = strategySet.get(strategy, 0.5)
    new_score = alpha * (1 - error_magnitude) + (1 - alpha) * current_score
    strategySet[strategy] = new_score

def calculate_volatility_factor(count, half_of_population):
    if len(count) >= 5:
        recent_volatility = stdev(count[-5:])
        return recent_volatility / half_of_population
    return 1

# -----------------------------------------------------------------------------
#                              run simulation
# -----------------------------------------------------------------------------

iterations = 300
for i in range(iterations):
    attendance = 0
    strategy_to_actions = generate_strategies(count, half_of_population)
    strategy_predictions = {strategy: func for strategy, func in strategy_to_actions.items()}
    for agent_id, strategies in agents.items():
        chosen_strategy = max(strategies, key=lambda x: strategySet[x])
        predicted_attendance = strategy_predictions[chosen_strategy]
        if predicted_attendance < half_of_population:
            attendance += 1
    count.append(attendance)
    actual_attendance = attendance
    for strategy, prediction in strategy_predictions.items():
        update_strategy_value(strategy, prediction, actual_attendance, strategySet, alpha=0.1)


# -----------------------------------------------------------------------------
#                               plot values
# -----------------------------------------------------------------------------

plt.figure(figsize=(10, 6))
plt.plot(range(1, iterations+1), count, label='Attendance')
plt.axhline(y=half_of_population, color='r', linestyle='--', label='Optimal attendance threshold')
plt.title('El Farol Bar Attendance Over 300 Weeks')
plt.xlabel('Week')
plt.ylabel('Number of Attendees')
plt.legend()
plt.show()
print('Done')
