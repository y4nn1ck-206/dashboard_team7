import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
 
import streamlit as st
if 'naam' not in st.session_state:
    st.session_state['naam'] = ''

st.session_state['naam'] = st.text_input('volledige naam?')