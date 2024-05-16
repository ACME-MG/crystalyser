"""
 Title:         Gridder
 Description:   Converting CSV files of EBSD data into manipulatable formats
 Author:        Janzen Choi

"""

# Special element IDs
VOID_PIXEL_ID       = 100000 # large number
UNORIENTED_PIXEL_ID = 100001 # large number + 1
NO_ORIENTATION      = [0, 0, 0] # for both void and unoriented

def get_void_pixel_grid(x_cells:list, y_cells:list) -> list:
    """
    Creates a grid of void pixels
    
    Parameters:
    * `x_cells`:    The number of pixels on the horizontal axis
    * `y_cells`:    The number of pixels on the vertical axis
    * `init_value`: The initial value of the cell in the piel grid
    
    Returns a grid of void pixels
    """
    pixel_grid = []
    for _ in range(y_cells):
        pixel_list = []
        for _ in range(x_cells):
            pixel_list.append(VOID_PIXEL_ID)
        pixel_grid.append(pixel_list)
    return pixel_grid

def get_neighbours(x:float, y:float, x_size:int, y_size:int) -> list:
    """
    Gets the neighbouring indices of a pixel
    
    Parameters:
    * `x`:      The x coordinate
    * `y`:      The y coordinate
    * `x_size`: The maximum x value 
    * `y_size`: The maximum y value
    
    Returns a list of the neighbouring coordinates 
    """
    neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    neighbours = [
        neighbour for neighbour in neighbours
        if neighbour[0] >= 0 and neighbour[0] < x_size
        and neighbour[1] >= 0 and neighbour[1] < y_size
    ]
    return neighbours

def get_all_neighbours(x_list:list, y_list:list, x_size:int, y_size:int):
    """
    Gets the neighbouring indices of a group of pixels
    
    Parameters:
    * `x_list`: The list of x coordinates
    * `y_list`: The list of y coordinates
    * `x_size`: The maximum x value 
    * `y_size`: The maximum y value
    
    Returns a list of all the neighbouring coordinates 
    """
    
    # Gets all the neighbours
    all_neighbours = []
    for i in range(len(x_list)):
        neighbours = get_neighbours(x_list[i], y_list[i], x_size, y_size)
        all_neighbours += neighbours
    
    # Remove duplicates and neighbours in the group
    all_neighbours = list(set(all_neighbours))
    group = [(x_list[i],y_list[i]) for i in range(len(x_list))]
    all_neighbours = [neighbour for neighbour in all_neighbours if not neighbour in group]

    # Return
    return all_neighbours
