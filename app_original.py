import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(
        uploaded_file,
        low_memory=False
    )

# Set Page config
st.set_page_config(
    page_title="Accidents Analysis Dashboard",
    page_icon="🎀",
    layout="wide"
)

# helper Functions

def sidebar_controls():
    with st.sidebar:
        st.header("Dashboard Controls")
        st.write("Upload dataset to begin analysis")

        # File upload
        uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    return uploaded_file

def dataset_shape(df):
    st.subheader("Dataset Shape")
    rows, cols = df.shape
    col1, col2 = st.columns(2)

    col1.metric("Total Rows", rows)
    col2.metric("Total Columns", cols)

def dataset_preview(df):
    st.subheader("Dataset Preview")
    st.dataframe(
        df.head(20),
        use_container_width=True,
        height=400
    )

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

def distribution_analysis(df):

    st.subheader("Distribution Analysis")

    numeric_cols = df.select_dtypes(
        include='number'
    ).columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns found.")
        return

    selected_col = st.selectbox(
        "Select Numeric Column",
        numeric_cols
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            df,
            x=selected_col,
            nbins=30,
            title=f"Distribution of {selected_col}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig2 = px.box(
            df,
            y=selected_col,
            title=f"Box Plot of {selected_col}"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # Statistical Insights
    st.write("### Statistical Insights")

    stats_df = pd.DataFrame({
        "Statistic": [
            "Mean",
            "Median",
            "Standard Deviation",
            "Minimum",
            "Maximum",
            "Skewness",
            "Kurtosis"
        ],

        "Value": [
            round(df[selected_col].mean(), 2),
            round(df[selected_col].median(), 2),
            round(df[selected_col].std(), 2),
            round(df[selected_col].min(), 2),
            round(df[selected_col].max(), 2),
            round(df[selected_col].skew(), 2),
            round(df[selected_col].kurtosis(), 2)
        ]
    })

    st.dataframe(
        stats_df,
        use_container_width=True
    )

def outlier_analysis(df):

    st.subheader("Outlier Detection")

    numeric_cols = df.select_dtypes(
        include='number'
    ).columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns found.")
        return

    selected_col = st.selectbox(
        "Select Column for Outlier Detection",
        numeric_cols,
        key="outlier_col"
    )

    # Quartiles
    Q1 = df[selected_col].quantile(0.25)
    Q3 = df[selected_col].quantile(0.75)

    # IQR
    IQR = Q3 - Q1

    # Bounds
    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)

    # Outliers
    outliers = df[
        (df[selected_col] < lower_bound) |
        (df[selected_col] > upper_bound)
    ]

    outlier_count = outliers.shape[0]

    outlier_percentage = (
        round((outlier_count / len(df)) * 100,2)
        if len(df) > 0 else 0
    )

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Q1",
        round(Q1, 2)
    )

    col2.metric(
        "Q3",
        round(Q3, 2)
    )

    col3.metric(
        "Outliers",
        outlier_count
    )

    col4.metric(
        "Outlier %",
        f"{outlier_percentage}%"
    )

    # Visualization
    fig = px.box(
        df,
        y=selected_col,
        points="outliers",
        title=f"Outlier Detection for {selected_col}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Bounds Table
    bounds_df = pd.DataFrame({
        "Metric": [
            "Lower Bound",
            "Upper Bound",
            "Minimum Value",
            "Maximum Value"
        ],

        "Value": [
            round(lower_bound, 2),
            round(upper_bound, 2),
            round(df[selected_col].min(), 2),
            round(df[selected_col].max(), 2)
        ]
    })

    st.dataframe(
        bounds_df,
        use_container_width=True
    )

    # Show outliers
    if outlier_count > 0:

        st.write("### Outlier Records")

        st.dataframe(
            outliers.head(20),
            use_container_width=True
        )

def relationship_analysis(df):

    st.subheader("Relationship Analysis")

    numeric_cols = list(
        dict.fromkeys(
            df.select_dtypes(include='number').columns.tolist()
        )
    )

    if len(numeric_cols) < 2:
        st.warning("At least 2 numeric columns required.")
        return

    col1, col2 = st.columns(2)

    with col1:
        x_axis = st.selectbox(
            "Select X-axis",
            numeric_cols,
            key="rel_x"
        )

    available_y = [
        col for col in numeric_cols
        if col != x_axis
    ]

    with col2:
        y_axis = st.selectbox(
            "Select Y-axis",
            available_y,
            key="rel_y"
        )

    graph_type = st.selectbox(
        "Select Graph Type",
        [
            "Scatter Plot",
            "Line Chart",
            "Box Plot",
            "Violin Plot"
        ]
    )

    if graph_type == "Scatter Plot":
        fig = px.scatter(
            df,
            x=x_axis,
            y=y_axis,
            title=f"{y_axis} vs {x_axis}"
        )

    elif graph_type == "Line Chart":

        fig = px.line(
            df,
            x=x_axis,
            y=y_axis,
            title=f"{y_axis} vs {x_axis}"
        )

    elif graph_type == "Box Plot":

        fig = px.box(
            df,
            x=x_axis,
            y=y_axis,
            title=f"{y_axis} vs {x_axis}"
        )

    elif graph_type == "Violin Plot":

        fig = px.violin(
            df,
            x=x_axis,
            y=y_axis,
            box=True,
            title=f"{y_axis} vs {x_axis}"
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Correlation Value
    try:
        correlation = df[x_axis].corr(df[y_axis])

        if pd.isna(correlation):
            st.warning("Correlation could not be calculated.")
            return
        st.metric(
            "Correlation Coefficient",
            round(correlation, 3)
        )

    except Exception as e:
        st.error(f"Correlation error: {e}")
        return

    # Relationship Insight
    if correlation > 0.7:
        st.success("Strong Positive Correlation")

    elif correlation > 0.3:
        st.info("Moderate Positive Correlation")

    elif correlation > -0.3:
        st.warning("Weak Correlation")

    elif correlation > -0.7:
        st.info("Moderate Negative Correlation")

    else:
        st.error("Strong Negative Correlation")

def show_missing_values(df):

    st.subheader("Missing Value Analysis")

    # Missing values count
    missing_value = df.isnull().sum()

    # Create dataframe
    missing_df = pd.DataFrame({
        "Column": missing_value.index,
        "Missing Values": missing_value.values,
        "Missing Percentage": (
            (missing_value.values / len(df)) * 100
        ).round(2)
    })

    # Show dataframe
    st.dataframe(
        missing_df,
        use_container_width=True
    )

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Rows",
        df.shape[0]
    )
    col2.metric(
        "Columns",
        df.shape[1]
    )
    col3.metric(
        "Total Missing Values",
        int(df.isnull().sum().sum())
    )

    # Filter only columns with missing values
    missing_plot = missing_df[
        missing_df["Missing Values"] > 0
    ]

    # Visualization
    if not missing_plot.empty:
        fig = px.bar(
            missing_plot,
            x="Column",
            y="Missing Values",
            color="Missing Values",
            title="Missing Values by Column"
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.success("No missing values found in dataset.")

def statistic_summary(df):
    st.subheader("Statistical Summary")
    st.dataframe(
        df.describe().transpose(),
        use_container_width=True
    )

def show_dataset_info(df):
    st.subheader("Dataset Information")
    info_df = pd.DataFrame({
        "Column": df.columns.tolist(),
        "Non-Null Count": df.count().values.tolist(),
        "Data Type": [str(dtype) for dtype in df.dtypes.values]
    })
    st.dataframe(info_df, use_container_width=True)

def correlation_heatmap(df):
    st.subheader("Correlation Heatmap")

    # Select numeric columns only
    numeric_df = df.select_dtypes(include='number')

    # Check if numeric columns exist
    if numeric_df.shape[1] < 2:
        st.warning("Not enough numeric columns for correlation analysis.")
        return

    # Correlation matrix
    corr_matrix = numeric_df.corr()

    # Create heatmap
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Feature Correlation Heatmap"
    )
    st.plotly_chart(
        fig,
        use_container_width=True
    )

def interactive_visualizations(df):
    st.subheader("Interactive Visualizations")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns available for visualization.")
        return
    
    col1, col2, col3 = st.columns(3)

    with col1:
        chart_type = st.selectbox(
            "Select Chart Type", 
            ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot", "Pie Chart"], 
            key="viz_chart_type"
        )
        
    with col2:
        if chart_type == "Pie Chart":
            pie_col = st.selectbox(
                "Select Column for Pie Chart",
                df.columns.tolist(),
                key="pie_col"
            )
        else:
            x_axis = st.selectbox(
                "Select X-axis", 
                df.columns.tolist(), 
                key="viz_x_axis"
            )

    with col3:
        if chart_type == "Pie Chart":
            st.write(" ")  # Empty placeholder for alignment
        else:
            y_axis = st.selectbox(
                "Select Y-axis", 
                numeric_cols, 
                key="viz_y_axis"
            )

    st.divider()
    fig = None

    if chart_type == "Pie Chart":
        value_counts = df[pie_col].value_counts().reset_index()
        value_counts.columns = [pie_col, "count"]
        fig = px.pie(
            value_counts,
            names=pie_col,
            values="count",
            title=f"Distribution of {pie_col}",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set3
        )

    elif chart_type == "Bar Chart":
        fig = px.bar(
            df, 
            x=x_axis, 
            y=y_axis, 
            title=f"{y_axis} by {x_axis}", 
            color_discrete_sequence=px.colors.qualitative.Set2
        )
    elif chart_type == "Line Chart":
        fig = px.line(
            df, 
            x=x_axis, 
            y=y_axis, 
            title=f"{y_axis} Trend over {x_axis}", 
            markers=True
        )
    elif chart_type == "Scatter Plot":
        fig = px.scatter(
            df, 
            x=x_axis, 
            y=y_axis, 
            title=f"Relationship: {y_axis} vs {x_axis}", 
            trendline="ols" if len(df) > 1 else None, 
            opacity=0.7
        )
    elif chart_type == "Histogram":
        if x_axis not in numeric_cols:
            st.warning(f"Histogram requires a numeric X-axis. '{x_axis}' is not numeric.")
            return
        fig = px.histogram(
            df, 
            x=x_axis, 
            nbins=30, 
            title=f"Distribution of {x_axis}", 
            color_discrete_sequence=px.colors.qualitative.Set1
        )
    elif chart_type == "Box Plot":
        fig = px.box(
            df, 
            x=x_axis, 
            y=y_axis, 
            title=f"Distribution of {y_axis} by {x_axis}", 
            points="outliers"
        )

    if fig is not None:
        st.plotly_chart(
            fig, 
            use_container_width=True
        )
        if chart_type == "Scatter Plot" and len(df) > 1:
            try:
                correlation = df[x_axis].corr(df[y_axis])

                if not pd.isna(correlation):
                    st.info(f"Correlation Coefficient: {round(correlation, 3)}")
                    if abs(correlation) > 0.7:
                        st.success("Strong correlation detected")
                    elif abs(correlation) > 0.3:
                        st.info("Moderate correlation detected")
                    else:
                        st.warning("Weak or no correlation detected")
            except Exception:
                pass
    else:
        st.error("Could not generate the requested chart. Please check your selection.")

def advanced_visualizations(df):
    with st.expander("Advanced EDA"):
        st.subheader("Advanced Exploratory Data Analysis")
        adv_tab1, adv_tab2, adv_tab3 = st.tabs([
            "Distribution Analysis", 
            "Outlier Detection", 
            "Relationship Analysis"
        ])
        with adv_tab1:
            distribution_analysis(df)
        with adv_tab2:
            outlier_analysis(df)
        with adv_tab3:
            relationship_analysis(df)

# Data Cleaning Dashboard Functions

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
    col1.metric(
        "Rows", 
        display_df.shape[0]
    )

    col2.metric(
        "Columns", 
        display_df.shape[1]
    )

    col3.metric(
        "Missing Values", 
        total_missing
    )
    
    col4, col5, col6 = st.columns(3)
    col4.metric(
        "Duplicate Rows", 
        duplicate_rows
    )
    
    col5.metric(
        "Outlier Columns", 
        outlier_columns
    )

    col6.metric(
        "Empty Columns", 
        empty_columns
    )
    
    return total_missing, duplicate_rows, outlier_columns

def display_health_score(display_df, total_missing, duplicate_rows, outlier_columns):
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
                st.metric(
                    "Rows Removed", 
                    before_rows - after_rows
                )

            with c2:
                st.metric(
                    "Missing Values Fixed", 
                    before_missing - after_missing
                )
            
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
    preview_tab1, preview_tab2 = st.tabs([
        "Original Dataset", 
        "Cleaned Dataset"
    ])
    
    with preview_tab1:
        st.dataframe(
            st.session_state.original_df.head(20), 
            use_container_width=True
        )
    
    with preview_tab2:
        st.dataframe(
            st.session_state.working_df.head(20), 
            use_container_width=True
        )
    
    if "cleaning_completed" in st.session_state and st.session_state.cleaning_completed:
        csv = st.session_state.working_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Cleaned Dataset", 
            csv, 
            "cleaned_dataset.csv", 
            "text/csv", 
            use_container_width=True
        )

