"""
SmartShift - AI-Powered Warehouse Workforce Rebalancing System
Main Streamlit application interface.
"""
import streamlit as st
import pandas as pd
from crewai import Crew, Process
from data_loader import load_workers, save_workers, update_worker_zone
from tools import initialize_tools
from tasks import create_crew_tasks
from agents import skill_matcher_agent, shift_planner_agent
import json


# Page configuration
st.set_page_config(
    page_title="SmartShift - Workforce Rebalancing",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'workers_df' not in st.session_state:
        st.session_state.workers_df = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'crew_output' not in st.session_state:
        st.session_state.crew_output = None
    if 'tools_initialized' not in st.session_state:
        st.session_state.tools_initialized = False


def load_data():
    """Load worker data from CSV."""
    try:
        st.session_state.workers_df = load_workers("workers.csv")
        return True
    except Exception as e:
        st.error(f"Error loading workers data: {str(e)}")
        return False


def initialize_system():
    """Initialize the SmartShift system."""
    if not st.session_state.tools_initialized:
        with st.spinner("Initializing SmartShift system..."):
            try:
                initialize_tools()
                st.session_state.tools_initialized = True
                st.success("✅ System initialized successfully!")
                return True
            except Exception as e:
                st.error(f"Error initializing system: {str(e)}")
                return False
    return True


def run_crew(manager_input: str):
    """
    Run the CrewAI crew to process the manager's request.
    
    Args:
        manager_input: Natural language input from the manager
    """
    try:
        with st.spinner("🤖 AI agents are analyzing the situation..."):
            # Create tasks
            tasks = create_crew_tasks(manager_input)
            
            # Create crew
            crew = Crew(
                agents=[skill_matcher_agent, shift_planner_agent],
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            # Execute crew
            result = crew.kickoff()
            
            st.session_state.crew_output = result
            st.session_state.recommendations = result
            
        return True
    except Exception as e:
        st.error(f"Error running AI crew: {str(e)}")
        st.exception(e)
        return False


def display_workforce_overview():
    """Display current workforce overview."""
    st.header("📊 Current Workforce Overview")
    
    if st.session_state.workers_df is not None:
        df = st.session_state.workers_df
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Workers", len(df))
        with col2:
            available = len(df[df['available'] == 'Yes'])
            st.metric("Available Workers", available)
        with col3:
            high_load = len(df[df['load_status'] == 'High'])
            st.metric("High Load Workers", high_load, delta=None if high_load < 6 else "⚠️")
        with col4:
            avg_load = df['load_percentage'].mean()
            st.metric("Average Load", f"{avg_load:.1f}%")
        
        # Zone breakdown
        st.subheader("Zone Distribution")
        zone_cols = st.columns(4)
        
        for idx, zone in enumerate(['Zone A', 'Zone B', 'Zone C', 'Zone D']):
            zone_workers = df[df['current_zone'] == zone]
            with zone_cols[idx]:
                st.markdown(f"**{zone}**")
                st.write(f"Workers: {len(zone_workers)}")
                st.write(f"Available: {len(zone_workers[zone_workers['available'] == 'Yes'])}")
                avg_zone_load = zone_workers['load_percentage'].mean()
                st.write(f"Avg Load: {avg_zone_load:.1f}%")
        
        # Detailed table
        st.subheader("Worker Details")
        
        # Add filters
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            zone_filter = st.multiselect(
                "Filter by Zone",
                options=['Zone A', 'Zone B', 'Zone C', 'Zone D'],
                default=['Zone A', 'Zone B', 'Zone C', 'Zone D']
            )
        
        with filter_col2:
            load_filter = st.multiselect(
                "Filter by Load Status",
                options=['Low', 'Medium', 'High'],
                default=['Low', 'Medium', 'High']
            )
        
        with filter_col3:
            availability_filter = st.multiselect(
                "Filter by Availability",
                options=['Yes', 'No'],
                default=['Yes', 'No']
            )
        
        # Apply filters
        filtered_df = df[
            (df['current_zone'].isin(zone_filter)) &
            (df['load_status'].isin(load_filter)) &
            (df['available'].isin(availability_filter))
        ]
        
        # Display table
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data",
            data=csv,
            file_name="workforce_data.csv",
            mime="text/csv"
        )


def display_recommendations():
    """Display AI recommendations."""
    st.header("🎯 AI Recommendations")
    
    if st.session_state.recommendations:
        st.success("✅ Analysis complete! Here are the recommendations:")
        
        # Display the crew output
        st.markdown("### Detailed Analysis")
        st.markdown(str(st.session_state.crew_output))
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Approve Recommendations", type="primary"):
                st.success("Recommendations approved! (Implementation pending)")
        
        with col2:
            if st.button("📝 Request Modifications"):
                st.info("Modification request noted. Please provide feedback below.")
        
        with col3:
            if st.button("❌ Reject"):
                st.warning("Recommendations rejected.")
                st.session_state.recommendations = None
                st.rerun()
    else:
        st.info("No recommendations yet. Enter an overload description above to get started.")


def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("🏭 SmartShift")
    st.markdown("### AI-Powered Warehouse Workforce Rebalancing System")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ System Controls")
        
        # Load data button
        if st.button("🔄 Load/Reload Data", type="primary"):
            if load_data():
                st.success("Data loaded successfully!")
                st.rerun()
        
        # Initialize system button
        if st.button("🚀 Initialize System"):
            initialize_system()
        
        st.markdown("---")
        
        # System status
        st.subheader("System Status")
        if st.session_state.workers_df is not None:
            st.success("✅ Data Loaded")
        else:
            st.warning("⚠️ Data Not Loaded")
        
        if st.session_state.tools_initialized:
            st.success("✅ System Initialized")
        else:
            st.warning("⚠️ System Not Initialized")
        
        st.markdown("---")
        
        # About
        st.subheader("About")
        st.markdown("""
        SmartShift uses AI agents powered by IBM Granite LLM to:
        - 🔍 Search for skilled workers
        - 📊 Analyze workload distribution
        - 🎯 Recommend optimal shifts
        - ⚖️ Balance workforce efficiently
        """)
    
    # Main content
    if st.session_state.workers_df is None:
        st.warning("⚠️ Please load data using the sidebar button.")
        if st.button("Load Data Now"):
            if load_data():
                st.success("Data loaded!")
                st.rerun()
    else:
        # Display workforce overview
        display_workforce_overview()
        
        st.markdown("---")
        
        # Overload input section
        st.header("🚨 Report Overload Situation")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            manager_input = st.text_area(
                "Describe the overload situation:",
                placeholder="Example: Zone A dispatch is overloaded, need forklift help",
                height=100,
                help="Describe which zone is overloaded and what skill is needed"
            )
        
        with col2:
            st.markdown("### Quick Examples")
            if st.button("📦 Packing Help"):
                manager_input = "Zone C needs packing help for afternoon shift"
                st.rerun()
            if st.button("🚜 Forklift Help"):
                manager_input = "Zone A dispatch is overloaded, need forklift help"
                st.rerun()
            if st.button("✅ Quality Inspector"):
                manager_input = "Zone B is at 90% capacity, need quality inspector"
                st.rerun()
        
        if st.button("🤖 Get AI Recommendations", type="primary", disabled=not manager_input):
            if not st.session_state.tools_initialized:
                st.error("Please initialize the system first using the sidebar button.")
            else:
                run_crew(manager_input)
                st.rerun()
        
        st.markdown("---")
        
        # Display recommendations
        display_recommendations()


if __name__ == "__main__":
    main()

# Made with Bob
