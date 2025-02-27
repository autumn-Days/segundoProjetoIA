from PQA import *
import contextlib 

    
def test():
    amountGenes = [40,60]
    amountGenerations = [75,150,300]
    
    txElitism  = math.ceil(0.08*40)
    
    for amountG in amountGenes:
    
        locals_ = genRandomLocals(amountG)
        allocate = locals_
        eucDistancies = eucDistCartesianProduct(locals_)
        flows = genRandomFlows(amountFlows=amountG, maxFlowValue=amountG*2)
        myQPA = PQA(locals_, flows, eucDistancies, allocate)
        
        for amountGeneration in amountGenerations:
            with open(f"Gns{amountG}_Gen{amountGeneration}_pop40_elit0.08_m0.2.txt", "w") as file:                        
                print(f"Gns{amountG}_Gen{amountGeneration}")
                with contextlib.redirect_stdout(file):
                    print(f"-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\nQUANT. GEN.: {amountG}\nQUANT. GER.: {amountGeneration}\nPOP. TAM.:40\nTx. ELIT:0.08\nTX. MUT.: 0.2\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
                    myQPA.doOperation("rankingSel", "crossoverAroundPoint", "swapMutation", "elitismWithDiversity", 40, amountGeneration,0.2,txElitism)


test()
