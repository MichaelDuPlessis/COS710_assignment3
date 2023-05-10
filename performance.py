# this module is used to determine how could a tree is

import numpy as np
from typing import List, Dict, Tuple
from grammer import Genome, Run

def rmse(predictions, targets) -> float:
    mse = np.mean((predictions - targets)**2)
    rmse = np.sqrt(mse)
    
    return rmse

def r_squared(predictions, targets) -> float:
    ss_residual = np.sum((targets - predictions)**2)
    ss_total = np.sum((targets - np.mean(targets))**2)
    r2 = 1 - (ss_residual / ss_total)

    return r2


def median_absolute_error(predictions, targets) -> float:
    mae = np.median(np.abs(predictions - targets))

    return mae

def mean_absolute_error(predictions, targets) -> float:
    mae = np.mean(np.abs(predictions - targets))
    
    return mae

# runs all the performance measures for a given tree and data set
# frequires the tree/program and data set
def run_all_measures(genome: Genome, data: List[Dict[str, float]]) -> Tuple[float, float, float, float]:
    run = Run()
    prediction_target = [(run(genome, d), float(d['Duration'])) for d in data]
    predictions, targets = zip(*prediction_target)
    predictions = np.array(predictions)
    targets = np.array(targets)

    return rmse(predictions, targets), r_squared(predictions, targets), median_absolute_error(predictions, targets), mean_absolute_error(predictions, targets)
