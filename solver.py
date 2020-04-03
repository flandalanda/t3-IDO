#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Clinic = namedtuple("Clinic", 'index cost regions')


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
    
def density_cover(regions_count, clinics_count, clinics):

    # We begin with no clinics built and no regions covered
    clinics_built = [0]*clinics_count
    regions_covered = set()
    
    # We order the clinics based on their cost per region ratio in ascending order
    clinics.sort(key = lambda x: x.cost/len(x.regions))

    # While there are regions left to cover
    while len(regions_covered) != regions_count:
        #print("--------------Nueva lista ordernada--------------------")
        #print(clinics)


        # We build the most cost efficient clinic
        build = clinics.pop(0)
        clinics_built[build.index] = build.cost
        # We update the regions covered
        regions_covered.update(build.regions)

        # We update the uncovered regions for other clinics
        discard = False
        for clinic in clinics:
            clinic.regions.difference_update(build.regions)
            
            # if there are clinics that service no new regions we eliminate them
            if not discard:
                discard = len(clinic.regions) == 0
            #print(clinic)
            #print(discard)

        if discard:
            clinics = [clinic for clinic in clinics if len(clinic.regions) != 0]
        
        # We resort the list of clinics with the new cost per region ratio
        clinics.sort(key = lambda x: x.cost/len(x.regions))

        #print("Fin de ciclo \n\n\n")

    total_costs = sum(clinics_built)

    output_data = str(total_costs) + '\n'
    output_data += ' '.join(map(str, clinics_built))

    return output_data


## TODO: Modifica este diccionario
algorithms = {
    'trivial_covering': trivial_cover,
    'dc': density_cover
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
