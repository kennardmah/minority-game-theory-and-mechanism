import numpy as np
import matplotlib.pyplot as plt

# Parameters
N = 101  # Number of agents
capacity = 60  # Bar capacity
weeks = 100  # Simulation length
alpha = 0.01  # Additive increase factor
beta = 0.05   # Multiplicative decrease factor

attendance_history = []
probability_of_attending = np.full(N, 0.5)  # Start with a 50% chance of attending

def update_probabilities(week_attendance):
    """Update attending probabilities using AIMD based on last week's attendance."""
    global probability_of_attending
    if week_attendance < capacity:
        # Additive increase
        probability_of_attending = np.minimum(probability_of_attending + alpha, 1.0)
    else:
        # Multiplicative decrease
        probability_of_attending = np.maximum(probability_of_attending * (1 - beta), 0)

# Simulation loop
for week in range(weeks):
    decisions = np.random.rand(N) < probability_of_attending
    week_attendance = np.sum(decisions)
    attendance_history.append(week_attendance)
    update_probabilities(week_attendance)

plt.figure(figsize=(12, 6))
plt.plot(attendance_history, label='Attendance')
plt.ylim(0, N)
plt.axhline(y=capacity, color='r', linestyle='--', label='Capacity')
plt.title('Bar Attendance Over Time with AIMD Strategy')
plt.xlabel('Week')
plt.ylabel('Attendance')
plt.legend()
plt.show()
