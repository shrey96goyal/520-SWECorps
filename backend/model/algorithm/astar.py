from ..algorithm.interface import SearchAlgorithmInterface
from ..GraphUtils import getEdgeLength, getEdgeAbsElevation
import heapq
from geopy import distance


class AStarSearch(SearchAlgorithmInterface):
    def search(self, G, origNode, destNode, shortestDistance, distRestriction, minElevation=1):
        maxDistance = shortestDistance * (1 + distRestriction)
        print('shortest distance is ' + str(shortestDistance))
        print('max distance is ' + str(maxDistance))
        nodeDistAndElev = {}
        nodeSet = set([])
        openList = [(0, 0, 0, origNode, [origNode])]
        possiblePath = []
        destNodeData = G.nodes(data=True)[destNode]
        while len(openList) > 0 and openList[0][1] <= maxDistance:
            f, dist, g, node, path = openList[0]
            openList.pop(0)

            if (node, g, dist) in nodeSet:
                continue

            nodeSet.add((node, g, dist))

            if node == destNode:
                print('adding')
                possiblePath = path
                print(dist)
                if dist <= maxDistance:
                    break
            else:
                if node not in nodeDistAndElev:
                    nodeDistAndElev[node] = (g, dist)
                else:
                    nodeDistAndElev[node] = (min(g, nodeDistAndElev[node][0]), min(dist, nodeDistAndElev[node][1]))

                for edges in G.out_edges(node):
                    nextNode = edges[1]
                    if nextNode in path:
                        continue
                    nextG = g + getEdgeAbsElevation(G, node, nextNode) * minElevation
                    nextDist = dist + getEdgeLength(G, node, nextNode)
                    if nextDist > maxDistance:
                        continue
                    if nextNode not in nodeDistAndElev or nodeDistAndElev[nextNode][0] > nextG or nodeDistAndElev[nextNode][1] > nextDist:
                        nextNodeData = G.nodes(data=True)[nextNode]
                        nextNodePath = path.copy()
                        nextF = nextG
                        if nextNode != destNode:
                            nextF += minElevation * (abs(destNodeData['elevation'] - nextNodeData['elevation']) / (
                                    distance.distance((nextNodeData['y'], nextNodeData['x']),
                                                      (destNodeData['y'], destNodeData['x'])).km * 1000))
                        nextNodePath.append(nextNode)
                        openList.append((nextF, nextDist, nextG, nextNode, nextNodePath))

            heapq.heapify(openList)

        print(len(possiblePath))
        return possiblePath
