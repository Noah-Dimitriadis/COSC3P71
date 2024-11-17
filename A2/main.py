import easygui as gui
import random
from pprint import pprint

'''
TODO actual GA function that does all the parts (once everything works individually)
TODO elite function - may require a redo of how the population is created, (dict or tuple)
TODO remove elites from mutation
TODO finish crossover function 
TODO once GA function works, write results to output file
'''

DATA = dict()
# no_conflicts = [[0, 1, 0], [1, 0, 10], [2, 3, 5], [3, 0, 8], [4, 1, 15], [5, 0, 0], [6, 1, 2], [7, 1, 3], [8, 1, 17], [9, 1, 7], [10, 1, 13], [11, 0, 7], [12, 0, 6], [13, 0, 19], [14, 1, 20], [15, 1, 6], [16, 0, 2], [17, 3, 10], [18, 0, 4], [19, 0, 13], [20, 0, 16], [21, 1, 19], [22, 0, 17], [23, 0, 18], [24, 1, 9]]

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

    # adding a list of professors to the data set
    courses = data['courses']
    all_professors = []

    for course in courses:
        prof = courses[course][1]
        if prof not in all_professors:
            all_professors.append(prof)

    data.update({'professors':all_professors})

    # breaking up the timeslots into the actual time slots per day
    timeslots = data['timeslots']
    all_days = []
    current_day = []
    current_day.append(timeslots[0][1])                 # need to add the first time of the first day as it will be skipped

    for i in range(1, len(timeslots)):
        if timeslots[i][0] == timeslots[i-1][0]:        # if the prev day name is the same as the current day name
            current_day.append(timeslots[i][1])         # the actual time
        else:                                           # reset for the next day
            all_days.append(current_day)
            current_day = []
            current_day.append(timeslots[i][1])         # add the first time for the next day

    all_days.append(current_day)                        # add the last day to all the days
    
    data.update({'days':all_days})
    return data

def generate_population(size:int) -> list[list[list]]:
    population = []
    courses = DATA['courses']
    for i in range(size):
        chromosome = []
        for course in courses:
            random_room = random.randrange(0, len(DATA['rooms']))
            random_time = random.randrange(0, len(DATA['timeslots']))
            gene = [course, random_room, random_time]
            chromosome.append(gene)

        population.append(chromosome)
    return population

def print_gene(gene:list):
    print(f'{DATA['courses'][gene[0]]}:{DATA['rooms'][gene[1]]}:{DATA['timeslots'][gene[2]]}')

def print_room_usages(chromosome:list[list]):
    usages = get_room_usages(chromosome)
    for schedule in usages:
        room_name = DATA['rooms'][usages.index(schedule)]
        for timeslot in schedule:

            print(f'{room_name}', end="")
            print_gene(timeslot)
    
def print_prof_schedules(chromosome:list[list]):
    schedules = get_professor_schedules(chromosome)
    for schedule in schedules:
        prof_name = DATA['professors'][schedules.index(schedule)]
        for timeslot in schedule:

            print(f'{prof_name}', end="")
            print_gene(timeslot)
    
def print_chromosome(chromosome:list[list]):
    for gene in chromosome:
        print_gene(gene)

def get_room_usages(chromosome:list[list]) -> list:
    all_room_usages = []
    rooms = DATA['rooms']

    for i in rooms:
        room = rooms[i][0]                              # the name of the room
        room_usage = []
        for gene in chromosome:
            gene_room = DATA['rooms'][gene[1]][0]       # name of the room for the current gene
            if room == gene_room:
                room_usage.append(gene)
        room_usage.sort(key = lambda slot: slot[2])     # sort by timeslots
        all_room_usages.append(room_usage)

    return all_room_usages

def get_professor_schedules(chromosome:list[list]):
    all_prof_schedules = []
    professors = DATA['professors']

    for prof in professors:
        prof_schedule = []
        for gene in chromosome:
            gene_prof = DATA['courses'][gene[0]][1]         # name of the professor
            if prof == gene_prof:
                prof_schedule.append(gene)                  # appending indexes
        prof_schedule.sort(key = lambda slot: slot[2])      # sort by timeslots
        all_prof_schedules.append(prof_schedule)

    return all_prof_schedules

