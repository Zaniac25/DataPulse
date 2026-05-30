def generate_eda_report(profile, insights):

    report_sections = {}

    # Dataset Overview
    report_sections["Dataset Overview"] = f"""
        Dataset contains {profile['rows']} rows and {profile['columns']} columns.

        Numeric Columns:
        {len(profile['numeric_columns'])}

        Categorical Columns:
        {len(profile['categorical_columns'])}
        """

    # Missing Values
    missing_values = profile["missing_values"]

    if missing_values:

        missing_text = []

        for col, val in missing_values.items():

            percent = profile[
                "missing_percentages"
            ][col]

            missing_text.append(
                f"{col}: {val} missing values ({percent}%)"
            )

        report_sections["Missing Value Analysis"] = (
            "\n".join(missing_text)
        )

    else:

        report_sections["Missing Value Analysis"] = (
            "No missing values detected."
        )

    # Duplicate Rows
    report_sections["Duplicate Analysis"] = f"""
        Duplicate Rows Found:
        {profile['duplicate_rows']}
        """

    # Outlier Summary
    outlier_lines = []

    for col, data in profile[
        "outlier_summary"
    ].items():

        if data["count"] > 0:

            outlier_lines.append(
                f"{col}: "
                f"{data['count']} outliers "
                f"({data['percentage']}%)"
            )

    if outlier_lines:

        report_sections["Outlier Analysis"] = (
            "\n".join(outlier_lines)
        )

    else:

        report_sections["Outlier Analysis"] = (
            "No major outliers detected."
        )

    # Correlation Summary
    correlation_summary = profile[
        "correlation_summary"
    ]

    correlation_lines = []

    for col, corr_data in (
        correlation_summary.items()
    ):

        correlation_lines.append(
            f"{col}: {corr_data}"
        )

    if correlation_lines:

        report_sections["Correlation Analysis"] = (
            "\n".join(correlation_lines)
        )

    else:

        report_sections["Correlation Analysis"] = (
            "No strong correlations detected."
        )

    # Dataset Insights
    report_sections["Dataset Insights"] = (
        "\n".join(insights)
    )

    # Final Recommendation
    report_sections["Final Recommendation"] = """
        Recommended Actions:
        - Handle missing values carefully
        - Review outliers before modeling
        - Remove unnecessary columns
        - Validate feature relationships
        - Apply preprocessing before ML training
        """

    return report_sections