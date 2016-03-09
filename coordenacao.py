import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

#===========================Variaveis==============================
#Fator de crescimento
k = 2
#Criacao da arvore
G = nx.Graph()
#Leitura do arquivo
m = np.loadtxt("topologia7.txt").astype(int)
#Fusiveis
fus = np.array([6, 10, 15, 25, 40, 65, 100, 200])
G.add_node(1)
#===========================Variaveis==============================

#===========================Arvore=================================
#Estrutura basica de uma arvore
class Prot:
	def __init__(self, de, para, tipo, curto, corrente, fusivel = None):
		self.de = de
		self.para = para
		self.tipo = tipo
		self.curto = curto
		self.corrente = corrente
		self.fusivel = fusivel
	def __str__(self):
		return str(self.tipo)
#===========================Arvore=================================

#===========================Funcoes================================
#Dimensionamento elo fusivel
def dimens(prot):
	prot.fusivel = fus[(prot.corrente * k)/1.5 <= fus][0]
#===========================Funcoes================================

#=============================Etapas===============================
#Cria a arvore
for i in m:
	G.add_edge(i[0], i[1], prot = Prot(i[0], i[1], i[2], None, i[3]))
#Dimensionamento na arvore
for i in G.edges():
	dimens(G[i[0]][i[1]]['prot'])







print G[1][2]['prot'].fusivel


pos=nx.graphviz_layout(G,prog='dot')
nx.draw(G,pos)

"""
p = Prot(1, 2, 5, 100, 65)
dimens(p)
print p.fusivel
"""
# plt.show()