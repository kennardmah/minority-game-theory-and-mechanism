import random
import matplotlib.pyplot as plt

def custom_minority_game_with_agent_and_plot(N, X, P_game, P_agent, num_iterations):
    # Lists to store results for plotting
    num_agents_going_list = []
    outcome_list = []
    individual_agent_decision_list = []
    
    for _ in range(num_iterations):
        # Convert the probability to a fraction
        probability_game = P_game
        
        # Initialize agents' decisions based on the custom probability
        agents_decisions = [random.choices([0, 1], weights=[1 - probability_game, probability_game])[0] for _ in range(N)]
        
        # Count the number of agents going to the bar
        num_agents_going = sum(agents_decisions)
        
        # Determine the outcome based on the majority/minority rule
        if num_agents_going < X:
            outcome = "Good time"
        else:
            outcome = "Bad time"
        
        # Print the outcome
        print(f"{num_agents_going} agents going to the bar -> {outcome}")
        
        # Individual agent's decision
        individual_agent_decision = random.choices([0, 1], weights=[1 - P_agent, P_agent])[0]
        print("The individual agent's decision is: " + str(individual_agent_decision))
        
        # Check if the individual agent is in the minority
        if individual_agent_decision == 1 and num_agents_going + 1 < X:
            print("Individual agent is in the minority")
        elif individual_agent_decision == 0 and num_agents_going >= X:
            print("Individual agent is in the minority")
        else:
            print("Individual agent is not in the majority")
        
        # Append results to lists for plotting
        num_agents_going_list.append(num_agents_going)
        outcome_list.append(1 if outcome == "Good time" else 0)  # Map "Good time" to 1, "Bad time" to 0
        individual_agent_decision_list.append(individual_agent_decision)
    
    # Plot both subplots on the same figure
    plt.figure(figsize=(12, 8))

    # Subplot 1: Number of Agents Going and Threshold
    plt.subplot(2, 1, 1)
    plt.plot(range(1, num_iterations + 1), num_agents_going_list, label='Number of Agents Going')
    plt.axhline(y=X, color='r', linestyle='--', label='Threshold (X)')
    plt.xlabel('Iteration')
    plt.ylabel('Values')
    plt.title('Number of Agents Going and Threshold')
    plt.legend()

    # Subplot 2: Individual Agent's Decision and Minority Status
    plt.subplot(2, 1, 2)
    plt.scatter(range(1, num_iterations + 1), individual_agent_decision_list, c=outcome_list, cmap='viridis', label='Individual Agent Decision')
    plt.xlabel('Iteration')
    plt.ylabel('Not going / Going')
    plt.title('Individual Agent Decision and Minority Status')
    plt.legend()

    plt.tight_layout()  # Adjust layout for better spacing
    plt.show()
    
    return num_agents_going_list, outcome_list, individual_agent_decision_list

# Example usage with 100 agents, a custom probability of 30% for the game, and a probability of 0.4 for the individual agent, running for 5 iterations
num_iterations = 50
custom_minority_game_with_agent_and_plot(100, 50, 0.5, 0.4, num_iterations)
