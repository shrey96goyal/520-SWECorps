from ..GraphUtils import getGraphForLocation, getNearestNodes, getRouteDistance, getShortestRoute, getRouteElevation
from ..LocationDetails import getCommonLocation
from ..algorithm.astar import AStarSearch
from ..algorithm.djikstra import DjikstraSearch
import time

class Graph:
    def __init__(self, args):
        self.sourceLat = float(args['src_lat'])
        self.sourceLong = float(args['src_lang'])
        self.destLat = float(args['dest_lat'])
        self.destLong = float(args['dest_lang'])
        self.pathType = int(args['elevation'])
        self.distanceRestriction = float(args['distance']) / 100
        self.graph = None
        self.__loadGraph()

    '''
    Initialize and load graph
    '''
    def __loadGraph(self):
        source = [self.sourceLat, self.sourceLong]
        destination = [self.destLat, self.destLong]

        commonLocation = getCommonLocation(source, destination)
        self.graph = getGraphForLocation(commonLocation)

    '''
    1. Get the routes as per input distance % and elevation using both A* and Dijkstra's
    2. Compare the elevation value for both algorithms to find the best possible depending on input
    3. Return the route containing nodes
    '''
    def getPath(self):
        if self.distanceRestriction < 0:
            print('Incorrect distance restriction')
            return None

        origNode = getNearestNodes(self.graph, self.sourceLong, self.sourceLat)
        destNode = getNearestNodes(self.graph, self.destLong, self.destLat)

        shortestRoute = getShortestRoute(self.graph, origNode, destNode)
        shortestDistance = getRouteDistance(self.graph, shortestRoute)

        if self.pathType == 0:
            isMinElevation = 0
        elif self.pathType == 1:
            isMinElevation = 1
        else:
            isMinElevation = -1

        djikstra = DjikstraSearch()

        startTime = time.time()
        djikstraPath = djikstra.search(self.graph, origNode, destNode, shortestDistance, self.distanceRestriction, isMinElevation)
        djikstraEndTime = time.time()

        astar = AStarSearch()
        astarPath = astar.search(self.graph, origNode, destNode, shortestDistance, self.distanceRestriction, isMinElevation)
        astarEndTime = time.time()

        print('Djikstra runtime is ' + str(djikstraEndTime - startTime))
        print('AStar runtime is ' + str(astarEndTime - djikstraEndTime))

        # If no elevation option selected
        if isMinElevation == 0:
            return djikstraPath
        else:
            # Get route for both algorithms
            djikstraElev = getRouteElevation(self.graph, djikstraPath)
            astarElev = getRouteElevation(self.graph, astarPath)

            if isMinElevation == -1:
                djikstraElev *= -1
                astarElev *= -1

            # Compare and return most possible result
            if djikstraElev < astarElev:
                return djikstraPath
            else:
                return astarPath