# main data cleaning dashboard function

def data_cleaning_dashboard(display_df, working_df, df):
    st.subheader("Data Cleaning Dashboard")
    
    total_missing, duplicate_rows, outlier_columns = display_dataset_metrics(display_df)
    
    st.divider()
    
    display_health_score(display_df, total_missing, duplicate_rows, outlier_columns)
    
    st.divider()
    
    with st.expander(
        "Cleaning Section", 
        expanded=True
    ):
        cleaning_tab1, cleaning_tab2 = st.tabs([
            "Smart Auto Cleaning", 
            "Advanced Cleaning"
        ])
        
        with cleaning_tab1:
            smart_auto_cleaning_ui(working_df)
        
        with cleaning_tab2:
            advanced_cleaning_ui()
    
    st.divider()
    
    with st.expander(
        "Preview Section", 
        expanded=True
    ):
        preview_section_ui()

# Auto Cleaning Functions

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

def handle_missing_values_numeric(
        df, 
        col, 
        cleaning_log, 
        warning_log, 
        missing_count, 
        missing_percent
):
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

def detect_outlier_columns(df):
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

# Auto cleaning main function

def auto_clean_dataset(df):
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
                    cleaned_df, 
                    col, cleaning_log, 
                    warning_log, 
                    missing_count, 
                    missing_percent
                )
            else:
                cleaned_df, cleaning_log = handle_missing_values_categorical(cleaned_df, col, cleaning_log)
    
    cleaned_df, cleaning_log = trim_text_columns(cleaned_df, cleaning_log)
    outlier_cols = detect_outlier_columns(cleaned_df)
    
    return cleaned_df, cleaning_log, warning_log, outlier_cols

