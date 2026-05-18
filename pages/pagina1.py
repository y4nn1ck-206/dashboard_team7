import streamlit as st

st.title('Welkom')

if st.session_state['naam']:
    st.success({st.session_state['naam']})