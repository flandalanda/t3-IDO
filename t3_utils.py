
import sys
def total_cost(clinics, clinics_built):
    return sum([clinic.cost*clinics_built[clinic.index] for clinic in clinics if clinic.index < len(clinics_built)])

def is_sol(regions_count, clinics, sol):
    covered = set()
    for clinic in clinics:
        if sol[clinic.index] == 1:
            covered |= set(clinic.regions)
    return len(covered) == regions_count

def getLogger(debug):
    def log_s(string):
        if debug:
            sys.stdout.write("\r" + string)
            sys.stdout.flush()
    def log(*args):
        if debug:
            for arg in args:
                print(arg)
    return log_s, log
    
def dict_union(d1, d2):
    """ Simplifica la unión de dos diccionarios """
    d = dict(d1)
    d.update(d2)
    return d

def output_string(total_costs, clinics_built):
    # Convertimos la solución en el formato esperado
    output_data = str(total_costs) + '\n'
    output_data += ' '.join(map(str, clinics_built))

    return output_data
