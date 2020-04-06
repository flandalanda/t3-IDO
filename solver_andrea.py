#!/usr/bin/python
# -*- coding: utf-8 -*-
import functools
from collections import namedtuple
from operator import attrgetter, itemgetter

Clinic = namedtuple("Clinic", ['index', 'cost', 'regions'])

#------------------------------------------------------------
#
#                  AUX FUNCTIONS
#
#------------------------------------------------------------
def is_feasible(solution, regions_count):
    covered = set()

    for clinic in solution['clinics']:
        covered = covered.union(clinic.regions)

    return len(clinic) == regions_count

def parse_solution(solution, clinics_count):
    clinics_built = [0]*clinics_count

    for clinic in solution['clinics']:
        clinics_built[clinic.index] = 1

    output_data = str(solution['cost']) + '\n'
    output_data += ' '.join(map(str, clinics_built))

    return output_data

#------------------------------------------------------------
#
#                  OPTIMIZATION FUNCTIONS
#
#------------------------------------------------------------
def greedy_cover(regions_count, clinics_count, clinics, key = None, reverse = False):
    clinics_built = []
    total_cost = 0
    covered = set()

    if key:
        # Sort items in a particular order
        clinics = sorted(clinics, key = key, reverse = reverse)

    for clinic in clinics:
        clinics_built.append(clinic)
        covered |= clinic.regions

        total_cost += clinic.cost

        if len(covered) >= regions_count:
            break # We are done, we covered all the regions


    solution = {
        'clinics': clinics_built,
        'cost': total_cost
    }

    return solution

#------------------------------------------------------------
#
#                  PARTIAL FUNCTIONS
#
#------------------------------------------------------------
cost_greedy = functools.partial(greedy_cover, key = attrgetter('cost'))
coverage_greedy = functools.partial(greedy_cover, key = lambda x: len(x.regions), reverse = True)
density_greedy = functools.partial(greedy_cover, key = lambda x: x.cost/len(x.regions) if len(x.regions) > 0 else 0, reverse = True)

inverse_cost_greedy = functools.partial(greedy_cover, key = attrgetter('cost'), reverse = True)
inverse_coverage_greedy = functools.partial(greedy_cover, key = lambda x: len(x.regions))

## TODO: Modifica este diccionario
algorithms = {
    'trivial_cover': greedy_cover,
    'cost_greedy': cost_greedy,
    'coverage_greedy': coverage_greedy,
    'density_greedy': density_greedy,
    'inverse_cost_greedy': inverse_cost_greedy,
    'inverse_coverage_greedy': inverse_coverage_greedy
}

def solve_it(input_data, algorithm = greedy_cover):

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    regions_count = int(firstLine[0])
    clinics_count = int(firstLine[1])

    clinics = []

    for i in range(1, clinics_count+1):
        parts = lines[i].split()
        regions = set(map(int,parts[1:]))
        regions.discard(-1)
        clinics.append(Clinic(i-1, float(parts[0]), regions))

    output_data = algorithm(regions_count, clinics_count, clinics)

    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        file_location = sys.argv[1].strip()
        algorithm = algorithms[sys.argv[2].strip()]

        print(f"Ejecutando el algoritmo {algorithm} en {file_location}")
        
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data, algorithm))
    else:
        print("""Este script requiere dos argumentos: \n"""
              """El archivo con los datos del problema y el nombre del algoritmo que diseñaste.\n"""
              """i.e. python solver.py ./data/sc_6_1 trivial_cover""")
