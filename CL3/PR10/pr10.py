import numpy as np
import random

dm = np.array([
    [0,10,20,30],
    [10,0,20,30],
    [10,20,0,30],
    [10,20,30,0]
])
num_cities = 4
num_ants = 10
num_iterations = 10
heuristic_const = 0.5
visibility = np.zeros((num_cities,num_cities))
for i in range(0,num_cities):
    for j in range(0,num_cities):
        if i!=j:
            visibility[i][j] = 1/dm[i][j]

for _ in range(0,num_iterations):
    ant_route = []
    for _ in range(0,num_ants):
        current_city = random.randint(0,num_cities-1)
        visited = [current_city]
        route = [current_city]
        while(len(visited)<num_cities):
            prob = []
            for city in range(0,num_cities):
                if city not in visited:
                    visibility_value = visibility[current_city][city]
                    probability = (visibility_value ** heuristic_const) 
                    prob.append((city,probability))
            prob.sort(key = lambda x:x[1]  ,reverse=True)

            selected_city = prob[0][0]
            route.append(selected_city)
            visited.append(selected_city)
            current_city = selected_city
        
        ant_route.append(route)
    


def route_distance(route):
    x = 0
    for i in range(0,num_cities):
        x = x + dm[route[i]][route[(i + 1) % num_cities]]
    return x 

best_route = min(ant_route, key=route_distance)
shortest_distance = route_distance(best_route)

print("Best route:", best_route)
print("Shortest distance:", shortest_distance)


