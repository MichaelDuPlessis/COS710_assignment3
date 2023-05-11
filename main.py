from typing import Dict, List, Tuple
from population_generation import initial, generate_next_population
from fitness import population_raw_fitness
from performance import run_all_measures

# this function is used to run the algorithm
def run(pop_size: int, max_len: int, generations: int, runs: int, weights: Tuple[float, float, float], training_data: List[Dict[str, float]], testing_data: List[Dict[str, float]]):
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
        print(f"Starting run {r}")

        population = initial(pop_size, max_len)
        fitness = population_raw_fitness(population, training_data)
        fp = zip(fitness, population)
        best = min(fp, key=lambda x: x[0])

        for g in range(generations):
            population = generate_next_population(fp, max_len, weights)
            fitness = population_raw_fitness(population, training_data)
            fp = zip(fitness, population)
            best = min(fp, key=lambda x: x[0])

            print(f"Generation {g} - best: {best[0]}")

        performance_training = run_all_measures(best[1], training_data)
        performance_testing = run_all_measures(best[1], testing_data)

        session[str(r)] = {
            "genome": best[1],
            "raw_fitness": best[0],
            "performance": {
                "training": {
                    "rmse": performance_training[0],
                    "rsquared": performance_training[1],
                    "medae": performance_training[2],
                    "mae": performance_training[3],
                },  
                "testing": {
                    "rmse": performance_testing[0],
                    "rsquared": performance_testing[1],
                    "medae": performance_testing[2],
                    "mae": performance_testing[3],
                },  
            }
        }

if __name__ == "__main__":
    pass