def evaluate_fitness(chromosome:list[list]) -> float:
    # capacity conflicts
    capacity_conflicts = 0
    courses = DATA['courses']
    rooms = DATA['rooms']

    for gene in chromosome:
        gene_course = gene[0]
        gene_room = gene[1]

        if int(courses[gene_course][2]) > int(rooms[gene_room][1]):
            capacity_conflicts += 1

    # room usage conflicts
    room_conflicts = 0
    room_usages = get_room_usages(chromosome)

    for schedule in room_usages:
        for booking in schedule:
            day = DATA['timeslots'][booking[2]][0]
            start_time = int(DATA['timeslots'][booking[2]][1])
            duration = int(DATA['courses'][booking[0]][3])
            end_time = start_time + duration                                    # start time + class duration

            for gene in schedule:
                gene_day = DATA['timeslots'][gene[2]][0]
                gene_start_time = int(DATA['timeslots'][gene[2]][1])
                
                if gene_start_time >= end_time:
                    break                                           # room_usages is sorted by time so we can break when we start later then the current end_time
                elif gene_start_time >= start_time and gene_start_time < end_time and day == gene_day and gene[0] != booking[0]: # if the gene start time is inside the duration of the bookings time, the days are the same and the courses different
                        room_conflicts += 1
    
    # professor scheduling conflicts
    prof_conflicts = 0
    professor_schedules = get_professor_schedules(chromosome)

    for schedule in professor_schedules:
        for booking in schedule:
            day = DATA['timeslots'][booking[2]][0]
            start_time = int(DATA['timeslots'][booking[2]][1])
            duration = int(DATA['courses'][booking[0]][3])
            end_time = start_time + duration                                    # start time + class duration

            for gene in schedule:
                gene_day = DATA['timeslots'][gene[2]][0]
                gene_start_time = int(DATA['timeslots'][gene[2]][1])
                
                if gene_start_time >= end_time:
                    break                                           # professor_schedules is sorted by time so we can break when we start later then the current end_time
                elif gene_start_time >= start_time and gene_start_time < end_time and day == gene_day and gene[0] != booking[0]: # if the gene start time is inside the duration of the bookings time, the days are the same and the courses different
                        prof_conflicts += 1 

    conflicts = capacity_conflicts + room_conflicts + prof_conflicts
    # print(f'capacity conflicts: {capacity_conflicts} room conflicts: {room_conflicts} prof conflicts: {prof_conflicts} total conflicts: {conflicts}')
    # print(conflicts)
    return 1 / (1 + conflicts)

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
        
        fittest.sort(key=lambda k: k[0], reverse=True)        # sort by the fitness (the first part of the tuple), strongest at the front

        fit.append(fittest[0][1])        # the last two elements i.e. the two the least fit are removed from the population
        fit.append(fittest[1][1])

    return fit

def mutate(mutation_rate:float, population:list[list[list]]) -> list[list[list]]:
    # remove elites 
    num_indexes = int(mutation_rate * len(population[0]))       # all the chromosomes have the same number of genes
    
    for chromosome in population:
        mutation_indexes = random.sample(chromosome, num_indexes)
        print_chromosome(chromosome)
        for gene in mutation_indexes:
            mutated_room = random.randrange(0, len(DATA['rooms']))
            mutated_time = random.randrange(0, len(DATA['timeslots']))

            gene[1] = mutated_room
            gene[2] = mutated_time
        print()
        print_chromosome(chromosome)

    return population

def crossover_population(crossover_rate:float, crossover_method:int, population) -> list[list[list]]:
    num_indexes = int(crossover_rate * len(population))
    # have elites clone themselves here
    # iterate over the remaining chromosome pairs
    # pass pairs to crossover method 
    # choose crossover method based on param
    # append returned offspring to population

    return population

def uniform_crossover(crossover_rate:float, k:int, parents:list[list[list]]) -> list[list[list]]:
    offspring = []

    # 50/50 chance to choose gene from parent, random num between 0,1 then choose
    # create new child with selected genes
    # repeat for 2 children

    return offspring

def GA(population_size:int, generations:int, mutation_rate:float, crossover_rate:float):
    population = generate_population(population_size)

    for i in range(generations):
        population = tournament_select(population)
        population = mutate(mutation_rate, population)
        population = crossover_population(crossover_rate)



if __name__ == "__main__":
    DATA = read_all()

    population_1 = generate_population(1)
    population_2 = mutate(0.5, population_1)
    