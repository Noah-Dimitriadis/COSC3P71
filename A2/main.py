import easygui as gui
import random
from pprint import pprint

'''

TODO write fitness function -> see pseudo code provided
TODO fitness function -> need to flag cases where duration is a factor

TODO decide on crossover strat implementation and write func
TODO decide on mutation strat implementation and write func
'''

DATA = dict()

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
        chromosome = []         # TODO could this be easier with a dictionary? test
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
    conflicts = 0
    prof_conflicts = 0
    room_conflicts = 0
    capacity_conflicts = 0
    room_usages = get_room_usages(chromosome)
    professor_schedules = get_professor_schedules(chromosome)

    courses = DATA['courses']
    rooms = DATA['rooms']
    days = DATA['days']

    for gene in chromosome:
        gene_course = gene[0]
        gene_room = gene[1]
        # gene_time = gene[2]
        if int(courses[gene_course][2]) > int(rooms[gene_room][1]):     # check capacity conflicts
            # print_gene(gene)

            conflicts += 1
            capacity_conflicts += 1
            pass

        #TODO need to add a check to see if durations overlap

        for day in days:
            for hour in day:
                
                pass


        for schedule in room_usages:                                    # check room start conflicts
            for i in range(1, len(schedule)):
                if schedule[i][2] == schedule[i-1][2]:
                    print('room conflict [')
                    print_gene(schedule[i])
                    print_gene(schedule[i-1])
                    print(']')
                    room_conflicts += 1
                    conflicts += 1
        
        for schedule in professor_schedules:                            # check prof start conflicts
            for i in range(1, len(schedule)):
                if schedule[i][2] == schedule[i-1][2]:
                    print('prof conflict [')
                    print_gene(schedule[i])
                    print_gene(schedule[i-1])
                    print(']')
                    prof_conflicts += 1
                    conflicts += 1

        

    # print(f'capacity conflicts: {capacity_conflicts} room conflicts: {room_conflicts} prof conflicts: {prof_conflicts} total conflicts: {conflicts}')
    return 1 / (1 + conflicts)

def tournament_select(population:list[list[list]]) -> list[list[list]]:
    fit = []
    rounds = int(len(population)/4)
    for i in range(rounds):
        fittest = []
        choices = random.sample(population, 4)
        print('checking fitnesses for selected choices')
        for choice in choices:
            fitness = evaluate_fitness(choice)
            print(fitness)
            pair = (fitness, choice)
            fittest.append(pair)
            population.remove(choice)
        
        print('selecting top two')
        fittest.sort(key=lambda k: k[0], reverse=True)        # sort by the fitness (the first part of the tuple), strongest at the front

        fit.append(fittest[0][1])        # the last two elements i.e. the two the least fit are removed from the population
        print(fittest[0][0])
        print(fittest[1][0])
        fit.append(fittest[1][1])

    return fit

if __name__ == "__main__":
    DATA = read_all()
    # population_before = generate_population(10)
    # print('performing tournament select')
    # population = tournament_select(population_before)