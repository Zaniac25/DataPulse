import streamlit as st
import pandas as pd
from cleaning import auto_clean_dataset, data_cleaning_module
from utils import detect_outlier_columns

def sidebar_controls():
    with st.sidebar:
        st.header("Dashboard Controls")
        st.write("Upload dataset to begin analysis")
        uploaded_file = st.file_uploader("Upload File", type=["csv","xlsx","json"])
    return uploaded_file

def dataset_preview(df):
    st.subheader("Dataset Preview")
    st.dataframe(df.head(20), use_container_width=True, height=400)

def display_dataset_metrics(display_df):
    total_missing = int(display_df.isnull().sum().sum())
    duplicate_rows = int(display_df.duplicated().sum())
    
    numeric_cols = display_df.select_dtypes(include='number').columns.tolist()
    outlier_columns = 0

    for col in numeric_cols:
        Q1 = display_df[col].quantile(0.25)
        Q3 = display_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - (1.5 * IQR)
        upper = Q3 + (1.5 * IQR)
        outliers = display_df[(display_df[col] < lower) | (display_df[col] > upper)]

        if len(outliers) > 0:
            outlier_columns += 1
    
    empty_columns = int(display_df.columns[display_df.isnull().all()].shape[0])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", display_df.shape[0])
    col2.metric("Columns", display_df.shape[1])
    col3.metric("Missing Values", total_missing)
    
    col4, col5, col6 = st.columns(3)
    col4.metric("Duplicate Rows", duplicate_rows)
    col5.metric("Outlier Columns", outlier_columns)
    col6.metric("Empty Columns", empty_columns)
    
    return total_missing, duplicate_rows, outlier_columns

def display_health_score(
        display_df, 
        total_missing, 
        duplicate_rows, 
        outlier_columns
    ):
    st.subheader("Dataset Health Score")
    health_score = 100
    health_score -= min(int(total_missing / max(len(display_df), 1) * 100), 40)
    health_score -= min(duplicate_rows * 2, 20)
    health_score -= min(outlier_columns * 5, 40)
    health_score = max(0, health_score)
    st.progress(health_score / 100)
    st.metric("Health Score", f"{health_score}%")

def smart_auto_cleaning_ui(working_df):
    with st.container(border=True):
        st.subheader("Smart Auto Cleaning")
        st.write("### What Smart Cleaning Will Fix")
        st.markdown("""
            - Remove duplicate rows
            - Fill missing numeric values using median
            - Fill missing categorical values using mode
            - Standardize column names
            - Trim extra spaces from text columns
            - Remove empty columns
            - Remove constant columns
            - Attempt automatic datatype conversion
        """)
        st.write("### What It Will Only Analyse")
        st.markdown("""
            - Detect outlier columns
            - Detect high missing percentage columns
            - Show warnings for risky columns
            - Leave advanced manual cleaning decisions to user
        """)
        
        if st.button("Auto Clean Dataset", use_container_width=True, type="primary"):
            before_rows = working_df.shape[0]
            before_missing = working_df.isnull().sum().sum()
            
            auto_cleaned_df, cleaning_log, warning_log, outlier_cols = auto_clean_dataset(working_df)
            
            st.session_state.working_df = auto_cleaned_df
            st.session_state.cleaning_completed = True
            st.session_state.cleaning_log = cleaning_log
            st.session_state.warning_log = warning_log
            st.session_state.outlier_cols = outlier_cols
            
            after_rows = auto_cleaned_df.shape[0]
            after_missing = auto_cleaned_df.isnull().sum().sum()
            
            st.success("Dataset cleaned successfully.")
            st.write("Cleaning Impact")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Rows Removed", before_rows - after_rows)
            with c2:
                st.metric("Missing Values Fixed", before_missing - after_missing)
            
            st.write("### Fixed Automatically")
            for log in cleaning_log:
                st.success(log)
            
            st.write("### Requires Manual Attention")
            if warning_log:
                for warning in warning_log:
                    st.warning(warning)
            else:
                st.success("No major warning detected.")
            
            if outlier_cols:
                st.info(f"Outliers still exist in: {', '.join(outlier_cols)}")
            else:
                st.success("No significant outliers detected.")

def advanced_cleaning_ui():
    st.subheader("Advanced Cleaning")
    cleaned_df = data_cleaning_module(st.session_state.working_df)

def preview_section_ui():
    st.subheader("Dataset Preview")
    preview_tab1, preview_tab2 = st.tabs(["Original Dataset", "Cleaned Dataset"])
    with preview_tab1:
        st.dataframe(st.session_state.original_df.head(20), use_container_width=True)
    with preview_tab2:
        st.dataframe(st.session_state.working_df.head(20), use_container_width=True)
    
    if "cleaning_completed" in st.session_state and st.session_state.cleaning_completed:
        csv = st.session_state.working_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Cleaned Dataset", 
            csv, 
            "cleaned_dataset.csv", 
            "text/csv", 
            use_container_width=True
        )

def data_cleaning_dashboard(display_df, working_df, df):
    st.subheader("Data Cleaning Dashboard")
    total_missing, duplicate_rows, outlier_columns = display_dataset_metrics(display_df)
    st.divider()
    display_health_score(
        display_df, 
        total_missing, 
        duplicate_rows,
        outlier_columns
    )
    st.divider()
    
    with st.expander("Cleaning Section", expanded=True):
        cleaning_tab1, cleaning_tab2 = st.tabs(["Smart Auto Cleaning", "Advanced Cleaning"])
        with cleaning_tab1:
            smart_auto_cleaning_ui(working_df)
        with cleaning_tab2:
            advanced_cleaning_ui()
    
    st.divider()
    with st.expander("Preview Section", expanded=True):
        preview_section_ui()

def sidebar_filters(df):
    st.sidebar.divider()
    st.sidebar.subheader("Dataset Filters")
    
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    
    if categorical_cols:
        filter_column = st.sidebar.selectbox("Select Column", ["None"] + categorical_cols)
        if filter_column != "None" and filter_column in df.columns:
            unique_values = sorted(df[filter_column].dropna().astype(str).unique().tolist())
            filter_values = st.sidebar.multiselect("Select Values", unique_values)
            if filter_values:
                df = df[df[filter_column].astype(str).isin(filter_values)]
    return df