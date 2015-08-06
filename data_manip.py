import scipy.stats as scs
from collections import defaultdict

def change_type(df, columns, type): 
	for column in columns: 
		df[column] = df[column].astype(type)

def test_transforms(target, feature, df=None): 
	if df: 
		target = df[target]
		feature = df[feature]

	transformations = {'x2': np.square, 'sqrt': np.sqrt, '1/x2': lambda x: 1 / (x ** 2), '1 / x': lambda x: 1 /x, 
					   'log': np.log }

	transforms_dict = {}
	for k, v in transformations.iteritems(): 
		feature_transformed = v(feature)
		pearson = scs.pearsonr(feature_transformed, target)
		transforms_dict[k] = pearson

	return transforms_dict

