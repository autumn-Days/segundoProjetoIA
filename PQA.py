from typing import *
"""
Técnicas a serem utilizadas:

- Seleção por torneio
- Seleção por ranking

- crossOver metade-metade
- crossOver uniforme

- mutação swap : seleciona dois indivíduos aleatórios para fazer
- mutação inversão : remove um elemento aleatório da lista e o insere em outro lugar

- promover elitismo pela substituição direta dos piores (aka, elitismo simples)
- promover elitismo percentual (aka, elitismo percentual)
"""

class PQA():
    def __init__(self, locals_:List[Tuple[int,int]], flows:Dict[Tuple[int,int],int], distancies:Dict[Tuple[Tuple[int,int],Tuple[int,int]],int], allocate=None):
        self.locals_ = locals_
        self.flows = flows
        self.distancies = distancies
        self.allocate = allocate
        if not allocate:
            self.allocate = genAllocateFunction() #achei que esse nome seria legal para a função l

    def __genAllocateFunction(self,):
        """
        Essa função gerará a função de alocação "l". A ideia é muito simples:
        Ela embaralhará todos os locais de "self.locals_" de tal modo que o 
        local com o i-ésimo indice guardará o objeto "i".
        """
        copyLocals = self.locals_
        random.shuffle(copyLocals)
        return copyLocals
    
    def __genRandomIndividual(self):
        """
        When the localitions are shuffled in the array of locations, it is the same thing as 
        making anexing new facilities to them, since the facilities are related to the locations
        because of their indixies, such that, if you have a location (x,y) and it its in the i-th
        index of the array, them the facility "i" is related to (x,y)
        """
        copyLocals = self.locals_.copy()
        random.shuffle(copyLocals)
        return copyLocals

    def __genInitPopulation(self, lengthPop:int):
        initPop:List[List[Tuple[int,int]]] = []
        for i in range(lengthPop):
            individual = self.__genRandomIndividual()
            initPop.append(individual)

    def __findLocal(self, locations:List[Tuple[int,int]], facility:int):
        #discovers where a facility is located
        return locations[facility]

    def calcSingularFlowCost(self, facility1:int, facility2:int, locations:List[Tuple[int,int]]):
        """
        O objetivo desta função é calcular o custo de um único fluxo entre um facility1 e um facility2
        como essa função é bijetora, acredito que nunca vai acontecer de l(facility1) == l(facility2) para facility1 != facility2
        """
        if facility1 == facility2:
            print("estranho") # putted this flag just to visualize weird things happening
        return self.flows[(facility1,facility2)] * self.distancies[self.__findLocal(locations,facility1), self.__findLocal(locations,facility2)]

    def calcTotalFlowCost(self, locations:List[Tuple[int,int]]):
        #This is the actual fitness function
        amountObjs = len(self.locals_)
        totalCost:int = 0
        
        allObjPairs:List[Tuple[int,int]] = list(self.flows.keys())

        for pair in allObjPairs:
            totalCost += self.calcSingularFlowCost(pair[0],pair[1], locations)
        
        return totalCost

    #selecion methods

    def tournamentSel(self, population: List[List[Tuple[int, int]]], tournamentSize: int) -> List[Tuple[int,int]]:
        """
        It returns the selected individual from the tournment (a list of locations).
        It rondomly chooses `tournamentSize` individuals from the population
        """
        tourment:List[List[int,int]] = random.sample(population,tournamentSize)
        """
        What the line bellow basically does is: It associates, for every individual
        in the population a value `key`, which is its fitness function, and the indi-
        vidual with the highest fitness function (which, in this case, means it has the
        lowest "calcTotalFlowCost") from all the others guys that make up the tournment
        """
        bestIndividual = min(tournment, key = lambda individual: self.calcTotalFlowCost(individual))
        return bestIndividual

    def rankingSel(self, population: List[List[Tuple[int, int]]]):
        """
        This selection method works by sorting the individuals of the population accordining to their
        fitness (keep in mind that the smallest the "calcTotalFlowCost" the highest the fitness). The highest
        the fitness, the better is the chances of it being selected. To do this, for each individual, a
        weight is associated to them according to their position in the list, them we randomly select an
        individual in the population (having those weights in mind) 
        """

        sortedPopulation:List[List[int,int]] = sorted(population, key = lambda individual: self.calcTotalFlowCost(individual))
        
        weights:List[int] = []
        
        n = len(sortedPopulation)
        for i in range(n):
            weights.append(n-i)
        
        #the line bellow returns a list of only one individual (the fittest), so we select it by making [0]
        individualSelected:List[int,int] = random.choices(sortedPopulation, weights=weights, k=1)[0]
        return individualSelected

    #crossover methods
        #In other part of the code, it is necessary to check if the offspring is valid, because there is the possibility of
        #repetition like [(x1,y1),(x2,y2),(x3,y3), (x1,y1)]. So there is the need of veryfying if there are no repeated element
        #otherwise, the function would be bijective
    def crossoverAroundPoint(self, parent1: List[Tuple[int, int]], parent2: List[Tuple[int, int]]) -> Tuple[List[Tuple[int,int]],Tuple[int,int]]:
        """
        Performs one-point crossover between two parents.
        """

        point:int = random.randint(1, len(parent1)-2)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

        return (child1,child2)

    def uniformCrossover(self, parent1: List[Tuple[int, int]], parent2: List[Tuple[int, int]]) -> Tuple[List[Tuple[int,int], Tuple[int,int]]]:
        n = len(parent1)

        child1 = []
        child2 = []

        for i in range(n):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        return (child1,child2)

    #mutations

    def swapMutation(self, individual: List[Tuple[int, int]]):
        #changes the location of 2 genes

        indexGene1 = None
        indexGene2 = None
        
        n = len(individual) 

        while indexGene1 == indexGene2:
            indexGene1 = random.randint(0,n-1)
            indexGene2 = random.randint(0,n-1)

        temp:Tuple[int,int] = individual[indexGene1]

        individual[indexGene1] = individual[indexGene2]
        individual[indexGene2] = temp

        return individual


    def inversion_mutation(self, individual: List[Tuple[int, int]]):
        """
        The ideia is to select a subslist of the list that represents the individual
        and invert this specific strip.
        """
        startIndex = None
        endIndex = None

        while startIndex == endIndex:
            startIndex = random.randint(0, n-2)
            endIndex = random.randint(1, n-1)

        individual[startIndex:endIndex] = reversed(individual[startIndex:endIndex])
        return individual


def test():
    locals_ = ["A","B","C"]
    distancies = {
        (("A"),("B")): 10,
        #(("B"),("A")): 10,

        (("A"),("C")): 15,
        #(("C"),("A")): 15,

        (("B"),("C")): 12,
        #(("C"),("B")): 12
    }
    flows = {
        (0,1): 3,
        #(1,0): 3,

        (0,2): 6,
        #(2,0): 6,

        (1,2): 1,
        #(2,1): 1,
    }
    allocate = ["A","B","C"]

    myPQA = PQA(locals_,flows,distancies,allocate)
    print(myPQA.calcSingularFlowCost(0,1,myPQA.locals_))
    print(myPQA.calcTotalFlowCost(myPQA.locals_))

test()