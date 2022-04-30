#DESAFIO DEV JR - MILENIO CAPITAL#

#AUTHOR: LUCAS COSTA DE ANDRADE#
from fastapi import FastAPI, Path
from modeloGraph import payload
from modeloGraph import calcRoutes, createAdjNodes

graphBD: payload = []

app = FastAPI()

#ENDPOINTS#


@app.get("/descricaoAPI")
def desc():
    return("API para o cálculo de rotas de um grafo")


#Retorna todos os grafos salvos até o momento#
@app.get("/retornagrafos")
def retornagrafos():
    if (graphBD == []):
        return "Não tem nenhum grafo registrado!"
    else:
        return graphBD

#recebe as rotas do grafo e salva com o id do grafo#


@app.post("/graph")
def pegaID(graph: payload):
    if(graphBD):
        graph.id = graphBD[-1].id + 1
    else:
        graph.id = 1
    graphBD.append(graph)
    return graphBD[-1]

#busca um grafo salvo anteriormente#


@app.get("/graph/{graphId}")
def returnGraph(graphId: int = Path(None, description="Digite o ID do grafo que está buscando")):
    if (graphBD == []):
        return "HTTP NOT FOUND"
    for i in graphBD:  # Lê os dicionários da lista/BD#
        if(graphId == i.id):
            return i
        elif i == graphBD[-1]:
            return "HTTP NOT FOUND"

#verifica as rotas disponíveis entre origem e destino, com limite de paradas opcional#


@app.get("/adjacentes/{graphId}")
def returnAdjacents(graphId: int):
    for i in graphBD:
        if(graphId == i.id):
            return createAdjNodes(i)


@app.post("/routes/{graphId}/from/{town1}/to/{town2}")
def routes(graphId: int, town1: str, town2: str):
    if (graphBD == []):
        return "HTTP NOT FOUND"
    for i in graphBD:
        if(graphId == i.id):
            graph = createAdjNodes(i)
            return calcRoutes(graph, town1, town2)
        elif i == graphBD[-1]:
            return "HTTP NOT FOUND"
