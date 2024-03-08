# import stuff
import random
import matplotlib.pyplot as plt

def generate_strategies():
    strategies = {}
    for strategy_number in range(0, 256):
        action_map_bin = format(strategy_number, '08b')
        strategy = {}
        for i in range(8):
            outcome = format(i, '03b')
            strategy[outcome] = int(action_map_bin[i])
        strategies[strategy_number] = strategy
    return strategies

# def update_strategy_values(strategySet):

# INITIALISE VALUES
    
d = '000' # short term memory
# initialise strategySet (strategy : value)
# e.g., strategy = 000 if last three rounds were >50, >50, >50
strategySet = {x: 0 for x in range(256)}
# initialise agents (agents : [strategy set])
agents = {agent: [random.randint(0, 255) for _ in range(15)] for agent in range(1, 102)}
# strategy_to_actions (strategy num: all potential history -> outcome)
strategy_to_actions = generate_strategies()
# graph count
count = []

# RUN SIMULATION
print(strategy_to_actions)
for i in range(300):
    farol = 0
    house = 0
    for x, strats in agents.items():
        # find active strategies
        active_strategies = []
        maxVal = float('-inf')
        for s in strats:
            if strategySet[s] > maxVal:
                active_strategies = [s]
                maxVal = strategySet[s]
            elif strategySet[s] == maxVal:
                active_strategies.append(s)
        # choose out of the active strategies randomly
        selected_strategy = random.choice(active_strategies)
        # check action
        action = strategy_to_actions[selected_strategy][d]
        if action == 1:
            farol += 1
        else: house += 1

    if farol < house:
        minority = 1
    else: minority = 0

    # update strategy values
    for s in range(256):
        # if strategy is correct, add 1 for value
        if strategy_to_actions[s][d] == minority:
            strategySet[s] += 1

    # update memory
    if farol < house:
        d = d[1:] + '1' # farol is minority
    else: d = d[1:] + '0' # home is minority
    count.append(farol)

# Plotting
plt.figure(figsize=(10, 6))  # Set the figure size (optional)
plt.plot(list(range(len(count))), count, label='Count', linestyle='-')
plt.axhline(y=50, color='r', linestyle='--', label='Y=50')  # Add horizontal line at y=50
plt.title('How busy is El Farol?')
plt.xlabel('Week')
plt.ylabel('Bar Count')
plt.legend()
plt.ylim(0, 100)
plt.grid(True)
plt.show()