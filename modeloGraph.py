from collections import defaultdict
from turtle import distance
from typing import List, Optional
from numpy import Infinity
from pydantic import BaseModel


class modeloRota(BaseModel):
    source: str
    target: str
    distance: int


class payload(BaseModel):
    id: Optional[int]
    data: list[modeloRota]


class routeBase(dict):  # diiconario de uma rota#
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


class routesBig(defaultdict):
    routes: list[routeBase]


class adjList(dict):  # cria um dicionario com keys de cada cidade e valores das cidades vizinhas#
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


class shortestPath(defaultdict):  # dicionario responsável pelo caminho mais curto#
    distance: Optional[int]
    path: list


#FUNÇÕES DE CÁLCULO DE ROTA#

class calc_rotas:
    def getRoutes(graph: adjList, source: str, path: str, target: str, maxStops: Optional[int]) -> routesBig:
        def dfs(graph: adjList, source: str, path: str, target: str, maxStops: Optional[int]):
            route = routeBase()
            if source in graph.keys():
                for node in graph[source]:
                    if node == target:
                        temp = [x for x in path]
                        temp.append(node)
                        s = ''.join(temp)
                        if(maxStops != None):
                            if((len(originalSource+s)-1) <= maxStops):
                                route.add("route", originalSource+s)
                                route.add("stops", len(originalSource+s)-1)
                                routes["routes"].append(route)
                        else:
                            route.add("route", originalSource+s)
                            route.add("stops", len(originalSource+s)-1)
                            routes["routes"].append(route)
                    else:
                        if(node not in path):
                            path = path+node
                            dfs(graph, node, path, target, maxStops)
                            path = path.rstrip(path[-1])
            else:
                return routes
        originalSource = source
        routes = routesBig(routes=[])
        dfs(graph, source, path, target, maxStops)
        return routes

#CRIA UM GRAFO ONDE SE PEGA A CIDADE E SEU VALOR É UMA LISTA COM AS CIDADES VIZINHAS#


def createAdjNodes(graph: payload) -> adjList:
    nodesAndAdj = adjList()
    for i in graph.data:
        if(i.source not in nodesAndAdj.keys()):
            nodesAndAdj.add(i.source, [])
            for y in graph.data:
                if y.source in nodesAndAdj.keys() and y.target not in nodesAndAdj[y.source]:
                    nodesAndAdj[y.source].append(y.target)
    return nodesAndAdj


#FUNÇÃO DE CÁLCULO DA ROTA MAIS CURTA DADO UMA CIDADE ORIGEM E UMA  DESTINO#
def calcShortestPath(routes: routesBig, graph: payload) -> shortestPath:
    path = ''
    distance = 0
    shortPath = shortestPath(distance=Infinity, path=[])
    for i in routes["routes"]:
        nodes = [x for x in i["route"]]
        countNodes = 0
        for j in nodes:
            countNodes = countNodes + 1
            path = path + j
            if(countNodes < len(nodes)):
                for k in graph.data:
                    if k.source == path[countNodes - 1] and k.target == nodes[countNodes]:
                        distance = k.distance + distance
                        if(shortPath["distance"] > distance and (countNodes+1) == len(nodes)):
                            shortPath["distance"] = distance
                            shortPath["path"] = nodes
    return shortPath
