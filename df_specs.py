import pandas as pd
import numpy as np

def load_data(filename):
	df = pd.read_csv(filename) 
	return df

def get_columns(df, column_list, filename = None, output = False): 
	return df[column_list]

def output_columns(df, df_name, filename, append = True, pdb = False):
	# If the user has selected to append to the file then 
	# we need to make sure we do that.  
	write_mode = 'a' if append else 'w'

	# Create the file if it doesn't already exist. 
	try: 
		open(filename, 'r') 
	except: 
		with open(filename, 'w') as f: 
			pass

	with open(filename, 'rw') as f: 
		df_columns = pd.DataFrame({df_name: df.columns})
		# If the write mode is append, then I need to read in the current 
		# file contents and append to that. 
		if write_mode == 'a': 
			file_contents = pd.read_csv(filename)
			file_output = file_contents.join(df_columns, how = 'outer', lsuffix = 'l', rsuffix = 'r')
			file_output.to_csv(path_or_buf=filename, sep = ',', index = False)
		else: 
		# If it's not in append mode then I just take the colums and name input and output 
		# it to the .csv. 
			df_columns.to_csv(path_or_buf=filename, sep = ',', index = False)


		
			