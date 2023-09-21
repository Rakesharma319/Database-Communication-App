import streamlit as st
import sqlite3
from Curr_User_Fun import Current_User as CU

st.title('CM DataChat App')
#curr_user=st.write(st.experimental_user['email'])
curr_user=st.experimental_user['email']
st.write(CU(curr_user))

# Connect database

conn = sqlite3.connect('chinook.db')
c = conn.cursor()

def sq(str,con=conn):
    return pd.read_sql('''{}'''.format(str), con)

df=sq('''SELECT c.CustomerId, c.FirstName, c.LastName, SUM(i.Total) AS TotalInvoice
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId, c.FirstName, c.LastName
ORDER BY TotalInvoice DESC
LIMIT 5''',conn)

st.dataframe(df)

