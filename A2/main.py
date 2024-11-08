import easygui as gui
import random
from pprint import pprint

'''
TODO fitness function will need a way to see prof schedule and room schedule, func to generate these will be required,
probably on chromosome creation is best

TODO write fitness function -> see pseudo code provided
TODO write selection function
TODO decide on crossover strat implementation and write func
TODO decide on mutation strat implementation and write func
'''

def create_dict(file_name:str) -> dict:
    file = open(file_name)
    lines = file.readlines()
    file.close()
    courses = dict()
    
    i = 0
    for line in lines[1:]:
        line = line.strip().split(',')
        courses.update({i:line})
        i += 1
        
    return courses

def read_all() -> dict:
    files = gui.fileopenbox(msg='Select 3 files to be read', default='COSC3P71/A2/', multiple=True)
    data = dict()
    for file in files:
        item = create_dict(file)
        filename = file.split('\\')[-1][:-4]        # last element in the filepath (the actual filename) without the .txt characters
        data.update({filename:item})
    return data

def generate_population(data:dict, size:int) -> list[list[list]]:
    population = []
    courses = data['courses']
    for i in range(size):
        chromosome = []
        for course in courses:
            random_room = random.randrange(0, len(data['rooms']))
            random_time = random.randrange(0, len(data['timeslots']))
            gene = [course, random_room, random_time]
            chromosome.append(gene)

        population.append(chromosome)
    return population

def evaluate_fitness(chromosome:list[list]) -> float:
    return 1

def tournament_select(population:list[list[list]]) -> list[list[list]]:
    fit = []
    rounds = int(len(population)/4)
    for i in range(rounds):
        fittest = []
        choices = random.sample(population, 4)

        for choice in choices:
            fitness = evaluate_fitness(choice)
            pair = (fitness, choice)
            fittest.append(pair)
            population.remove(choice)
        
        fittest.sort(key=lambda k: k[0])        # sort by the fitness (the first part of the tuple)

        fit.append(fittest[0][1])        # the last two elements i.e. the two the least fit are removed from the population
        fit.append(fittest[1][1])

    return fit
        
def get_fitness(chromosome:list[list]) -> float:
    conflicts = 0
    # room usage = dict
    # professor schedule = dict

    # for each (course, room, timeslot) in chromosome:
    # if course number of students > room capacity:
    #     number of conflicts += 2

    # for each possible hour of class: # (0 to course hours -1)
    #     current slot = timeslot index + hour of class
    #     if (room index, current slot) not in room usage:
    #         room usage [(room index, current slot)] = 0 
    #     add 1 to room usage [(room index, current slot)]
    #     if room usage [(room index, current slot)] list is > 1 
    #         number conflicts += 3
        
    #     if (course professor, current slot) not in professor schedule
    #         professor schedule [(course professor, current slot)] = 0
    #     professor schedule [(course professor, current slot)] += 1
    #     if professor schedule [(course professor, current slot)] > 1
    #         number of conflicts += 1

    return 1 / (1 + conflicts)


if __name__ == "__main__":
    data = read_all()
    population = generate_population(data, 40)
    print(len(population))
    population = tournament_select(population)
    print(len(population))
