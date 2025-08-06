from PQA import *
from generateInput import *
import math

locals_ = genRandomLocals(10)
locate = locals_
flows = genRandomFlows(amountFlows=10, maxFlowValue=20)
eucDistancies = eucDistCartesianProduct(locals_)

myPQA = PQA(locals_, flows, eucDistancies)

#basta copiar o nome do método e passar como umas string para "doOperation" (que é o equivalente a função evolve)
#os valores numéricos dizem respeito a quantidade de indivíduos na população, quantidade de gerações limite,
#taxa de mutação e taxa de elitismo (10% de 20 indivíduos da população)
#myPQA.doOperation("rankingSel", "crossoverAroundPoint", "swapMutation", "elitismWithDiversity", 20, 15, 0.3, math.ceil(0.1*20))
myPQA.doOperation("tournamentSel", "crossoverAroundPoint", "inversionMutation", "simpleElitism", 20, 200, 0.3, 2,tournamentSize=3) #math.ceil(0.1*20), tournamentSize=5)
