from typing import *
import math

"""
Técnicas a serem utilizadas:

- Seleção por torneio
- Seleção por ranking

- crossOver metade-metade
- crossOver uniforme

- mutação swap : seleciona dois indivíduos aleatórios para fazer
- mutação inversão : remove um elemento aleatório da lista e o insere em outro lugar

- promover elitismo pela substituição direta dos piores (aka, elitismo simples)
- promover elitismo SIMPLES + DIVERSIDADE
"""

class PQA():
    def __init__(self, locals_:List[Tuple[int,int]], flows:Dict[Tuple[int,int],int], distancies:Dict[Tuple[Tuple[int,int],Tuple[int,int]],int], allocate=None):
        self.locals_ = locals_
        self.flows = flows
        self.distancies = distancies
        self.allocate = allocate

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

    def rankingSel(self, population: List[List[Tuple[int, int]]], nothingImportant=None) -> List[Tuple[int,int]]:
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

    def uniformCrossover(self, parent1: List[Tuple[int, int]], parent2: List[Tuple[int, int]]) -> Tuple[Tuple[int,int], Tuple[int,int]]:
        """
        """
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

    def inversionMutation(self, individual: List[Tuple[int, int]]):
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

    #elitismPropagation

    def simpleElitism(self, previousPopulation:List[List[Tuple[int, int]]], currentPopulation:List[List[Tuple[int,int]]], elitAmount:int) -> List[List[Tuple[int,int]]]:
        sortedPreviousPopulation = sorted(previousPopulation, key= lambda individual: self.calcTotalFlowCost(individual))
        sortedCurrentPopulation = sorted(currentPopulation, key= lambda individual: self.calcTotalFlowCost(individual))
        
        sortedPreviousPopulation = sortedPreviousPopulation[:elitAmount]
        sortedCurrentPopulation = sortedCurrentPopulation[:-elitAmount]

        return sortedPreviousPopulation + sortedCurrentPopulation

    def elitismWithDiversity(self, previousPopulation:List[List[Tuple[int,int]]], currentPopulation:List[List[Tuple[int,int]]], oldIndividualAmount:int) ->List[List[Tuple[int,int]]]:
        """
        In this strategy, there will be a number "n" corresponding to the amount of individuals taken from the previous population. This "n"
        is composed by numbers "a" and "b", such that "a" + "b" >= 2. The idea is that, if "n" is even, "a" will correspond to the n/2 most fit
        from the previous generation and that "b" will correspond to some random "n/2" individuals who are not among the fittest. If "n" is odd,
        then "a" will correspond to "floor(n/2)" and b to the "ceil(n/2)".
        """
        
        if (oldIndividualAmount <=1):
            raise ValueError(f"Valor inválido para 'oldIndividualAmount': precisa ser maior ou igual a 2")
        elif (len(previousPopulation)//2 < oldIndividualAmount):
            raise ValueError(f"'oldIndividualAmount' pode ser, no máximo, a metade do tamanho de 'previousPopulation'")

        else:
            sortedPreviousPopulation = sorted(previousPopulation, key = lambda individual: self.calcTotalFlowCost(individual))
            sortedCurrentPopulation = sorted(currentPopulation, key = lambda individual: self.calcTotalFlowCost(individual))

            amountGroupA = None #grupo dos melhores
            amountGroupB = None #grupo dos outros
            lenSortedCurrentPopulation = len(sortedCurrentPopulation)


            if (lenSortedCurrentPopulation%2 == 0):
                amountGroupA = oldIndividualAmount/2
                amountGroupB = amountGroupA
            else:
                amountGroupA = math.floor(oldIndividualAmount/2)
                amountGroupB = math.ceil(oldIndividualAmount/2)
            
            elitePrevious = sortedPreviousPopulation[:amountGroupA]
            nonElitePrevious = sortedPreviousPopulation[amountGroupA:]
            nonElitePrevious = random.sample(nonElitePrevious,amountGroupB)

            """
            The list bellow corresponds to the indexies of the elements that are going to be substituted by the individuals of
            groups A and B,
            """
            finalGroup2replace:List[Tuple[int,int]] = elitePrevious + nonElitePrevious
            elements2replace:List[int] = self.__randomNumbers(self, lenSortedCurrentPopulation-1, oldIndividualAmount)


            for i in range(oldIndividualAmount):
                for indexCurrentInd in elements2replace:
                    sortedCurrentPopulation[indexCurrentInd] = finalGroup2replace[i]
        
            return currentPopulation

    #main method

    def doOperation(self, selectionMethod:str, crossOverMethod:str,
                    mutationMethod:str, elitismPropagationMethod:str,
                    genLimit:int, mutationTax:int, elitismTax:int, tournmentSize:int)

        selectionMethod:Callable =              getattr(self, selectionMethod,          None)
        crossOverMethod:Callable =              getattr(self, crossOverMethod,          None)
        mutationMethod:Callable =               getattr(self, mutationMethod,           None)
        elitismPropagationMethod:Callable =     getattr(self, elitismPropagationMethod, None)

        oldPopulation:List[List[Tuple[int,int]]] = self.__genInitPopulation()

        #statistics
        fittestIndividual:List[Tuple[int,int]] = None
        bestFitness:int = float('inf')
        mediumFitness:int = 0


        n = len(oldPopulation)

        for i in range(genLimit):
            newPopulation:List[List[Tuple[int,int]]] = []

            for i in range(len(n)):
                parent1 = selectionMethod(oldPopulation, tournamentSize)
                parent2 = selectionMethod(oldPopulation, tournmentSize)

                child1,child2 = crossOverMethod(parent1,parent2)

                newPopulation.extend([child1,child2])
            
            newPopulation = newPopulation[:n]

            #mutation
            for i in range(n):
                if random.random() <= mutationTax:
                    newPopulation[i] = mutationMethod(newPopulation[i])
            #elitism propagation
            newPopulation = elitismPropagation(oldPopulation,newPopulation,elitismTax) #tenho que ver se isso não gera um problema de referência nos dicionários do python
            #updating statistics
            bestFitness, bestIndividual = self.__getBestFitness_and_individual(newPopulation)
            populationMean = self.__calculateMean(newPopulation)
            print(f"""-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            \t\t\t\t\t\t\t\tGERAÇÃO{i}
            •melhor indivíduo: {bestIndividual}
                •aptidão: {bestFitness}
            •aptidão média: {populationMean}""")
            
            

    #private methods
    def __getBestFitness_and_individual(self,population:List[List[Tuple[int,int]]]) -> List[Tuple[int, int]]:
        return min(population, key=lambda individual: (self.calcTotalFlowCost(individual),individual))

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

    def __genInitPopulation(self, lengthPop:int) -> List[List[Tuple[int,int]]]:
        initPop:List[List[Tuple[int,int]]] = []
        for i in range(lengthPop):
            individual = self.__genRandomIndividual()
            initPop.append(individual)
        return initPop

    def __randomNumbers(self, rangeLimit:int, lenList:int) -> List[int]:
        randomlySelected = []

        while len(randomlySelected) != lenList:
            randomElement = random.randint(0,rangeLimit)
            if randomElement in randomlySelected:
                continue
            randomlySelected.append(randomElement)

        return randomlySelected

    def __findLocal(self, locations:List[Tuple[int,int]], facility:int):
        #discovers where a facility is located
        return locations[facility]

    def __calculateMean(self, population:List[List[Tuple[int,int]]], n) -> float :
        """
        This method is pretty slow, because we are re-calculating everything that was already calculated, but is simplier to implement.
        If the processing take too much time, I'll implement some cache mecanism. While I was writting this, I noticed I am sorting a
        lot, and this taked O(n logn), it would be faster if the lists were already sorted, but I'll check this latter.
        """
        mean:float = 0
        for i in range(n):
            mean += self.calcTotalFlowCost(population)
        
        return mean/n

    """
    def swap(self, l1:List[Any], l2:List[Any], i:int, j:int=None):
        if j == None:
            j = i
        
        temp = l1[i]
        l1 = 
    """



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
        #(#,1): 1,
    }
    allocate = ["A","B","C"]

    myPQA = PQA(locals_,flows,distancies,allocate)
    print(myPQA.calcSingularFlowCost(0,1,myPQA.locals_))
    print(myPQA.calcTotalFlowCost(myPQA.locals_))

test()

"""

alocação = [(x,y), (x1,y1), (x2,y2), (x3,y3)]
           [  0       1        2        3

alocação[i]
"""
