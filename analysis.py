import pandas as pd
import streamlit as st
import plotly.express as px

def dataset_shape(df):
    st.subheader("Dataset Shape")
    rows, cols = df.shape
    col1, col2 = st.columns(2)
    col1.metric("Total Rows", rows)
    col2.metric("Total Columns", cols)

def show_columns(df):
    st.subheader("Column Names")
    column_df = pd.DataFrame({
        "index": range(len(df.columns)),
        "column Names": df.columns.tolist()
    })
    st.dataframe(column_df, use_container_width=True)

def show_datatypes(df):
    st.subheader("Data Types")
    dtype_df = pd.DataFrame({
        "Column": df.columns.tolist(),
        "Datatype": [str(dtype) for dtype in df.dtypes]
    })
    st.dataframe(dtype_df, use_container_width=True)

def show_dataset_info(df):
    st.subheader("Dataset Information")
    info_df = pd.DataFrame({
        "Column": df.columns.tolist(),
        "Non-Null Count": df.count().values.tolist(),
        "Data Type": [str(dtype) for dtype in df.dtypes.values]
    })
    st.dataframe(info_df, use_container_width=True)

def statistic_summary(df):
    st.subheader("Statistical Summary")
    st.dataframe(df.describe().transpose(), use_container_width=True)

def show_missing_values(df):
    st.subheader("Missing Value Analysis")
    missing_value = df.isnull().sum()
    missing_df = pd.DataFrame({
        "Column": missing_value.index,
        "Missing Values": missing_value.values,
        "Missing Percentage": ((missing_value.values / len(df)) * 100).round(2)
    })
    st.dataframe(missing_df, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Total Missing Values", int(df.isnull().sum().sum()))
    
    missing_plot = missing_df[missing_df["Missing Values"] > 0]
    
    if not missing_plot.empty:
        fig = px.bar(
            missing_plot, 
            x="Column", 
            y="Missing Values", 
            color="Missing Values", 
            title="Missing Values by Column"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No missing values found in dataset.")

def correlation_heatmap(df):
    st.subheader("Correlation Heatmap")
    numeric_df = df.select_dtypes(include='number')

    if numeric_df.shape[1] < 2:
        st.warning("Not enough numeric columns for correlation analysis.")
        return
    
    corr_matrix = numeric_df.corr()
    fig = px.imshow(
        corr_matrix, 
        text_auto=True, 
        aspect="auto", 
        color_continuous_scale="RdBu_r", 
        title="Feature Correlation Heatmap"
    )
    st.plotly_chart(fig, use_container_width=True)