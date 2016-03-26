import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from itertools import izip

from .processing import remove_outliers

def plot_var_dist(var_data, categorical=False, ax=None, show=True): 
    """Plot the distribution of the inputted variable data. 

    Given the inputted data, plot the distribution of the data
    by calling the relevant function (continuous or categorical). 

    Args: 
        var_data: 1d numpy.ndarray
        categorical: bool
    """

    if not categorical: 
        _plot_continuous_var_dist(var_data, ax, show)
    else: 
        _plot_categorical_var_dist(var_data, ax, show)

def _plot_categorical_var_dist(var_data, ax, show): 
    """Plot a boxplot of the continuous variable data inputted. 

    Args: 
        var_data: 1d numpy.ndarray
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

    Args: 
        var_data: 1d numpy.ndarray
    """

    # Plot the data with outliers. 
    if ax is not None: 
        _plot_box(var_data, ax[0], outliers=True)
        _plot_hist_kde(var_data, ax[1], outliers=True)
    else: 
        ax = plt.subplot(1, 4, 1)
        var_data.plot(kind='box')
        ax.set_title('With Outliers')
        ax = plt.subplot(1, 4, 2)
        sns.distplot(var_data, bins=20, ax=ax)
        ax.set_title('With Outliers')

    var_data_wo_outliers = remove_outliers(var_data)
    # Plot the data without outliers. 
    if ax is not None: 
        _plot_box(var_data_wo_outliers, ax[2], outliers=False)
        _plot_hist_kde(var_data, ax[3], outliers=False)
    else: 
        ax = plt.subplot(1, 4, 3)
        var_data_wo_outliers.plot(kind='box')
        ax.set_title('Without outliers')
        ax = plt.subplot(1, 4, 4)
        sns.distplot(var_data_wo_outliers, bins=20, ax=ax)
        ax.set_title('Without outliers')
    

    if show: 
        plt.show()

def _plot_box(var_data, ax, outliers=True): 
    """Plot a boxplot of the continuous variable data inputted

    Args: 
        var_data: 1d numpy.ndarray
    """

    title = "With Outliers" if outliers else "Without outliers"
    if ax is not None: 
        var_data.plot(kind='box', ax=ax)
        ax.set_title(title)
    else: 
        ax = plt.subplot(1, 1, 1)
        var_data.plot(kind='box', ax=ax)
        ax.set_title('With Outliers')

def _plot_hist_kde(var_data, ax, outliers=True): 
    """Plot a histogram/kde with the continuous variable data inputted. 

    Args: 
        var_data: 1d numpy.ndarray
    """

    title = "With Outliers" if outliers else "Without outliers"
    if ax is not None: 
        sns.distplot(var_data, bins=20, ax=ax)
        ax.set_title(title)
    else: 
        ax = plt.subplot(1, 1, 1)
        sns.distplot(var_data, bins=20, ax=ax)
        ax.set_title('With Outliers')

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
