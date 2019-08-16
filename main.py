import functions as f
import numpy as np
import copy

def find_max(features, function, life_time, feature_range, num_of_children, speed_parameter):
    init_results = np.average(f.evaluate(features, function))
    print(f.evaluate(features, function))
    print('init results: ', init_results)
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


def find_min(old_features, function, life_time, feature_range, num_of_children, speed_parameter, sensivity,
             smart_mutation=False):
    new_features = copy.deepcopy(old_features)
    print(new_features)
    init_results = np.average(f.evaluate(old_features, function))
    old_generation_results = init_results
    print(f.evaluate(old_features, function))
    print('init results: ', init_results)
    History = []

    find_max = False
    for year in range(life_time):
        # print(year)

        if smart_mutation == True:
            new_features, old_features = f.run_genetic_algorithm_with_smart_mutation(new_features, old_generation_results,
                                                                                   function, feature_range,
                                                                                   num_of_children, sensivity=sensivity,
                                                                                   find_max=find_max)
        else:
            old_features = f.run_genetic_algorithm(old_features, function, feature_range, num_of_children,
                                                 speed_parameter, year, sensivity=sensivity, find_max=find_max)
        old_generation_results = f.evaluate(old_features, function)
        result = np.average(old_generation_results)
        History.append(result)

    print('done!')
    print('final result', np.average(old_generation_results))
    f.plot(History)
    return new_features

features = [[10, 4], [14, 21], [10, 1], [14, 10], [10, 40]]
function = f.parabula
life_time = 1000

feature_range = range(-40, 40)
num_of_children = 20
speed_parameter = 100
sensivity = 1

find_min(features, function, life_time, feature_range, num_of_children, speed_parameter, sensivity)
find_max(features, function, life_time, feature_range, num_of_children, speed_parameter)

smart_mutation = True
num_of_children = 100
function = f.ackley

find_min(features, function, life_time, feature_range, num_of_children, speed_parameter, sensivity, smart_mutation)