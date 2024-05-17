"""
 Title:        Shower
 Description:  Visualises the grains of an EBSD map
 Author:       Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from crystalyser.ebsd.reader import read_pixels, remap_grains
from crystalyser.ebsd.plotter import EBSDPlotter, save_plot

# EBSD data paths
# EBSD_DIR = "/mnt/c/Users/z5208868/OneDrive - UNSW/PhD/data/20240516 (ondrej_P91)"
EBSD_DIR = "/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/data/20240516 (ondrej_P91)"
EBSD_CSV = "/S1_2/deer-in/res_015um/ebsdExportColumnsTableJanzen_fill.csv"
# EBSD_CSV = "/S1_2/deer-in/res_030um/ebsdExportColumnsTableJanzen_fill.csv"
# EBSD_CSV = "/S1_2/deer-in/res_060um/ebsdExportColumnsTableJanzen_fill.csv"
HEADERS = ["x", "y", "phaseId", "grainId", "EulerMean_phi1", "EulerMean_Phi", "EulerMean_phi2"]
STEP_SIZE = 0.15 # um
ID_LIST = None # [58]

# Plot EBSD map
ebsd_path = f"{EBSD_DIR}/{EBSD_CSV}"
pixel_grid, grain_map = read_pixels(ebsd_path, STEP_SIZE, HEADERS)
pixel_grid, grain_map = remap_grains(pixel_grid, grain_map)
plotter = EBSDPlotter(pixel_grid, grain_map, STEP_SIZE, 10)
plotter.plot_ebsd("x")
plotter.plot_ids(ID_LIST, {"fontsize": 12, "color": "black"})
plotter.plot_boundaries(ID_LIST, {"linewidth": 1, "color": "black"})
# plotter.plot_border()
save_plot("results/ebsd.png")
