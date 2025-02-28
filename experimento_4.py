import random

from typing import List, Tuple, Dict
from generateInput import genRandomLocals, eucDistCartesianProduct, genRandomFlows
from PQA import *

# 1. Definição de parâmetros constantes
populationSize = 40
genLimit = 100
mutationTax = 0.2
elitismTax = 2
tournamentSize = 5
n = 10  # Tamanho da instância do PQA
numExecucoes = 20 #Número de repetições do experimento

# 2. Definição das funções de seleção e mutação a serem testadas
selecao_metodos = ["tournamentSel", "rankingSel"]
mutacao_metodos = ["swapMutation", "inversionMutation"]

# 3. Função para gerar uma instância aleatória do PQA
def gerar_instancia_pqa(n: int) -> PQA:
    locals_ = genRandomLocals(n) #Gera n locais aleatórios
    distancies = eucDistCartesianProduct(locals_) #Calcula a distancia euclidiana entre os pontos
    flows = genRandomFlows(amountFlows=n, maxFlowValue=2*n) #Gera matriz de fluxo aleatória
    return PQA(locals_=locals_, flows=flows, distancies=distancies)

def executar_algoritmo_genetico(pqa: PQA, selecao_metodo: str, mutacao_metodo: str) -> float:
    """Executa o algoritmo genético uma vez e retorna o fitness do melhor indivíduo."""
    pqa.doOperation(
        selectionMethod=selecao_metodo,
        crossOverMethod="crossoverAroundPoint",
        mutationMethod=mutacao_metodo,
        elitismPropagationMethod="simpleElitism",
        populationSize=populationSize,
        genLimit=genLimit,
        mutationTax=mutationTax,
        elitismTax=elitismTax,
        tournamentSize=tournamentSize
    )
    # Acessando o método privado com a sintaxe correta
    # E pegando apenas o fitness (primeiro elemento da tupla retornada)
    population = pqa._PQA__genInitPopulation(populationSize)
    best_fitness, _ = pqa._PQA__getBestFitness_and_individual(population)
    return best_fitness

# 4. Preparação para salvar os resultados em um arquivo
nome_arquivo = "./resultados_experimento_4.txt"

with open(nome_arquivo, "w") as arquivo:
    arquivo.write("Resultados do Experimento:\n")
    arquivo.write(f"Tamanho da população: {populationSize}, Limite de gerações: {genLimit}, Taxa de mutação: {mutationTax}, Taxa de elitismo: {elitismTax}, Tamanho do torneio: {tournamentSize}\n")

# 5. Execução do experimento
instancia_pqa = gerar_instancia_pqa(n) #Gera uma instancia do PQA para manter a entrada constante

for selecao_metodo in selecao_metodos:
    for mutacao_metodo in mutacao_metodos:
        resultados = []
        with open(nome_arquivo, "a") as arquivo:
            arquivo.write(f"\nResultados para Seleção: {selecao_metodo}, Mutação: {mutacao_metodo}\n")
        for i in range(numExecucoes): #Repete o experimento 20 vezes
            #Gera uma nova população inicial para cada execução
            instancia_pqa = gerar_instancia_pqa(n)

            #Executa o algoritmo genético
            fitness = executar_algoritmo_genetico(instancia_pqa, selecao_metodo, mutacao_metodo)
            resultados.append(fitness)

            print(f"Execução {i+1}: Fitness (Seleção={selecao_metodo}, Mutação={mutacao_metodo}) = {fitness}")
            with open(nome_arquivo, "a") as arquivo:
                arquivo.write(f"Execução {i+1}: Fitness = {fitness}\n")

        # 6. Análise dos resultados
        media = sum(resultados) / len(resultados)
        print(f"\nMédia do fitness (Seleção={selecao_metodo}, Mutação={mutacao_metodo}): {media}")
        with open(nome_arquivo, "a") as arquivo:
            arquivo.write(f"Média do fitness: {media}\n")

print(f"\nResultados salvos em {nome_arquivo}")