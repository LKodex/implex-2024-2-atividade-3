################################################################################
#                                                                              #
#                             Trabalho 3 de IMPLEX                             #
#                    José Vitor Oda Pires (2020.1906.049-0)                    #
#                  Lucas Gonçalves Cordeiro (2021.1906.031-0)                  #
#                                                                              #
################################################################################
import sys
import time
import hashlib
import random
from tabulate import tabulate 

def generateGraph(verticesAmount: int, connectionProbability: float) -> dict:
    """Gera um grafo não direcionado com base na quantidade de vértices e probabilidade de conexão."""
    graph = {v: list() for v in range(verticesAmount)}
    for vi in range(len(graph) - 1):
        for vj in range(vi + 1, len(graph)):
            shouldConnect = random.random() < connectionProbability
            if shouldConnect:
                graph[vi].append(vj)
                graph[vj].append(vi)
    return graph

def calculateVertices(graph: dict) -> int:
    """Calcula o número de vértices V do grafo G."""
    return len(graph)

def calculateEdges(graph: dict) -> int:
    """Calcula o número de arestas E do grafo G."""
    return sum(len(connectedVertices) for connectedVertices in graph.values()) // 2

def calculateMinimumDegree(graph: dict) -> int:
    """Calcula o grau mínimo do grafo G."""
    return min(len(neighbors) for neighbors in graph.values())

def calculateMaximumDegree(graph: dict) -> int:
    """Calcula o grau máximo do grafo G."""
    return max(len(neighbors) for neighbors in graph.values())

def calculateAverageDegree(graph: dict) -> float:
    """Calcula a média dos graus gmed do grafo G."""
    totalDegrees = sum(len(neighbors) for neighbors in graph.values())
    verticesCount = calculateVertices(graph)
    return totalDegrees / verticesCount if verticesCount > 0 else 0

def countConnectedComponents(graph: dict) -> int:
    """Conta o número de componentes conectadas no grafo."""
    visited = set()
    components = 0

    def dfs(vertex):
        stack = [vertex]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                stack.extend(neighbor for neighbor in graph[current] if neighbor not in visited)

    for vertex in graph:
        if vertex not in visited:
            components += 1
            dfs(vertex)

    return components

def calculateDiameter(graph: dict) -> int:
    """Calcula o diâmetro do grafo."""
    componentsCount = countConnectedComponents(graph)
    if componentsCount > 1:
        return 0

    verticesCount = calculateVertices(graph)
    maximumDistance = 0
    for v in range(verticesCount):
        bfsTreePath = generateTreePath(graph, v)
        distances = [vertice["distance"] for vertice in bfsTreePath.values() if "distance" in vertice]
        if distances:
            maximumDistance = max(maximumDistance, max(distances))
    return maximumDistance

def generateTreePath(graph: dict, origin: int):
    WHITE = "WHITE"
    GRAY = "GRAY"
    BLACK = "BLACK"

    bfsTreeGraph = {}
    for v, neighbors in graph.items():
        bfsTreeGraph[v] = {
            "neighbors": neighbors.copy(),
            "color": WHITE
        }
    
    originVertice = bfsTreeGraph[origin]
    originVertice["distance"] = 0
    originVertice["color"] = GRAY
    originVertice["previous"] = -1

    grayVertices = [(origin, originVertice)]
    for (v, vertice) in grayVertices:
        vertice["color"] = BLACK
        for neighbor in vertice["neighbors"]:
            neighborVertice = bfsTreeGraph[neighbor]
            if neighborVertice["color"] == WHITE:
                neighborVertice["color"] = GRAY
                neighborVertice["distance"] = vertice["distance"] + 1
                neighborVertice["previous"] = v
                grayVertices.append((neighbor, neighborVertice))
    return bfsTreeGraph

def main(ini: int, fim: int, stp: int, p: float, seed, *args):
    random.seed(seed)
    dataSet = {}
    for n in range(ini, fim + 1, stp):
        graph = generateGraph(n, p)
        dataSet[n] = { "graph": graph }
    
    for data in dataSet.values():
        graph = data["graph"]

        verticesCount = calculateVertices(graph)
        data |= { "verticesCount": verticesCount }

        edgesCount = calculateEdges(graph)
        data |= { "edgesCount": edgesCount }

        minimumDegree = calculateMinimumDegree(graph)
        data |= { "minimumDegree": minimumDegree }

        maximumDegree = calculateMaximumDegree(graph)
        data |= { "maximumDegree": maximumDegree }
        
        averageDegree = calculateAverageDegree(graph)
        data |= { "averageDegree": averageDegree }

        diameter = calculateDiameter(graph)
        data |= { "diameter": diameter }

    displayResults(dataSet)

def displayResults(dataSet):
    """Gera e exibe uma tabela com os dados dos grafos."""
    headers = ["V", "E", "gmin", "gmax", "gmed", "diam"]
    table = []
    for data in dataSet.values():
        table.append([
            data["verticesCount"],
            data["edgesCount"],
            data["minimumDegree"],
            data["maximumDegree"],
            f"{data['averageDegree']:.1f}",
            data["diameter"]
        ])
    
    print(tabulate(table, headers=headers, tablefmt="pretty"))

def generateRandomSeed() -> str:
    """Gera um hash SHA3 de 512 caracteres como seed."""
    now = str(time.time())
    nowEncoded = now.encode()
    timeHash = hashlib.sha3_512(nowEncoded).hexdigest()
    return timeHash

if __name__ == "__main__":
    if len(sys.argv) < 5:
        programName = sys.argv[0]
        errorMessage = f"Usage: {programName} <ini> <fim> <stp> <p> [seed]"
        print(errorMessage, file=sys.stderr)
        sys.exit(1)
    try:
        ini = int(sys.argv[1])
        fim = int(sys.argv[2])
        stp = int(sys.argv[3])
        p = float(sys.argv[4])
    except ValueError as e:
        errorMessage = f"Could not convert parameters to the expected types.\nException: {e}"
        print(errorMessage, file=sys.stderr)
        sys.exit(1)
    seed = sys.argv[5] if len(sys.argv) > 5 else generateRandomSeed()
    print(f"Seed set = {seed}")
    main(ini, fim, stp, p, seed, *sys.argv[6:])
