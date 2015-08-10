
import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np

def plt_specs(ax = None, xlab = None, ylab = None, title = None, save_title = None, 
			  sub_plot = None, xlim = None, ylim = None, xticks = None, yticks = None,
			  legend = None, tight_layout = None, grid_bool = None, axis = None, tit_fontsize = 16): 
	'''
	Inputs: Any of a number of plotting parameters. 
	Outputs: None. 

	If a given plotting parameter was passed in, set it for that plot. Otherwise do nothing. 
	The first parameter we check for is the axis. If the axis was passed, then we call the plt_axis 
	function and plot everything on that axis. Then we come back and plot the more general plt things 
	(tight layout and save_title).  

	This function is a convenience function to save time from having to type plt. all the time. 
	'''
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
			plt.title(title, fontsize=tit_fontsize)
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
	''' 
	Input: Any number of matplotlib.pyplot.axis parameters. 
	Output: None. 

	If the parameter was passed in, then set it for the axis that is passed in. This is an axis 
	version of the plt_specs function. Note that an axis has to be passed in. It's not explicit, 
	since I have put a default in as None - I'm using that to let the user know that an axis has 
	to be passed in. 
	''' 

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
	'''
	Input: DataFrame, possible plotting parameters. 
	Output: Grid of Seaborn histogram plots. 

	The point of this function is just to give a little bit more flexibility than the pandas.df.hist
	function that is offered. Instead of restricting all histograms to look the exact same (as in the 
	pandas.df.hist function), I want users to be able to pass parameters for each of those histograms. If
	they want the x-label on one histogram to be different than the others, so be it. If they want the grid 
	off on all of their histograms, then I want to make that happen. 

	As of right now, this function doesn't offer too much functionality past the pandas.df.hist function 
	that currrently exists. It is a work in progress. 
	'''
	# If the user didn't pass a list of columns in, then plot all columns in the DataFrame. 
	plot_columns = df.columns if columns is None else columns
	if gridsize is None: 
		# If the user doesn't pass in a gridsize, make it as close to n x n as possible, where 
		# n is the sqrt of the number of columns, unless there are two, in which case we default
		# to a (1, 2). 
		sqrt_columns = math.ceil(len(plot_columns) ** 0.5)
		gridsize = (sqrt_columns, sqrt_columns)
		
		if len(plot_columns) == 2: 
			gridsize = (1, 2)

	for index, col in enumerate(plot_columns): 
		data = df.ix[:, col]
		sub = plt.subplot(gridsize[0], gridsize[1], index + 1)
		data = np.nan_to_num(data)
		sns.distplot(data, hist = True, bins = bins, kde = kde, norm_hist = norm_hist, hist_kws = hist_kws)
		plt_specs(ax = sub, xlim = xlim, ylim = ylim, xlab = xlab, ylab = ylab, title = title, legend = legend, 
		 		  grid_bool = grid_bool, save_title = save_title, tight_layout = tight_layout)