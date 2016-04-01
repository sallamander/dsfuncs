"""A fairly basic set of tools for data processing. 

As of now, there is only one fuction in the module - 
`remove_outliers`. 

`remove_outliers` is meant to remove outliers from your
inputted data, where outliers are defined to be so many
standard deviations way from the mean. 
"""

import numpy as np

def remove_outliers(data, std_dev_cutoff=2): 
    """Remove outliers from the inputted data. 

    This function will remove outliers from the inputted data, based
    off of a potentially inputted method.  Right now, it will simply
    allow removal based off of how many standard deviations an ob.
    is from the mean. Two standard deviations is used by default, but 
    it is available as an argument to be passed in. 

    Args: 
        data: 1d numpy.ndarray 
        std_dev_cutoff: int
            defines how many standard deviations to go away 
            from the mean to label outliers 
    """

    mean, std_dev = data.mean(), data.std()

    lower_bound = mean - std_dev_cutoff * std_dev
    upper_bound = mean + std_dev_cutoff * std_dev

    filtered_data = data[np.logical_and(data >= lower_bound, 
            data <= upper_bound)]

    return filtered_data
