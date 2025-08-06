import contextlib
from PQA import *
from generateInput import *
from SERIALIZER import *
import time

def teste1():
    """
    locals_ = genRandomLocals(10)
    eucDistancies = eucDistCartesianProduct(locals_)
    flows = genRandomFlows(amountFlows=10,maxFlowValue=20)

    mySerializer = DataHandler(locals_, eucDistancies, flows)
    mySerializer.serialize("inputTeste1.txt")    
    myPQA = PQA(locals_,flows,eucDistancies)
    """
    locals_ = None
    eucDistancies = None
    flows = None
    
    mySerializer = DataHandler([],[],[])
    mySerializer.deserialize("inputTeste1.txt")
    
    locals_ = mySerializer.locals_
    flows = mySerializer.flows
    eucDistancies = mySerializer.eucDistancies
    
    myPQA = PQA(locals_,flows,eucDistancies)

    #selections = ["tournamentSel", "rankingSel"]
    selections = ["rankingSel"]
    for sel in selections:
        for i in range(1,7):
            with open(f"t1_{i}_{sel}.txt", "w") as file:
                print(f"t1_{i}_{sel}")
                with contextlib.redirect_stdout(file):
                    tournamentSize ="\n"
                    if sel == "tournamentSel":
                        tournamentSize = "\nTOURNAMENT SIZE: 6\n\n"
                     
                    print(f"""
SELECTION METHOD: {sel}
POPULATION SIZE: 20
GEN. AMOUNT: 100
MUTATION RATE: 0.3
ELITISM RATE: 0.1*20{tournamentSize}
crossoverAroundPoint
swapMutation
elitismWithDiversity
""")
                    start = time.time()
                    myPQA.doOperation(sel,"crossoverAroundPoint","swapMutation","elitismWithDiversity",20,100,0.3,2,tournamentSize=6)
                    end = time.time()
                    print(f"-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n+TEMPO DE EXECUÇÃO:{end-start} segs")

teste1()