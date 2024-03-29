# this file is for the different genetic operators that can be applied.

from grammer import Genome
from random import randrange, randint, sample
from copy import deepcopy
from array import array
from itertools import chain, islice
from typing import Tuple

# this is the mutation operator it randomly selects a chromosome and change the number in it 
def mutate_chormosome(genome: Genome, _min_len: int, _max_len: int) -> Genome:
    genome = deepcopy(genome)
    genome[randrange(len(genome))] = randrange(256)
    return genome

# this is the mutation operator it randomly selects a chromosome and changes it and the following chromosomea 
def mutate_chormosomes(genome: Genome, _: int, max_len: int) -> Genome:
    chromosome = randrange(len(genome))
    genome = array('B', [genome[i] if i <= chromosome else randrange(256) for i in range(0, randint(chromosome + 1, max_len))])
    return genome

def mutate(genome: Genome, _min_len: int, _max_len: int) -> Genome:
    mutations = randrange(len(genome))
    codons = sample(range(len(genome)), mutations)

    genome = deepcopy(genome)
    for c in codons:
        genome[c] = randrange(256)

    return genome

def destructive_crossover(genome1: Genome, genome2: Genome, max_len: int) -> Tuple[Genome, Genome]:
    point1 = randrange(len(genome1))
    point2 = randrange(len(genome2))

    return (
        array('B', islice(chain.from_iterable([
            genome1[:point1],
            genome2[point2:]
        ]), min(point1 + len(genome2) - point2, max_len))),
        array('B', islice(chain.from_iterable([
            genome2[:point2],
            genome1[point1:]
        ]), min(point2 + len(genome1) - point1, max_len)))
    )    

# two point crossover
def two_point_crossover(genome1: Genome, genome2: Genome, _: int) -> Tuple[Genome, Genome]:
    genome1, genome2 = (genome2, genome1) if len(genome2) < len(genome1) else (genome1, genome2)

    point1 = randint(0, len(genome1) - 1)
    point2 = randint(0, len(genome1) - 1)

    # Ensure point1 is less than point2
    point1, point2 = min(point1, point2), max(point1, point2)

    return (
        array('B', genome1[:point1] + genome2[point1:point2] + genome1[point2:]),
        array('B', genome2[:point1] + genome1[point1:point2] + genome2[point2:])
    )
