from typing import List, Optional
from pydantic import BaseModel


class modeloRota(BaseModel):
    source: str
    target: str
    distance: int


class payload(BaseModel):
    id: Optional[int]
    data: list[modeloRota]


class routeBase(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


class routesBig(BaseModel):
    routes: list[routeBase]


class adjList(dict):  # cria um dicionario com keys de cada cidade e valores das cidades vizinhas#
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


#FUNÇÕES DE CÁLCULO DE ROTA#


def calcRoutes(graph: adjList, source: str, target: str, route: Optional[routeBase] = {}, routes: Optional[routesBig] = [], path: Optional[str] = ''):
    route = routeBase()
    routes: routesBig = []
    path = path + source
    for neighbour in graph[source]:
        path = path + neighbour
        graph[source].remove(neighbour)
        if(path[-1] == target):
            route.add("route", path)
            route.add("stops", len(path)-1)
            routes.append(route)
        calcRoutes(graph, neighbour, target, route, routes, path)
    return routes


#CRIA UM GRAFO ONDE SE PEGA A CIDADE E SEU VALOR É UMA LISTA COM AS CIDADES VIZINHAS#
def createAdjNodes(graph: payload):
    nodesAndAdj = adjList()
    for i in graph.data:
        if(i.source not in nodesAndAdj.keys()):
            nodesAndAdj.add(i.source, [])
            for y in graph.data:
                if y.source in nodesAndAdj.keys() and y.target not in nodesAndAdj[y.source]:
                    nodesAndAdj[y.source].append(y.target)
    return nodesAndAdj
