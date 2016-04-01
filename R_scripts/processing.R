# -------------------------------------------------------------------- #
# -------------------------------------------------------------------- #
# processing.R
# A basic set of tools for processing data. 
# sallamander 1 April 2016, Last Update 1 April 2016 
# -------------------------------------------------------------------- #
# -------------------------------------------------------------------- #
require('stats')

# -------------------------------------------------------------------- #
# -------------------------------------------------------------------- #
# Function to remove outliers, as denoted by being an inputted number 
# of standard deviations from the mean. 
# Arguments: 
#   -- data: Numerical array
#   -- std_dev_cutoff (optional): integer/float
# -------------------------------------------------------------------- #
# -------------------------------------------------------------------- #

remove_outliers <- function(data, std_dev_cutoff=2) {
    
    data_mean = mean(data)
    data_std_dev = sd(data)

    lower_bound = data_mean - std_dev_cutoff * data_std_dev
    upper_bound = data_mean + std_dev_cutoff * data_std_dev

    filtered_data = data[data > lower_bound & data < upper_bound]

    return(filtered_data)
}
