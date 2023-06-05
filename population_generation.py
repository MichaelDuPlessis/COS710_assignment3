# This file contains code to generate the initial population

from array import array
from copy import deepcopy
import math
from typing import Callable, Iterable, List, Tuple
import random as rand
from grammer import Genome
from genetic_operator import mutate_chormosomes, two_point_crossover, mutate
from fitness import tournament, tournament_precomputed

# create an individual
# returns an array of unsigned 1 byte ints
def individual(max_len: int, min_len: int = 2) -> Genome:
    return array('B', [rand.randrange(256) for _ in range(rand.randint(min_len, max_len))])

# This function generates the initial population
# returns an array of arrays
def initial(size: int, max_len: int, min_len: int = 2) -> List[Genome]:
    return [individual(max_len, min_len) for _ in range(size)]

# generate a new population
def generate_next_population_precomputed(population: List[Tuple[float, Genome]], min_len: int, max_len: int, tournament_size: int, weights: Tuple[float, float, float],
                             crossover: Callable[[Genome, Genome, int], Tuple[Genome, Genome]]=two_point_crossover,
                             mutation: Callable[[Genome, int, int], Genome]=mutate) -> List[Genome]:
    pop_len = len(population)
    # crossover
    new_population = [genome for genome in crossover(tournament_precomputed(population, tournament_size), tournament_precomputed(population, max_len), max_len) for _ in range(math.floor(pop_len * weights[0]) // 2)]
    # mutation
    new_population.extend([mutation(tournament_precomputed(population, tournament_size), min_len, max_len) for _ in range(math.floor(pop_len * weights[1]))])
    # reproduction
    new_population.extend([deepcopy(tournament_precomputed(population, tournament_size)) for _ in range(math.floor(pop_len * weights[2]))])
    # filling in missing
    current_len = len(new_population)
    new_population.extend([deepcopy(tournament_precomputed(population, tournament_size)) for _ in range(current_len, pop_len)])

    return new_population

def generate_next_population(population: List[Genome], data: Iterable, min_len: int, max_len: int, tournament_size: int, weights: Tuple[float, float, float],
                             crossover: Callable[[Genome, Genome, int], Tuple[Genome, Genome]]=two_point_crossover,
                             mutation: Callable[[Genome, int, int], Genome]=mutate) -> List[Genome]:
    pop_len = len(population)
    cache = {}
    # crossover
    new_population = [genome for genome in crossover(tournament(population, data, tournament_size, cache), tournament(population, data, tournament_size, cache), max_len) for _ in range(math.floor(pop_len * weights[0]) // 2)]
    # mutation
    new_population.extend([mutation(tournament(population, data, tournament_size, cache), min_len, max_len) for _ in range(math.floor(pop_len * weights[1]))])
    # reproduction
    new_population.extend([deepcopy(tournament(population, data, tournament_size, cache)) for _ in range(math.floor(pop_len * weights[2]))])
    # filling in missing
    current_len = len(new_population)
    new_population.extend([deepcopy(tournament(population, data, tournament_size, cache)) for _ in range(current_len, pop_len)])

    return new_population
