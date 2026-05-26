import pandas as pd
import streamlit as st
from utils import get_outlier_bounds, detect_outlier_columns

# ============ AUTO CLEANING FUNCTIONS ============

def standardize_column_names(df, cleaning_log):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    cleaning_log.append("Standardized column names.")
    return df, cleaning_log

def remove_duplicate_rows(df, cleaning_log):
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        df = df.drop_duplicates()
        cleaning_log.append(f"Removed {duplicate_count} duplicate rows.")
    return df, cleaning_log

def remove_empty_columns(df, cleaning_log):
    empty_cols = df.columns[df.isnull().all()].tolist()
    if empty_cols:
        df = df.drop(columns=empty_cols)
        cleaning_log.append(f"Removed {len(empty_cols)} empty columns.")
    return df, cleaning_log

def remove_constant_columns(df, cleaning_log):
    constant_cols = []
    for col in df.columns:
        if df[col].nunique() <= 1:
            constant_cols.append(col)
    if constant_cols:
        df = df.drop(columns=constant_cols)
        cleaning_log.append(f"Removed {len(constant_cols)} constant columns.")
    return df, cleaning_log

def auto_convert_datatypes(df, cleaning_log):
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors="ignore")
        except:
            pass
    cleaning_log.append("Attempted automatic datatype conversion.")
    return df, cleaning_log

def handle_missing_values_numeric(df, col, cleaning_log, warning_log, missing_count, missing_percent):
    if missing_percent > 40:
        warning_log.append(f"'{col}' has high missing values ({missing_percent:.1f}%).")
    median_value = df[col].median()
    df[col] = df[col].fillna(median_value)
    cleaning_log.append(f"Filled missing values in '{col}' using median.")
    return df, cleaning_log, warning_log

def handle_missing_values_categorical(df, col, cleaning_log):
    mode_series = df[col].mode()
    mode_value = mode_series[0] if not mode_series.empty else "Unknown"
    df[col] = df[col].fillna(mode_value)
    cleaning_log.append(f"Filled missing values in '{col}' using mode.")
    return df, cleaning_log

def trim_text_columns(df, cleaning_log):
    object_cols = df.select_dtypes(include='object').columns.tolist()
    for col in object_cols:
        df[col] = df[col].astype(str).str.strip()
    cleaning_log.append("Trimmed extra spaces from text columns.")
    return df, cleaning_log

def auto_clean_dataset(df):
    """Main auto-cleaning function"""
    cleaned_df = df.copy()
    cleaning_log = []
    warning_log = []
    
    cleaned_df, cleaning_log = standardize_column_names(cleaned_df, cleaning_log)
    cleaned_df, cleaning_log = remove_duplicate_rows(cleaned_df, cleaning_log)
    cleaned_df, cleaning_log = remove_empty_columns(cleaned_df, cleaning_log)
    cleaned_df, cleaning_log = remove_constant_columns(cleaned_df, cleaning_log)
    cleaned_df, cleaning_log = auto_convert_datatypes(cleaned_df, cleaning_log)
    
    # Handle missing values
    for col in cleaned_df.columns:
        missing_count = cleaned_df[col].isnull().sum()
        if missing_count > 0:
            missing_percent = (missing_count / len(cleaned_df)) * 100
            
            if pd.api.types.is_numeric_dtype(cleaned_df[col]):
                cleaned_df, cleaning_log, warning_log = handle_missing_values_numeric(
                    cleaned_df, col, cleaning_log, warning_log, missing_count, missing_percent
                )
            else:
                cleaned_df, cleaning_log = handle_missing_values_categorical(cleaned_df, col, cleaning_log)
    
    cleaned_df, cleaning_log = trim_text_columns(cleaned_df, cleaning_log)
    outlier_cols = detect_outlier_columns(cleaned_df)
    
    return cleaned_df, cleaning_log, warning_log, outlier_cols

# ============ MANUAL CLEANING UI ============

def data_cleaning_module(df):
    """Manual cleaning module with tabs"""
    cleaned_df = df.copy()

    clean_tab1, clean_tab2, clean_tab3, clean_tab4 = st.tabs([
        "Missing Values", "Duplicates", "Columns", "Outliers"
    ])

    with clean_tab1:
        missing_cols = cleaned_df.columns[cleaned_df.isnull().sum() > 0].tolist()
        if missing_cols:
            selected_missing_col = st.selectbox("Select Column", missing_cols, key="missing_col")
            method = st.selectbox("Select Method", [
                "Drop Missing Rows", "Fill with Mean", "Fill with Median", 
                "Fill with Mode", "Fill with Custom Value"
            ], key="missing_method")
            
            custom_value = None
            if method == "Fill with Custom Value":
                custom_value = st.text_input("Enter Custom Value")
            
            if st.button("Apply Missing Value Treatment"):
                if method == "Drop Missing Rows":
                    cleaned_df = cleaned_df.dropna(subset=[selected_missing_col])
                elif method == "Fill with Mean":
                    cleaned_df[selected_missing_col] = cleaned_df[selected_missing_col].fillna(cleaned_df[selected_missing_col].mean())
                elif method == "Fill with Median":
                    cleaned_df[selected_missing_col] = cleaned_df[selected_missing_col].fillna(cleaned_df[selected_missing_col].median())
                elif method == "Fill with Mode":
                    cleaned_df[selected_missing_col] = cleaned_df[selected_missing_col].fillna(cleaned_df[selected_missing_col].mode()[0])
                elif method == "Fill with Custom Value":
                    cleaned_df[selected_missing_col] = cleaned_df[selected_missing_col].fillna(custom_value)
                
                st.session_state.working_df = cleaned_df.copy()
                st.success("Missing values handled successfully.")
                st.rerun()
        else:
            st.success("No missing values found.")

    with clean_tab2:
        duplicate_count = cleaned_df.duplicated().sum()
        st.metric("Duplicate Rows", duplicate_count)
        if duplicate_count > 0 and st.button("Remove Duplicates"):
            cleaned_df = cleaned_df.drop_duplicates()
            st.session_state.working_df = cleaned_df.copy()
            st.success("Duplicates removed successfully.")
            st.rerun()

    with clean_tab3:
        drop_cols = st.multiselect("Select Columns to Drop", cleaned_df.columns.tolist())
        if st.button("Drop Selected Columns"):
            cleaned_df = cleaned_df.drop(columns=drop_cols)
            st.session_state.working_df = cleaned_df.copy()
            st.success("Columns dropped successfully.")
            st.rerun()

    with clean_tab4:
        numeric_cols = cleaned_df.select_dtypes(include='number').columns.tolist()
        if numeric_cols:
            outlier_col = st.selectbox("Select Numeric Column", numeric_cols, key="outlier_remove")
            if st.button("Remove Outliers"):
                Q1, Q3, IQR, lower, upper = get_outlier_bounds(cleaned_df[outlier_col])
                cleaned_df = cleaned_df[(cleaned_df[outlier_col] >= lower) & (cleaned_df[outlier_col] <= upper)]
                st.session_state.working_df = cleaned_df.copy()
                st.success("Outliers removed successfully.")
                st.rerun()

    return cleaned_df