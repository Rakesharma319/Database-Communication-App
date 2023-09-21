import streamlit as st
import sqlite3
import pandas as pd
from Curr_User_Fun import Current_User as CU
from GetTableSchema import get_table_schema as gts

st.title('CM DataChat App')
#curr_user=st.write(st.experimental_user['email'])
curr_user=st.experimental_user['email']
st.write(CU(curr_user))

st.write(gts())

