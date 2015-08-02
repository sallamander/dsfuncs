import pandas as pd

def load_data(filename):
	df = pd.read_csv(filename) 
	return df

def get_columns(df, column_list): 
	return df[column_list]
