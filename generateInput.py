import random
import math
from typing import *

"""
Funções verificadas:
    -eucDist
    -genRandomLocals
    -eucDistCartesianProduct
    -displayDistanciesMatrix
"""

def eucDist(local1:Tuple[int,int], local2:Tuple[int,int]):
    x1,y1 = local1
    x2,y2 = local2
    return math.floor(math.sqrt(pow(abs(x1-x2),2) + pow(abs(y1-y2),2)))

def genRandomLocals(amountLocals:int) ->List[Tuple[int,int]]:
    #"locals" é uma palavra reservada, então eu pôs um underline no final
    locals_:List[int] = []
    for i in range(amountLocals):
        local = (random.randint(0,30), random.randint(0,30))
        while local in locals_:
            local = (random.randint(0,30), random.randint(0,30))
        locals_.append(local)
    return locals_
            
def eucDistCartesianProduct(localities:List[Tuple[int,int]]) -> Dict[Tuple[Tuple[int,int],Tuple[int,int]],int]:
    """
    {(Local1,Local2):dist}
    {((x1,y1),(x2,y2)):dist}

    Essa função será responsável por cálcular a distância euclidiana de todos os pares de locais possíveis.
    Essa função não calcula a distância euclidiana de um ponto A até ele mesmo, pois isso seria um desperdício
    de recursos computacionais. Portanto, (A,A) não está no dicionário que representa a matriz das distâncias.
    Logo, o caso em que o termo d(A,A) é calculado para o cálculo do custo do fluxo total tem que ser tratado
    exteriormente.
    """
    distancies: Dict[Tuple[Tuple[int,int],Tuple[int,int]],int] = {}

    for i in range(0,len(localities)):
        for j in range(i+1,len(localities)):
            local1 = localities[i]
            local2 = localities[j]
            distancy = eucDist(local1,local2)

            distancies[(local1,local2)] = distancy
            #Na vdd, não é para adicionar os duplicados. Em última instância, isso gera o dobro do valor esperado no PQA
            #distancies[(local2,local1)] = distancy
    
    return distancies

def genRandomFlows(amountFlows:int) -> Dict[Tuple[int,int],int]:
    """
    {(obj1,obj2):flow}
    {(n1,n2)}:flow
    De forma semelhante a função anterior, não guardo o fluxo de obj_{x} para obj_{x}.
    """
    flows:Dict[Tuple[int,int],int] = {} 
    for i in range(0,amountFlows):
        for j in range(i+1,amountFlows):
            randomFlow = random.randint(1,100)
            flows[(i,j)] = randomFlow
            #Na vdd, não é para adicionar os duplicados. Em última instância, isso gera o dobro do valor esperado no PQA
            #flows[(j,i)] = randomFlow
    return flows

def displayDistanciesMatrix(matrix:Dict[Tuple[Tuple[int,int],Tuple[int,int]],int]) -> None:
    for key, value in matrix.items():
        print(f"[{key[0]},{key[1]}]:{value}")

def displayFlowMatrix(matrix:Dict[Tuple[int,int],int]) -> None:
    for key, value in matrix.items():
        print(f"{key}:{value}")


displayFlowMatrix(genRandomFlows(3))
print("-=-=-=-=-=-=-=-=-=-=")
locals_ = genRandomLocals(3)
print("-=-=-=-=-=-=-=-=-=")
print(locals_)
print("-=-=-=-=-=-=-=-=-=")
displayDistanciesMatrix(eucDistCartesianProduct(locals_))
