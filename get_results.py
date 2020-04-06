import glob
import time
import logging
import timeout_decorator
from collections import namedtuple

# Global variables
Clinic = namedtuple("Clinic", ['index', 'cost', 'regions'])


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')


# Local imports
from solver import algorithms, parse_solution, is_feasible

def read_file(input_file):
    with open(input_file, 'r') as input_data_file:
        input_data = input_data_file.read()

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

    return regions_count, clinics_count, clinics

    
@timeout_decorator.timeout(10800)
def solve(regions_count, clinics_count, clinics, key = 'trivial_cover'):
    try:
        solution = algorithms[key](regions_count, clinics_count, clinics)
        solution['feasible'] = is_feasible(solution, regions_count)
    except:
        logger.error(f'Error with algorithm: {key}', exc_info=True)
        solution = {'clinics': [], 'cost': float('inf')}
    
    return solution


def get_best_solution(regions_count, clinics_count, clinics,):
    solutions = {}

    for algorithm in algorithms:
        logging.info(f'\t Trying for {algorithm}')

        # time execution
        start_time = time.time()
        start_process_time = time.process_time()

        solution = solve(regions_count, clinics_count, clinics, algorithm)

        elapsed_time = time.time() - start_time  
        elapsed_process_time = time.process_time() - start_process_time

        solution['algorithm'] = algorithm
        solutions[algorithm] = solution

        if solution['cost'] == float('inf'):
            logging.info('\t\tTimeoutError')
        else:
            logging.info('\t\tFinished in {0:.4f}s, process time is {0:.4f}s'.format(elapsed_time, elapsed_process_time))
            logging.info('\t\tCost: {}'.format(solution['cost']))
            logging.info('\t\tFeasible: {}'.format(solution['feasible']))

    best_algorithm = min(solutions, key = lambda x: solutions[x]['cost'])

    best_solution = solutions[best_algorithm]
    """
    if solutions[best_algorithm]['value'] == solutions['knapsack_recursivo']['value']:
        best_solution = solutions['knapsack_recursivo']
    else:
        best_solution = solutions[best_algorithm]
    """
    
    return best_solution

    
