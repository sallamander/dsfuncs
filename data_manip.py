import scipy.stats as scs
import numpy as np
from collections import defaultdict

def change_type(df, columns, type): 
	'''
	Input: Data Frame, list of columns, list of types
	Ouput: DataFrame with each column in list of columns changed to the type in the corresponding.
	in list of types. 
	'''

	for column in columns: 
		df[column] = df[column].astype(type)

	return df

def test_transforms(target, feature, df=None): 
	''' 
	Input: Column DataFrame/Numpy Array, Column DataFrame/Numpy Array
	Output: Dictionary of possible transformations as keys and correlation values as values. 

	This function runs through a number of different transformations that we could perform on our 
	feature/X variable and calculates the pearson correlation between the target and transformed 
	feature. It outputs a dictionary that holds the results of each transformation, as well as a 
	key named 'best' that corresponds to the transformation that had the highest pearson correlation 
	(in absolute value). 
	'''

	if df: 
		target = df[target]
		feature = df[feature]

	transformations = {'x2': np.square, 'sqrt': np.sqrt, '1/x2': lambda x: 1 / (x ** 2), '1 / x': lambda x: 1 /x, 
					   'log': np.log }

	transforms_dict = {}
	best = 0
	for k, v in transformations.iteritems(): 
		feature_transformed = v(feature)
		mask = np.logical_and(~np.isnan(feature_transformed), ~np.isinf(feature_transformed))
		feature_transformed = feature_transformed[mask]
		pearson = scs.pearsonr(feature_transformed, target[mask])
		transforms_dict[k] = pearson
		if abs(pearson[0]) > best: 
			best = abs(pearson[0])
			transforms_dict['best'] = k


	return transforms_dict

