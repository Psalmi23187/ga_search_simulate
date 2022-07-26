import numpy
import copy
import random

from simulator import layer_schedule_to_runtime
from bfs_toolkit import get_bfs_level, combine_bfs_bias_to_schedule
from model_config import dependency

"""
note: this version search, base on the bfs_bias vector
author: Haochen Yuan
time: 2022-07-22
chromosome: bias on bfs
"""

iteration_times = 30
solution_per_population = 10
saved_parents_per_population = 6
mating_parents_per_population = 4
mutation_per_population = 2
op_num = 435

fitness_record = [0 for i in range(solution_per_population)]
temp_population = []
temp_saved_parents = []
temp_mating_parents = []
temp_children = []

best_solution_per_generation = []

bfs = get_bfs_level(dependency=dependency)


def fitness_func(layer_schedule):
    fitness = layer_schedule_to_runtime(layer_schedule=layer_schedule) # runtime越短，fitness越高
    return fitness

def on_start():
    # initialize the population
    print("dependency:", dependency)
    length = len(dependency)
    for i in range(solution_per_population):
        highest_bfs_level = max(bfs) # maybe useful?
        temp_chromosome = [random.randint(0,1) for i in range(length)]
        temp_population.append(temp_chromosome) # here, parameter 3 can be modifieds
    for i in temp_population:
        print(i)
    print("on_start()")

def on_fitness():
    index = 0
    for chromosome in temp_population:
        ops_stage, schedule = combine_bfs_bias_to_schedule(bfs=bfs,bias=chromosome, dependency=dependency)
        print(schedule)
        fitness_record[index] = fitness_func(layer_schedule=schedule)
        index += 1
    for runtime in fitness_record:
        print(runtime)
    best_solution_per_generation.append((min(fitness_record), temp_population[fitness_record.index(min(fitness_record))]))
    print("on calculate fitness()")

def on_parents():
    temp_fitness_record = sorted(fitness_record) # 这里优先取运行时间短的，作为优良的
    for i in range(saved_parents_per_population):
        temp_saved_parents.append(temp_population[fitness_record.index(temp_fitness_record[i])])
    print("on parents()")

def on_crossover():
    for i in range(int(mating_parents_per_population/2)):
        father_bias = temp_saved_parents[2*i]
        mother_bias = temp_saved_parents[2*i+1]
        child_one_bias = father_bias[:(int)(len(father_bias)/2)] + mother_bias[(int)(len(mother_bias)/2):]
        child_two_bias = mother_bias[:(int)(len(mother_bias)/2)] + father_bias[(int)(len(father_bias)/2):]
        temp_children.append(child_one_bias)
        temp_children.append(child_two_bias)
    print("on_crossover()")

def on_mutation():
    for i in range(mutation_per_population):
        index = random.randint(0,solution_per_population-1)
        chromosome_mutate = temp_population[index]
        for bias_index in range(len(chromosome_mutate)):
            if random.random() > 0.8:
                option = random.randint(0,2)
                if option == 0:
                    chromosome_mutate[bias_index] += 1
                elif option == 1 and chromosome_mutate[bias_index] > 0:
                    chromosome_mutate[bias_index] -= 1
                else:
                    pass
        temp_population[index] = chromosome_mutate
    print("on_mutation()")

def on_generation():
    temp_population = temp_saved_parents + temp_children
    print("on_generation()")

def on_stop():
    print("final population: ", temp_population)
    print("on_stop()")


on_start()
for i in range(iteration_times):
    on_fitness()
    on_parents()
    on_crossover()
    on_mutation()
    on_generation()
    print("generation {}".format(i), "-"*150)

print("\niteration ended")
for solution in best_solution_per_generation:
    print("runtime: ", solution[0], " schedule: ", combine_bfs_bias_to_schedule(bfs, solution[1], dependency)[1])
