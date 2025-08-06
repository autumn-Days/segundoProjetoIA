import contextlib
from PQA import *
from generateInput import *
from SERIALIZER import *
import time

def teste3():
    locals_ = genRandomLocals(10)
    eucDistancies = eucDistCartesianProduct(locals_)
    flows = genRandomFlows(amountFlows=10,maxFlowValue=20)

    mySerializer = DataHandler(locals_, eucDistancies, flows)
    mySerializer.serialize("inputTeste3.txt")    
    myPQA = PQA(locals_,flows,eucDistancies)

    elites = ["elitismWithDiversity", "simpleElitism"]

    limInf = 1
    limSup = 21

    for elite in elites:
        limInf = 1
        while limInf != limSup:
            with open(f"t3_{limInf}_{elite}.txt", "w") as file:
                print(f"t3_{limInf}_{elite}")
                with contextlib.redirect_stdout(file):
                     
                    print(f"""
SELECTION METHOD: Tournament
TOURNAMENT SIZE: 6
POPULATION SIZE: 20
GEN. AMOUNT: 100
MUTATION RATE: 0.3
ELITISM RATE: 0.1*20
crossoverAroundPoint
inversionMutation
{elite}
""")
                    start = time.time()
                    try:
                        myPQA.doOperation("tournamentSel","crossoverAroundPoint","inversionMutation",elite,20,100,0.3,2,tournamentSize=3)
                    except IndexError:
                        continue
                    end = time.time()
                    print(f"-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n+TEMPO DE EXECUÇÃO:{end-start} segs")
                    limInf +=1

teste3()
