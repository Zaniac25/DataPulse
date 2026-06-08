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
from insights import (
    generate_dataset_insights,
    generate_advanced_insights
)
from report_generator import generate_eda_report
from report_export import (
    export_eda_report_pdf,
    export_text_report_pdf
)
from ai_reports import (
    generate_ai_eda_report,
    generate_executive_summary,
    generate_cleaning_recommendations
)

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

        advanced_insights = (
            generate_advanced_insights(
                profile
            )
        )

        st.session_state.advanced_insights = (
            advanced_insights
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

            st.subheader(
                "Advanced Insights"
            )

            for insight in (
                st.session_state.advanced_insights
            ):

                st.warning(insight)

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

            st.subheader(
                "AI EDA Report"
            )

            if st.button(
                "Generate AI Report"
            ):

                try:

                    with st.spinner(
                        "Generating AI Report..."
                    ):

                        st.session_state.ai_report = (
                            generate_ai_eda_report(
                                st.session_state.dataset_profile,
                                st.session_state.dataset_insights,
                                st.session_state.advanced_insights,
                                st.secrets["GEMINI_API_KEY"]
                            )
                        )

                except Exception as e:

                    st.error(
                        f"AI Report Error: {e}"
                    )

                if (
                    "ai_report" in st.session_state
                    and
                    st.session_state.ai_report
                ):

                    st.markdown(
                        st.session_state.ai_report
                    )

                if st.button(
                    "Generate AI Report PDF"
                ):

                    pdf_path = (
                        export_text_report_pdf(
                            "AI EDA Report",
                            st.session_state.ai_report,
                            "ai_report.pdf"
                        )
                    )

                    with open(
                        pdf_path,
                        "rb"
                    ) as pdf_file:

                        st.download_button(
                            "Download AI Report PDF",
                            pdf_file,
                            "AI_Report.pdf",
                            "application/pdf"
                        )

            st.subheader(
                "Executive Summary"
            )

            if st.button(
                "Generate Executive Summary"
            ):

                try:

                    with st.spinner(
                        "Generating Executive Summary..."
                    ):

                        st.session_state.executive_summary = (
                            generate_executive_summary(
                                st.session_state.dataset_profile,
                                st.session_state.dataset_insights,
                                st.session_state.advanced_insights,
                                st.secrets["GEMINI_API_KEY"]
                            )
                        )

                except Exception as e:

                    st.error(
                        f"Executive Summary Error: {e}"
                    )

                if (
                    "executive_summary" in st.session_state
                    and
                    st.session_state.executive_summary
                ):

                    st.markdown(
                        st.session_state.executive_summary
                    )

                if st.button(
                    "Generate Executive Summary PDF"
                ):

                    pdf_path = (
                        export_text_report_pdf(
                            "Executive Summary",
                            st.session_state.executive_summary,
                            "executive_summary.pdf"
                        )
                    )

                    with open(
                        pdf_path,
                        "rb"
                    ) as pdf_file:

                        st.download_button(
                            "Download Executive Summary PDF",
                            pdf_file,
                            "Executive_Summary.pdf",
                            "application/pdf"
                        )

            st.subheader(
                "Cleaning Recommendation Report"
            )

            if st.button(
                "Generate Cleaning Recommendations"
            ):

                try:

                    with st.spinner(
                        "Generating Recommendations..."
                    ):

                        st.session_state.cleaning_report = (
                            generate_cleaning_recommendations(
                                st.session_state.dataset_profile,
                                st.session_state.dataset_insights,
                                st.session_state.advanced_insights,
                                st.secrets["GEMINI_API_KEY"]
                            )
                        )

                except Exception as e:

                    st.error(
                        f"Cleaning Report Error: {e}"
                    )

                if (
                    "cleaning_report" in st.session_state
                    and
                    st.session_state.cleaning_report
                ):

                    st.markdown(
                        st.session_state.cleaning_report
                    )

                if st.button(
                    "Generate Cleaning Report PDF"
                ):

                    pdf_path = (
                        export_text_report_pdf(
                            "Cleaning Recommendation Report",
                            st.session_state.cleaning_report,
                            "cleaning_report.pdf"
                        )
                    )

                    with open(
                        pdf_path,
                        "rb"
                    ) as pdf_file:

                        st.download_button(
                            "Download Cleaning Report PDF",
                            pdf_file,
                            "Cleaning_Report.pdf",
                            "application/pdf"
                        )

            

    except Exception as e:
        st.error(f"Error while reading file: {e}")

else:
    st.info("Please upload a CSV file to begin analysis.")