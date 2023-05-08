# This file contains code to generate the initial population

from array import array
from typing import List
import random as rand
from grammer import GRAMMER_LEN

# create an individual
# returns an array of unsigned 1 byte ints
def individual(max_len: int) -> array:
    return array('B', [rand.randint(0, GRAMMER_LEN) for _ in range(rand.randint(1, max_len))])

# This function generates the initial population
# returns an array of arrays
def initial(size: int, max_len: int) -> List[array]:
    return [individual(max_len) for _ in range(size)]
