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
from crystalyser.helper import dict_to_csv

# Parameters
HEADERS = ["x", "y", "phaseId", "grainId", "EulerMean_phi1", "EulerMean_Phi", "EulerMean_phi2"]
EBSD_DIR = "/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/data/20240516 (ondrej_P91)"
# EBSD_CSV = "/S1_2/deer-in/res_015um/ebsdExportColumnsTableJanzen_fill.csv"
# STEP_SIZE = 0.15 # um
EBSD_CSV = "/S1_2/deer-in/res_060um/ebsdExportColumnsTableJanzen_fill.csv"
STEP_SIZE = 0.60 # um

# Plots the EBSD
def plot(pixel_grid:list, grain_map:dict, id_list:list, plot_name:str) -> None:
    """
    For quickly plotting multiple plots
    
    Parameters:
    * `pixel_grid`: A grid of pixels
    * `grain_map`:  A mapping of the grains to the average orientations
    * `id_list`:    List of grain IDs
    * `plot_name`:  Name of plot file
    """
    plotter = EBSDPlotter(pixel_grid, grain_map, STEP_SIZE, 10)
    plotter.plot_ebsd("x")
    plotter.plot_boundaries(id_list, {"linewidth": 1, "color": "black"})
    plotter.plot_ids(id_list, {"fontsize": 20, "color": "black"})
    save_plot(f"results/{plot_name}.png")

# Get original map
ebsd_path = f"{EBSD_DIR}/{EBSD_CSV}"
pixel_grid_1, grain_map_1 = read_pixels(ebsd_path, STEP_SIZE, HEADERS)

# Simulate deformation
pixel_grid_2 = deform_x(pixel_grid_1, STEP_SIZE, 1.2)
pixel_grid_2 = deform_y(pixel_grid_2, STEP_SIZE, 0.9)
grain_map_2 = orient_noise(grain_map_1)
pixel_grid_2, grain_map_2 = merge_grains(pixel_grid_2, grain_map_2)

# Display and save mapping
map_dict = map_ebsd(pixel_grid_1, grain_map_1, pixel_grid_2, grain_map_2)
plot(pixel_grid_1, grain_map_1, map_dict["ebsd_1"], "ebsd_1")
plot(pixel_grid_2, grain_map_2, map_dict["ebsd_2"], "ebsd_2")
dict_to_csv(map_dict, "results/grain_map.csv")
