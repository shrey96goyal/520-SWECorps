from ..algorithm.interface import SearchAlgorithmInterface
from ..GraphUtils import getEdgeLength, getEdgeAbsElevation
import heapq
from geopy import distance


class DjikstraSearch(SearchAlgorithmInterface):
    def search(self, G, origNode, destNode, shortestDistance, distRestriction, minElevation = 1):
        maxDistance = shortestDistance * (1 + distRestriction)
        print('shortest distance is ' + str(shortestDistance))
        print('max distance is ' + str(maxDistance))
        nodeDistAndElev = {}
        nodeSet = set([])
        openList = [(0,  0, origNode, [origNode])]
        possiblePath = []
        while len(openList) > 0 and openList[0][1] <= maxDistance:
            f, dist, node, path = openList[0]
            openList.pop(0)

            if (node, f, dist) in nodeSet:
                continue

            nodeSet.add((node, f, dist))

            if node == destNode:
                print('adding')
                possiblePath = path
                print(dist)
                if dist <= maxDistance:
                    break
            else:
                if node not in nodeDistAndElev:
                    nodeDistAndElev[node] = (f, dist)
                else:
                    nodeDistAndElev[node] = (min(f, nodeDistAndElev[node][0]), min(dist, nodeDistAndElev[node][1]))

                for edges in G.out_edges(node):
                    nextNode = edges[1]
                    if nextNode in path:
                        continue
                    nextF = f + getEdgeAbsElevation(G, node, nextNode) * minElevation
                    nextDist = dist + getEdgeLength(G, node, nextNode)
                    if nextDist > maxDistance:
                        continue
                    if nextNode not in nodeDistAndElev or nodeDistAndElev[nextNode][0] > nextF or nodeDistAndElev[nextNode][1] > nextDist:
                        nextNodePath = path.copy()
                        nextNodePath.append(nextNode)
                        openList.append((nextF, nextDist, nextNode, nextNodePath))

            heapq.heapify(openList)

        print(len(possiblePath))
        return possiblePath
