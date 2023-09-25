########### All Requirements Imported
import openai
import streamlit as st
import sqlite3
import pandas as pd
from Curr_User_Fun import Current_User as CU
from GetTableSchema import get_table_schema as gts

import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from pathlib import Path
import os
import datetime


########### App Title with User Name
st.title("Database Communication App")

delimiters = ["@", "GITHUB"]
curr_user=st.experimental_user['email']
st.write(CU(curr_user,delimiters))

########### Ask api key
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
openai.api_key = openai_api_key

######## SQL Connection
conn = sqlite3.connect('chinook.db')
def sq(str,con=conn):
	return pd.read_sql('''{}'''.format(str), con)

######### Table lists for reference

tables_List = sq(
    '''select distinct name
    from sqlite_master
    where type='table';'''
    ,conn)

st.sidebar.text('Tables For Reference')
st.sidebar.table(tables_List)


########### Frame Prompt

dialect="SQL"

few_shot_examples = """
<<Template>>
Question: User Question
Thought 1: Your thought here.
Action: 
```python
#Import neccessary libraries here
import numpy as np
#Query some data 
sql_query = "SOME SQL QUERY"
step1_df = execute_sql(sql_query)
# Replace 0 with NaN. Always have this step
step1_df['Some_Column'] = step1_df['Some_Column'].replace(0, np.nan)
#observe query result
observe("some_label", step1_df) #Always use observe() instead of print
```
Observation: 
step1_df is displayed here
Thought 2: Your thought here
Action:  
```python
import plotly.express as px 
#from step1_df, perform some data analysis action to produce step2_df
#To see the data for yourself the only way is to use observe()
observe("some_label", step2_df) #Always use observe() 
#Decide to show it to user.
fig=px.line(step2_df)
#visualize fig object to user.  
show(fig)
#you can also directly display tabular or text data to end user.
show(step2_df)
```
Observation: 
step2_df is displayed here
Answer: Your final answer and comment for the question
<</Template>>

"""

TableSchema = gts()

Prompt = f"""Given an input question, first create a syntactically correct {dialect} query to run, 
always show distinct data,
default show limited 10 rows until user ask for all rows.
        1. Use plotly library for data visualization. 
            - If you want to show  user a plotly visualization, then use ```show(fig)`` 
            - If you want to show user data which is a text or a pandas dataframe or a list, use ```show(data)```
            - Never use print(). User don't see anything with print()
        2. Lastly, don't forget to deal with data quality problem. You should apply data imputation technique to deal with missing data or NAN data.

SQLQuery: "SQL Query to run"

Only use the following tables:

{TableSchema}.

Some examples of SQL queries that corrsespond to questions are:

{few_shot_examples}

"""


# Set a default model
if "openai_model" not in st.session_state:
	st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
	st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])
		
# Accept user input
if UserInput := st.chat_input("Create a Snowflake query for top 5 customers by maximum total invoice"):
	# Add user message to chat history
	#st.session_state.messages.append({"role": "user", "content": UserInput})
	# Display user message in chat message container
	with st.chat_message("user"):
		st.markdown(UserInput)
		
	# Display assistant response in chat message container
	with st.chat_message("assistant"):
		#message_placeholder = st.empty()
		full_response = ""
		for response in openai.ChatCompletion.create(
			model=st.session_state["openai_model"],
			messages = [{"role": "user", "content": f'''{Prompt},Question: {UserInput}'''}],
			temperature=0,
			max_tokens=300,
			stream=True
		):
			full_response += response.choices[0].delta.get("content", "")
			#message_placeholder.markdown(full_response + "▌")
		#message_placeholder.markdown(full_response)
		
		# Execute SQL in Database.
		OutPut_raw=full_response
		RawSQL=f"{OutPut_raw}"
		CleanSQL=RawSQL.replace("SQLQuery: \n","")
		CleanSQL=RawSQL.replace("SQLQuery: ","")
		Database_Output=sq(f'''{CleanSQL}''',conn)
	st.text(full_response)
	st.table(Database_Output)
	#st.session_state.messages.append({"role": "assistant", "content": full_response})
	#st.session_state.messages.append({"role": "assistant", "content": Database_Output})

	
	

	
