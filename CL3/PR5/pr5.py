import numpy as np

# Objective function (minimize)
def objective(x):
    return np.sum(x**2)

# Initialize population
def init_population(pop_size, dim, bounds):
    return np.random.uniform(bounds[0], bounds[1], (pop_size, dim))

# Clone and mutate
def clone_and_mutate(pop, fitness, beta, bounds):
    clones = []
    for i, ind in enumerate(pop):
        n_clones = int(beta * len(pop) / (i+1))
        for _ in range(n_clones):
            mutation = np.random.normal(0, 0.1, size=ind.shape)
            clone = np.clip(ind + mutation, bounds[0], bounds[1])
            clones.append(clone)
    return np.array(clones)

# Select top individuals
def select(pop, num_selected):
    fitness = np.array([objective(ind) for ind in pop])
    idx = np.argsort(fitness)
    return pop[idx[:num_selected]], fitness[idx[:num_selected]]

# Clonal Selection Algorithm
def clonal_selection(pop_size=10, dim=5, bounds=(-5, 5), generations=20, beta=2.0):
    pop = init_population(pop_size, dim, bounds)
    for gen in range(generations):
        fitness = np.array([objective(ind) for ind in pop])
        pop_sorted = [x for _, x in sorted(zip(fitness, pop), key=lambda pair: pair[0])]
        clones = clone_and_mutate(pop_sorted, fitness, beta, bounds)
        pop = np.vstack((pop, clones))
        pop, _ = select(pop, pop_size)
    return pop[0], objective(pop[0])

best_sol, best_fit = clonal_selection()
print("Best Solution:", best_sol)
print("Fitness:", best_fit)
