from typing import Dict, List, Tuple
from population_generation import initial, generate_next_population
from fitness import population_raw_fitness

# this function is used to run the algorithm
def run(pop_size: int, max_len: int, generations: int, runs: int, weights: Tuple[float, float, float], data: List[Dict[str, float]]):
    # creating object to hold information of runs
    session = {
        'pop_size': pop_size,
        'max_len': max_len,
        'generations': generations,
        'runs': runs,
        'weights': {
            'crossover': weights[0],
            'mutation': weights[1],
            'reproduction': weights[2],
        }
        # runs are added as new objects
    } 

    for r in range(runs):
        population = initial(pop_size, max_len)
        fitness = population_raw_fitness(population, data)

        for g in range(generations):
            population = generate_next_population(zip(fitness, population), max_len, weights)
            fitness = population_raw_fitness(population, data)

if __name__ == "__main__":
    pass
