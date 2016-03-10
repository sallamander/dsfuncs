import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from .processing import remove_outliers

def plot_var_dist(var_data, categorical=False): 
    """Plot the distribution of the inputted variable data. 

    Given the inputted data, plot the distribution of the data
    by calling the relevant function (continuous or categorical). 

    Args: 
        var_data: 1d numpy.ndarray
        categorical: bool
    """

    if not categorical: 
        _plot_continuous_var_dist(var_data)
    else: 
        _plot_categorical_var_dist(var_data)

def _plot_categorical_var_dist(var_data): 
    """Plot a boxplot of the continuous variable data inputted. 

    Args: 
        var_data: 1d numpy.ndarray
    """
    pass 

def _plot_continuous_var_dist(var_data): 
    """Plot a boxplot of the continuous variable data inputted, both with 
    and without outliers. 

    Args: 
        var_data: 1d numpy.ndarray
    """
    pass

