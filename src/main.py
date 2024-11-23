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
        print(data)

def generateRandomSeed() -> str:
    '''
    Gera um hash SHA3 de 512 caracteres
    '''
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
        errorMessage = f"Could not convert parameters to an integer.\nException: {e}"
        print(errorMessage, file=sys.stderr)
        sys.exit(1)
    seed = sys.argv[5] if len(sys.argv) > 5 else generateRandomSeed()
    print(f"Seed set = {seed}")
    main(ini, fim, stp, p, seed, *sys.argv[6:])
