from typing import Dict, List, Tuple
from grammer import Mapper
import random as rand
from data import read_csv
from population_generation import initial, generate_next_population
from fitness import population_raw_fitness
from performance import run_all_measures

# this function is used to run the algorithm
def run(pop_size: int, max_len: int, generations: int, runs: int, tournament_size: int, weights: Tuple[float, float, float], training_data: List[Dict[str, str]], testing_data: List[Dict[str, str]]):
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
        fp = list(zip(fitness, population))
        best = min(fp, key=lambda x: x[0])
        print(best)
        # print(f"Generation 0 - best: {best[0]}")

        for g in range(generations - 1):
            population = generate_next_population(fp, max_len, tournament_size, weights)
            fitness = population_raw_fitness(population, training_data)
            fp = list(zip(fitness, population))
            best = min(fp, key=lambda x: x[0])

            print(best)
            # print(f"Generation {g + 1} - best: {best[0]}")

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


    print(session)

if __name__ == "__main__":
    data = read_csv('./data/For_modeling.csv', 100_000)
    run(50, 10, 30, 1, 4, (0.3, 0.7, 0), data[:75_000], data[75_000:])
