import networkx as nx
import time
from datetime import datetime
#from guppy import hpy

from networkx.algorithms.clique import find_cliques

Grafo = nx.Graph
max = 0
elementosClique = []

def inicio():
    global Grafo
    #arq = open('C:/Users/Barbara/PycharmProjects/TP_Final_PAA/facebook/1684.edges', 'rb')
    arq = open('C:/Users/Barbara/Dropbox/UFMG/PAA/Projeto Final/Entrega 2/testes preliminares/bases/1912.edges', 'rb')

    print("Arquivo")
    print(arq)
    #Leitura do arquivo
    G = nx.read_edgelist(arq)

    #para cada vértice, vou adicionar a aresta com vértice 0 - orientacao da base
    vertices = [x for x in nx.nodes(G)]
    for n in vertices:
        G.add_edge('1912', n)

    print("Vertice")
    print(nx.number_of_nodes(G))

    print("Arestas")
    print(nx.number_of_edges(G))

    print("Densidade")
    print("%.4f" % nx.density(G))

    print((nx.is_connected(G)))

    #print(psutil.virtual_memory())

    #Congela Grafo
    nx.freeze(G)

    Grafo = G

    #Lista de tuplas(vertice, grau)
    grafosList = list(G.degree)

    #ordenação crescente pelo grau
    grafosList.sort(key=lambda tup: tup[1])

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
        cliquesTemp.append(i);
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
#l = [len(x) for x in cliques]
#print('Outro: ' + str(sorted(l)[-1:]))
tempoFim = time.time()
print("TEMPO -> " + "%.4f" % (tempoFim - tempoInicio))

#x = h.heap() #depois do coigo
#print('memoria: '+str(x.size))
#print ('memoria'+ str(x))

#print(psutil.virtual_memory())
#print(psutil.swap_memory())

