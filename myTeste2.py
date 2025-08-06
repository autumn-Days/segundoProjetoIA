import contextlib
from PQA import *
from generateInput import *
from SERIALIZER import *
import time

def teste2():
    locals_ = genRandomLocals(10)
    eucDistancies = eucDistCartesianProduct(locals_)
    flows = genRandomFlows(amountFlows=10,maxFlowValue=20)

    mySerializer = DataHandler(locals_, eucDistancies, flows)
    mySerializer.serialize("inputTeste2.txt")    
    myPQA = PQA(locals_,flows,eucDistancies)

    cruzamentos = ["crossoverAroundPoint", "uniformCrossover"]
    
    limInf = 1
    limSup = 21

    for cruzamento in cruzamentos:
        limInf=1
        while limInf != limSup:
            with open(f"t2_{limInf}_{cruzamento}.txt", "w") as file:
                print(f"t2_{limInf}_{cruzamento}")
                with contextlib.redirect_stdout(file):
                     
                    print(f"""
SELECTION METHOD: Ranking
POPULATION SIZE: 20
GEN. AMOUNT: 100
MUTATION RATE: 0.3
ELITISM RATE: 0.1*20
{cruzamento}
swapMutation
simpleElitism
""")
                    start = time.time()
                    try:
                        myPQA.doOperation("rankingSel",cruzamento,"swapMutation","simpleElitism",20,100,0.3,2,tournamentSize=6)
                    except IndexError:
                        continue
                    end = time.time()
                    print(f"-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n+TEMPO DE EXECUÇÃO:{end-start} segs")
                    limInf +=1

teste2()