if __name__ == '__main__': 

    files = [
        'data/sc_6_1', 
        'data/sc_9_0', 
        'data/sc_15_0', 
        'data/sc_25_0', 
        'data/sc_27_0', 
        'data/sc_45_0', 
        'data/sc_81_0', 
        'data/sc_135_0', 
        'data/sc_157_0', 
        'data/sc_192_0', 
        'data/sc_243_0', 
        'data/sc_330_0', 
        'data/sc_405_0', 
        'data/sc_448_0', 
        'data/sc_450_3', 
        'data/sc_450_4', 
        'data/sc_450_2', 
        'data/sc_450_0', 
        'data/sc_450_1', 
        'data/sc_495_0', 
        'data/sc_500_3', 
        'data/sc_500_4', 
        'data/sc_500_2', 
        'data/sc_500_0', 
        'data/sc_500_1', 
        'data/sc_595_2', 
        'data/sc_595_4', 
        'data/sc_595_3', 
        'data/sc_595_1', 
        'data/sc_595_0', 
        'data/sc_715_0', 
        'data/sc_729_0', 
        'data/sc_760_1', 
        'data/sc_760_0', 
        'data/sc_760_2', 
        'data/sc_760_3', 
        'data/sc_760_4', 
        'data/sc_945_2', 
        'data/sc_945_3', 
        'data/sc_945_4', 
        'data/sc_945_1', 
        'data/sc_945_0', 
        'data/sc_1000_9', 
        'data/sc_1000_0', 
        'data/sc_1000_7', 
        'data/sc_1000_6', 
        'data/sc_1000_1', 
        'data/sc_1000_8', 
        'data/sc_1000_13', 
        'data/sc_1000_14', 
        'data/sc_1000_12', 
        'data/sc_1000_4', 
        'data/sc_1000_3', 
        'data/sc_1000_2', 
        'data/sc_1000_5', 
        'data/sc_1000_10', 
        'data/sc_1000_11', 
        'data/sc_1024_0', 
        'data/sc_1150_0', 
        'data/sc_1150_1', 
        'data/sc_1150_2', 
        'data/sc_1150_3', 
        'data/sc_1150_4', 
        'data/sc_1165_0',
        'data/sc_1215_0', 
        'data/sc_1272_0', 
        'data/sc_1272_1', 
        'data/sc_1272_3',
        'data/sc_1272_4', 
        'data/sc_1272_2', 
        'data/sc_1400_1', 
        'data/sc_1400_0', 
        'data/sc_1400_2', 
        'data/sc_1400_3', 
        'data/sc_1400_4', 
        'data/sc_1534_4', 
        'data/sc_1534_3', 
        'data/sc_1534_2', 
        'data/sc_1534_0', 
        'data/sc_1534_1', 
        'data/sc_2000_2', 
        'data/sc_2000_5', 
        'data/sc_2000_4', 
        'data/sc_2000_3', 
        'data/sc_2000_6', 
        'data/sc_2000_1', 
        'data/sc_2000_8', 
        'data/sc_2000_9', 
        'data/sc_2000_0', 
        'data/sc_2000_7', 
        'data/sc_2187_0', 
        'data/sc_2241_0', 
        'data/sc_2304_0', 
        'data/sc_3000_3', 
        'data/sc_3000_4', 
        'data/sc_3000_5', 
        'data/sc_3000_2', 
        'data/sc_3000_7', 
        'data/sc_3000_0', 
        'data/sc_3000_9', 
        'data/sc_3000_8', 
        'data/sc_3000_1', 
        'data/sc_3000_6', 
        'data/sc_3095_0', 
        'data/sc_3202_0', 
        'data/sc_3314_0', 
        'data/sc_3425_0', 
        'data/sc_3558_0', 
        'data/sc_3701_0', 
        'data/sc_3868_0', 
        'data/sc_4000_4', 
        'data/sc_4000_3', 
        'data/sc_4000_2', 
        'data/sc_4000_5', 
        'data/sc_4000_9', 
        'data/sc_4000_0', 
        'data/sc_4000_7', 
        'data/sc_4000_6', 
        'data/sc_4000_1', 
        'data/sc_4000_8', 
        'data/sc_4025_0', 
        'data/sc_4208_0', 
        'data/sc_4413_0', 
        'data/sc_5000_5', 
        'data/sc_5000_2', 
        'data/sc_5000_3', 
        'data/sc_5000_4', 
        'data/sc_5000_8', 
        'data/sc_5000_1', 
        'data/sc_5000_6', 
        'data/sc_5000_7', 
        'data/sc_5000_0', 
        'data/sc_5000_9', 
        'data/sc_5120_0', 
        'data/sc_6931_0', 
        'data/sc_6951_0', 
        'data/sc_7435_0', 
        'data/sc_8002_0', 
        'data/sc_8661_1', 
        'data/sc_8661_0', 
        'data/sc_9524_0', 
        'data/sc_10000_2', 
        'data/sc_10000_5', 
        'data/sc_10000_4', 
        'data/sc_10000_3', 
        'data/sc_10000_6', 
        'data/sc_10000_1', 
        'data/sc_10000_8', 
        'data/sc_10000_0', 
        'data/sc_10000_7', 
        'data/sc_10370_0', 
        'data/sc_11264_0', 
        'data/sc_18753_0', 
        'data/sc_25032_0', 
        'data/sc_47311_0', 
        'data/sc_55515_0', 
        'data/sc_63009_0', 
        'data/sc_920683_0', 
        'data/sc_968672_0', 
        'data/sc_1081841_0', 
        'data/sc_1092610_0'
    ]

    #solutions = {}
    output_solutions = ''
    output_algorithms = ''
    output_results = ''

    for file in files:
        logging.info('==='*30)
        logging.info(f'Generating solutions for: {file}')

        regions_count, clinics_count, clinics = read_file(file)
        solution = get_best_solution(regions_count, clinics_count, clinics)

        key = file.split('/')[-1]

        #solutions[key] = solution

        logging.info('\n\nBest algorithm: {}'.format(solution['algorithm']))
        logging.info('Value: {}'.format(solution['cost']))

        logging.info('==='*30)

        # Create output strings
        output_solutions += file
        output_solutions += '\n'
        output_solutions += parse_solution(solution, clinics_count)
        output_solutions += '\n'

        output_algorithms += '{} {} \n'.format(file, solution['algorithm'])

        output_results += '{} {} {}\n'.format(file, solution['algorithm'], solution['cost'])

    with open('solutions.txt', 'w') as file:
        file.write(output_algorithms)
   
    with open('answers.txt', 'w') as file:
        file.write(output_solutions)

    with open('respuestas.txt', 'w') as file:
        file.write(output_results)




