"""
 Title:         Plotter
 Description:   Plots EBSD maps using a plot
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import matplotlib.pyplot as plt
from crystalyser.ebsd.reader import get_centroids
from crystalyser.ebsd.ipf_cubic import euler_to_rgb

# EBSD Plotter class
class EBSDPlotter:
    
    def __init__(self, pixel_grid:list, grain_map:dict, scaler:float):
        """
        Constructor for the plotter class
        
        Parameters:
        * `pixel_grid`: A grid of pixels
        * `grain_map`:  A mapping of the grains to the average orientations
        * `scaler`:     The step size of the EBSD map
        """
        
        # Initialise internal variables
        self.pixel_grid = pixel_grid
        self.grain_map = grain_map
        self.scaler = scaler
        
        # Calculate pixel size
        disp_p1 = plt.gca().transData.transform((0, 0))
        disp_p2 = plt.gca().transData.transform((self.scaler, 0))
        self.pixel_size = self.scaler*3/2
        self.square_size = np.linalg.norm(disp_p1 - disp_p2)*self.pixel_size
        
        # Initialise the plot
        x_length = len(pixel_grid[0])*scaler
        y_length = len(pixel_grid)*scaler
        plt.figure(figsize=(x_length, y_length))

    def plot_ebsd(self, ipf:str="x") -> None:
        """
        Plots the EBSD map using Matplotlib
        
        Parameters:
        * `pixel_grid`: A grid of pixels
        * `grain_map`:  A mapping of the grains to the average orientations
        * `scaler`:     The step size of the EBSD map
        * `ipf`:        The IPF direction
        """
        
        # Create colour map
        colour_map = {}
        for grain_id in self.grain_map.keys():
            orientation = self.grain_map[grain_id].get_orientation()
            colour = [rgb/255 for rgb in euler_to_rgb(*orientation, ipf=ipf)]
            colour_map[grain_id] = colour
        
        # Prepare pixel data
        x_list, y_list, colour_list = [], [], []
        for row in range(len(self.pixel_grid)):
            for col in range(len(self.pixel_grid[row])):
                x_list.append(col*self.scaler)
                y_list.append(row*self.scaler)
                colour_list.append(colour_map[self.pixel_grid[row][col]])

        # Plot and format
        plt.scatter(x_list, y_list, c=colour_list, s=self.square_size**2, marker="s")
        plt.xlim(min(x_list)-self.pixel_size/2, max(x_list)+self.pixel_size/2)
        plt.ylim(min(y_list)-self.pixel_size/2, max(y_list)+self.pixel_size/2)

    def plot_centroids(self, colour:str="black") -> None:
        """
        Writes the grain IDs at the centroids
        
        Parameters:
        * `colour`: The colour of the text
        """
        centroid_dict = get_centroids(self.pixel_grid)
        for grain_id in centroid_dict.keys():
            x, y = centroid_dict[grain_id]
            x *= self.scaler
            y *= self.scaler
            plt.text(x, y, str(grain_id), fontsize=12, ha="center", va="center", color=colour)

    def plot_boundaries(self, colour:str="red") -> None:
        """
        Plots the grain boundaries
        
        Parameters:
        * `colour`: The colour of the grain boundaries
        """
        
        # Initialise
        x_size = len(self.pixel_grid[0])
        y_size = len(self.pixel_grid)
        x_list, y_list = [], []
        
        # Iterate through pixels
        for row in range(y_size):
            for col in range(x_size):
                
                # Check to add boundary on the right
                if col+1 < x_size and self.pixel_grid[row][col] != self.pixel_grid[row][col+1]:
                    
                
                
        #         neighbours = get_common_neighbours(self.pixel_grid, col, row, x_size, y_size)
        #         if len(neighbours) < 4:
        #             x_list.append(col*self.scaler)
        #             y_list.append(row*self.scaler)

        # # Plot the grain boundaries
        # plt.scatter(x_list, y_list, color=colour, s=self.square_size**2, marker="s")

def save_plot(file_path:str) -> None:
    """
    Saves the plot and clears the figure

    Parameters:
    * `file_path`: The path to save the plot
    """
    plt.savefig(file_path)
    plt.cla()
    plt.clf()
    plt.close()
