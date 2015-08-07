import pandas as pd
import numpy as np

# This function here is so that you can get an easily readable format 
# for all the columns in your dataframes. This isn't really worthwhile when you only 
# have a couple of data frames, or a data frame with only 1 or two columns. 
# But, if you have 10 dataframes/csvs in one project, this should pretty quickly allow 
# you to get a .csv file where you can get the different columns in each table. 
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
			file_contents = load_data(filename)
			file_output = file_contents.join(df_columns, how = 'outer', lsuffix = 'l', rsuffix = 'r')
			file_output.to_csv(path_or_buf=filename, sep = ',', index = False)
		else: 
		# If it's not in append mode then I just take the colums and name input and output 
		# it to the .csv. 
			df_columns.to_csv(path_or_buf=filename, sep = ',', index = False)

# This function will take in as input a DataFrame object. It will then 
# compare its columns to the columns frome one of two places. 

# 1.) If a filename is entered, then it that file will be read in. If compare_csv is True, 
# then I will assume that the filename is another DataFrame, and I will read that in and 
# output the columns the two share. If not, then I will asume that it is the output of 
# output_columns (see above), and I will compare the columns from input_df to the columns 
# in every table listed in the filename, or only the table compare_df if that is not None. 

# 2.) If no filename is entered, then compare_df must be an inputted DataFrame object, in which
# case I will simply output the columns that input_df and output_df have in common. 
def get_similar_columns(input_df, filename = None, compare_df = None, compare_csv = False): 
	# Handle the case of the filename being present first. Everything else depends upon this. 
	if filename: 
		if compare_csv: 
			# Read the filename in as a DataFrame. 
			file_df = load_data(filename)




		
			