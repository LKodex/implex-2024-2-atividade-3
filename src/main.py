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
    graph = { v: list() for v in range(verticesAmount) }
    for vi in range(len(graph) - 1):
        for vj in range(vi + 1, len(graph)):
            shouldConnect = random.random() < connectionProbability
            if shouldConnect:
                graph[vi].append(vj)
                graph[vj].append(vi)
    return graph

def main(ini: int, fim: int, stp: int, p: float, seed, *args):
    random.seed(seed)
    generatedGraphs = {}
    for verticesAmount in range(ini, fim + 1, stp):
        graph = generateGraph(verticesAmount, p)
        generatedGraphs[verticesAmount] = graph

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
