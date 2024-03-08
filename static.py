# import random

# def minority_game(num_agents):
#     # Generate random choices for each agent (0 or 1)
#     choices = [random.choice([-1, 1]) for _ in range(num_agents)]

#     # Calculate the majority choice (0 or 1)
#     majority_choice = max(set(choices), key=choices.count)

#     # Determine the minority choice
#     minority_choice = 1 if majority_choice == -1 else -1

#     # Calculate the payoff for each agent
#     payoffs = [1 if choice == minority_choice else -1 for choice in choices]

#     return choices, payoffs, minority_choice

# # Example: Run a game with 100 agents
# num_agents = 101
# choices, payoffs, minority_choice = minority_game(num_agents)

# # Print the results
# print(f"Choices: {choices}")
# print(f"Payoffs: {payoffs}")
# print(f"Minority Choice: {minority_choice}")


import random

def custom_minority_game(N, X, P):
    # Validate the probability value
    if not 0 <= X <= 100:
        raise ValueError("Probability X must be in the range [0, 100]")
    
    # Convert the probability to a fraction
    probability = P
    
    # Initialize agents' decisions based on the custom probability
    agents_decisions = [random.choices([0, 1], weights=[1 - probability, probability])[0] for _ in range(N)]
    
    # Count the number of agents going to the bar
    num_agents_going = sum(agents_decisions)
    
    # Determine the outcome based on the majority/minority rule
    if num_agents_going < X:
        outcome = "Good time"
    else:
        outcome = "Bad time"
    
    # Print the outcome
    print(f"{num_agents_going} agents going to the bar -> {outcome}")

# Example usage with 100 agents and a custom probability of 30%
custom_minority_game(100, 65, 0.5)