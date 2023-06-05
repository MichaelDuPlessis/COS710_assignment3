from typing import Iterable, List, Tuple, Dict
from grammer import Mapper, Genome
import random as rand

# calculate the fitness for a genome
def raw_fitness(genome: Genome, data: Iterable, cache: Dict[Genome, float]) -> float:
    mapper = Mapper()
    genome = tuple(genome)
    if genome in cache:
        return cache[genome]
    else:
        res = sum([abs(mapper(genome, d) - float(d['Duration'])) for d in data])
        cache[genome] = res
        return res

# calculate the entire populaitons fitness
def population_raw_fitness(population: List[Genome], data: Iterable) -> List[float]:
    cache = {}
    return [raw_fitness(p, data, cache) for p in population]

# tournament selection
def tournament(population: List[Genome], data: Iterable, size: int, cache: Dict[Genome, float]) -> Genome:
    participants = rand.sample(population, size)
    return min(participants, key=lambda p: raw_fitness(p, data, cache))

# tournament selection if the fitness is already calculated
def tournament_precomputed(population: List[Tuple[float, Genome]], size: int) -> Genome:
    participants = rand.sample(population, size)
    return min(participants, key=lambda t: t[0])[1]
