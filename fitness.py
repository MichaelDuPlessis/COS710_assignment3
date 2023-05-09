from typing import Iterable, List, Tuple
from grammer import Run, Genome
import random as rand

# calculate the fitness for a genome
def raw_fitness(genome: Genome, data: Iterable) -> float:
    run = Run()
    return sum([abs(run(genome, d) - d['Duration']) for d in data])

# tournament selection
def tournament(population: List[Genome], data: Iterable, size: int) -> Genome:
    participants = rand.choices(population, k=size)
    return min(participants, key=lambda p: raw_fitness(p, data))

# tournament selection if the fitness is already calculated
def tournament_precomputed(population: List[Tuple[float, Genome]], size: int) -> Genome:
    participants = rand.choices(population, k=size)
    return min(participants, key=lambda t: t[0])[1]
