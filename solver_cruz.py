#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import inf
from t3_utils import * 
from search import *
from collections import namedtuple
from functools import partial
Clinic = namedtuple("Clinic", 'index cost regions')
log_s, log = getLogger(False)


def trivial_cover(regions_count, clinics_count, clinics):
    """ picks and sets one-by-one until all the regions are covered """
    clinics_built = [0]*clinics_count
    coverted = set()

    for clinic in clinics:
        clinics_built[clinic.index] = 1
        coverted |= set(clinic.regions)
        if len(coverted) >= regions_count:
            break # We are done, we cover all the regions

    # Calculamos el costo total de construcción
    total_costs = sum([clinic.cost*clinics_built[clinic.index] for clinic in clinics])
    
    # Convertimos la solución en el formato esperado
    output_data = str(total_costs) + '\n'
    output_data += ' '.join(map(str, clinics_built))

    return output_data

def greedy_density(regions_count, clinics_count, clinics):
    """ picks and sets one-by-one until all the regions are covered """
    clinics_built = [0]*clinics_count
    coverted = set()
    clinics.sort(key=lambda clinic: clinic.cost/len(clinic.regions))
    for clinic in clinics:
        clinics_built[clinic.index] = 1
        coverted |= set(clinic.regions)
        if len(coverted) >= regions_count:
            break # We are done, we cover all the regions

    # Calculamos el costo total de construcción
    total_costs = sum([clinic.cost*clinics_built[clinic.index] for clinic in clinics])
    
    # Convertimos la solución en el formato esperado
    output_data = str(total_costs) + '\n'
    output_data += ' '.join(map(str, clinics_built))

    return output_data

def greedy(regions_count, clinics_count, clinics, key):
    """ picks and sets one-by-one until all the regions are covered """
    clinics_built = [0]*clinics_count
    coverted = set()
    clinics.sort(key=key)
    for clinic in clinics:
        clinics_built[clinic.index] = 1
        coverted |= set(clinic.regions)
        if len(coverted) >= regions_count:
            break # We are done, we cover all the regions

    # Calculamos el costo total de construcción
    total_costs = sum([clinic.cost*clinics_built[clinic.index] for clinic in clinics])
    
    # Convertimos la solución en el formato esperado
    output_data = str(total_costs) + '\n'
    output_data += ' '.join(map(str, clinics_built))

    return output_data

def dfs(regions_count, clinics_count, clinics):
    clinics_built = [0]*clinics_count
    coverted = set()
    clinics.sort(key=lambda clinic: clinic.cost/len(clinic.regions))
    clinics_regions = [ clinic.regions for clinic in clinics ]

    def goal(nodo):
        covered = set()
        for i in range(len(nodo)):
            if nodo[i] == 1:
                covered |= set(clinics_regions[i])
        return len(covered) >= regions_count
    
    def expande(nodo):
        if len(nodo) < len(clinics):
            return [ nodo + [0], nodo + [1]]
        else:
            return []
    
    def check_point(nodo, frontera):
        clinicas_asignadas = [n for n in nodo if n==1]
        log_s(f"Costo minimo alcanzado: {min_cost}. Clinicas asignadas: {len(clinicas_asignadas)} frontera: {len(frontera)}")
    min_cost = inf
    for sol in generalSearch(goal, expande, start=[], check_point= check_point):
        cost = total_cost(clinics, sol[0])
        if cost < min_cost :
            min_cost = cost

def regions(regions_count, clinics_count, clinics):
    region_dic = { x: [] for x in range(regions_count)}
    clinics_built = [0]*clinics_count
    for clinic in clinics:
        for r in clinic.regions:
            if r >= 0:
                region_dic[r].append(clinic)
    
    for r in range(regions_count):
        region_dic[r].sort(key=lambda clinic: clinic.cost/len(clinic.regions))
    covered = set()
    def priority( clinic ):
        diff = clinic.regions - covered
        return clinic.cost/len(diff) if len(diff) > 0 else inf
    ordered_regions = list(range(regions_count))
    ordered_regions.sort(key = lambda r : len(region_dic[r]))
    for r in ordered_regions:
        if r not in covered:
            region_dic[r].sort(key=priority)
            clinic = region_dic[r].pop(0)
            clinics_built[clinic.index] = 1
            covered |= clinic.regions
    #log('Es sol:', is_sol(regions_count,clinics, clinics_built))
    #log(total_cost(clinics, clinics_built))

    return output_string(total_cost(clinics, clinics_built), clinics_built)

