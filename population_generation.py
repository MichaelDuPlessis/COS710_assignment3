# This file contains code to generate the initial population

from array import array
from typing import List
import random as rand
from grammer import Genome

# create an individual
# returns an array of unsigned 1 byte ints
def individual(max_len: int) -> Genome:
    return array('B', [rand.randint(0, 255) for _ in range(rand.randint(1, max_len))])

# This function generates the initial population
# returns an array of arrays
def initial(size: int, max_len: int) -> List[Genome]:
    return [individual(max_len) for _ in range(size)]
