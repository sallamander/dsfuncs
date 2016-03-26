"""A fairly basic set of tools for plotting the distributions 
of variables. 

Only two functions here are meant to be called externally, while 
the rest are used internally. `plot_dist_var` and 
`plot_binary_response` are those two. 

The former plots the distribution of an inputted categorical or 
continuous variable. If categorical, it creates a bar plot with the 
heights equal to the percentage of each category. If continuous, 
it creates 4 plots - a box and then hist/kde with and without outliers. 
The latter creates a bar plot for a categorical variable, with 
the heights equal to the percentage of each category, but with the  
bar text equal to percentage of True's in a response variable. 
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from itertools import izip

from .processing import remove_outliers

def plot_var_dist(var_data, categorical, show=True, ax=None): 
    """Plot the distribution of the inputted variable data. 

    Given the inputted data, plot the distribution of the data
    by calling the relevant function (continuous or categorical). 

    Args: 
        var_data: 1d numpy.ndarray
        categorical: bool
        show (optional): bool 
            Whether or not to show the plot. Defaults to True. 
        ax (optional): matplotlib.pylot.Axes object(s)
            Axes to plot the following plots on. Current usage 
            expects that if it is passed in, this axes object 
            contains 4 individual axes to plot on - 1 each for 
            a boxplot and hist/kde both with and without outliers.  
    """

    if not categorical: 
        _plot_continuous_var_dist(var_data, ax, show)
    else: 
        _plot_categorical_var_dist(var_data, ax, show)

def _plot_categorical_var_dist(var_data, ax, show): 
    """Plot a boxplot of the continuous variable data inputted. 
    
    This is a helper function called from plot_var_dist. It'll 
    be used in the case that categorical data is passed in. 

    Args: 
        var_data: 1d numpy.ndarray
        ax: matplotlib.pyplot.Axes object 
            This may or may not be None, depending on what 
            was passed from plot_var_dist. 
        show: bool 
    """

    var_data_counts = var_data.value_counts()
    var_data_percs = var_data_counts / var_data_counts.sum()

    if ax: 
        sns.barplot(var_data_percs.index, 
                var_data_percs.values, palette="BuGn_d", ax=ax)
    else: 
        ax = sns.barplot(var_data_percs.index, 
                var_data_percs.values, palette="BuGn_d") 
    bars = ax.patches
    labels = var_data_percs.values
    _add_bar_text(ax, bars, labels) 

    if show: 
        plt.show()

def _add_bar_text(ax, bars, labels): 
    """Add text labels to some plotted bars. 

    Args: 
        ax: matplotlib.axes object
        bars: matplotlib.patches object
        labels: numpy.ndarray
    """

    labels_font = {'fontname':'Arial', 'size':'12', 
            'color':'black', 'weight':'normal', 'verticalalignment':'bottom'}

    for idx, bar, label in izip(xrange(len(labels)), bars, labels): 
        height = bar.get_height()
        width = bar.get_width()
        label = label * 100
        ax.text(idx, height, "{0:.2f}".format(label), 
                ha='center', va='bottom', **labels_font)

def _plot_continuous_var_dist(var_data, ax, show): 
    """Plot a boxplot of the continuous variable data inputted, both with 
    and without outliers. 

    This is a helper function called from plot_var_dist. It'll 
    be used in the case that continuous data is passed in. 

    Args: 
        var_data: 1d numpy.ndarray
        ax: matplotlib.pyplot.Axes object 
            This may or may not be None, depending on what 
            was passed from plot_var_dist. If it is None, 
            then we'll build a set of 4 axes with no given 
            figure size and run with it. The idea is that this 
            will be used to plot both a box and hist/kde with 
            and without outliers.
        show: bool 
    """
   
    if ax is None: 
        f, ax = plt.subplots(1, 4)
    
    # Plot the data with outliers. 
    _plot_box(var_data, ax[0], outliers=True)
    _plot_hist_kde(var_data, ax[1], outliers=True)

    var_data_wo_outliers = remove_outliers(var_data)

    # Plot the data without outliers. 
    _plot_box(var_data_wo_outliers, ax[2], outliers=False)
    _plot_hist_kde(var_data, ax[3], outliers=False)

    if show: 
        plt.show()

def _plot_box(var_data, ax, outliers=True): 
    """Plot a boxplot of the continuous variable data inputted. 

    This is a helper function called from _plot_continuous_var_dist, 
    used for plotting a box plot of the continuous variable data. 

    Args: 
        var_data: 1d numpy.ndarray
        ax: matplotlib.pyplot.Axes object
        outliers (optional): bool
            This helps us determine what the title for the 
            plot will be. 
    """

    title = "With Outliers" if outliers else "Without outliers"

    var_data.plot(kind='box', ax=ax)
    ax.set_title(title)

def _plot_hist_kde(var_data, ax, outliers=True): 
    """Plot a histogram/kde with the continuous variable data inputted. 

    This is a helper function called from _plot_continuous_var_dist, 
    used for plotting a box plot of the continuous variable data. 

    Args: 
        var_data: 1d numpy.ndarray
        ax: matplotlib.pyplot.Axes object
        outliers (optional): bool
            This helps us determine what the title for the 
            plot will be. 
    """

    title = "With Outliers" if outliers else "Without outliers"
    sns.distplot(var_data, bins=20, ax=ax)
    ax.set_title(title)

def plot_binary_response(df, categorical, response): 
    """Plot the percentage of a True/False binary response across
    a categorical variable. 

    Take the inputted DataFrame, and plot the binary response variable
    percentages across cateogries of a categorical variable. For each 
    category in the categorical variable, use the percent of True's as the 
    height of the bar. Use the percent of the total obs. that that category 
    makes up as the text above the bar. 

    Args: 
        df: Pandas DataFrame
        categorical: str
            Holds the column name of the categorical variable. 
        response: str
            Holds the column name of the response variable. 
    """

    category_numbers = df.groupby(categorical).count().iloc[:, 0]
    category_percents = category_numbers / category_numbers.sum()
    
    categories = category_numbers.index

    response_percents = []
    for idx, category in enumerate(categories):
        response_counts = ((df[categorical] == category) & 
            (df[response] == True)).sum()
        response_cat_percent = float(response_counts) / category_numbers[idx] 
        response_percents.append(response_cat_percent)

    ax = sns.barplot(categories, response_percents, palette="BuGn_d") 

    bars = ax.patches
    labels = category_percents.values
    _add_bar_text(ax, bars, labels) 

    plt.show()
