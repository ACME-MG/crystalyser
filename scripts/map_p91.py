"""
 Title:        Mapper
 Description:  Maps the grains of different EBSD maps
 Author:       Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from crystalyser.ebsd.reader import read_pixels, remap_grains
from crystalyser.ebsd.plotter import EBSDPlotter, save_plot

# EBSD data paths
# EBSD_DIR = "/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/data/20240516 (ondrej_P91)"
EBSD_DIR = "/mnt/c/Users/z5208868/OneDrive - UNSW/PhD/data/20240516 (ondrej_P91)"
EBSD_CSV_LIST = [
    "/S1_2/deer-in/res_060um/ebsdExportColumnsTableJanzen_fill.csv",
]

# File constants
HEADERS = ["x", "y", "phaseId", "grainId", "EulerMean_phi1", "EulerMean_Phi", "EulerMean_phi2"]
STEP_SIZE = 0.6 # um

# Iterate through csv files
for ebsd_csv in EBSD_CSV_LIST:
    ebsd_path = f"{EBSD_DIR}/{ebsd_csv}"
    pixel_grid, grain_map = read_pixels(ebsd_path, STEP_SIZE, HEADERS)
    pixel_grid, grain_map = remap_grains(pixel_grid, grain_map)
    plotter = EBSDPlotter(pixel_grid, grain_map, STEP_SIZE/5)
    plotter.plot_ebsd("x")
    plotter.plot_centroids()
    plotter.plot_boundaries()
    save_plot("ebsd.png")
    