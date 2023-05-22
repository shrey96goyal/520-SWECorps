'''
    Interface for Search Algos.
'''
class SearchAlgorithmInterface:
    '''
        Function definition of search function.
        This should be overridden to return a path between origNode and destNode as required
        graph - Graph object
        origNode - node ID of source Node
        destNode - node ID of destination Node
        shortestDistance - shortest distance between origNode and destNode
        distRestriction - Restriction on distance. Returned path should be within this% of shortest distance
        minElevation - Pass 0 for path without considering elevation, 1 for min elevation, -1 for max elevation
    '''
    def search(self, graph, origNode, destNode, shortestDistance, distRestriction, minElevation = 1):
        """Search for path"""
        pass