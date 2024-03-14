# -----------------------------------------------------------------------------
# El Farol Bar Attendance Simulation
# Authors: Ken Mah, Felix Brochier
# Date: March 8th, 2024
# 
# This simulation models the decision-making process of agents attempting
# to attend a bar based on past attendance records, utilising various predictive
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

def trend(count):
    if len(count) <= 1:
        return 0
    return count[-1] - count[0]

def get_mirror_image(capacity, attendance):
    return capacity - abs(capacity - attendance)

def generate_strategies(memory, capacity):
    if not memory:  # If memory is empty, default to predicting capacity
        return {i: capacity for i in range(15)}
    strategies = {
        0: lambda m: m[-1],
        1: lambda m: mean(m[-3:]) if len(m) >= 3 else capacity,
        2: lambda m: trend(m[-4:]) + m[-1] if len(m) >= 4 else capacity,
        3: lambda m: random.randint(0, N),
        4: lambda m: mean(m[-5:]) if len(m) >= 5 else capacity,
        5: lambda m: get_mirror_image(capacity, m[-1]),
        6: lambda m: median(m[-3:]) if len(m) >= 3 else capacity,
        7: lambda m: capacity,
        8: lambda m: stdev(m[-4:]) if len(m) >= 5 else capacity,
        9: lambda m: m[-1] - mean(m[-4:]) + m[-1] if len(m) >= 4 else capacity,
        10: lambda m: capacity if m[-1] % 2 == 0 else capacity + 10,
        11: lambda m: sum(m[-4:]) / len(m[-4:]) if len(m) >= 4 else capacity,
        12: lambda m: min(m[-4:]) if len(m) >= 4 else capacity,
        13: lambda m: max(m[-4:]) if len(m) >= 4 else capacity,
        14: lambda m: trend(m[-6:]) + m[-1] if len(m) >= 6 else capacity,
        15: lambda m: get_mirror_image(capacity, mean(m[-2:])) if len(m) >= 2 else capacity,
        16: lambda m: get_mirror_image(capacity, median(m[-4:])) if len(m) >= 4 else capacity,
        17: lambda m: get_mirror_image(capacity, min(m[-4:])) if len(m) >= 4 else capacity,
        18: lambda m: get_mirror_image(capacity, max(m[-4:])) if len(m) >= 4 else capacity,
        19: lambda m: get_mirror_image(capacity, stdev(m[-4:])) if len(m) >= 5 else capacity,
        20: lambda m: capacity + (m[-1] - capacity) * 0.5 if m else capacity,
        21: lambda m: capacity - trend(m[-3:]) if len(m) >= 3 else capacity,
        22: lambda m: capacity * 0.9 if m[-1] > capacity else capacity * 1.1,
        23: lambda m: get_mirror_image(capacity, mean(m[-2:])) + 5 if len(m) >= 2 else capacity,
        24: lambda m: capacity if mean(m[-4:]) == capacity else (mean(m[-4:]) + median(m[-4:])) / 2 if len(m) >= 4 else capacity,
    }
    strategies_actions = {key: strategy(memory) for key, strategy in strategies.items()}
    return strategies_actions

# -----------------------------------------------------------------------------
#                              define parameters
# -----------------------------------------------------------------------------

N = 101
capacity = 60
memory = []
agents_payoffs = {agent: 0 for agent in range(1, N+1)}

strategy_to_actions = generate_strategies(memory, capacity)
strategySet = {x: 0 for x in range(len(strategy_to_actions))}
agents = {agent: [random.randint(0, len(strategy_to_actions)-1) for _ in range(5)] for agent in range(1, N+1)}

# -----------------------------------------------------------------------------
#            update active strategies (weighted benefits/penalties)
# -----------------------------------------------------------------------------


def update_strategy_value(strategy, prediction, actual, strategySet, alpha=0.5):
    error_magnitude = abs(prediction - actual) / N
    current_score = strategySet.get(strategy, 0.5)
    if actual >= capacity:
        if prediction >= capacity: # good
            new_score = current_score + 1 
        elif prediction < capacity: # bad
            new_score = current_score + alpha*(1 - error_magnitude)
    elif actual < capacity:
        if prediction < capacity: # good
            new_score = current_score + 1 
        elif prediction >= capacity: # bad
            new_score = current_score + alpha*(1 - error_magnitude)
    # if strategy == 3:
    #     print(strategy, current_score, new_score, prediction, actual, prediction - actual)
    strategySet[strategy] = new_score

def calculate_volatility_factor(memory, capacity):
    if len(memory) >= 5:
        recent_volatility = stdev(memory[-5:])
        return recent_volatility / capacity
    return 1

# -----------------------------------------------------------------------------
#                              run simulation
# -----------------------------------------------------------------------------

iterations = 300
for i in range(iterations):
    attendance = 0
    decisions = []
    strategy_to_actions = generate_strategies(memory, capacity)
    strategy_predictions = {strategy: func for strategy, func in strategy_to_actions.items()}
    for agent_id, strategies in agents.items():
        chosen_strategy = max(strategies, key=lambda x: strategySet[x])
        prediction = strategy_predictions[chosen_strategy]
        decision_to_go = prediction < capacity
        decisions.append((agent_id, decision_to_go))
        if decision_to_go:
            attendance += 1
    for id, decision in decisions:
        if decision and attendance < capacity:
            agents_payoffs[id] += 1
        elif decision and attendance >= capacity:
            agents_payoffs[id] -= 1
    print(i, agents_payoffs[1])

    memory.append(attendance)
    for strategy, prediction in strategy_predictions.items():
        update_strategy_value(strategy, prediction, attendance, strategySet, alpha=0.5)
    

# -----------------------------------------------------------------------------
#                               plot values
# -----------------------------------------------------------------------------

print("Individual Payoff:")
collective_payoff = 0
for agent_id, payoff in agents_payoffs.items():
    print(f"Agent {agent_id}: {payoff}")
    collective_payoff += payoff
print(f"Collective Payoff: {collective_payoff}")


plt.figure(figsize=(10, 6))
plt.plot(range(1, iterations+1), memory, label='Attendance')
plt.axhline(y=capacity, color='r', linestyle='--', label='Optimal attendance threshold')
plt.title('El Farol Bar Attendance Over 300 Weeks')
plt.xlabel('Week')
plt.ylabel('Number of Attendees')
plt.legend()
plt.show()