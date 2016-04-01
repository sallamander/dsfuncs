# -------------------------------------------------------------------- #
# -------------------------------------------------------------------- #
# dist_plotting.R
# A fairly basic set of tools for plotting the distributions of variables. 
# sallamander 1 April 2016, Last Update 1 April 2016 
# -------------------------------------------------------------------- #
# -------------------------------------------------------------------- #

require('plyr')
require('ggplot2')

# -------------------------------------------------------------------- #
# -------------------------------------------------------------------- #
# Bar plot of categorical variable, by percentage of each cateogry.  
# Arguments: 
#   -- var_data: Factor array
#   -- save (optional): str - filepath location to save figure at
# -------------------------------------------------------------------- #
# -------------------------------------------------------------------- #

plot_categorical_var_dist <- function(var_data, save=NULL) {

    var_data_df = count(var_data)
    var_data_df$perc = var_data_df$freq / sum(var_data_df$freq)

    num_categories = length(var_data_df$perc)
    label_x_coords = seq(from=0.7, by=1.2, length.out=num_categories)
    percs = var_data_df$perc
    max_perc = max(percs)

    bp = barplot(height=var_data_df$perc, names.arg = var_data_df[, 1], 
            ylim=c(0, max_perc + 0.07))
    for (idx in seq(num_categories)) {
        text(label_x_coords[idx], percs[idx] + 0.05, percs[idx] * 100)
    }

    if(!is.null(save)){
        dev.copy(png, save) 
        def.off()
    } 
    return(bp)
}
