import numpy as np

population = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
weights = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
weights_normalized = []
weight_sum = sum(weights)	
#print(weight_sum)
for w in weights:
	weights_normalized.append(w/weight_sum)
#print(weights_normalized)
sample = np.random.choice(a = population, size = 3, replace = False, p = weights_normalized)

allvals = set([1, 2, 3, 4, 6, 7])
training = set([1, 2])
test = list(set(allvals) - set(training))
print(test)