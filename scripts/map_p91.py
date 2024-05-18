"""
 Title:        Mapper
 Description:  Maps the grains of deformed EBSD maps
 Author:       Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from crystalyser.ebsd.reader import read_pixels
from crystalyser.ebsd.plotter import EBSDPlotter, save_plot
from crystalyser.ebsd.changer import deform_x, deform_y, orient_noise, merge_grains
from crystalyser.ebsd.mapper import map_ebsd

# EBSD data paths
EBSD_DIR = "/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/data/20240516 (ondrej_P91)"
# EBSD_CSV = "/S1_2/deer-in/res_015um/ebsdExportColumnsTableJanzen_fill.csv"
EBSD_CSV = "/S1_2/deer-in/res_060um/ebsdExportColumnsTableJanzen_fill.csv"
HEADERS = ["x", "y", "phaseId", "grainId", "EulerMean_phi1", "EulerMean_Phi", "EulerMean_phi2"]
STEP_SIZE = 0.60 # um
ID_LIST = None # [58]

# Plots the EBSD
def plot(pixel_grid:list, grain_map:dict, plot_name:str) -> None:
    """
    For quickly plotting multiple plots
    
    Parameters:
    * `pixel_grid`: A grid of pixels
    * `grain_map`:  A mapping of the grains to the average orientations
    * `plot_name`:  Name of plot file
    """
    plotter = EBSDPlotter(pixel_grid, grain_map, STEP_SIZE, 10)
    plotter.plot_ebsd("x")
    plotter.plot_ids(ID_LIST, {"fontsize": 12, "color": "black"})
    plotter.plot_boundaries(ID_LIST, {"linewidth": 1, "color": "black"})
    save_plot(f"results/{plot_name}.png")

# Get original map
ebsd_path = f"{EBSD_DIR}/{EBSD_CSV}"
pixel_grid_0, grain_map_0 = read_pixels(ebsd_path, STEP_SIZE, HEADERS)
plot(pixel_grid_0, grain_map_0, "ebsd_0")

# Simulate deformation
pixel_grid_1 = deform_x(pixel_grid_0, STEP_SIZE, 1.2)
pixel_grid_1 = deform_y(pixel_grid_1, STEP_SIZE, 0.9)
grain_map_1 = orient_noise(grain_map_0)
pixel_grid_1, grain_map_1 = merge_grains(pixel_grid_1, grain_map_1)
plot(pixel_grid_1, grain_map_1, "ebsd_1")

# Print mapping
map_ebsd(pixel_grid_0, pixel_grid_1)
