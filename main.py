import functions as f
import numpy as np

def find_max():
    features = [[10, 4], [14, 21], [10, 1], [14, 10], [10, 40]]

    function = f.parabula
    init_results = np.average(f.evaluate(features, function))
    print(f.evaluate(features, function))
    print('init results: ', init_results)

    life_time = 1000
    old_generation_results = init_results
    feature_range = range(-40, 40)
    num_of_children = 10
    barrier = 10
    #speed_parameter = int(life_time / 50)
    speed_parameter = 10
    History = []

    find_max = True
    for year in range(life_time):
        # print(year)
        features = f.run_genetic_algorithm(features, function, feature_range, num_of_children, speed_parameter, year, find_max)
        old_generation_results = f.evaluate(features, function)
        result = np.average(old_generation_results)
        History.append(result)

    print('done!')
    print('final result', np.average(old_generation_results))

    f.plot(History)


def find_min():

    features = [[10, 4], [14, 21], [10, 1], [14, 10], [10, 40]]

    function = f.parabula
    init_results = np.average(f.evaluate(features, function))
    print(f.evaluate(features, function))
    print('init results: ', init_results)

    life_time = 1000
    old_generation_results = init_results
    feature_range = range(-40, 40)
    num_of_children = 10
    barrier = 10
    #speed_parameter = int(life_time / 50)
    speed_parameter = 10
    History = []

    find_max = False
    for year in range(life_time):
        # print(year)
        features = f.run_genetic_algorithm(features, function, feature_range, num_of_children, speed_parameter, year, find_max = find_max)
        old_generation_results = f.evaluate(features, function)
        result = np.average(old_generation_results)
        History.append(result)

    print('done!')
    print('final result', np.average(old_generation_results))

    f.plot(History)

find_min()
find_max()