def branch_and_bound(regions_count, clinics_count, clinics):
    Nodo = namedtuple("Nodo", 'regions covered')
    log('Num of regions:', regions_count)
    region_dic = { x: [] for x in range(regions_count)}
    total_regions = set(range(regions_count))
    clinics_built = [0]*clinics_count
    clinic_dic = { clinic.index : clinic for clinic in clinics}
    for clinic in clinics:
        for r in clinic.regions:
            region_dic[r].append(clinic)
    
    for r in range(regions_count):
        region_dic[r].sort(key=lambda clinic: clinic.cost/len(clinic.regions))
    min_costo_region = { r: c[0].cost/len(c[0].regions) for r, c in region_dic.items()}
    covered = set()
    def priority( clinic, covered ):
        diff = clinic.regions - covered
        return clinic.cost/len(diff) if len(diff) > 0 else inf
    ordered_regions = list(range(regions_count))
    ordered_regions.sort(key = lambda r : len(region_dic[r]))
    def goal(nodo):
        return len(nodo.regions) == regions_count
    def est_cost(nodo):
        covered_regions = set(nodo.covered.keys())
        missing_regions = total_regions - covered_regions
        costo = 0
        for r in missing_regions:
            costo+= min_costo_region[r]
        for c in set(nodo.regions.values()):
            costo+=clinic_dic[c].cost
        return costo
    pruned = 0
    min_costo = inf
    def expande(nodo):
        nonlocal pruned
        vecinos = []
        #log('entra expande')
        if len(nodo.regions) < regions_count :
            region = ordered_regions[len(nodo.regions)]
            #log('region', region)
            if region in nodo.covered.keys():
                vecinos.append(Nodo(dict_union(nodo.regions, {region: nodo.covered[region]}), dict(nodo.covered)))
            else:
                region_dic[region].sort(key=partial(priority, covered=set(list(nodo.covered.keys()))), reverse=True)
                for clinic in region_dic[region]:
                    covered = { r: clinic.index for r in clinic.regions}
                    vecino = Nodo(dict_union(nodo.regions,{ region:clinic.index}), dict_union(covered,nodo.covered ))
                    #vecinos.append(vecino)
                    if est_cost(vecino) < min_costo:
                        vecinos.append(vecino)
                    else:
                        pruned= pruned + 1
        return vecinos
    def check_point(nodo, frontera):
        log_s(f"Costo minimo: {min_costo}. Regiones cubiertas: {len(nodo.regions)} frontera: {len(frontera)}. Pruned: {pruned}.")
    for sol in generalSearch(goal, expande, start=Nodo({},{}), check_point= check_point):
        nodo = sol[0]
        clinics_built = [0]*clinics_count
        for r, c in nodo.regions.items():
            clinics_built[c] = 1
        cost = total_cost(clinics, clinics_built)
        log_s('\t'*10 + f'Costo:{cost}')
        if cost < min_costo :
            min_costo = cost
    log('')


def prueba( regions_count, clinics_count, clinics):
    print('Regions_count: ')
    print(regions_count)
    print('Clinics_count:')
    print(clinics_count)
    print('Clinics: ')
    print(clinics)

## TODO: Modifica este diccionario
algorithms = {
    'trivial_cover': trivial_cover,
    'p': prueba,
    'greedy_density':greedy_density,
    'dfs':dfs,
    'r': regions,
    'bb': branch_and_bound
    }

def solve_it(input_data, algorithm=trivial_cover):

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    regions_count = int(firstLine[0])
    clinics_count = int(firstLine[1])

    clinics = []

    for i in range(1, clinics_count+1):
        parts = lines[i].split()
        clinics.append(Clinic(i-1, float(parts[0]),set(map(lambda x: int(x), parts[1:]))))
        
    #print(clinics)
    #print('\n\n\n\n\n\n')

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
