def change_type(df, columns, type): 
	for column in columns: 
		df[column] = df[column].astype(type)