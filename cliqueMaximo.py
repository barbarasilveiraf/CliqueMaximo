import networkx as nx
import time
from math import sqrt
import sys
import os
from guppy import hpy
import re
from operator import itemgetter


Grafo = nx.Graph
max = 0
elementosClique = []
mediaGrauVertices = 0
desvioPadrao = 0
vizinhos = {}

def desvio_padrao(m, g):
    diffMedia = 0
    vertices = [x[0] for x in g]
    for n in vertices[:-1]:
        diffMedia += pow((Grafo.degree[n] - m),2)
    diffMedia /= (len(vertices)-1)
    return sqrt(diffMedia)

def inicio():
    global Grafo
    global mediaGrauVertices
    global desvioPadrao
    global vizinhos

    end = None

    #nomeCaminhoArq = 'C:/Users/Barbara/Dropbox/UFMG/PAA/Projeto Final/Entrega 2/testes preliminares/bases/0.edges'
    nomeCaminhoArq = str(sys.argv[1])
    resultados = re.findall(r'\d+', nomeCaminhoArq)
    verticeAddBaseFacbook  = resultados[-1]

    arq = open(nomeCaminhoArq, 'rb')

    # print("1 Arquivo")
    print(verticeAddBaseFacbook+".edges")

    # Leitura do arquivo
    G = nx.read_edgelist(arq)

    #para cada vertice, vou adicionar a aresta com vetice 0 - orientacao da base

    vertices = [x for x in nx.nodes(G)]
    for n in vertices:
        G.add_edge(verticeAddBaseFacbook, n)

    Grafo = G

    #Congela Grafo
    #nx.freeze(G)

    #Lista de tuplas(vertice, grau)
    grafosList = list(G.degree)

    #ordenacao crescente pelo grau, depois pelo id do vertice
    grafosList.sort(key=itemgetter(1,0))

    vizinhosOrdenados = {}
    for node in grafosList:
        vizinhosVertice = list(Grafo.neighbors(node[0])) #vizinhos do vertice corrente
        vizinhosPeloGrau = [x for x in Grafo.degree if x[0] in vizinhosVertice] #viznhos encontrados com o grau, pra poder ordenar
        vizinhosPeloGrau.sort(key=itemgetter(1, 0)) #odena pelo grau e depois pelo ID
        vizinhosOrdenados[node[0]] = [x[0] for x in vizinhosPeloGrau] #adicona no map

    vizinhos = vizinhosOrdenados

    #pra pegar os vertices ja ordenados pelo grau
    vertices = [x[0] for x in grafosList]

    for n in vertices[:-1]: # -1 pra ignorar o valor mais alto...
        mediaGrauVertices += G.degree[n]
    mediaGrauVertices /= ((nx.number_of_nodes(G)-1)*1.0)

    #calcular o desvio padrao
    desvioPadrao = desvio_padrao(mediaGrauVertices, grafosList)

    # print("2 Vertice Orign")
    print(nx.number_of_nodes(G))

    # print("3 Arestas Orign")
    print(nx.number_of_edges(G))

    #print("4 media")
    print("%.4f" % mediaGrauVertices)

    #print("5 Densidade")
    print("%.4f" % nx.density(G))


    #remove os elementos cujo grau menor que a media
    for n in vertices:
       if(G.degree[n] < mediaGrauVertices):
            v = [x for x, y in enumerate(grafosList) if y[0] == n]
            grafosList.pop(v[0])
            Grafo.remove_node(n)

    #print("6 Vertice Utiliz")
    print(nx.number_of_nodes(Grafo))

    #print("7 Arestas Orign")
    print(nx.number_of_edges(Grafo))

    # print("8 Desvio Padrao")
    print("%.4f" % desvioPadrao)

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
        if(tamanho + len(S) <= max):
            return
        i = S[0]
        S.remove(i)
        cliquesTemp.append(i);
        clique(list(set(S).intersection(set(list(vizinhos[i])))), tamanho+1, cliquesTemp)

h = hpy()
h.setrelheap()

#print("HORA ATUAL " + str(datetime.now().hour )+ ":" + str(datetime.now().minute) +":" + str(datetime.now().second))
tempoInicio = time.time()
lista = [x[0] for x in inicio()]
clique(lista, 0, [])
# print('9 CLIQUE MAX ')
print(str(max))
#print('Elementos MAX - ' + str(elementosClique))
#cliques = list(find_cliques(Grafo))
tempoFim = time.time()
# print("10 Tempo")
print("%.4f" % (tempoFim - tempoInicio))

x = h.heap() #depois do coigo

# print("11 Memoria")
print(str(x.size))