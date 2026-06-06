def generate_dataset_insights(profile):

    insights = []

    # Dataset Size
    rows = profile["rows"]
    cols = profile["columns"]

    insights.append(
        f"Dataset contains {rows} rows and {cols} columns."
    )

    # Missing Values
    missing_values = profile["missing_values"]

    if missing_values:

        total_missing = sum(
            missing_values.values()
        )

        insights.append(
            f"Dataset contains {total_missing} missing values."
        )

        high_missing_cols = []

        for col, percent in profile[
            "missing_percentages"
        ].items():

            if percent > 40:

                high_missing_cols.append(col)

        if high_missing_cols:

            insights.append(
                "High missing values detected in: "
                + ", ".join(high_missing_cols)
            )

    else:

        insights.append(
            "No missing values detected."
        )

    # Duplicate Rows
    duplicate_rows = profile["duplicate_rows"]

    if duplicate_rows > 0:

        insights.append(
            f"{duplicate_rows} duplicate rows detected."
        )

    else:

        insights.append(
            "No duplicate rows found."
        )

    # Outlier Analysis
    outlier_summary = profile[
        "outlier_summary"
    ]

    severe_outlier_cols = []

    for col, data in outlier_summary.items():

        if data["percentage"] > 15:

            severe_outlier_cols.append(col)

    if severe_outlier_cols:

        insights.append(
            "Significant outliers detected in: "
            + ", ".join(severe_outlier_cols)
        )

    # Correlation Analysis
    correlation_summary = profile[
        "correlation_summary"
    ]

    if correlation_summary:

        insights.append(
            "Strong feature correlations detected."
        )

    # Constant Columns
    constant_columns = profile[
        "constant_columns"
    ]

    if constant_columns:

        insights.append(
            "Constant columns detected: "
            + ", ".join(constant_columns)
        )

    # Health Score Insight
    total_issues = (
        len(missing_values)
        + duplicate_rows
        + len(severe_outlier_cols)
    )

    if total_issues == 0:

        insights.append(
            "Dataset quality appears excellent."
        )

    elif total_issues < 5:

        insights.append(
            "Dataset quality appears good with minor issues."
        )

    else:

        insights.append(
            "Dataset requires preprocessing before advanced analysis."
        )

    return insights

def generate_advanced_insights(profile):

    advanced_insights = []

    # Missing Values

    for col, percent in profile[
        "missing_percentages"
    ].items():

        if percent > 40:

            advanced_insights.append(
                f"Column '{col}' contains "
                f"{percent}% missing values "
                f"and should be reviewed."
            )

        elif percent > 20:

            advanced_insights.append(
                f"Column '{col}' contains "
                f"{percent}% missing values."
            )

    # Outliers

    for col, data in profile[
        "outlier_summary"
    ].items():

        if data["percentage"] > 15:

            advanced_insights.append(
                f"Column '{col}' contains "
                f"{data['percentage']}% outliers."
            )

    # Correlations

    for col, corr_data in profile[
        "correlation_summary"
    ].items():

        for target, value in corr_data.items():

            advanced_insights.append(
                f"Strong correlation detected "
                f"between '{col}' and "
                f"'{target}' ({value})."
            )

    # Constant Columns

    for col in profile[
        "constant_columns"
    ]:

        advanced_insights.append(
            f"'{col}' contains only one "
            f"unique value and may be removed."
        )

    return advanced_insights