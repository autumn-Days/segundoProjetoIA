from PQA import *
import contextlib 

    
def test():
    amountGenes = [20]
    amountGenerations = [150]
    populationSizes = [40,60,80]
    txsElitismo = [0.05, 0.08, 0.1]
    txsMutation = [0.2,0.4,0.8]
    
    
    for amountG in amountGenes:
    
        locals_ = genRandomLocals(amountG)
        allocate = locals_
        eucDistancies = eucDistCartesianProduct(locals_)
        flows = genRandomFlows(amountFlows=amountG, maxFlowValue=amountG*2)
        myQPA = PQA(locals_, flows, eucDistancies, allocate)
        
        for amountGeneration in amountGenerations:
            for populationSize in populationSizes:
                for txElitismo in txsElitismo:
                    for txMutation in txsMutation:
                        with open(f"Gns{amountG}_Gen{amountGeneration}_pop{populationSize}_elit{txElitismo}_m{txMutation}.txt", "w") as file:                        
                            print("processando...")
                            with contextlib.redirect_stdout(file):
                                print(f"-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\nQUANT. GEN.: {amountG}\nQUANT. GER.: {amountGeneration}\nPOP. TAM.:{populationSize}\nTx. ELIT:{txElitismo}\nTX. MUT.:{txMutation}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
                                myQPA.doOperation("rankingSel", "crossoverAroundPoint", "swapMutation", "elitismWithDiversity", populationSize, amountGeneration,txMutation,math.ceil(txElitismo*populationSize))


test()
