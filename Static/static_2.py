import random
import matplotlib.pyplot as plt
import numpy as np

def custom_minority_game_with_agent_and_plot(N, X, P_game, P_agent, num_iterations):
    # Lists to store results for plotting and scores for analysis
    num_agents_going_list = []
    outcome_list = []
    individual_agent_decision_list = []
    individual_scores = [0] * N  # Initialize scores for all agents
    
    for _ in range(num_iterations):
        # Convert the probability to a fraction
        probability_game = P_game
        
        # Initialize agents' decisions based on the custom probability
        agents_decisions = [random.choices([0, 1], weights=[1 - probability_game, probability_game])[0] for _ in range(N-1)]
        
        # Count the number of agents going to the bar
        num_agents_going = sum(agents_decisions)
        
        # Determine the outcome based on the majority/minority rule
        if num_agents_going < X:
            outcome = "Good time"
            score_change = 1
        else:
            outcome = "Bad time"
            score_change = -1
        
        # Update scores based on decisions and outcomes
        for i, decision in enumerate(agents_decisions):
            if decision == 1:  # Agent decided to go
                individual_scores[i] += score_change
        
        # Append results to lists for plotting
        num_agents_going_list.append(num_agents_going)
        outcome_list.append(1 if outcome == "Good time" else 0)  # Map "Good time" to 1, "Bad time" to 0
        individual_agent_decision_list.extend(agents_decisions)  # Note: this will be a large list
    
    # Plot results
    plt.figure(figsize=(12, 8))

    # Histogram of Individual Scores
    plt.hist(individual_scores, bins=25, color='tan', alpha=0.7)  # Changed color to light brown ('tan')
    plt.xlabel('Individual Scores')
    plt.ylabel('Frequency')
    plt.title('Distribution of Individual Payoffs')
    mean_score = np.mean(individual_scores)
    plt.axvline(mean_score, color='brown', linestyle='--', label=f'Mean: {mean_score:.2f}')  # Adding a vertical line at the mean
    plt.show()
    
    collective_score = sum(individual_scores)
    print(f"Collective score over {num_iterations} iterations: {collective_score}")
    print(f"Average individual score: {mean_score}")

    return num_agents_going_list, outcome_list, individual_agent_decision_list, individual_scores, collective_score

# Example usage
num_iterations = 1000
P_game, P_agent = 0.59, 0.59
custom_minority_game_with_agent_and_plot(101, 60, P_game, P_agent, num_iterations)
