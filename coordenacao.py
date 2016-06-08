import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#===========================Variaveis==============================
#Fator de crescimento
k = 1
#Criacao da arvore
G = nx.DiGraph()
#Leitura do arquivo
#Topologia
m = np.loadtxt("topologia 7/topologia7.txt").astype(int)
#Zona
z = np.loadtxt("topologia 7/zonatopologia7.txt").astype(int)
#Fusiveis
fus = np.array([6, 10, 15, 25, 40, 65, 100, 200])
#Tabela Elo Fusivel
tabela = pd.read_table("tabelaEloFusivel.txt", delimiter=" ", index_col=0)
G.add_node(1)
#===========================Variaveis==============================

#===========================Arvore=================================
#Estrutura basica de uma arvore
class Prot:
	def __init__(self, de, para, tipo, corrente, curtoDe, curtoPara, fusivel = None, zona = None):
		self.de = de
		self.para = para
		self.tipo = tipo
		self.corrente = corrente
		self.curtoDe = curtoDe
		self.curtoPara = curtoPara
		self.fusivel = fusivel
        self.zona = zona
	def __str__(self):
		return str(self.tipo)
#===========================Arvore=================================

#===========================Funcoes================================
#Dimensionamento elo fusivel
def dimens(prot):
	prot.fusivel = fus[(prot.corrente * k)/1.5 <= fus][0]

#Coordena dois nodos
def coorenacao(protegido, protetor):
	#Verifica se os fusiveis a serem coordenados sao iguais, se forem a amperagem do protegido aumenta
	if(protegido.fusivel <= protetor.fusivel):	
		protegido.fusivel = int(fus[np.where(fus == protegido.fusivel)[0]+1])
	#Seleciona o maximo valor de correne passando no protetor
	a = max(protetor.curtoDe)
	#Realiza a comparacao na tabela elo fusivel para verificar o valor maximo de corrente de curto para que haja coordenacao
	b = tabela.loc[protetor.fusivel].loc[str(protegido.fusivel)]

	while a > b:
		#Seleciona o proximo valor de fusivel
		protegido.fusivel = fus[np.where(fus > protegido.fusivel)[0]][0]
		b = tabela.loc[protetor.fusivel].loc[str(protegido.fusivel)]


#Percorre a arvore e coordena os seus varios nodos
def perCoor(pai):
	for i in G.successors(pai.para):
		coorenacao(pai, perCoor(G[pai.para][i]['prot']))
	return pai
#Percorre a arvore para buscar os primeiros nodos que sao fusiveis
def findFus(pai):
	for i in G.successors(pai.para):
		if G[pai.para][i]['prot'].tipo == 5:
			perCoor(G[pai.para][i]['prot'])
		else:
			findFus(G[pai.para][i]['prot'])

#Selecao do menor valor de curto da zona
def menorCurto(nodo, listaZona):
    nodo = G[nodo[0]][nodo[1]]['prot']
    if listaZona:
        for z in listaZona:
            criaZona(nodo, z)
    nodo.zona = set(nodo.zona)
    #Seleciona o menor valor de curto da zona

#Cria a zona de um nodo
def criaZona(origem, nodo):
    if nodo == origem.de:
        pass
    else:
        origem.zona.append(nodo)
        criaZona(origem, G.predecessors(nodo)[0])

def imprime(ini, origem):
    if ini == origem:
        return ini
    elif G.predecessors(ini) == []:
        print "nao existe"
    else:
        return [ini, imprime(G.predecessors(ini)[0], origem)]
#===========================Funcoes================================

#=============================Etapas===============================
#Cria a arvore
for i in m:
	G.add_edge(i[0], i[1], prot = Prot(i[0], i[1], i[2], i[3], [i[4], i[5], i[6], i[7]], [i[8], i[9], i[10], i[11]]))

#Dimensionamento na arvore
for i in G.edges():
	if G[i[0]][i[1]]['prot'].tipo == 5:
		dimens(G[i[0]][i[1]]['prot'])

"""#Selecionar o valor de maximo fusivel para cada par de pontos
for i in G.edges():
	if G[i[0]][i[1]]['prot'].tipo == 5:
        pass
"""


a = np.array([])
b = np.array([])

for i in G.edges():
    a = np.hstack((a, G[i[0]][i[1]]['prot'].fusivel))
fila = []
def busca(nodo, alvo):
    fila.append(nodo)
    while fila != []:
        a = fila.pop(0)
        print a
        for i in G.successors(a):
            fila.append(i)
        if a == alvo:
            return a
#menorCurto((9, 12), z[9, 
print z

#Coordenacao
findFus(G[1][2]['prot'])
"""
print "Comparacao dos valor dos fusiveis antes e depois da coordenacao"
for i in G.edges():
    b = np.hstack((b, G[i[0]][i[1]]['prot'].fusivel))
print a
print b
"""
#EXEMPLO DE TESTES=====================================================
#======================================================================

"""
for a in G.successors(6):
	print G.successors(a)


#a = np.array([1, 1, 2, 3, 5, 8, 13, 21])
#b = 10
#print a[np.where(a > b)[0]][0]
#print max(a)

#Linha, Coluna
# a = dados.loc[6].loc['15']

#""
a = Prot(1, 2, 5, 20, [30, 50, 40])
b = Prot(2, 3, 5, 20, [20, 1101, 9])

# print fus[np.where(fus == 40)[0]+1]

print a.fusivel
print b.fusivel

dimens(a)
dimens(b)

#""
print a.fusivel
print b.fusivel

coorenacao(a, b)

print a.fusivel
print b.fusivel


""

for i in G.edges():
	print G[i[0]][i[1]]['prot'].fusivel

perCoor(G[1][2]['prot'])


for i in G.edges():
	print G[i[0]][i[1]]['prot'].fusivel

"""

#=======================================================================
#=======================================================================


#print dados.loc[6].loc[10]

#p = Prot(1, 2, 5, 100, 65)
#dimens(p)
#print p.fusivel
#print G.order()

#Plot da arvore
#G1 = nx.subgraph()
#pos=nx.graphviz_layout(G1,prog='dot')
#nx.draw(G1,pos)
#plt.show()
