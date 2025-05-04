import random

# Objective function: smaller is better
def fitness(x):
    return x * x

# Create initial population (random numbers)
def create_population(size, lower_bound, upper_bound):
    population = []
    for _ in range(size):
        individual = random.uniform(lower_bound, upper_bound)
        population.append(individual)
    return population

# Clone good individuals (more clones for better ones)
def clone_individuals(population, num_clones):
    clones = []
    for individual in population:
        for _ in range(num_clones):
            clones.append(individual)
    print("Clones:",clones)
    return clones

# Mutate the clones a little
def mutate(individual, mutation_rate, lower_bound, upper_bound):
    change = random.uniform(-mutation_rate, mutation_rate)
    new_value = individual + change
    # Keep it within bounds
    new_value = max(min(new_value, upper_bound), lower_bound)
    return new_value

# Main Clonal Selection Algorithm
def clonal_selection(generations=10, pop_size=5, clones_per_ind=3, mutation_rate=0.5):
    lower = -5
    upper = 5

    #population = create_population(pop_size, lower, upper)
    #print(population)
    population = [0.45,-1.5,3.99,-0.22,4.00]
    print(population)

    for generation in range(generations):
        # Sort population by fitness (lower is better)
        population.sort(key=fitness)

        # Keep the best individuals (e.g., top 3)
        best = population[:3]

        # Clone and mutate
        clones = clone_individuals(best, clones_per_ind)
        mutated_clones = []
        for c in clones:
            mutated = mutate(c, mutation_rate, lower, upper)
            mutated_clones.append(mutated)

        # Combine original best with mutated clones
        population = best + mutated_clones

        # Keep only top pop_size individuals
        population.sort(key=fitness)
        population = population[:pop_size]

        print(f"Generation {generation+1}: Best = {population[0]:.4f}, Fitness = {fitness(population[0]):.4f}")

    return population[0]

# Run the algorithm
best_solution = clonal_selection()
print("\nBest solution found:", best_solution)
