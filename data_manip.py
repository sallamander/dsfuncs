def change_type(df, column, type): 
	df[column] = df[column].astype(type)