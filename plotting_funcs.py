# This is a module that will have some convience functions for plotting. For some, they 
# might actually be pretty convinient (like the ones that relate to plotting columsn from 
# data frames.) Others aren't really anything special - I just got tired of typing plt.feature
# any time I wanted to set a feature. 

import matplotlib.pyplot as plt

def plt_specs(xlab = None, ylab = None, title = None, save_title = None, 
			  sub_plot = None, xlim = None, ylim = None, 
			  legend = None, tight_layout = None): 
	# If the parameter was passed in, set it for that plot. Otherwise 
	# do nothing. 
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
	if legend:
		plt.legend() 
	if tight_layout: 
		plt.tight_layout()
	### Make sure this is the last thing!
	if save_title: 
		plt.savefig(save_title)

def plt_axis(ax = None, xlab = None, ylab = None, title = None, xlim = None, ylim = None, grid = None): 
	# If the parameter was passed in, then set it for the axis that is passed in. Note that 
	# an axis has to be passed in. It's not explicit, since I have put a default in as None - I'm 
	# using that to let the user know that an axis has to be passed in. 
	if ax is None: 
		raise Exception('No axis passed in... if there isnt one, try using plt_specs instead.')
	if xlab: 
		ax.xlabel(xlab)
	if ylab: 
		ax.ylabel(ylab)
	if title: 
		ax.set_title(title)
	if xlim: 
		ax.xlim(xlim)
	if ylim: 
		ax.ylim(ylim)
	if grid: 
		ax.grid(grid)