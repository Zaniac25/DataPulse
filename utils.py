import pandas as pd
import streamlit as st

def detect_outlier_columns(df):
    """Detect which numeric columns contain outliers"""
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    outlier_cols = []
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - (1.5 * IQR)
        upper = Q3 + (1.5 * IQR)
        outliers = df[(df[col] < lower) | (df[col] > upper)]
        if len(outliers) > 0:
            outlier_cols.append(col)
    return outlier_cols

def get_outlier_bounds(series):
    """Calculate outlier bounds for a series"""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)
    return Q1, Q3, IQR, lower_bound, upper_bound