def data_cleaning_module(df):
    cleaned_df = df.copy()

    clean_tab1, clean_tab2, clean_tab3, clean_tab4 = st.tabs([
        "Missing Values",
        "Duplicates",
        "Columns",
        "Outliers"
    ])

    with clean_tab1:
        missing_cols = cleaned_df.columns[
            cleaned_df.isnull().sum() > 0
        ].tolist()

        if missing_cols:
            selected_missing_col = st.selectbox(
                "Select Column",
                missing_cols,
                key="missing_col"
            )

            method = st.selectbox(
                "Select Method",
                [
                    "Drop Missing Rows",
                    "Fill with Mean",
                    "Fill with Median",
                    "Fill with Mode",
                    "Fill with Custom Value"
                ],
                key="missing_method"
            )

            if method == "Fill with Custom Value":
                custom_value = st.text_input(
                    "Enter Custom Value"
                )

            if st.button(
                "Apply Missing Value Treatment"
            ):

                if method == "Drop Missing Rows":
                    cleaned_df = cleaned_df.dropna(
                        subset=[selected_missing_col]
                    )

                elif method == "Fill with Mean":
                    cleaned_df[selected_missing_col] = (
                        cleaned_df[selected_missing_col]
                        .fillna(
                            cleaned_df[selected_missing_col].mean()
                        )
                    )

                elif method == "Fill with Median":
                    cleaned_df[selected_missing_col] = (
                        cleaned_df[selected_missing_col]
                        .fillna(
                            cleaned_df[selected_missing_col].median()
                        )
                    )

                elif method == "Fill with Mode":
                    cleaned_df[selected_missing_col] = (
                        cleaned_df[selected_missing_col]
                        .fillna(
                            cleaned_df[selected_missing_col].mode()[0]
                        )
                    )

                elif method == "Fill with Custom Value":
                    cleaned_df[selected_missing_col] = (
                        cleaned_df[selected_missing_col]
                        .fillna(custom_value)
                    )

                st.session_state.working_df = (
                    cleaned_df.copy()
                )

                st.success(
                    "Missing values handled successfully."
                )
                st.rerun()

        else:
            st.success("No missing values found.")

    with clean_tab2:
        duplicate_count = (
            cleaned_df.duplicated().sum()
        )

        st.metric(
            "Duplicate Rows",
            duplicate_count
        )

        if duplicate_count > 0:
            if st.button(
                "Remove Duplicates"
            ):

                cleaned_df = (
                    cleaned_df.drop_duplicates()
                )

                st.session_state.working_df = (
                    cleaned_df.copy()
                )

                st.success(
                    "Duplicates removed successfully."
                )
                st.rerun()

    with clean_tab3:
        drop_cols = st.multiselect(
            "Select Columns to Drop",
            cleaned_df.columns.tolist()
        )

        if st.button(
            "Drop Selected Columns"
        ):
            
            cleaned_df = cleaned_df.drop(
                columns=drop_cols
            )

            st.session_state.working_df = (
                cleaned_df.copy()
            )

            st.success(
                "Columns dropped successfully."
            )
            st.rerun()

    with clean_tab4:
        numeric_cols = cleaned_df.select_dtypes(
            include='number'
        ).columns.tolist()

        if numeric_cols:
            outlier_col = st.selectbox(
                "Select Numeric Column",
                numeric_cols,
                key="outlier_remove"
            )

            if st.button(
                "Remove Outliers"
            ):

                Q1 = cleaned_df[outlier_col].quantile(0.25)
                Q3 = cleaned_df[outlier_col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - (1.5 * IQR)
                upper = Q3 + (1.5 * IQR)

                cleaned_df = cleaned_df[
                    (cleaned_df[outlier_col] >= lower) &
                    (cleaned_df[outlier_col] <= upper)
                ]

                st.session_state.working_df = (
                    cleaned_df.copy()
                )

                st.success(
                    "Outliers removed successfully."
                )
                st.rerun()

    return cleaned_df


# UI Part

# Title
st.title("Accidents Analysis Dashboard")
uploaded_file = sidebar_controls()

# Check file upload
if uploaded_file is not None:
    try:
        # Read Dataset
        df = load_data(uploaded_file)

        # Session State Initialization
        if "original_df" not in st.session_state:
            st.session_state.original_df = df.copy()

        # Reset working dataframe if new file uploaded
        if (
            "working_df" not in st.session_state or
            st.session_state.get("current_file") != uploaded_file.name
        ):
            st.session_state.working_df = df.copy()
            st.session_state.current_file = uploaded_file.name

        working_df = st.session_state.working_df

        if "cleaning_completed" not in st.session_state:
            st.session_state.cleaning_completed = False

        if "cleaning_log" not in st.session_state:
            st.session_state.cleaning_log = []

        if "warning_log" not in st.session_state:
            st.session_state.warning_log = []

        if "outlier_cols" not in st.session_state:
            st.session_state.outlier_cols = []

        # Sidebar Filters
        st.sidebar.divider()
        st.sidebar.subheader("Dataset Filters")

        display_df = working_df.copy()

        # Get categorical columns
        categorical_cols = display_df.select_dtypes(
            include='object'
        ).columns.tolist()

        if categorical_cols:

            filter_column = st.sidebar.selectbox(
                "Select Column",
                ["None"] + categorical_cols
            )

            if (
                filter_column != "None" and
                filter_column in display_df.columns
            ):

                unique_values = sorted(
                    display_df[filter_column]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                filter_values = st.sidebar.multiselect(
                    "Select Values",
                    unique_values
                )

                if filter_values:

                    display_df = display_df[
                        display_df[filter_column]
                        .astype(str)
                        .isin(filter_values)
                    ]

        # Empty dataset protection
        if display_df.empty:
            st.warning("No data available after applying filters.")
            st.stop()

        # Success message
        st.success("Uploaded Successfully")

        tab1, tab2, tab3, tab4 = st.tabs([
            "Overview",
            "EDA",
            "Visualizations",
            "Data Cleaning"
        ])

        with tab1:
            dataset_shape(display_df)
            st.divider()
            dataset_preview(display_df)
            st.divider()

            col1,col2 = st.columns(2)
            with col1:
                show_columns(display_df)
            with col2:
                show_datatypes(display_df)

        with tab2:
            show_dataset_info(display_df)
            st.divider()
            statistic_summary(display_df)
            st.divider()
            show_missing_values(display_df)
            st.divider()
            correlation_heatmap(display_df)
            st.divider()
            advanced_visualizations(display_df)

        with tab3:
            interactive_visualizations(display_df)

        with tab4:
            data_cleaning_dashboard(display_df, working_df, df)

    except Exception as e:
        st.error(f"Error while reading file: {e}")

else:
    st.info("Please upload a CSV file to begin analysis.")