# This file contains code to generate the initial population

from array import array
from copy import deepcopy
import math
from typing import Callable, Iterable, List, Tuple
import random as rand
from grammer import Genome
from genetic_operator import destructive_crossover, mutate_chormosomes
from fitness import tournament_precomputed

# create an individual
# returns an array of unsigned 1 byte ints
def individual(max_len: int) -> Genome:
    return array('B', [rand.randint(0, 255) for _ in range(rand.randint(1, max_len))])

# This function generates the initial population
# returns an array of arrays
def initial(size: int, max_len: int) -> List[Genome]:
    return [individual(max_len) for _ in range(size)]

# generate a new population
def generate_next_population(population: List[Tuple[float, Genome]], max_len: int, weights: Tuple[float, float, float],
                             crossover: Callable[[Genome, Genome, int], Tuple[Genome, Genome]]=destructive_crossover,
                             mutation: Callable[[Genome, int], Genome]=mutate_chormosomes) -> List[Genome]:
    pop_len = len(population)
    # crossover
    new_population = [genome for genome in crossover(tournament_precomputed(population, max_len), tournament_precomputed(population, max_len), max_len) for _ in range(math.floor(pop_len * weights[0]) // 2)]
    # mutation
    new_population.extend([mutation(tournament_precomputed(population, max_len), max_len) for _ in range(math.floor(pop_len * weights[1]))])
    # reproduction
    new_population.extend([deepcopy(tournament_precomputed(population, max_len)) for _ in range(math.floor(pop_len * weights[2]))])
    # filling in missing
    current_len = len(new_population)
    new_population.extend([deepcopy(tournament_precomputed(population, max_len)) for _ in range(current_len, pop_len)])

    return new_population
