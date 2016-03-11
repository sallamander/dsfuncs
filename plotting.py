import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from itertools import izip

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

    var_data_counts = var_data.value_counts()
    var_data_percs = var_data_counts / var_data_counts.sum()

    ax = sns.barplot(var_data_percs.index, 
            var_data_percs.values, palette="BuGn_d") 
    bars = ax.patches
    labels = var_data_percs.values
    indices = var_data_percs.index
    labels_font = {'fontname':'Arial', 'size':'12', 
            'color':'black', 'weight':'normal', 'verticalalignment':'bottom'}

    for idx, bar, label in izip(indices, bars, labels): 
        height = bar.get_height()
        label = label * 100
        ax.text(idx, height, "{0:.2f}".format(label), 
                ha='center', va='bottom', **labels_font)

    plt.show()

def _plot_continuous_var_dist(var_data): 
    """Plot a boxplot of the continuous variable data inputted, both with 
    and without outliers. 

    Args: 
        var_data: 1d numpy.ndarray
    """

    # Plot the data with outliers. 
    plt.subplot(1, 2, 1)
    var_data.plot(kind='box')

    var_data_wo_outliers = remove_outliers(var_data)
    # Plot the data without outliers. 
    plt.subplot(1, 2, 2)
    var_data_wo_outliers.plot(kind='box')

    plt.show()
