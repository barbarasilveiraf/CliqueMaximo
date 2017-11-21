import networkx as nx
import time
from datetime import datetime
from math import sqrt
import sys
#from guppy import hpy

from networkx.algorithms.clique import find_cliques

Grafo = nx.Graph
max = 0
elementosClique = []
mediaGrauVertices = 0
desvioPadrao = 0

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
    #arq = open(str(sys.argv[0]), 'rb')
    nomeCaminhoArq = 'C:/Users/Barbara/Dropbox/UFMG/PAA/Projeto Final/Entrega 2/testes preliminares/bases/1684.edges'
    arq = open(nomeCaminhoArq, 'rb')

    G = nx.read_edgelist(arq)

    #para cada vertice, vou adicionar a aresta com vértice 0 - orientacao da base
    end = None
    nomeArq = nomeCaminhoArq[84:end].replace(".edges","")

    vertices = [x for x in nx.nodes(G)]
    for n in vertices:
        G.add_edge(nomeArq, n)

    Grafo = G

    print("Vertices incicio")
    print(nx.number_of_nodes(Grafo))
    #Congela Grafo
    #nx.freeze(G)

    #Lista de tuplas(vertice, grau)
    grafosList = list(G.degree)

    #ordenacao crescente pelo grau
    grafosList.sort(key=lambda tup: tup[1])

    #pra pegar os vertices ja ordenados pelo grau
    vertices = [x[0] for x in grafosList]

    for n in vertices[:-1]: #pra ignorar o valor mais alto...
        mediaGrauVertices += G.degree[n]
    mediaGrauVertices /= (nx.number_of_nodes(G)-1)

    #calcular o desvio padrao
    desvioPadrao = desvio_padrao(mediaGrauVertices, grafosList)

    #remove os elementos cujo grau menor que a media
    for n in vertices:
       if(G.degree[n] < mediaGrauVertices - desvioPadrao):
            v = [x for x, y in enumerate(grafosList) if y[0] == n]
            grafosList.pop(v[0])
            Grafo.remove_node(n)

    print("Vertices depois")
    print(nx.number_of_nodes(Grafo))

    return grafosList

def clique(S, tamanho, cliquesTemp):
    global Grafo
    global max
    global elementosClique

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
        cliquesTemp.append(i)
        clique(list(set(S).intersection(set(list(Grafo.neighbors(i))))), tamanho+1, cliquesTemp)

#h = hpy()
#h.setrelheap()

print("HORA ATUAL " + str(datetime.now().hour )+ ":" + str(datetime.now().minute) +":" + str(datetime.now().second))
tempoInicio = time.time()
lista = [x[0] for x in inicio()]
clique(lista, 0, [])
print('CLIQUE MAX - ' + str(max))
#print('Elementos MAX - ' + str(elementosClique))
#cliques = list(find_cliques(Grafo))
tempoFim = time.time()
print("TEMPO -> " + "%.4f" % (tempoFim - tempoInicio))

#x = h.heap() #depois do coigo
#print('memoria: '+str(x.size))
#print ('memoria'+ str(x))
