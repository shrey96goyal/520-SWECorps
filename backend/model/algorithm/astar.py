from ..algorithm.interface import SearchAlgorithmInterface
from ..GraphUtils import getEdgeLength, getEdgeAbsElevation
import heapq
from geopy import distance

'''
    Class for A-Star algorithm
'''
class AStarSearch(SearchAlgorithmInterface):
    '''
        A-Star algorithm to find path with min elevation/max elevation/without considering elevation.
        Elevation Delta / Euclidean distance between that point and destination is used as additional heuristic for AStar
        graph - Graph object
        origNode - node ID of source Node
        destNode - node ID of destination Node
        shortestDistance - shortest distance between origNode and destNode
        distRestriction - Restriction on distance. Returned path should be within this% of shortest distance
        minElevation - Pass 0 for path without considering elevation, 1 for min elevation, -1 for max elevation
    '''
    def search(self, G, origNode, destNode, shortestDistance, distRestriction, minElevation=1):
        maxDistance = shortestDistance * (1 + distRestriction)
        print('Shortest distance is ' + str(shortestDistance))
        print('Max allowed distance is ' + str(maxDistance))

        # Stores minimum elevation and distance of nodeID till now
        nodeDistAndElev = {}

        # Visited nodes with elevation and distance
        nodeSet = set([])

        # Heap stores elevation, distance, nodeID, path till nodeID
        heap = [(0, 0, 0, origNode, [origNode])]
        possiblePath = []
        destNodeData = G.nodes(data=True)[destNode]
        while len(heap) > 0 and heap[0][1] <= maxDistance:
            f, dist, g, node, path = heap[0]
            heap.pop(0)

            if (node, g, dist) in nodeSet:
                continue

            # Adding node with elevation and distance to visited node
            nodeSet.add((node, g, dist))

            if node == destNode:
                # Possible path found
                possiblePath = path
                if dist <= maxDistance:
                    print('Path found using A-Star Algorithm with distance ' + str(dist))
                    break
            else:
                # Process current node
                if node not in nodeDistAndElev:
                    nodeDistAndElev[node] = (g, dist)
                else:
                    nodeDistAndElev[node] = (min(g, nodeDistAndElev[node][0]), min(dist, nodeDistAndElev[node][1]))

                # Process neighbours
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
                        heap.append((nextF, nextDist, nextG, nextNode, nextNodePath))

            heapq.heapify(heap)
        return possiblePath
