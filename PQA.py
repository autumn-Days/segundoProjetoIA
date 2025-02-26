from typing import *
from generateInput import *

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

"""
Se em algm momento vc receber um erro do tipo "KeyError: ((8, 16), (8, 16))",
dps de algms inferências lógicas, é possível concluir que vc tem um individuo
como locais repetidos. Portanto, é preciso verificar se um crossover ou uma 
propagação de elitismo gera locais repetidos.

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
        
        flowCost:int = None
        
        try:
            flowCost = self.flows[(facility1,facility2)]
        except KeyError:
            flowCost = self.flows[(facility2,facility1)]
        
        location1:Tuple[int,int] = self.__findLocal(locations,facility1)
        location2:Tuple[int,int] = self.__findLocal(locations,facility2) 
        
        eucDistance:int = None
        
        try:
            eucDistance = self.distancies[(location1,location2)]
        except KeyError:
            eucDistance = self.distancies[(location2,location1)]
        
        return flowCost * eucDistance

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
        tournament:List[List[int,int]] = random.sample(population,tournamentSize)
        """
        What the line bellow basically does is: It associates, for every individual
        in the population a value `key`, which is its fitness function, and the indi-
        vidual with the highest fitness function (which, in this case, means it has the
        lowest "calcTotalFlowCost") from all the others guys that make up the tournment
        """
        bestIndividual = min(tournament, key = lambda individual: self.calcTotalFlowCost(individual))
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
        
        parent1_firstHalf = parent1[:point]
        parent1_secondHalf = parent1[point:]
        
        parent2_firstHalf = parent2[:point]
        parent2_secondHalf = parent2[point:]
        
        reservaGenesChild1 = parent2_firstHalf + parent1_secondHalf
        reservaGenesChild2 = parent1_firstHalf + parent2_secondHalf
        
        n = len(reservaGenesChild1)
        m = len(reservaGenesChild2)
        
        removedGenesReservaGenesC1 = []
        removedGenesReservaGenesC2 = []
        
        
        child1 = parent1_firstHalf 
        child2 = parent2_firstHalf
        
        #selecting the second half of child1
        for gene in parent2_secondHalf:
            if gene in child1:
                for i in range(n):
                    if reservaGenesChild1[i] in child1:
                        removedGenesReservaGenesC1.append(i)
                        continue
                    child1.append(reservaGenesChild1[i])
                    #reservaGenesChild1.pop(i)
                    
                    #n -= len(removedGenesReservaGenesC1) + 1
                    
                    #for index in removedGenesReservaGenesC1:
                    #    reservaGenesChild1.pop(index)
                    #removedGenesReservaGenesC1.clear()
                    break
            else:
                child1.append(gene)
                
        #selecting the second half of child2
        for gene in parent1_secondHalf:
            if gene in child2:
                for i in range(m):
                    if reservaGenesChild2[i] in child2:
                        removedGenesReservaGenesC2.append(i)
                        continue
                    child2.append(reservaGenesChild2[i])
                    #reservaGenesChild2.pop(i)
                    
                    #m -= len(removedGenesReservaGenesC2) + 1
                    
                    #for index in removedGenesReservaGenesC2:
                    #    reservaGenesChild2.pop(index)
                    #removedGenesReservaGenesC2.clear()
                    break
            else:
                child2.append(gene)

            
        #selecting the second half of child2
        
        #child2_part1 = parent2[:point] + parent1[point:]

        

        return (child1,child2)

    def uniformCrossover(self, parent1: List[Tuple[int, int]], parent2: List[Tuple[int, int]]) -> Tuple[Tuple[int,int], Tuple[int,int]]:
        """
        There is the possibility that the parents have genes that are equal to one another
        and there is the possibility that, when performing the cross over, a child end up
        having equal genes. To put matters more precisely, the "allocate" function will end
        up with equal locations. This is not necessarily wrong, but in this problem we are
        dealing with locations that can only have one facility associated to them.
        
        To solve this the idea is the following: Instead of simply making:

            for i in range(n):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        return (child1,child2)            
            
    
        If the gene from the parent was already included in the child, then I will
        select the next element. Simple.
        """
        n = len(parent1)

        child1 = []
        child2 = []

        j:int = None

        for i in range(n):
            j = i
            if random.random() < 0.5:
                while parent1[j] in child1:
                    j = (j+1)%n
                child1.append(parent1[j])
                j = i
                while parent2[j] in child2:
                    j =(j+1)%n
                child2.append(parent2[j])
            else:
                while parent2[j] in child1:
                    j = (j+1)%n
                child1.append(parent2[j])
                j = i
                while parent1[j] in child2:
                    j = (j+1)%n
                child2.append(parent1[j])
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
        
        n= len(individual)
        
        while startIndex == endIndex:
            startIndex = random.randint(0, n-2)
            endIndex = random.randint(1, n-1)

        individual[startIndex:endIndex] = reversed(individual[startIndex:endIndex])
        return individual

    #elitismPropagation

    def simpleElitism(self, previousPopulation:List[List[Tuple[int, int]]], currentPopulation:List[List[Tuple[int,int]]], elitAmount:int) -> List[List[Tuple[int,int]]]:
        sortedPreviousPopulation = sorted(previousPopulation, key= lambda individual: self.calcTotalFlowCost(individual))
        sortedCurrentPopulation = sorted(currentPopulation, key= lambda individual: self.calcTotalFlowCost(individual))
        
        aptIndividuals = []
        
        #esse laço abaixo é para evitar que 2 individuos iguais estejam na mesma população
        #se não, o crossover entre eles sempre vai produzir eles próprios
        j = 0
        for i in range(elitAmount):
            for j in range(len(sortedPreviousPopulation)):
                if sortedPreviousPopulation[j] not in currentPopulation:
                    aptIndividuals.append(sortedPreviousPopulation[j])
                    sortedPreviousPopulation.pop(j)
                    break
        

        lessAptIndividuals = sortedCurrentPopulation[-elitAmount:]
        indexiesLessAptIndividuals = []
        
        for i in range(len(lessAptIndividuals)):
            lessAptIndividual:List[Tuple[int,int]] = lessAptIndividuals[i]
            indexiesLessAptIndividuals.append(currentPopulation.index(lessAptIndividual))
            
        currentPopulation = self.__replaceByAptPrevious(indexiesLessAptIndividuals,aptIndividuals, currentPopulation)


        return currentPopulation
    
    def __replaceByAptPrevious(self, indexies:List[int], aptIndividuals, currentPopulation):
        
        aptIndividualsSize = len(aptIndividuals)
        
        for i in range(len(indexies)):
            currentPopulation[indexies[i]] = aptIndividuals[i] 
        
        return currentPopulation
            
        

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
                amountGroupA = int(oldIndividualAmount/2)
                amountGroupB = amountGroupA
            else:
                amountGroupA = int(math.floor(oldIndividualAmount/2))
                amountGroupB = int(math.ceil(oldIndividualAmount/2))
            
            
            
            
            nonElitePrevious = sortedPreviousPopulation[amountGroupA:]
            nonElitePrevious2 = []
            
            elitePrevious = []
            self.__adder(amountGroupA, len(sortedPreviousPopulation), sortedPreviousPopulation, currentPopulation, elitePrevious)

            
            while len(nonElitePrevious2) == 0: #por algum motivo misterioso, às vezes, msm dps do loop de dentro desse while, nonElitePrevious2 continuava vazio. 1/3 vezes dava erro de indexOutOfRange por causa disso. Decidi resolver na marra e funcionou
                for i in range(amountGroupB):
                    index = random.randint(0,len(nonElitePrevious)-1)
                    if nonElitePrevious[index] not in currentPopulation:
                        nonElitePrevious2.append(nonElitePrevious[index])
                

            """
            The list bellow corresponds to the indexies of the elements that are going to be substituted by the individuals of
            groups A and B,
            """
            
            #Início: Substitui os piores individuos da atual pelos melhores da anterior
            indexiesLessApt = []
            for ind in sortedCurrentPopulation[-amountGroupA:]:
                indexInd = currentPopulation.index(ind)
                indexiesLessApt.append(indexInd)
            self.__replaceByAptPrevious(indexiesLessApt, elitePrevious, currentPopulation)
            #fim
            
            #Início: Substitui "m" não melhores aleatórios da anterior por "m" não melhores da atual
            
            #fim
            elements2replace:List[int] = self.__randomNumbers(len(currentPopulation),amountGroupB)

                
            for i in range(amountGroupB):
                #a = currentPopulation[indexCurrentInd]
                #try :
                #    b = nonElitePrevious2[i]
                #except IndexError:
                #    print("oi")
                #    print("ui")
                #try :
                print(len(currentPopulation))
                print(elements2replace[i])
                try :
                    currentPopulation[elements2replace[i]] = nonElitePrevious2[i]
                except IndexError:
                    print("IO")
                    print("io")
            return currentPopulation

    #main method

    def doOperation(self, selectionMethod:str, crossOverMethod:str,
                    mutationMethod:str, elitismPropagationMethod:str,
                    populationSize:int, genLimit:int, mutationTax:int,
                    elitismTax:int,tournamentSize:int=None):

        selectionMethod:Callable =              getattr(self, selectionMethod,          None)
        crossOverMethod:Callable =              getattr(self, crossOverMethod,          None)
        mutationMethod:Callable =               getattr(self, mutationMethod,           None)
        elitismPropagationMethod:Callable =     getattr(self, elitismPropagationMethod, None)

        oldPopulation:List[List[Tuple[int,int]]] = self.__genInitPopulation(populationSize)

        #statistics
        fittestIndividual:List[Tuple[int,int]] = None
        bestFitness:int = float('inf')
        mediumFitness:int = 0


        n = len(oldPopulation)

        for i in range(genLimit):
            newPopulation:List[List[Tuple[int,int]]] = []
            """
            Se a população for pequena e o tamanho do torneio for pequeno, então os mesmos pais tem grandes chances de serem selecionados novamente, o que gera filhos iguais, por
            causa 
            
            electedParents:List[Tuple[List[Tuple[int,int],List[Tuple[int,int]]]] = [] #Uma lista cujo elementos são tuplas 
            """
            
            
            while len(newPopulation) <= n:
                parent1=None
                parent2=None
                while parent1 == parent2 :
                    parent1 = selectionMethod(oldPopulation, tournamentSize)
                    if ((parent1 != parent2) and (parent2 != None)):
                        break
                    parent2 = selectionMethod(oldPopulation, tournamentSize)
                
                
                #verificar se parent1 e parent2 já foram selecionados para um cruzamento, pode ser uma boa idea, mas pode fazer com que o processamento demore mt                
                child1,child2 = crossOverMethod(parent1,parent2)

                newPopulation.extend([child1,child2])
            
            newPopulation = newPopulation[:n]

            #mutation
            if mutationTax != 0:
                for j in range(n):
                    if random.random() <= mutationTax:
                        print("MUTOU")
                        newPopulation[j] = mutationMethod(newPopulation[j])
            #elitism propagation
            if elitismTax != 0:
                newPopulation = elitismPropagationMethod(oldPopulation,newPopulation,elitismTax) #tenho que ver se isso não gera um problema de referência nos dicionários do python
            
            #updating statistics
            bestFitness, bestIndividual = self.__getBestFitness_and_individual(newPopulation)
            populationMean = self.__calculateMean(newPopulation, n)
            print(f"""-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            \t\t\t\t\t\t\t\tGERAÇÃO{i}
            •melhor indivíduo: {bestIndividual}
                •aptidão: {bestFitness}
            •aptidão média: {populationMean}""")
        
        return (fittestIndividual, bestFitness, mediumFitness)
            
            

    #private methods
    def __getBestFitness_and_individual(self,population:List[List[Tuple[int,int]]]) -> List[Tuple[int, int]]:
        bestIndividual = min(population, key=lambda individual: self.calcTotalFlowCost(individual))
        return (self.calcTotalFlowCost(bestIndividual),bestIndividual) 

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
            while individual in initPop:
                individual = self.__genRandomIndividual()
            initPop.append(individual)
        return initPop

    # self.__randomNumbers(lenSortedCurrentPopulation,amountGroupB)
    def __randomNumbers(self, rangeLimit:int, lenList:int) -> List[int]:
        randomlySelected = []

        while len(randomlySelected) != lenList:
            randomElement = random.randint(0,rangeLimit-1)
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
            mean += self.calcTotalFlowCost(population[i])
        
        return mean/n

    """
    def swap(self, l1:List[Any], l2:List[Any], i:int, j:int=None):
        if j == None:
            j = i
        
        temp = l1[i]
        l1 = 
    """

    def __adder(self, amount2add, listRefSize, oldSortedPop, newPop, list2add):
        for i in range(amount2add):
            for j in range(listRefSize):
                if oldSortedPop[j] not in newPop:
                    list2add.append(oldSortedPop[j])
                    oldSortedPop.pop(j)
                    break


#teste com valores simbólicos
def test00():
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

#teste com valores
def test01():
    locals_ = genRandomLocals(10)
    allocate = locals_
    eucDistancies = eucDistCartesianProduct(locals_)
    flows = genRandomFlows(amountFlows=5,maxFlowValue=10)
    myQPA = PQA(locals_, flows, eucDistancies, allocate)
    print(myQPA.calcTotalFlowCost(myQPA.locals_))
    #por algum motivo só pega quando genLimit == populationSize, tenho que ver o pq
    #myQPA.doOperation("tournamentSel", "crossoverAroundPoint", "swapMutation", "simpleElitism", 25, 100, 0.2, 2,tournamentSize=5)
    myQPA.doOperation("rankingSel", "uniformCrossover", "inversionMutation", "elitismWithDiversity", 10, 100, 0.2, 2,tournamentSize=5)

test00()
test01()



"""

alocação = [(x,y), (x1,y1), (x2,y2), (x3,y3)]
           [  0       1        2        3

alocação[i]
"""
