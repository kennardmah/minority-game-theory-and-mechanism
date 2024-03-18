import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def custom_minority_game_with_agent_and_plot(N, X, P_game, P_agent, num_iterations):
    # Lists to store results for plotting
    num_agents_going_list = []
    outcome_list = []
    individual_agent_decision_list = []
    individual_agent_score = 0  # Initialize the individual player's score
    individual_outcome = 0

    for _ in range(num_iterations):
        
        # Initialize agents' decisions based on the custom probability
        agents_decisions = [random.choices([0, 1], weights=[1 - P_game, P_game])[0] for _ in range(N-1)]
        
        # Count the number of agents going to the bar
        num_agents_going = sum(agents_decisions)
        
        # Determine the outcome based on the majority/minority rule
        if num_agents_going < X:
            outcome = "Good time"
        else:
            outcome = "Bad time"
        
        # Individual agent's decision
        individual_agent_decision = random.choices([0, 1], weights=[1 - P_agent, P_agent])[0]
        
        # Check if the individual agent is in the minority and adjust the score accordingly
        if individual_agent_decision == 1:
            if num_agents_going < X:  # Good time and went to the bar
                individual_agent_score += 1
                individual_outcome = 1
            elif num_agents_going >= X:  # Bad time and went to the bar
                individual_agent_score -= 1
                individual_outcome = 0
        else:
            if num_agents_going < X:  # Good time and went to the bar
                individual_outcome = 0
            elif num_agents_going >= X:  # Bad time and went to the bar
                individual_outcome = 1
        # If the individual agent decides to stay home, do nothing (score remains the same)
        
        # Append results to lists for plotting
        num_agents_going_list.append(num_agents_going)
        outcome_list.append(individual_outcome)  # Map "Good time" to 1, "Bad time" to 0
        individual_agent_decision_list.append(individual_agent_decision)
    
    plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])

    ax0 = plt.subplot(gs[0])
    ax0.plot(range(1, num_iterations + 1), num_agents_going_list, color='saddlebrown', label='Number of Agents Going')
    ax0.axhline(y=X, color='darkorange', linestyle='--', label='Threshold (X)')
    ax0.set_xlabel('Iteration')
    ax0.set_ylabel('Values')
    ax0.set_title('Number of Agents Going and Threshold')
    ax0.legend()
    ax0.set_ylim(30, 90)

    # Subplot 2: Individual Agent's Decision and Minority Status, make it vertically shorter
    ax1 = plt.subplot(gs[1])
    ax1.scatter(range(1, num_iterations + 1), individual_agent_decision_list, c=outcome_list, cmap='copper', label='Individual Agent Decision')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Not going / Going')
    ax1.set_yticks([0, 1])  # Only show values 0 and 1 on the y-axis
    ax1.set_title('Individual Agent Decision and Minority Status')
    ax1.legend()

    plt.tight_layout()  # Adjust layout for better spacing
    plt.show()
    
    print(f"Individual agent's score over {num_iterations} iterations: {individual_agent_score}")
    
    return num_agents_going_list, outcome_list, individual_agent_decision_list, individual_agent_score

# Example usage
num_iterations = 50
custom_minority_game_with_agent_and_plot(101, 60, 60/101, 60/101, num_iterations)

