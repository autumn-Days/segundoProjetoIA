import contextlib
from PQA import *
from generateInput import *
from SERIALIZER import *
import time
import multiprocessing 


popSize2generation = {
    20:100,
    40:125,
    60:150,
    80:200,
}

MSG_TIME_OUT = "O ALGORITMO EXCEDEU O LIMITE DE EXECUÇÃO\n"
divisor = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"

def worker(obj, methodArgs:List):
    populationSize = methodArgs[0]
    amountGenerations = methodArgs[1]
    tournamentSize = methodArgs[2]
    elitismRate = methodArgs[3]
    mutationRate = methodArgs[4]

    selection = methodArgs[5]
    crossOver = methodArgs[6]
    mutation = methodArgs[7]
    elitism = methodArgs[8]

    obj.doOperation(selection, crossOver, mutation, elitism, populationSize, amountGenerations, mutationRate, elitismRate, tournamentSize)

def runAlgo(obj, argsAlgorithm:List[int],stopProcessingEvent):
    start = time.time()
    process2 = multiprocessing.Process(target=worker, args=(obj,argsAlgorithm))
    process2.start()

    while process2.is_alive():
        if stopProcessingEvent.is_set():
            process2.terminate()
            process2.join()
            return (start - time.time() -1) 
        #time.sleep(0.3) #Só para não consumir muito processamento 
    process2.join()
    return (start - time.time() - 1) #subtraio 1, pois houve um delay de cerca de 1 seg para se detectar que o alg. terminou

def runAlgoWithTimeout(obj, args, timeOut):
    stopProcessingEvent = multiprocessing.Event()
    """
    As duas linhas abaixo são responsáveis por criar 2 processos que irão complartilhar uma lista entre sí. Essa lista
    guardará o tempo de execução em que o algoritmo levou para rodar.
    """
    status_tempoExecucao = multiprocessing.Manager()
    resultado = status_tempoExecucao.list([None])

    def monitorarExecucao():
        resultado[0] = runAlgo(obj, args, stopProcessingEvent)

    process = multiprocessing.Process(target=monitorarExecucao)
    process.start()
    
    process.join(timeOut) #Se o tempo estourar, então o "caller process" continua, se o processo chamado retornar, o timeOut não acontece

    if process.is_alive():
        stopProcessingEvent.set()
        time.sleep(1) #o tempo dele retornar o resultado
        process.terminate()
        process.join()

    return resultado[0]
"""
    selection = methodArgs[5]
    crossOver = methodArgs[6]
    mutation = methodArgs[7]
    elitism = methodArgs[8]
"""
def main():
    ganhador = None
    statusCapeoes = [True,True,True,True]
    algsCampeoes = [
        ["tournamentSel",       "crossoverAroundPoint",  "swapMutation",     "elitismWithDiversity"],
        ["rankingSel",          "crossoverAroundPoint",  "swapMutation",      "simpleElitism"],
        ["tournamentSel",       "crossoverAroundPoint",  "inversionMutation", "elitismWithDiversity"],
        ["rankingSel",          "uniformCrossover",      "swapMutation",      "elitismWithDiversity"]
    ]

    amountGenes = 0
    populationSize = 0
    amountGenerations = 0
    tournamentSize = None

    rodadas = 0

    while True in statusCapeoes: #Se algm dos 4 algoritmos der 10 min de execução, já tá bom
        amountGenes += 10
        if amountGenes <= 40:
            populationSize = amountGenes*2
        else:
            populationSize += 20

        elitismRate = populationSize//10
        
        amountGenerations = popSize2generation.get(populationSize, amountGenerations+40) #com 100 genes, leva 240, gerações, com 120, 280, etc
        """
            populationSize = methodArgs[0]
            amountGenerations = methodArgs[1]
            tournamentSize = methodArgs[2]
            elitismRate = methodArgs[3]
            mutationRate = methodArgs[4]
        """

        locals_ = genRandomLocals(amountGenes)
        eucDistancies = eucDistCartesianProduct(locals_)
        flows = genRandomFlows(amountFlows=amountGenes,maxFlowValue=amountGenes*2)

        mySerializer = DataHandler(locals_, eucDistancies, flows)
        mySerializer.serialize(f"inputTeste5_{amountGenes}Locals_{populationSize}popSize.txt")    
        myPQA = PQA(locals_,flows,eucDistancies)

        for i in range(len(algsCampeoes)):
            if i == 2:
                tournamentSize = (3*populationSize)//20 
            else:
                tournamentSize = (3*populationSize)//10
            
            args = [populationSize, amountGenerations, tournamentSize, elitismRate,0.3] + algsCampeoes[i]

            fileName =f"algChamp{i+1}_{amountGenes}genes_{populationSize}popSize.txt" 
            with open(fileName, "w") as file:
                print(amountGenes,",",algsCampeoes[i],":",statusCapeoes[i])
                with contextlib.redirect_stdout(file):
                    print(f"""
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
ALG: {algsCampeoes[i]}
AMOUNT GENES: {amountGenes}
POPULATION SIZE: {populationSize}
tournamentSize: {tournamentSize} (if applicable)
ELITISM RATE: {elitismRate}
AMOUNT GENERATIONS: {amountGenerations}
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
                    if (statusCapeoes[i] == False):
                        print("DESCLASSIFICADO")
                    else:
                        ganhador = algsCampeoes[i]
                        """
                        Eu preciso criar duas threads ou dois processos para essa parte, de tal modo que
                        a primeira vai executar essa parte e a segunda vai contar quanto tempo a primeira está
                        levando, de tal modo que se o tempo limite de 600 segundos for atingido, a execução da 
                        primeira thread ou processo é interrompido 
                        """
                        """
                        Código antigo:

                        start = time.time()
                        exec(algsCampeoes[i])
                        end = time.time()
                        print(f"-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n+TEMPO DE EXECUÇÃO:{end-start} segs")
                        if not isTimeLimitReached:
                           
                            #Essa condição vai impedir a condição em que o 1° alg estoura o lim. de tempo
                            #mas o 2° não.
                            
                            elapsedTime = end - start
                            if elapsedTime >= 600:
                                statusCapeoes[i] = DESQUALIFICADO
                        """
                        start = time.time()
                        timeSpent = runAlgoWithTimeout(myPQA,args,601)#20 min é o máximo que pode, então eu ponho que o time limit é 10min 1seg
                        end = time.time()
                        timeSpent = end-start
                        #statusCapeoes[i] = statusAlg
                        if timeSpent > 600:
                            print(f"{divisor}{MSG_TIME_OUT}{divisor}+TEMPO DE EXECUÇÃO:{timeSpent} segs")
                            statusCapeoes[i] = False
                        else:
                            print(f"{divisor}+TEMPO DE EXECUÇÃO:{timeSpent} segs")
        rodadas +=1
    print(f"Após {rodadas} rodadas, o campeonato chega ao fim!\n E o ganhador foi {ganhador}!")

if __name__ == "__main__":
    main()
