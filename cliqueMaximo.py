import networkx as nx
import time
from datetime import datetime
#from guppy import hpy
import os
import sys
import re
from operator import itemgetter

Grafo = nx.Graph
max = 0
elementosClique = []
vizinhos = {}

def inicio():
    global Grafo
    global vizinhos
    end = None

    #nomeCaminhoArq = 'C:/Users/Barbara/Dropbox/UFMG/PAA/Projeto Final/Entrega 2/testes preliminares/bases/1684.edges'
    nomeCaminhoArq = str(sys.argv[1])
    resultados = re.findall(r'\d+', nomeCaminhoArq)
    verticeAddBaseFacbook  = resultados[-1]

    #arq = open(str(sys.argv[1]), 'rb')
    arq = open(nomeCaminhoArq, 'rb')

    print("1 Arquivo")
    print(verticeAddBaseFacbook+".edges")

    #Leitura do arquivo
    G = nx.read_edgelist(arq)

    #para cada vértice, vou adicionar a aresta com vértice 0 - orientacao da base

    vertices = [x for x in nx.nodes(G)]
    for n in vertices:
        G.add_edge(verticeAddBaseFacbook, n)

    print("2 Vertice Orign")
    print(nx.number_of_nodes(G))

    print("3 Arestas Orign")
    print(nx.number_of_edges(G))

    print("4 media")
    print("0.00")

    print("5 Densidade")
    print("%.4f" % nx.density(G))

    print("6 Vertice Utiliz")
    print(nx.number_of_nodes(G))

    print("7 Arestas Orign")
    print(nx.number_of_edges(G))

    print("8 Desvio Padrao")
    print("0.00")

    #Congela Grafo
    nx.freeze(G)

    Grafo = G

    #Lista de tuplas(vertice, grau)
    grafosList = list(G.degree)

    #ordenação crescente pelo grau, depois pelo id do vertice
    grafosList.sort(key=itemgetter(1,0))

    vizinhosOrdenados = {}
    for node in grafosList:
        vizinhosVertice = list(Grafo.neighbors(node[0])) #vizinhos do vertice corrente
        vizinhosPeloGrau = [x for x in Grafo.degree if x[0] in vizinhosVertice] #viznhos encontrados com o grau, pra poder ordenar
        vizinhosPeloGrau.sort(key=itemgetter(1, 0)) #odena pelo grau e depois pelo ID
        vizinhosOrdenados[node[0]] = [x[0] for x in vizinhosPeloGrau] #adicona no map

    vizinhos = vizinhosOrdenados

    return grafosList

def clique(S, tamanho, cliquesTemp):
    global Grafo
    global max
    global elementosClique
    global vizinhos

    if(len(S) == 0):
        if(tamanho > max):
            max = tamanho
            elementosClique = cliquesTemp[-max:]; #pego os max elementos para tras, pois eles fazem parte do meu clique
        return
    while(len(S) != 0):
        if((tamanho + len(S)) <= max):
            return
        i = S[0]
        S.remove(i)
        cliquesTemp.append(i);
        clique(list(set(S).intersection(set(list(vizinhos[i])))), tamanho + 1, cliquesTemp)

#h = hpy()
#h.setrelheap()

tempoInicio = time.time()
lista = [x[0] for x in inicio()]
clique(lista, 0, [])
print('9 CLIQUE MAX ')
print(str(max))
#print('Elementos MAX - ' + str(elementosClique))
#cliques = list(find_cliques(Grafo))
#l = [len(x) for x in cliques]
#print('Outro: ' + str(sorted(l)[-1:]))
tempoFim = time.time()
print("10 Tempo")
print("%.4f" % (tempoFim - tempoInicio))

#x = h.heap() #depois do coigo
#print('memoria: '+str(x.size))

#print("11 Memoria")
#print(str(x.size))

#print ('memoria'+ str(x))

