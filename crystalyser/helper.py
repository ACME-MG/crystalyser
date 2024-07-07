"""
 Title:         Helper
 Description:   General helper functions
 Author:        Janzen Choi

"""

# Libraries
import pandas as pd
import math

def get_closest(x_list:list, y_list:list, x_value:float) -> float:
    """
    Finds the closest corresponding y value given an x value;
    does not interpolate

    Parameters:
    * `x_list`:  The list of x values
    * `y_list`:  The list of y values
    * `x_value`: The x value to get the closest value of
    
    Returns the closest value
    """
    x_diff_list = [abs(x-x_value) for x in x_list]
    x_min_diff = min(x_diff_list)
    x_min_index = x_diff_list.index(x_min_diff)
    return y_list[x_min_index]

def quick_spline(x_list:list, y_list:list, x_value:float) -> float:
    """
    Conducts a quick evaluation using spline interpolation without
    conducting the whole interpolation; assumes that the x_value is
    between min(x_list) and max(x_list) and that x_list is sorted

    Parameters:
    * `x_list`:  The list of x values
    * `y_list`:  The list of y values
    * `x_value`: The x value to evaluate
    
    Returns the evaluated y value
    """
    if len(x_list) != len(y_list):
        raise ValueError("Length of lists do not match!")
    for i in range(len(x_list)-1):
        if x_list[i] <= x_value and x_value <= x_list[i+1]:
            gradient = (y_list[i+1]-y_list[i])/(x_list[i+1]-x_list[i])
            y_value = gradient*(x_value - x_list[i]) + y_list[i]
            return y_value
    return None

def get_thinned_list(unthinned_list:list, density:int) -> list:
    """
    Gets a thinned list

    Parameters:
    * `unthinned_list`: The list before thinning
    * `density`:        The goal density of the thinned list

    Returns the thinned list
    """
    src_data_size = len(unthinned_list)
    step_size = src_data_size / density
    thin_indexes = [math.floor(step_size*i) for i in range(1, density - 1)]
    thin_indexes = [0] + thin_indexes + [src_data_size - 1]
    thinned_list = [unthinned_list[i] for i in thin_indexes]
    return thinned_list

def csv_to_dict(csv_path:str, delimeter:str=",") -> dict:
    """
    Converts a CSV file into a dictionary
    
    Parameters:
    * `csv_path`:  The path to the CSV file
    * `delimeter`: The separating character
    
    Returns the dictionary
    """

    # Read all data from CSV (assume that file is not too big)
    csv_fh = open(csv_path, "r", encoding="utf-8-sig")
    csv_lines = csv_fh.readlines()
    csv_fh.close()

    # Initialisation for conversion
    csv_dict = {}
    headers = csv_lines[0].replace("\n", "").split(delimeter)
    csv_lines = csv_lines[1:]
    for header in headers:
        csv_dict[header] = []

    # Start conversion to dict
    for csv_line in csv_lines:
        csv_line_list = csv_line.replace("\n", "").split(delimeter)
        for i in range(len(headers)):
            value = csv_line_list[i]
            if value == "":
                continue
            try:
                value = float(value)
            except:
                pass
            csv_dict[headers[i]].append(value)
    
    # Convert single item lists to items and things multi-item lists
    for header in headers:
        if len(csv_dict[header]) == 1:
            csv_dict[header] = csv_dict[header][0]
    
    # Return
    return csv_dict

def dict_to_csv(data_dict:dict, csv_path:str, add_header:bool=True) -> None:
    """
    Converts a dictionary to a CSV file
    
    Parameters:
    * `data_dict`: The dictionary to be converted
    * `csv_path`:  The path that the CSV file will be written to
    * `header`:    Whether to include the header or not
    """
    
    # Extract headers and turn all values into lists
    headers = data_dict.keys()
    for header in headers:
        if not isinstance(data_dict[header], list):
            data_dict[header] = [data_dict[header]]
    
    # Open CSV file and write headers
    csv_fh = open(csv_path, "w+")
    if add_header:
        csv_fh.write(",".join(headers) + "\n")
    
    # Write data and close
    max_list_size = max([len(data_dict[header]) for header in headers])
    for i in range(max_list_size):
        row_list = [str(data_dict[header][i]) if i < len(data_dict[header]) else "" for header in headers]
        row_str = ",".join(row_list)
        csv_fh.write(row_str + "\n")
    csv_fh.close()

def round_sf(value:float, sf:int) -> float:
    """
    Rounds a float to a number of significant figures

    Parameters:
    * `value`: The value to be rounded
    * `sf`:    The number of significant figures

    Returns the rounded number
    """
    format_str = "{:." + str(sf) + "g}"
    rounded_value = float(format_str.format(value))
    return rounded_value

def read_excel(excel_path:str, sheet:str, column:int) -> list:
    """
    Reads an excel file

    Parameters:
    * `excel_path`: The path to the excel file
    * `sheet`:      The name of the sheet to read from
    * `column`:     The column index

    Returns a list of values corresponding to that column
    """
    data_frame = pd.read_excel(excel_path, sheet_name=sheet)
    data_list = list(data_frame.iloc[:,column])
    # data_list = list(filter(lambda x: not math.isnan(x), data_list))
    # data_list = [round_sf(data, 8) for data in data_list]
    return data_list

def remove_nan(data_list:list) -> list:
    """
    Removes nan values from a list of data values

    Parameters:
    * `data_list`: The list of data values

    Returns the list of data values without nan values
    """
    return list(filter(lambda x: not math.isnan(x), data_list))

def get_sorted(value_list:list, reverse:bool=True) -> tuple:
    """
    Gets the top values and indexes of a list of values
    
    Parameters:
    * `value_list`: The list of values
    
    Returns the list of top values and indexes
    """
    sorted_value_list = sorted(value_list, reverse=reverse)
    sorted_index_list = []
    for value in sorted_value_list:
        for i in range(len(value_list)):
            if value == value_list[i] and not i in sorted_index_list:
                sorted_index_list.append(i)
                break
    return sorted_value_list, sorted_index_list
