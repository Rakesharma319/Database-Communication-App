########### All Requirements Imported
import openai
import streamlit as st
import sqlite3
import pandas as pd
from Curr_User_Fun import Current_User as CU
from GetTableSchema import get_table_schema as gts

########### App Title with User Name
st.title("DataChat App")
curr_user=st.experimental_user['email']
st.write(CU(curr_user))

########### Ask api key
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
openai.api_key = openai_api_key

########### Frame Prompt

dialect="SQL"

few_shot_examples="""Select col1,col2
from tabl t1 join tabl2 t2 on t1.col1=t2.col2
Where t1.col
Group By t1.Col1
Order By t2.Col1;"""

TableSchema = gts()

Prompt = f"""Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

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
	st.session_state.messages.append({"role": "user", "content": UserInput})
	# Display user message in chat message container
	with st.chat_message("user"):
		st.markdown(UserInput)
		
	# Display assistant response in chat message container
	with st.chat_message("assistant"):
		message_placeholder = st.empty()
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
			
			# Execute SQL in Database.
			conn = sqlite3.connect('chinook.db')

			def sq(str,con=conn):
				return pd.read_sql('''{}'''.format(str), con)

			RawSQL=f"{full_response}"
			CleanSQL=RawSQL.replace("SQLQuery: \n","")
			df=sq(f'''{CleanSQL}''',conn)
			
			message_placeholder.markdown(df + "▌")
		message_placeholder.markdown(full_response)
	st.session_state.messages.append({"role": "assistant", "content": full_response})
