from typing import Iterable, List, Tuple
from grammer import Mapper, Genome
import random as rand

# calculate the fitness for a genome
def raw_fitness(genome: Genome, data: Iterable) -> float:
    mapper = Mapper()
    return sum([abs(mapper(genome, d) - float(d['Duration'])) for d in data])

# calculate the entire populaitons fitness
def population_raw_fitness(population: List[Genome], data: Iterable) -> List[float]:
    return [raw_fitness(p, data) for p in population]

# tournament selection
def tournament(population: List[Genome], data: Iterable, size: int) -> Genome:
    participants = rand.choices(population, k=size)
    return min(participants, key=lambda p: raw_fitness(p, data))

# tournament selection if the fitness is already calculated
def tournament_precomputed(population: List[Tuple[float, Genome]], size: int) -> Genome:
    participants = rand.choices(population, k=size)
    return min(participants, key=lambda t: t[0])[1]
