import scipy.stats as scs
import numpy as np
from collections import defaultdict

def change_type(df, columns, type): 
	for column in columns: 
		df[column] = df[column].astype(type)

	return df

def test_transforms(target, feature, df=None): 
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

