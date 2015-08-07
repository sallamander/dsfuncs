# This is a module that will have some convience functions for plotting. For some, they 
# might actually be pretty convinient (like the ones that relate to plotting columsn from 
# data frames.) Others aren't really anything special - I just got tired of typing plt.feature
# any time I wanted to set a feature. 

import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np

def plt_specs(ax = None, xlab = None, ylab = None, title = None, save_title = None, 
			  sub_plot = None, xlim = None, ylim = None, xticks = None, yticks = None,
			  legend = None, tight_layout = None, grid_bool = None, axis = None): 
	# If the parameter was passed in, set it for that plot. Otherwise 
	# do nothing. The first parameter we check for is the axis = if the axis was 
	# passed, then we call the plt_axis function and plot everything on that axis. 
	# Then we come back and plot the more general plt things (tight layout and save_title. 
	if ax: 
		plt_axis(ax = ax, xlab = xlab, ylab = ylab, title = title, xlim = xlim, 
				 ylim =ylim, grid_bool = grid_bool, xticks = xticks, yticks = yticks, 
				 axis = axis)
	else: 
		if xlab: 
			plt.xlabel(xlab)
		if ylab: 
			plt.ylabel(ylab)
		if title: 
			plt.title(title)
		if xlim: 
			plt.xlim(xlim)
		if ylim: 
			plt.ylim(ylim)
	if grid_bool is not None and ax is None: 
		sub = plt.subplot(1, 1,1)
		sub.grid(grid_bool)
	if legend:
		plt.legend(loc = 'best') 
	if tight_layout: 
		plt.tight_layout()
	if xticks: 
		plt.xticks(xticks)
	if yticks: 
		plt.yticks(yticks)
	if axis: 
		plt.axis(axis)
	# This needs to be the last thing, or else anything rendered after this won't save. 
	if save_title: 
		plt.savefig(save_title)

def plt_axis(ax = None, xlab = None, ylab = None, title = None, xlim = None, ylim = None, grid_bool = None, legend = None, 
			xticks = None, yticks = None, axis = None): 
	# If the parameter was passed in, then set it for the axis that is passed in. Note that 
	# an axis has to be passed in. It's not explicit, since I have put a default in as None - I'm 
	# using that to let the user know that an axis has to be passed in. 
	if ax is None: 
		raise Exception('No axis passed in... if there isnt one, try using plt_specs instead.')
	if xlab: 
		ax.set_xlabel(xlab)
	if ylab: 
		ax.set_ylabel(ylab)
	if title: 
		ax.set_title(title)
	if xlim: 
		ax.set_xlim(xlim)
	if ylim: 
		ax.set_ylim(ylim)
	if legend: 
		ax.legend = True
	if xticks: 
		ax.xticks(xticks)
	if yticks: 
		ax.yticks(yticks)
	if axis: 
		ax.axis(axis)
	if grid_bool is not None: 
			ax.grid(grid_bool)

def df_hist(df, bins = 20, kde = False, norm_hist = True, columns = None, gridsize = None, xlim = None, 
			ylim = None, xlab = None, ylab = None, legend = None, hist_kws = None, grid_bool = None,
			title = None, save_title = None, tight_layout = None): 
	# We'll iterate through the columns the user passes in and plot a histogram for 
	# each column. If no columns were passed in, then plot a histogram for all of them. 
	plot_columns = df.columns if columns is None else columns
	if gridsize is None: 
		# If the gridsize is empty, then what we'll do is to simply make an n x n grid, where
		# n is equal to the sqrt of the number of columns (take the ciel of that though). 
		# It'll end up as square as possible.  The only issue with this is if there are only two
		# columns - we end up with a 2 by 2 plot, but we really just want a 1 x 2. 
		sqrt_columns = math.ceil(len(plot_columns) ** 0.5)
		gridsize = (sqrt_columns, sqrt_columns)
		
		if len(plot_columns) == 2: 
			gridsize = (1, 2)

	for index, col in enumerate(plot_columns): 
		# Grab the appropriate column of the data. Using ix 
		data = df.ix[:, col]
		sub = plt.subplot(gridsize[0], gridsize[1], index + 1)
		data = np.nan_to_num(data)
		sns.distplot(data, hist = True, bins = bins, kde = kde, norm_hist = norm_hist, hist_kws = hist_kws)
		plt_specs(ax = sub, xlim = xlim, ylim = ylim, xlab = xlab, ylab = ylab, title = title, legend = legend, 
		 		  grid_bool = grid_bool, save_title = save_title, tight_layout = tight_layout)