import pandas as pd
import streamlit as st
import plotly.express as px
from utils import get_outlier_bounds

def distribution_analysis(df):
    st.subheader("Distribution Analysis")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns found.")
        return
    
    selected_col = st.selectbox("Select Numeric Column", numeric_cols)
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            df, 
            x=selected_col, 
            nbins=30, 
            title=f"Distribution of {selected_col}"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig2 = px.box(
            df, 
            y=selected_col, 
            title=f"Box Plot of {selected_col}"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
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
    st.dataframe(stats_df, use_container_width=True)

def outlier_analysis(df):
    st.subheader("Outlier Detection")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns found.")
        return
    
    selected_col = st.selectbox(
        "Select Column for Outlier Detection", 
        numeric_cols, 
        key="outlier_col"
    )
    Q1, Q3, IQR, lower_bound, upper_bound = get_outlier_bounds(df[selected_col])
    
    outliers = df[(df[selected_col] < lower_bound) | (df[selected_col] > upper_bound)]
    outlier_count = outliers.shape[0]
    outlier_percentage = round((outlier_count / len(df)) * 100, 2) if len(df) > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Q1", round(Q1, 2))
    col2.metric("Q3", round(Q3, 2))
    col3.metric("Outliers", outlier_count)
    col4.metric("Outlier %", f"{outlier_percentage}%")
    
    fig = px.box(
        df, 
        y=selected_col, 
        points="outliers", 
        title=f"Outlier Detection for {selected_col}"
    )
    st.plotly_chart(fig, use_container_width=True)
    
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
    st.dataframe(bounds_df, use_container_width=True)
    
    if outlier_count > 0:
        st.write("### Outlier Records")
        st.dataframe(outliers.head(20), use_container_width=True)

def relationship_analysis(df):
    st.subheader("Relationship Analysis")
    numeric_cols = list(dict.fromkeys(df.select_dtypes(include='number').columns.tolist()))

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

    available_y = [col for col in numeric_cols if col != x_axis]
    with col2:
        y_axis = st.selectbox(
            "Select Y-axis", 
            available_y, 
            key="rel_y"
        )
    
    graph_type = st.selectbox("Select Graph Type", [
        "Scatter Plot", 
        "Line Chart", 
        "Box Plot", 
        "Violin Plot"
    ])
    
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
    else:
        fig = px.violin(
            df, 
            x=x_axis, 
            y=y_axis, 
            box=True, 
            title=f"{y_axis} vs {x_axis}"
        )

    st.plotly_chart(fig, use_container_width=True)
    
    try:
        correlation = df[x_axis].corr(df[y_axis])
        if pd.isna(correlation):
            st.warning("Correlation could not be calculated.")
            return
        
        st.metric("Correlation Coefficient", round(correlation, 3))
        
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
    except Exception as e:
        st.error(f"Correlation error: {e}")

def interactive_visualizations(df):
    st.subheader("Interactive Visualizations")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns available for visualization.")
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        chart_type = st.selectbox("Select Chart Type", [
            "Bar Chart", 
            "Line Chart", 
            "Scatter Plot", 
            "Histogram", 
            "Box Plot", 
            "Pie Chart"
        ], key="viz_chart_type")

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
        if chart_type != "Pie Chart":
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
        st.plotly_chart(fig, use_container_width=True)

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