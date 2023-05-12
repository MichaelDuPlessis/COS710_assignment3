from typing import Dict, List
import csv
from itertools import islice

def read_csv(filename: str, amount: int) -> List[Dict[str, str]]:
    with open(filename) as file:
        data = csv.DictReader(file)
        return list(islice(data, amount))
