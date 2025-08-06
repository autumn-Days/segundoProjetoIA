import contextlib
from PQA import *
from generateInput import *
from SERIALIZER import *
import time

def teste4():
    locals_ = genRandomLocals(10)
    eucDistancies = eucDistCartesianProduct(locals_)
    flows = genRandomFlows(amountFlows=10,maxFlowValue=20)

    mySerializer = DataHandler(locals_, eucDistancies, flows)
    mySerializer.serialize("inputTeste4.txt")    
    myPQA = PQA(locals_,flows,eucDistancies)

    mutations = ["swapMutation", "inversionMutation"]

    for mutation in mutations:
        for i in range(1,21):
            with open(f"t4_{i}_{mutation}.txt", "w") as file:
                print(f"t4_{i}_{mutation}")
                with contextlib.redirect_stdout(file):
                     
                    print(f"""
SELECTION METHOD: Ranking
POPULATION SIZE: 20
GEN. AMOUNT: 100
MUTATION RATE: 0.3
ELITISM RATE: 0.1*20
crossoverUniform
{mutation}
elitismWithDiversity
""")
                    start = time.time()
                    myPQA.doOperation("rankingSel","uniformCrossover",mutation,"elitismWithDiversity",20,100,0.3,2,tournamentSize=6)
                    end = time.time()
                    print(f"-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n+TEMPO DE EXECUÇÃO:{end-start} segs")

teste4()