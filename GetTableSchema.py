import pandas as pd
import sqlite3

def get_table_schema():
	conn = sqlite3.connect('chinook.db')
	c = conn.cursor()

	def sq(str,con=conn):
		return pd.read_sql('''{}'''.format(str), con)
	
	tables_List = sq(
		'''select distinct name
		from sqlite_master
		where type='table';'''
		,conn)

	#Ouptput Variable
	output=[]
	# Initialize variables to store table and column information
	current_table = ""
	columns = []

	for index,row in tables_List.iterrows():
		#print(row["name"])
		#table_schema="DWH"
		table_name_single=row["name"]
		# table_name = f"{table_schema}.{table_name_single}"
		df = sq(f'''PRAGMA table_info({table_name_single});''',conn)
		for index,row in df.iterrows():
			# table_name = f"{table_schema}.{table_name_single}"
			table_name = f"{table_name_single}"
			column_name = row["name"]
			data_type = row["type"]
			if " " in table_name:
				table_name = f"[{table_name}]"
				column_name = row["name"]
			if " " in column_name:
				column_name = f"[{name}]"

			# If the table name has changed, output the previous table's information
			if current_table != table_name and current_table != "":
				output.append(f"table: {current_table}, columns: {', '.join(columns)}")
				columns = []

			# Add the current column information to the list of columns for the current table
			columns.append(f"{column_name} {data_type}")

			# Update the current table name
			current_table = table_name

		# Output the last table's information
		output.append(f"table: {current_table}, columns: {', '.join(columns)}")
		output = "\n".join(output)
return output
