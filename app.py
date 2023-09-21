import streamlit as st
from Curr_User_Fun import Current_User as CU

st.title('CM DataChat App')
#curr_user=st.write(st.experimental_user['email'])
curr_user=st.experimental_user['email']
st.write(CU(curr_user))
