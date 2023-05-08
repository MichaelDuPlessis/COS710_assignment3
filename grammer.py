from array import array
from typing import Callable, Dict, List
import random as rand

GRAMMER_LEN = 3

# these functins reprsent the terminal and none terminal nodes of the grammer and are used to perform calculations
# genomes is the genome and pos is the position in the genome

# weird python hack I am doing because this sad programming language doesn't hoist
class Run(object):
    def __call__(self, genome: array[int], data: Dict[str, float]) -> float:
        self.pos = 0
        self.genome = genome
        self.data = data
        return self.expr()
        
    # terminals
    def constant(self) -> float:
        return rand.choice([-2, -1, 2]) 
   
    def parameter(self) -> float:
        return self.data[rand.choice(Run.PARAMS)]
    
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
        return self.production(Run.EXPR)(self)

    # helper methods
    # used to choose the production rule
    def production(self, productions: List[Callable[['Run'], float]]) -> Callable[['Run'], float]:
        production = productions[self.genome[self.pos % len(productions)]]
        self.pos = (self.pos + 1) % len(self.genome)
        return production

    EXPR = [
        add,
        sub,
        div,
        mul,
        constant,
        parameter,
    ]

    TERMINAL = [
        constant,
        parameter,
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
