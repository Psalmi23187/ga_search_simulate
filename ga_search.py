import numpy
import copy
import random

from simulator import get_e2e_latency
from bfs_toolkit import get_bfs_level, update_schedule
from gnode import *
import argparse

"""
note: this version search, base on the bfs_bias vector
author: Haochen Yuan & Yu Cheng
time: 2022-07-22
chromosome: bias on bfs
"""

parser = argparse.ArgumentParser()
parser.add_argument('--input_log', type=str, default='inception.log')
parser.add_argument('--iteration', type=int, default=100)
parser.add_argument('--population', type=int, default=300)
parser.add_argument('--saved_parents_per_population', type=int, default=30)
parser.add_argument('--mating_parents_per_population', type=int, default=20)
parser.add_argument('--mutation_per_population', type=int, default=20)
args = parser.parse_args()

class GA():
    def __init__(self, iteration, population, saved_parents_per_population, mating_parents_per_population, mutation_per_population):
        self.iteration = iteration
        self.population = population
        self.saved_parents_per_population = saved_parents_per_population
        self.mating_parents_per_population = mating_parents_per_population
        self.mutation_per_population = mutation_per_population
        self.cur_population = []
        self.cur_parents = []
        self.cur_children = []
        self.optimal_latency = 1e8
        self.optimal_chromosomes = []
        temp_best_schedule = []
        temp_best_chromosome = []
    



    def fitness_func(self, layer_schedule, gnodes):
        fitness = get_e2e_latency(layer_schedule, gnodes)
        return fitness

    def on_start(self, gnodes):
        # initialize the population
        for i in range(self.population):
            chromosome = [0 if len(gnode.src)==0 else random.randint(0,20) for gnode in gnodes]
            self.cur_population.append(chromosome)
        print("on_start()")

    def on_fitness(self, gnodes, bfs):
        self.temp_latency = []
        for chromosome in self.cur_population:
            ops_stage, schedule = update_schedule(schedule=bfs, bias=chromosome, gnodes=gnodes)
            #print(schedule)
            self.temp_latency.append(self.fitness_func(schedule, gnodes))

            """if fitness_record[index] < 59.5:
                print('*'*150)
                print("Latency: ", fitness_record[index])
                print("whole schedule: ", schedule)
                print('*'*150)"""

        self.optimal_latency = min(min(self.temp_latency), self.optimal_latency)
        self.optimal_chromosomes.append(\
                        (self.cur_population[self.temp_latency.index(min(self.temp_latency))], 
                        min(self.temp_latency))
                    )    # (chromosome_id, latency)
        print("on calculate fitness()")

    def on_parents(self):
        # self.cur_parents = []
        sorted_latency = sorted(self.temp_latency)
        for i in range(self.saved_parents_per_population):
            self.cur_parents.append(self.cur_population[self.temp_latency.index(sorted_latency[i])])
        print("on parents()")

    def on_crossover(self):
        for i in range(self.mating_parents_per_population // 2):
            father = self.cur_parents[2*i]
            mother = self.cur_parents[2*i+1]
            child_0 = father[:(int)(len(father)/2)] + mother[(int)(len(mother)/2):]
            child_1 = mother[:(int)(len(mother)/2)] + father[(int)(len(father)/2):]
            self.cur_children.append(child_0)
            self.cur_children.append(child_1)
        print("on_crossover()")

    def on_mutation(self):
        for i in range(self.mutation_per_population):
            idx = random.randint(0, self.population - 1)
            # print(idx)
            chromosome_mutate = self.cur_population[idx]
            for bias_index in range(len(chromosome_mutate)):
                if random.random() > 0.75:
                    option = random.randint(0, 2)
                    if option == 0:
                        chromosome_mutate[bias_index] += 1
                    elif option == 1 and chromosome_mutate[bias_index] > 0:
                        chromosome_mutate[bias_index] -= 1
                    else:
                        pass
            self.cur_population[idx] = chromosome_mutate
        print("on_mutation()")

    def on_generation(self):
        self.cur_population += self.cur_parents + self.cur_children
        print("on_generation()")

    def on_stop(self):
        print("final population: ", cur_population)
        print("on_stop()")

    def search(self, gnodes, bfs):
        self.on_start(gnodes)
        for i in range(self.iteration):
            self.on_fitness(gnodes, bfs)
            self.on_parents()
            self.on_crossover()
            self.on_mutation()
            self.on_generation()
            print("generation {}".format(i), "-"*150)


        print("\niteration ended")
        for solution in best_solution_per_generation:
            latency = solution[0]
            schedule = update_schedule(bfs, solution[1], gnodes)[1]
            count = 0
            fix_schedule = []
            for layer in schedule:
                fix_layer = []
                for op in layer:
                    if len(gnodes[op].src) == 0:
                        fix_layer.append(op)
                if len(fix_layer) != 0:
                    fix_schedule.append(fix_layer)
            if solution[0] == temp_min_latency[0]:
                temp_best_schedule = fix_schedule
                temp_best_chromosome = solution[1]
            print("latency: ", solution[0], " schedule: ", fix_schedule)

            bias = [0 for i in range(len(bfs))]
            schedule = update_schedule(bfs, bias, gnodes)[1]
            latency = fitness_func(schedule, gnodes)

            fix_schedule = []
            for layer in schedule:
                fix_layer = []
                for op in layer:
                    if len(gnodes[op].src) == 0:
                        fix_layer.append(op)
                if len(fix_layer) != 0:
                    fix_schedule.append(fix_layer)
            print("compare with bfs schedule", '-'*150) 
            print("latency: ", latency, " schedule: ", fix_schedule)
            print('-'*150)
            print("chromosome: ", bias)
            print('-'*150)
            print("whole schedule: ", update_schedule(bfs, bias, gnodes)[1])

            print()

            print("compare with the best schedule", '-'*150)
            print("latency: ", temp_min_latency, " schedule: ", temp_best_schedule)
            print('-'*150)
            print("chromosome: ", temp_best_chromosome)
            print('-'*150)
            print("whole schedule: ", update_schedule(bfs, temp_best_chromosome, gnodes)[1])


if __name__ == '__main__':
    gnodes = load_gnodes(args.input_log)
    bfs = get_bfs_level(gnodes)
    op_num = len(gnodes)
    ga = GA(args.iteration, args.population, args.saved_parents_per_population, args.mating_parents_per_population, args.mutation_per_population)
    ga.search(gnodes, bfs)