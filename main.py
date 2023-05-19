from typing import Dict, List, Tuple
import random as rand
from data import read_csv
from population_generation import initial, generate_next_population
from fitness import population_raw_fitness
from performance import run_all_measures
from datetime import datetime
import os
import json
import argparse
import sys

# this function is used to run the algorithm
def run(pop_size: int, max_len: int, generations: int, runs: int, tournament_size: int, weights: Tuple[float, float, float],
        training_data: List[Dict[str, str]], testing_data: List[Dict[str, str]], save: bool):
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
        seed = rand.randrange(sys.maxsize)
        print(f'The seed for the run is {seed}')
        rand.seed(seed)

        population = initial(pop_size, max_len)
        fitness = population_raw_fitness(population, training_data)
        fp = list(zip(fitness, population))
        best = min(fp, key=lambda x: x[0])
        print(f"Generation 0 - best: {best[0]}")
#
        for g in range(generations - 1):
            population = generate_next_population(fp, max_len, tournament_size, weights)
            fitness = population_raw_fitness(population, training_data)
            fp = list(zip(fitness, population))
            best = min(fp, key=lambda x: x[0])

            print(f"Generation {g + 1} - best: {best[0]}")

        performance_training = run_all_measures(best[1], training_data)
        performance_testing = run_all_measures(best[1], testing_data)

        session[str(r)] = {
            "genome": best[1],
            "seed": seed,
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
    if save:
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H#%M#%S.json")
        filepath = os.sep.join(['.', 'runs', f'{dt_string}'])
        with open(filepath, 'w') as file:
            json.dump(session, file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', help='Whether the output of the runs should be saved to a file. default true', action='store_true')
    parser.add_argument('-p', '--pop', help='The size of the population. default 100', default=100, type=int)
    parser.add_argument('-e', '--seed', help='The seed to be used in every run', type=int)
    parser.add_argument('-r', '--runs', help='The number of runs to perform. default 10', default=10, type=int)
    parser.add_argument('-l', '--len', help='The max number of chromosomes for each genome. default 5', default=5, type=int)
    parser.add_argument('-g', '--generations', help='The max number of generations of each run. default 20', default=20, type=int)
    parser.add_argument('-t', '--tournament', help='The size of the tournament for tournament selection. default 4', default=4, type=int)
    parser.add_argument('-w', '--weights', help='The crossover, mutation and reproduction chances as a comma seperated list e.g. 0.4,0.3,0.3. default "0.5,0.5,0"', default='0.5,0.5,0')
    parser.add_argument('-i', '--train', help='The amount from the data set to be trained on. default 100000', default=100_000, type=int)
    parser.add_argument('-j', '--test', help='The amount from the data set to be tested on. default 25000', default=25_000, type=int)
    default_path = os.sep.join(['.', 'data', 'For_modeling.csv'])
    parser.add_argument('-P', '--path', help=f'The path to the data set. default {default_path}', default=default_path, type=str)
    args = parser.parse_args()

    weights = tuple([float(w) for w in args.weights.split(',')])

    data = read_csv(args.path, args.train + args.test)


    run(pop_size=args.pop, max_len=args.len, generations=args.generations, runs=args.runs, tournament_size=args.tournament, weights=weights,
        training_data=data[:args.train], testing_data=data[args.train:], save=args.save)

