import random
from typing import List  , Tuple
from collections import namedtuple
import time
from functools import partial

random.seed(1)


Genome = List[int]
Population = List[Genome]

Thing = namedtuple('Thing',['name','value','weight'])
things = [
    Thing('thing1',500,2200),
    Thing('thing2',150,160),
    Thing('thing3',60,350),
    Thing('thing4',40,333),
    Thing('thing5',30,192),
    Thing('thing5',15,50),
    Thing('thing5',300,200),
    Thing('thing5',90,19),
    Thing('thing5',33,100),
]


def generate_genome(lenght: int) -> Genome  :
    return random.choices([0,1],k=lenght)

def generate_population(size :int,lenght : int) -> Population : #size : size of the population , lenght : lenght of the genome
    return [generate_genome(lenght) for _ in range(size)]

def fitness(genome :Genome,things :[Thing],Wmax :int):  
    if len(genome) != len(things) :
        raise ValueError("things and genome not the same lenght")

    value = weight = 0
    for i,thing in enumerate(things) :
        if genome[i] == 1 :
            value += thing.value
            weight += thing.weight
        if weight > Wmax :
            return 0
    return value

def selection_pair(population :Population,fitness) -> Tuple[Genome,Genome]: 
    return random.choices(population=population,weights=[fitness(genome) for genome in population],k=2)



def single_point_crossover(genome1 :Genome,genome2 :Genome) -> Tuple[Genome,Genome]:
    if len(genome1) != len(genome2) :
        raise ValueError("G1 and G2 not the same lenght")

    if len(genome1) < 2: 
        return genome2 ,genome1

    p = random.randint(1,len(genome1)-1)
    return genome1[0:p] + genome2[p:] , genome2[0:p] + genome1[p:] 




def mutation(genome : Genome,number_of_mutation :int=1, prob : float=0.5) -> Genome:
    for _ in range(number_of_mutation):
        index = random.randrange(len(genome))
        genome[index] = genome[index] if random.random() > prob else abs(genome[index]-1) 
    return genome





def run_evolution(fitness_funct, Generat_pop_funct,generation_limit :int=100):

    P = Generat_pop_funct()

    for i in range(generation_limit):
        P = sorted(P, key=lambda genome: fitness_funct(genome),reverse=True )

        if 0 not in P[0] :
            break
        
        next_generation = P[0:2]
        
        for j in range( int(len(P)/2 )-1):
            parents = selection_pair(P,fitness_funct)  
            g1,g2 = single_point_crossover(parents[0],parents[1])
            g1 = mutation(g1)
            g2 = mutation(g2)
            next_generation += [g1,g2]

        P = next_generation

    P = sorted(P, key=lambda genome: fitness_funct(genome),reverse=True )

    return P[0],i



def generate_thing(num_thing):
    things = []
    for _ in range(num_thing):
        things.append( Thing('',random.randrange(1,100),random.randrange(1,100)) )
    return things


print("item  | generation | time | rate | genome")   

for i in range(77,78):       #sumilation :array of ones
    X= generate_thing(i)

    Wmax=i*100   #max weight 
    sizeP=10    #size of population

    start = time.time() 
    genome,generation = run_evolution( fitness_funct=partial(fitness,things=X,Wmax=Wmax),
                                        Generat_pop_funct=partial(generate_population,size=sizeP,lenght=len(X)),
                                        generation_limit=100
                                    )
    end = time.time()

    s=0
    for h in genome : #for the calcule of the rate
        if h == 0 :
            s+=1

    print(i," | ",generation," | ",format(end-start,".2e")," | ",round((i-s)/i*100,2),"% | ",genome)



"""
Wmax=1000   #max weight 
sizeP=10    #size of population
genome,generation = run_evolution( fitness_funct=partial(fitness,things=things,Wmax=Wmax),
                                        Generat_pop_funct=partial(generate_population,size=sizeP,lenght=len(things)),
                                        generation_limit=100
                                    )
"""