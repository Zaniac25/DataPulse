import streamlit as st
from data_loader import load_data, initialize_session_state
from ui_components import (
    sidebar_controls, 
    sidebar_filters, 
    data_cleaning_dashboard, 
    dataset_preview
)
from analysis import (
    dataset_shape, show_columns, show_datatypes, show_dataset_info,
    statistic_summary, show_missing_values, correlation_heatmap
)
from visualizations import interactive_visualizations, advanced_visualizations
from profiling import generate_dataset_profile
from insights import generate_dataset_insights
from report_generator import generate_eda_report
from report_export import export_eda_report_pdf

# Title
st.title("Accidents Analysis Dashboard")

# Sidebar
uploaded_file = sidebar_controls()

# Main content
if uploaded_file is not None:
    try:
        # Load data
        df = load_data(uploaded_file)

        # Generate Dataset Profile
        profile = generate_dataset_profile(df)

        # Store Profile
        st.session_state.dataset_profile = profile

        # Generate Dataset Insights
        insights = generate_dataset_insights(
            profile
        )

        # Store Insights
        st.session_state.dataset_insights = insights

        # Generate EDA Report
        eda_report = generate_eda_report(
            profile,
            insights
        )

        # Store Report
        st.session_state.eda_report = eda_report
        
        # Initialize session state
        initialize_session_state(df, uploaded_file.name)
        working_df = st.session_state.working_df
        
        # Apply sidebar filters
        display_df = sidebar_filters(working_df.copy())
        
        # Empty dataset protection
        if display_df.empty:
            st.warning("No data available after applying filters.")
            st.stop()
        
        st.success("Uploaded Successfully")
        
        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Overview", 
            "EDA", 
            "Visualizations", 
            "Data Cleaning",
            "Reports"
        ])
        
        with tab1:
            dataset_shape(display_df)

            with st.expander("Dataset Profile Debug"):
                st.json(
                    st.session_state.dataset_profile
                )

            st.subheader("Dataset Insights")
            for insight in st.session_state.dataset_insights:
                st.info(insight)

            with st.expander(
                "Generated EDA Report"
            ):

                for section, content in (
                    st.session_state.eda_report.items()
                ):

                    st.write(f"## {section}")
                    st.text(content)

                if st.button(
                    "Generate PDF Report"
                ):

                    pdf_path = export_eda_report_pdf(
                        st.session_state.eda_report
                    )

                    with open(
                        pdf_path,
                        "rb"
                    ) as pdf_file:

                        st.download_button(
                            label="Download PDF",
                            data=pdf_file,
                            file_name="EDA_Report.pdf",
                            mime="application/pdf"
                        )

            st.divider()
            dataset_preview(display_df)
            st.divider()
            col1, col2 = st.columns(2)
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

        with tab5:
            st.header("Report Center")

            profile = st.session_state.dataset_profile
            st.subheader("Dataset Summary")
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Rows",
                profile["rows"]
            )
            col2.metric(
                "Columns",
                profile["columns"]
            )
            col3.metric(
                "Duplicates",
                profile["duplicate_rows"]
            )

            st.subheader("Generated Insights")
            for insight in st.session_state.dataset_insights:
                st.info(insight)
    
    except Exception as e:
        st.error(f"Error while reading file: {e}")

else:
    st.info("Please upload a CSV file to begin analysis.")