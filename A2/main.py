import easygui as gui
import random

'''
TODO make sure we have a way to determine the order of the data dict, it seems to be sorted but this needs to be confirmed
TODO figure out population size for generate func, also rename this 
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
        filename = file.split('\\')[-1][:-4]
        data.update({filename:item})
    return data

def generate(data:dict):
    keys = data.keys()
    print(keys)
    for test in range(20):
        c = []

        for key in keys:
            i = random.randrange(0, len(data[key]))
            c.append(i)

        print(c)


if __name__ == "__main__":
    data = read_all()
    generate(data)