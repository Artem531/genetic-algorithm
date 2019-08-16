import math
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

# equations
def parabula(x):
    return x[0]**2 - x[1]

def linear(x):
    return x[0] - x[1]

def ackley(x, a=20, b=0.2, c=2*np.pi):
    """
    x: vector of input values
    """
    d = len(x) # dimension of input vector x
    x = np.array(x)
    sum_sq_term = -a * np.exp(-b * np.sqrt(sum(x*x) / d))
    cos_term = -np.exp(sum(np.cos(c*x) / d))
    return (a + np.exp(1) + sum_sq_term + cos_term)

# mutation

def mutation(generation, features, feature_range, number_of_mutations, vis_key = False):
    if vis_key == True:
        features_for_vis = copy.deepcopy(features)
    mutants = random.sample(generation, number_of_mutations)
    for mutant_id in mutants:
        skill_id = random.sample(range(len(features[mutant_id])), 1)[0]
        new_skill = random.sample(feature_range, 1)
        if vis_key == True:
            features_for_vis[mutant_id][skill_id] = new_skill
        features[mutant_id][skill_id] = new_skill[0]
    if vis_key == True:
        return features, features_for_vis
    return features

# reproduction

# sigmoid to make + prob bigger
def sigmoid_plus(x):
    try:
        #math domain error fix
        shift = 1
        #---------------------
        x = math.log10(x + shift) if x > 0 else -math.log10(abs(x) + shift)
        result = 1 / (1 + math.exp(x))
    except OverflowError:
        result = 0
    return result

# sigmoid to make - prob bigger
def sigmoid_minus(x, std, sensivity):
    try:
        # add support of multiple min
        ## add sensivity
        ### add normalize [-1*sensisity : 1*sensisity]
        x = (x / std) * sensivity
        result = 1 / (1 + math.exp(-x))
    except OverflowError:
        if x > 0:
            result = 1
        if x < 1:
            result = 0
    return result

def count_probs_to_take_feature(generation, sensivity, find_max):
    alpha = 0.000000000000000000001

    # add max range of features
    max_result = abs(np.max(generation))
    min_result = abs(np.min(generation))
    if min_result > 0:
        std = max_result
    elif max_result < 0:
        std = abs(min_result)
    else:
        std = max_result + min_result

    if find_max == True:
        coefficient_to_survive = list(map(lambda i: 1 / (sigmoid_plus(i) + alpha), generation))
    else:
        # add support of multiple min
        coefficient_to_survive = list(map(lambda i: 1 / (sigmoid_minus(i, std, sensivity) + alpha), generation))
    sum_of_probs_to_survive = np.sum(coefficient_to_survive)
    probs = list(map(lambda i: i / sum_of_probs_to_survive, coefficient_to_survive))
    return probs


def make_child(father, mother):
    # barrier to split features
    alpha = random.sample(range(int(len(father) + 1)), 1)[0]
    alpha = -alpha % len(father)
    # add fix of not mixing features
    first_part, _ = np.split(father, [alpha])
    _, second_part = np.split(mother, [alpha])
    if not first_part:
        child = mother
    elif not second_part:
        child = father
    else:
        child = [i for i in first_part] + [i for i in list(second_part)]
    return child


def reproduction(generation_results, features, num_of_children, sensivity, find_max = True):
    # remove vis key

    #generation_results, index = np.unique(generation_results, return_index=True)
    #features = [features[i] for i in index]

    new_generation_features = []
    vis_new_generation_features = []
    probs = count_probs_to_take_feature(generation_results, sensivity, find_max)

    for child_id in range(num_of_children):
        # take father and mother with the best features
        father_id = np.random.choice(range(len(generation_results)), p=probs)
        mother_id = np.random.choice(range(len(generation_results)), p=probs)
        child = make_child(features[father_id], features[mother_id])
        new_generation_features.append(child)
    return new_generation_features

# evaluate

def evaluate(features, function):
    generation_results = []
    for feature in features:
        generation_results.append(function(feature))
    return generation_results

# run genetic algorithm

def run_genetic_algorithm(features, function, feature_range, num_of_children, speed_parameter, year, find_max, sensivity = 1):
    # add sensivity
    generation_results = evaluate(features, function)
    generation_ids = range(len(generation_results))
    if year % speed_parameter == 0:
        # make mutation
        number_of_mutations = random.sample(range(int(len(generation_results) / 10 + 1)), 1)[0]
        features = mutation(generation_ids, copy.deepcopy(features), feature_range, number_of_mutations)
        generation_results = evaluate(features, function)
    # get new features
    features = reproduction(generation_results, features, num_of_children, sensivity = sensivity, find_max = find_max)
    return features

# add run with smart mutation
def run_genetic_algorithm_with_smart_mutation(features, old_generation_results, function, feature_range, num_of_children, find_max, sensivity = 1):
    generation_results = evaluate(features, function)
    generation_ids = range(len(generation_results))
    #print('-isclose-',np.mean(generation_results), np.mean(old_generation_results), np.isclose(np.mean(generation_results), np.mean(old_generation_results)))
    if np.isclose(np.mean(generation_results), np.mean(old_generation_results)):
        # make mutation
        number_of_mutations = random.sample(range(int(len(generation_results) / 10 + 1)), 1)[0]
        features = mutation(generation_ids, copy.deepcopy(features), feature_range, number_of_mutations)
        generation_results = evaluate(features, function)
    # get new features
    new_features = reproduction(generation_results, features, num_of_children, sensivity = sensivity,find_max = find_max)
    return new_features, features

# plot history

def plot(History):
    fig = plt.figure()

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('year')
    ax.set_ylabel('value')

    # Create a legend for the first line.
    line1, = plt.plot(range(len(History)), History, label="agent", linestyle='--')

    first_legend = plt.legend(handles=[line1], loc=1)
    # Add the legend manually to the current Axes.
    ax = plt.gca().add_artist(first_legend)
    plt.show()