import math

n = 101
proba = 0.595
payoff = [0] * (n + 1)

for k in range(1, 61):
    P = math.factorial(n) / (math.factorial(k) * math.factorial(n - k)) * proba**k * (1 - proba)**(n - k)
    payoff[k] = P * k

for k in range(61, 102):
    P = math.factorial(n) / (math.factorial(k) * math.factorial(n - k)) * proba**k * (1 - proba)**(n - k)
    payoff[k] = -P * k

expected = sum(payoff)

print(expected)