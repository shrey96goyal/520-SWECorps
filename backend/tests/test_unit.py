import unittest
import sys

sys.path.append('..')
from model.graph.Graph import Graph
from model.GraphUtils import getGraphForLocation, getNodeIDForPoint, getNearestNodes, getShortestRoute, getEdgeLength, \
    getEdgeAbsElevation, getRouteDistance, getRouteElevation, getLatLongForRoute
from model.LocationDetails import getCommonLocation
from model.algorithm.astar import AStarSearch
from model.algorithm.djikstra import DjikstraSearch
from model.graph.Graph import Graph


class LocationUtilsTests(unittest.TestCase):
    # graph = getGraphForLocation('Amherst')
    # apiKey = 'AIzaSyCLWLZWWVKz107DGJoCh64jj0zs8gU9YnU'
    def testGetCommonLocation(self):
        source = [42.343488, -72.502818]
        dest = [42.377260, -72.519954]
        commonLocation = getCommonLocation(source, dest)
        self.assertEqual(commonLocation['city'], 'Amherst')
        dest2 = [42.360293, -72.539821]
        commonLocation = getCommonLocation(source, dest2)
        self.assertEqual(commonLocation['city'], '')


class GraphTests(unittest.TestCase):
    args = {'src_lat': 42.3772684,
            'src_lang': -72.5194994,
            'dest_lat': 42.3495879,
            'dest_lang': -72.5283459,
            'elevation': 1,
            'distance': 50}
    def testGraphInit(self):
        graph = Graph(self.args)
        self.assertNotEqual(None, graph)

    def testGraphGetPath(self):
        graph = Graph(self.args)
        route = graph.getPath()
        self.assertNotEqual(None, route)


class AlgorithmTests(unittest.TestCase):
    # Loading graph for Amherst
    commonLocation = getCommonLocation([42.343488, -72.502818], [42.377260, -72.519954])
    graph = getGraphForLocation(commonLocation)

    def testAStar(self):
        algo = AStarSearch()
        sourceNode = getNearestNodes(self.graph, -72.5194994, 42.3772684)
        destNode = getNearestNodes(self.graph, -72.5283459, 42.3495879)
        shortestRoute = getShortestRoute(self.graph, sourceNode, destNode)
        shortestDistance = getRouteDistance(self.graph, shortestRoute)
        shortestDistanceElevation = getRouteElevation(self.graph, shortestRoute)
        route = algo.search(self.graph, sourceNode, destNode, shortestDistance, 0.5, minElevation=1)
        routeDistance = getRouteDistance(self.graph, route)
        routeElevation = getRouteElevation(self.graph, route)

        self.assertEqual(True, routeElevation <= shortestDistanceElevation)
        self.assertEqual(True, routeDistance <= 1.5 * shortestDistance)

        route = algo.search(self.graph, sourceNode, destNode, shortestDistance, 0.5, minElevation=-1)
        routeDistance = getRouteDistance(self.graph, route)
        routeElevation = getRouteElevation(self.graph, route)

        self.assertEqual(True, routeElevation >= shortestDistanceElevation)
        self.assertEqual(True, routeDistance <= 1.5 * shortestDistance)

    def testDjikstra(self):
        algo = DjikstraSearch()
        sourceNode = getNearestNodes(self.graph, -72.5194994, 42.3772684)
        destNode = getNearestNodes(self.graph, -72.5283459, 42.3495879)
        shortestRoute = getShortestRoute(self.graph, sourceNode, destNode)
        shortestDistance = getRouteDistance(self.graph, shortestRoute)
        shortestDistanceElevation = getRouteElevation(self.graph, shortestRoute)
        route = algo.search(self.graph, sourceNode, destNode, shortestDistance, 0.5, minElevation=1)
        routeDistance = getRouteDistance(self.graph, route)
        routeElevation = getRouteElevation(self.graph, route)

        self.assertEqual(True, routeElevation <= shortestDistanceElevation)
        self.assertEqual(True, routeDistance <= 1.5 * shortestDistance)

        route = algo.search(self.graph, sourceNode, destNode, shortestDistance, 0.5, minElevation=-1)
        routeDistance = getRouteDistance(self.graph, route)
        routeElevation = getRouteElevation(self.graph, route)

        self.assertEqual(True, routeElevation >= shortestDistanceElevation)
        self.assertEqual(True, routeDistance <= 1.5 * shortestDistance)


class GraphUtilsTests(unittest.TestCase):
    # Loading graph for Amherst
    commonLocation = getCommonLocation([42.343488, -72.502818], [42.377260, -72.519954])
    graph = getGraphForLocation(commonLocation)

    # Point outside -> 42.360293, -72.539821

    def testGetNodeIDForPoint(self):
        nodeId = getNodeIDForPoint(self.graph, 42.343488, -72.502818)
        self.assertEqual(66618411, nodeId)
        # 1 -> 66618411
        # 2 -> 66714028

    def testGetGraphForLocation(self):
        commonLocation = getCommonLocation([42.343488, -72.502818], [42.377260, -72.519954])
        graph = getGraphForLocation(commonLocation)
        self.assertNotEqual(None, graph)
        commonLocation = getCommonLocation([42.343488, -72.502818], [42.360293, -72.539821])
        graph = getGraphForLocation(commonLocation)
        self.assertEqual(None, graph)

    def testGetNearestNodes(self):
        node = getNearestNodes(self.graph, -72.502818, 42.343488)
        self.assertEqual(node, 66618411)

    def testGetShortestRoute(self):
        route = getShortestRoute(self.graph, 66618411, 66774259)
        self.assertEqual([66618411, 66615547, 66774259], route)

    def testGetEdgeLength(self):
        length = getEdgeLength(self.graph, 66618411, 66615547)
        self.assertEqual(124.59299999999999, length)

    def testGetEdgeAbsElevation(self):
        edgeElevation = getEdgeAbsElevation(self.graph, 66618411, 66615547)
        self.assertEqual(0.027, edgeElevation)

        edgeElevationIfNegative = getEdgeAbsElevation(self.graph, 66615547, 66618411)
        self.assertEqual(0, edgeElevationIfNegative)

    def testGetRouteDistance(self):
        route = getShortestRoute(self.graph, 66618411, 66774259)
        routeDistance = getRouteDistance(self.graph, route)
        self.assertEqual(247.808, routeDistance)

    def testGetRouteElevation(self):
        route = getShortestRoute(self.graph, 66618411, 66774259)
        routeElevation = getRouteElevation(self.graph, route)
        self.assertEqual(0.048, routeElevation)

    def testGetLatLongForRoute(self):
        route = getShortestRoute(self.graph, 66618411, 66774259)
        latLongRoute = getLatLongForRoute(self.graph, route)
        self.assertEqual(latLongRoute, [[42.3432864, -72.5043174],
                                        [42.342192, -72.504628],
                                        [42.341084, -72.504608]])


if __name__ == '__main__':
    unittest.main()
