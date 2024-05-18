"""
 Title:         Mapper
 Description:   Maps the grains in multiple EBSD maps
 Author:        Janzen Choi

"""

# Libraries
import math, numpy as np
import networkx as nx
from crystalyser.ebsd.reader import get_centroids

# Edge class
class Edge:

    def __init__(self, node_1:int, node_2:int):
        """
        Constructor for mapped grain object

        Parameters:
        * `node_1`: First node
        * `node_2`: Second node
        """
        self.node_1 = node_1
        self.node_2 = node_2
        self.errors = []
        self.weight = None

    def get_node_1(self) -> int:
        """
        Returns the first node
        """
        return self.node_1

    def get_node_2(self) -> int:
        """
        Returns the second node
        """
        return self.node_1

    def add_error(self, error:float) -> None:
        """
        Adds an error to contribute to the weight

        Parameters:
        * `error`: The error to be added
        """
        self.errors.append(error)
        self.weight = np.average(self.errors)

    def get_weight(self) -> float:
        """
        Returns the averaged errors
        """
        return self.weight

def map_ebsd(pixel_grid_1:list, grain_map_1:dict, pixel_grid_2:list, grain_map_2:dict) -> tuple:
    """
    Maps grains from multiple EBSD maps
    
    Parameters:
    * `pixel_grid_1`: First grid of pixels
    * `grain_map_1`:  First mapping of grains
    * `pixel_grid_2`: Second grid of pixels
    * `grain_map_2`:  Second mapping of grains
    
    Returns the mapping of the grains
    """

    # Initialise edge list
    grain_ids_1 = list(set([pixel for pixel_list in pixel_grid_1 for pixel in pixel_list]))
    grain_ids_2 = list(set([pixel for pixel_list in pixel_grid_2 for pixel in pixel_list]))
    connected_list = [] # for second grid
    edge_list = []
    for grain_id_1 in grain_ids_1:
        for grain_id_2 in grain_ids_2:
            if grain_id_2 in connected_list:
                continue
            edge = Edge(grain_id_1, grain_id_2)
            connected_list.append(grain_id_2)
            edge_list.append(edge)
    
    # Initialise discrepancy sources
    centroid_dict_1, centroid_dict_2 = get_norm_centroids(pixel_grid_1, pixel_grid_2)

    # Define weights of edges
    for edge in edge_list:
        grain_id_1 = edge.get_node_1()
        grain_id_2 = edge.get_node_2()

        # Calculate centroid error
        x_1, y_1 = centroid_dict_1[grain_id_1]
        x_2, y_2 = centroid_dict_2[grain_id_2]
        distance = math.sqrt(math.pow(x_1-x_2,2) + math.pow(y_1-y_2,2))
        edge.add_error(distance)

    # Reduce edge list
    reduced_edge_list = []
    for edge in edge_list:
        reduced_edge_list.append((
            edge.get_node_1(),
            edge.get_node_2(),
            edge.get_weight()
        ))

    # Find minimum spanning tree
    graph = nx.Graph()
    mst = nx.minimum_spanning_tree(graph)
    for edge in mst.edges(data=True):
        print(edge)

def get_norm_centroids(pixel_grid_1:list, pixel_grid_2:list) -> tuple:
    """
    Gets normalised centroids of two maps
    
    Parameters:
    * `pixel_grid_1`: First grid of pixels
    * `pixel_grid_2`: Second grid of pixels

    Returns the normalised centroid maps
    """
    
    # Determine sizes of grids
    x_len_1 = len(pixel_grid_1[0])
    x_len_2 = len(pixel_grid_2[0])
    y_len_1 = len(pixel_grid_1)
    y_len_2 = len(pixel_grid_2)

    # Gets scaled centroids
    centroid_dict_1 = get_centroids(pixel_grid_1)
    for grain_id in centroid_dict_1.keys():
        x, y = centroid_dict_1[grain_id]
        centroid_dict_1[grain_id] = (x/x_len_1, y/y_len_1)
    centroid_dict_2 = get_centroids(pixel_grid_2)
    for grain_id in centroid_dict_2.keys():
        x, y = centroid_dict_2[grain_id]
        centroid_dict_2[grain_id] = (x/x_len_2, y/y_len_2)

    # Return centroid maps
    return centroid_dict_1, centroid_dict_2
