import pandas as pd
import numpy as np

def output_columns(df, df_name, filename, append = True):
	'''
	Input: DataFrame, string, filename
	Output: CSV saved as filename with all of the columns from DataFrame

	This function will save all of the columns from the DataFrame into a .csv. The df_name
	is simply a string that tells the CSV what to call that DataFrame. The append option 
	tells the output_columns function to append to the file, otherwise create it and write to 
	it. 
	'''
	write_mode = 'a' if append else 'w'

	try: 
		open(filename, 'r') 
	except: 
		with open(filename, 'w') as f: 
			pass

	with open(filename, 'rw') as f: 
		df_columns = pd.DataFrame({df_name: df.columns})
		if write_mode == 'a': 
			file_contents = load_data(filename)
			file_output = file_contents.join(df_columns, how = 'outer', lsuffix = 'l', rsuffix = 'r')
			file_output.to_csv(path_or_buf=filename, sep = ',', index = False)
		else: 
			df_columns.to_csv(path_or_buf=filename, sep = ',', index = False)

def get_similar_columns(input_df, filename = None, compare_df = None, compare_csv = False): 
	'''
	Input: DataFrame, Dataframe/CSV/filename
	Output: List of Strings

	This function returns the columns that the input DataFrame has in common with each of the columns 
	in the DatafFrame passed in (compare_df), each of the DataFrames saved in the filename (something
	similar in format to the output of to dsfuncs.df_specs.output_columns), or the the columns in the 
	DataFrame store in the compare_csv parameter. 

	Preference order if all three of filename, compare_df, and compare_csv are passed in is exactly in 
	that order. 

	This function is currently unfinshed. 

	'''
	if filename: 
		if compare_csv: 
			# Read the filename in as a DataFrame. 
			file_df = load_data(filename)




		
			