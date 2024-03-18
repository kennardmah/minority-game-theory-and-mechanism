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
    
d = '000'
strategySet = {x: 0 for x in range(256)}
agents = {agent: [random.randint(0, 255) for _ in range(15)] for agent in range(1, 102)}
strategy_to_actions = generate_strategies()
count = []

for i in range(300):
    farol = 0
    house = 0
    for x, strats in agents.items():
        active_strategies = []
        maxVal = float('-inf')
        for s in strats:
            if strategySet[s] > maxVal:
                active_strategies = [s]
                maxVal = strategySet[s]
            elif strategySet[s] == maxVal:
                active_strategies.append(s)
        selected_strategy = random.choice(active_strategies)
        action = strategy_to_actions[selected_strategy][d]
        if action == 1:
            farol += 1
        else: house += 1

    if farol < house + 10:
        minority = 1
    else: minority = 0

    for s in range(256):
        if strategy_to_actions[s][d] == minority:
            strategySet[s] += 1
    if farol < house + 10:
        d = d[1:] + '1'
    else: d = d[1:] + '0'
    count.append(farol)

plt.figure(figsize=(10, 6))
plt.plot(list(range(len(count))), count, label='Count', linestyle='-', color = 'tan')
plt.axhline(y=60, color='brown', linestyle='--', label='Y=50')
plt.title('How busy is El Farol?')
plt.xlabel('Week')
plt.ylabel('Bar Count')
plt.legend()
plt.ylim(0, 100)
plt.grid(True)
plt.show()