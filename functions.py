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
        x = math.log10(x) if x > 0 else -math.log10(abs(x))
        result = 1 / (1 + math.exp(x))
    except OverflowError:
        result = 0
    return result

# sigmoid to make - prob bigger
def sigmoid_minus(x):
    try:
        x = math.log10(x) if x > 0 else -math.log10(abs(x))
        result = 1 / (1 + math.exp(-x))
    except OverflowError:
        result = 0
    return result

def count_probs_to_take_feature(generation, find_max):
    alpha = 0.000000000000000000001
    if find_max == True:
        coefficient_to_survive = list(map(lambda i: 1 / (sigmoid_plus(i) + alpha), generation))
    else:
        coefficient_to_survive = list(map(lambda i: 1 / (sigmoid_minus(i) + alpha), generation))
    sum_of_probs_to_survive = np.sum(coefficient_to_survive)
    probs = list(map(lambda i: i / sum_of_probs_to_survive, coefficient_to_survive))
    return probs


def make_child(father, mother, vis_key):
    alpha = random.sample(range(int(len(father) / 2)), 1)[0]
    alpha = -alpha % len(father)
    child = father[:alpha] + mother[alpha:]
    if vis_key == True:
        vis_child = [father[:alpha]], mother[alpha:]
        return child, vis_child
    return child


def reproduction(generation_results, features, num_of_children, vis_key=False, find_max = True):
    generation_results, index = np.unique(generation_results, return_index=True)
    features = [features[i] for i in index]

    new_generation_features = []
    vis_new_generation_features = []

    for child_id in range(num_of_children):
        # take father and mother with the best features
        probs = count_probs_to_take_feature(generation_results, find_max)
        father_id = np.random.choice(range(len(generation_results)), p=probs)
        mother_id = np.random.choice(range(len(generation_results)), p=probs)

        if vis_key == True:
            child, vis_child = make_child(features[father_id], features[mother_id], vis_key)
            vis_new_generation_features.append(vis_child)
        else:
            child = make_child(features[father_id], features[mother_id], vis_key)
        new_generation_features.append(child)
    if vis_key == True:
        return new_generation_features, vis_new_generation_features
    return new_generation_features

# evaluate

def evaluate(features, function):
    generation_results = []
    for feature in features:
        generation_results.append(function(feature))
    return generation_results

# run genetic algorithm

def run_genetic_algorithm(features, function, feature_range, num_of_children, speed_parameter, year, find_max):
    generation_results = evaluate(features, function)
    print(generation_results)
    generation_ids = range(len(generation_results))
    if year % speed_parameter == 0:
        #print("mutation!")
        number_of_mutations = random.sample(range(int(len(generation_results) / 10 + 1)), 1)[0]
        features = mutation(generation_ids, copy.deepcopy(features), feature_range, number_of_mutations)
        generation_results = evaluate(features, function)
    features = reproduction(generation_results, features, num_of_children, find_max = find_max)
    return features

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