import pandas as pd
import streamlit as st

@st.cache_data
def load_data(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        df = pd.read_csv(
            uploaded_file,
            low_memory = False
        )

    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    elif file_name.endswith(".json"):
        df = pd.read_json(uploaded_file)

    else:
        raise ValueError("Unsupported file format.")

    return df

def initialize_session_state(df, file_name):
    if "original_df" not in st.session_state:
        st.session_state.original_df = df.copy()
    
    if "working_df" not in st.session_state or st.session_state.get("current_file") != file_name:
        st.session_state.working_df = df.copy()
        st.session_state.current_file = file_name
    
    if "cleaning_completed" not in st.session_state:
        st.session_state.cleaning_completed = False
    
    if "cleaning_log" not in st.session_state:
        st.session_state.cleaning_log = []
    
    if "warning_log" not in st.session_state:
        st.session_state.warning_log = []
    
    if "outlier_cols" not in st.session_state:
        st.session_state.outlier_cols = []