import pandas as pd
from utils import get_outlier_bounds

def generate_dataset_profile(df):

    profile = {}

    # Basic Information
    profile["rows"] = df.shape[0]
    profile["columns"] = df.shape[1]
    profile["column_names"] = df.columns.tolist()

    # Datatypes
    profile["datatypes"] = {
        col: str(dtype)
        for col, dtype in df.dtypes.items()
    }

    # Missing Values
    missing_values = df.isnull().sum()

    profile["missing_values"] = {
        col: int(val)
        for col, val in missing_values.items()
        if val > 0
    }

    profile["missing_percentages"] = {
        col: round((val / len(df)) * 100, 2)
        for col, val in missing_values.items()
        if val > 0
    }

    # Duplicate Rows
    profile["duplicate_rows"] = int(
        df.duplicated().sum()
    )

    # Numeric / Categorical Columns
    numeric_cols = df.select_dtypes(
        include='number'
    ).columns.tolist()

    categorical_cols = df.select_dtypes(
        include='object'
    ).columns.tolist()

    profile["numeric_columns"] = numeric_cols
    profile["categorical_columns"] = categorical_cols

    # Outlier Summary
    outlier_summary = {}

    for col in numeric_cols:

        Q1, Q3, IQR, lower, upper = (
            get_outlier_bounds(df[col])
        )

        outliers = df[
            (df[col] < lower) |
            (df[col] > upper)
        ]

        outlier_summary[col] = {
            "count": int(len(outliers)),
            "percentage": round(
                (len(outliers) / len(df)) * 100,
                2
            ) if len(df) > 0 else 0
        }

    profile["outlier_summary"] = outlier_summary

    # Correlation Summary
    correlation_summary = {}

    if len(numeric_cols) >= 2:

        corr_matrix = (
            df[numeric_cols]
            .corr()
            .round(2)
        )

        for col in corr_matrix.columns:

            strong_corr = (
                corr_matrix[col][
                    abs(corr_matrix[col]) > 0.7
                ]
                .drop(labels=[col], errors="ignore")
            )

            if not strong_corr.empty:

                correlation_summary[col] = (
                    strong_corr.to_dict()
                )

    profile["correlation_summary"] = correlation_summary

    # Constant Columns
    constant_columns = []

    for col in df.columns:

        if df[col].nunique() <= 1:
            constant_columns.append(col)

    profile["constant_columns"] = constant_columns

    return profile