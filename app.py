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

# Page configuration
st.set_page_config(
    page_title="Accidents Analysis Dashboard", 
    page_icon="🎀", 
    layout="wide"
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
    
    except Exception as e:
        st.error(f"Error while reading file: {e}")

else:
    st.info("Please upload a CSV file to begin analysis.")