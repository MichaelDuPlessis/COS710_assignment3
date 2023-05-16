from array import array
from typing import Callable, Dict, List
import random as rand

# defining genome
Genome = array

# these functins reprsent the terminal and none terminal nodes of the grammer and are used to perform calculations
# genomes is the genome and pos is the position in the genome

# weird python hack I am doing because this sad programming language doesn't hoist
class Mapper(object):
    def __call__(self, genome: Genome, data: Dict[str, str]) -> float:
        self.pos = 0
        self.genome = genome
        self.data = data
        self.chromosomes = 0
        return self.expr()
        
    # terminals
    def constant(self) -> float:
        if self.pos // len(self.genome)>= 5:
            return 999
        const = Mapper.CONSTANTS[self.genome[self.position()] % len(Mapper.CONSTANTS)]
        self.pos += 1
        return const
   
    def parameter(self) -> float:
        # checking if too many wraps occured
        if self.pos // len(self.genome) >= 5:
            return 999
        param = Mapper.PARAMS[self.genome[self.position()] % len(Mapper.PARAMS)]
        self.pos += 1
        return float(self.data[param])
    
    # non terminals
    def add(self) -> float:
        return self.expr() + self.expr()
    
    def sub(self) -> float:
        return self.expr() - self.expr()
    
    def div(self) -> float:
        try:
            return self.expr() / self.expr()
        except:
            return 0
    
    def mul(self) -> float:
        return self.expr() * self.expr()
    
    def expr(self) -> float:
        # checking if too many wraps occurred
        if self.pos // len(self.genome) >= 5:
            return 999
        return self.production(Mapper.PRODUCTIONS)(self)

    # helper methods
    # used to choose the production rule
    def production(self, productions: List[Callable[['Mapper'], float]]) -> Callable[['Mapper'], float]:
        production = productions[self.genome[self.position()] % len(productions)]
        self.pos += 1
        return production

    # used to prevent out of bounds
    def position(self) -> int:
        return self.pos % len(self.genome)

    # static members
    PRODUCTIONS = [
        add,
        sub,
        div,
        mul,
        constant,
        parameter,
    ]
    
    CONSTANTS = [
        -2,
        -1,
        2
    ]

    PARAMS = [
        'Distance',
        'PLong',
        'PLatd',
        'DLong',
        'DLatd',
        'Haversine',
        'Pmonth',
        'Pday',
        'Phour',
        'Pmin',
        'PDweek',
        'Dmonth',
        'Dday',
        'Dhour',
        'Dmin',
        'DDweek',
        'Temp',
        'Precip',
        'Wind',
        'Humid',
        'Solar',
        'Snow',
        'GroundTemp',
        'Dust'
    ]
