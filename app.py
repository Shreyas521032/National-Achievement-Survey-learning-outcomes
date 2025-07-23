import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="National Achievement Survey (NAS) - Class 8 Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and preprocess the NAS dataset"""
    try:
        # Try to load from uploaded file first
        df = pd.read_csv('Dataset/National_Achievement_Survey_dataset.csv')
        return df
    except FileNotFoundError:
        st.error("Please ensure 'National_Achievement_Survey_dataset.csv' is in the 'Dataset/' directory.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()


@st.cache_data
def preprocess_data(df):
    """Clean and preprocess the dataset"""
    # Clean column names
    cols = df.columns
    new_cols = []
    for col in cols:
        new_col = col.split('(')[0].strip().replace(' ', '_')
        new_cols.append(new_col)
    df.columns = new_cols
    
    # Extract year from the Year column - Fixed regex pattern
    try:
        df['Year'] = df['Year'].astype(str).str.extract(r'(\d{4})').astype(int)
    except:
        # If extraction fails, try to handle different year formats
        df['Year'] = pd.to_datetime(df['Year'], errors='coerce').dt.year
    
    # Identify subject-specific columns
    math_cols = [col for col in df.columns if '_In_M' in col]
    science_cols = [col for col in df.columns if '_In_Sci' in col]
    sst_cols = [col for col in df.columns if '_In_Sst' in col]
    language_cols = [col for col in df.columns if '_In_L' in col]
    
    # Calculate subject-wise performance scores
    if math_cols:
        df['Math_Performance'] = df[math_cols].mean(axis=1)
    else:
        df['Math_Performance'] = 0
        
    if science_cols:
        df['Science_Performance'] = df[science_cols].mean(axis=1)
    else:
        df['Science_Performance'] = 0
        
    if sst_cols:
        df['SST_Performance'] = df[sst_cols].mean(axis=1)
    else:
        df['SST_Performance'] = 0
        
    if language_cols:
        df['Language_Performance'] = df[language_cols].mean(axis=1)
    else:
        df['Language_Performance'] = 0
    
    # Calculate overall performance
    performance_cols = ['Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance']
    available_cols = [col for col in performance_cols if col in df.columns and df[col].notna().any()]
    
    if available_cols:
        df['Overall_Performance'] = df[available_cols].mean(axis=1)
    else:
        df['Overall_Performance'] = 0
    
    return df, math_cols, science_cols, sst_cols, language_cols


def main():
    """Main application function"""
    # Title
    st.markdown('<h1 class="main-header">📊 National Achievement Survey (NAS) - Class 8 Analysis</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    sections = [
        "🏠 Home & Dataset Overview",
        "🔧 Data Preprocessing",
        "📈 Exploratory Data Analysis",
        "📊 Performance Analysis",
        "🗺️ District-Level Mapping",
        "💡 Key Insights & Recommendations"
    ]
    
    selected_section = st.sidebar.selectbox("Choose a section:", sections)
    
    # Load and preprocess data
    try:
        df = load_data()
        df_processed, math_cols, science_cols, sst_cols, language_cols = preprocess_data(df)
        
        # Filter data for most recent year
        available_years = sorted(df_processed['Year'].dropna().unique())
        if available_years:
            latest_year = available_years[-1]
            df_latest = df_processed[df_processed['Year'] == latest_year].copy()
        else:
            df_latest = df_processed.copy()
            
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return
    
    # Route to appropriate section
    if selected_section == "🏠 Home & Dataset Overview":
        show_home_and_overview(df, df_processed)
    elif selected_section == "🔧 Data Preprocessing":
        show_preprocessing(df, df_processed, math_cols, science_cols, sst_cols, language_cols)
    elif selected_section == "📈 Exploratory Data Analysis":
        show_eda(df_latest)
    elif selected_section == "📊 Performance Analysis":
        show_performance_analysis(df_latest)
    elif selected_section == "🗺️ District-Level Mapping":
        show_district_mapping(df_latest)
    elif selected_section == "💡 Key Insights & Recommendations":
        show_insights_and_recommendations(df_latest)


def show_home_and_overview(df, df_processed):
    """Display home page and dataset overview"""
    st.markdown('<div class="section-header">🏠 Welcome to NAS Class 8 Analysis Dashboard</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    This interactive dashboard provides comprehensive analysis of the **National Achievement Survey (NAS)** 
    for Class 8 students across India. Explore learning outcomes, performance trends, and educational insights 
    from one of India's largest educational assessments.
    """)
    
    # Dataset Overview
    st.markdown('<div class="section-header">📋 About the Dataset</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### National Achievement Survey (NAS): Survey of Learning Outcomes - District Report for Class 8
        
        **Data Source:** Ministry of Education, Government of India  
        **Standardized By:** NDAP (National Data & Analytics Platform)  
        **Hosted By:** NDAP  
        
        #### Overview
        The National Achievement Survey (NAS) is a large-scale assessment conducted across India to evaluate 
        the learning outcomes of students in various classes, including Class 8. The District Report for Class 8 
        provides a detailed analysis of student performance in key subjects such as:
        
        - **Mathematics** - Numerical skills, problem-solving, and mathematical reasoning
        - **Science** - Scientific concepts, experimentation, and analytical thinking  
        - **Social Science** - Historical knowledge, geographical understanding, and civic awareness
        - **Language** - Reading comprehension, communication skills, and linguistic competency
        
        #### Key Features
        - **Competency-Based Assessment:** Measures understanding and application rather than rote memorization
        - **Aligned with NEP:** Follows National Education Policy framework
        - **Representative Sampling:** Covers diverse districts across all Indian states
        - **Standardized Testing:** Ensures consistency and reliability across regions
        """)
    
    with col2:
        # Get year range
        year_range = f"{df['Year'].min():.0f} - {df['Year'].max():.0f}" if 'Year' in df.columns else "N/A"
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📅 Year Range", year_range)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🌍 Geographic Coverage", "State & District Level")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📊 Data Frequency", "Yearly")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🏫 Sector", "Education & Training")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📈 Last Updated", "July 09, 2025")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Dataset Statistics
    st.markdown('<div class="section-header">📊 Dataset Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    
    with col2:
        district_count = df['District'].nunique() if 'District' in df.columns else 0
        st.metric("Districts Covered", f"{district_count:,}")
    
    with col3:
        state_count = df['State'].nunique() if 'State' in df.columns else 0
        st.metric("States/UTs", f"{state_count}")
    
    with col4:
        learning_outcome_cols = len([col for col in df.columns if 'Learning_Outcome' in col])
        st.metric("Learning Outcomes", f"{learning_outcome_cols}")
    
    # Sample data preview
    st.markdown('<div class="section-header">👀 Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)
    
    # Data collection methodology
    st.markdown('<div class="section-header">🔬 Data Collection Methodology</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Assessment Framework
        - **Competency-Based Evaluation:** Tests conceptual understanding and application
        - **Multiple Choice Questions:** Standardized format for consistency
        - **Representative Sampling:** Ensures geographic and demographic diversity
        - **Quality Assurance:** Rigorous validation and verification processes
        """)
    
    with col2:
        st.markdown("""
        #### Impact & Applications  
        - **Policy Development:** Informs educational policy decisions
        - **Teacher Training:** Identifies areas for professional development
        - **Curriculum Enhancement:** Guides curriculum design and improvement
        - **Resource Allocation:** Helps prioritize educational investments
        """)


def show_preprocessing(df, df_processed, math_cols, science_cols, sst_cols, language_cols):
    """Display data preprocessing steps and results"""
    st.markdown('<div class="section-header">🔧 Data Preprocessing Pipeline</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This section details the preprocessing steps applied to transform the raw NAS dataset 
    into a clean, analysis-ready format.
    """)
    
    # Step 1: Column Name Cleaning
    st.markdown("### Step 1: Column Name Standardization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Before Cleaning (Sample):**")
        original_cols = [
            "Average Performance Of Students In M601 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1",
            "Number Of Schools Surveyed (UOM:Number), Scaling Factor:1",
            "Average Performance Of Students In Sci703 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1"
        ]
        for col in original_cols:
            st.code(col, language="text")
    
    with col2:
        st.markdown("**After Cleaning:**")
        cleaned_cols = [
            "Average_Performance_Of_Students_In_M601_Learning_Outcome",
            "Number_Of_Schools_Surveyed",
            "Average_Performance_Of_Students_In_Sci703_Learning_Outcome"
        ]
        for col in cleaned_cols:
            st.code(col, language="text")
    
    # Step 2: Year Extraction
    st.markdown("### Step 2: Year Data Extraction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Original Year Format:**")
        st.code("Calendar Year (Jan - Dec), 2021", language="text")
    
    with col2:
        st.markdown("**Extracted Year:**")
        st.code("2021", language="text")
    
    # Step 3: Subject Classification
    st.markdown("### Step 3: Subject-wise Column Classification")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Mathematics Columns**")
        st.metric("Count", len(math_cols))
        with st.expander("View Math Columns"):
            for col in math_cols[:5]:
                st.text(col.replace('Average_Performance_Of_Students_In_', '').replace('_Learning_Outcome', ''))
            if len(math_cols) > 5:
                st.text(f"... and {len(math_cols)-5} more")
    
    with col2:
        st.markdown("**Science Columns**")
        st.metric("Count", len(science_cols))
        with st.expander("View Science Columns"):
            for col in science_cols[:5]:
                st.text(col.replace('Average_Performance_Of_Students_In_', '').replace('_Learning_Outcome', ''))
            if len(science_cols) > 5:
                st.text(f"... and {len(science_cols)-5} more")
    
    with col3:
        st.markdown("**Social Science Columns**")
        st.metric("Count", len(sst_cols))
        with st.expander("View SST Columns"):
            for col in sst_cols[:5]:
                st.text(col.replace('Average_Performance_Of_Students_In_', '').replace('_Learning_Outcome', ''))
            if len(sst_cols) > 5:
                st.text(f"... and {len(sst_cols)-5} more")
    
    with col4:
        st.markdown("**Language Columns**")
        st.metric("Count", len(language_cols))
        with st.expander("View Language Columns"):
            for col in language_cols[:5]:
                st.text(col.replace('Average_Performance_Of_Students_In_', '').replace('_Learning_Outcome', ''))
            if len(language_cols) > 5:
                st.text(f"... and {len(language_cols)-5} more")
    
    # Step 4: Performance Score Calculation
    st.markdown("### Step 4: Aggregated Performance Score Calculation")
    
    st.markdown("""
    **Methodology:** For each subject area, we calculate the mean performance across all related learning outcomes:
    
    - **Math Performance** = Average of all Mathematics learning outcomes
    - **Science Performance** = Average of all Science learning outcomes  
    - **SST Performance** = Average of all Social Science learning outcomes
    - **Language Performance** = Average of all Language learning outcomes
    - **Overall Performance** = Average of all four subject performances
    """)
    
    # Show sample calculations
    if len(df_processed) > 0:
        sample_district = df_processed.iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Sample District Performance:**")
            district_name = sample_district.get('District', 'N/A')
            state_name = sample_district.get('State', 'N/A')
            st.markdown(f"**District:** {district_name}, {state_name}")
            st.metric("Math Performance", f"{sample_district.get('Math_Performance', 0):.2f}%")
            st.metric("Science Performance", f"{sample_district.get('Science_Performance', 0):.2f}%")
        
        with col2:
            st.markdown("**Calculated Scores:**")
            st.markdown("&nbsp;")  # Spacing
            st.metric("SST Performance", f"{sample_district.get('SST_Performance', 0):.2f}%")
            st.metric("Overall Performance", f"{sample_district.get('Overall_Performance', 0):.2f}%")
    
    # Data Quality Check
    st.markdown("### Step 5: Data Quality Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        missing_data = df_processed.isnull().sum().sum()
        st.metric("Missing Values", missing_data)
    
    with col2:
        duplicate_rows = df_processed.duplicated().sum()
        st.metric("Duplicate Rows", duplicate_rows)
    
    with col3:
        data_types = df_processed.dtypes.value_counts()
        st.metric("Data Types", len(data_types))
    
    # Final dataset preview
    st.markdown("### Processed Dataset Preview")
    
    # Select key columns for display
    display_cols = []
    for col in ['Country', 'State', 'District', 'Year', 'Number_Of_Schools_Surveyed', 
                'Number_Of_Students_Surveyed', 'Math_Performance', 'Science_Performance', 
                'SST_Performance', 'Language_Performance', 'Overall_Performance']:
        if col in df_processed.columns:
            display_cols.append(col)
    
    if display_cols:
        st.dataframe(df_processed[display_cols].head(10), use_container_width=True)
    else:
        st.dataframe(df_processed.head(10), use_container_width=True)


def show_eda(df_latest):
    """Display exploratory data analysis"""
    st.markdown('<div class="section-header">📈 Exploratory Data Analysis</div>', unsafe_allow_html=True)
    
    if len(df_latest) == 0:
        st.warning("No data available for analysis.")
        return
    
    # National Summary Statistics
    st.markdown("### 📊 National Performance Summary")
    
    performance_cols = []
    for col in ['Overall_Performance', 'Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance']:
        if col in df_latest.columns and df_latest[col].notna().any():
            performance_cols.append(col)
    
    if not performance_cols:
        st.warning("No performance data available for analysis.")
        return
    
    summary_stats = df_latest[performance_cols].describe()
    
    # Create columns dynamically based on available data
    cols = st.columns(len(performance_cols))
    
    col_names = {
        'Overall_Performance': 'Overall Performance',
        'Math_Performance': 'Mathematics',
        'Science_Performance': 'Science',
        'SST_Performance': 'Social Science',
        'Language_Performance': 'Language'
    }
    
    for i, col in enumerate(performance_cols):
        with cols[i]:
            col_name = col_names.get(col, col)
            mean_val = summary_stats.loc['mean', col]
            std_val = summary_stats.loc['std', col]
            st.metric(col_name, f"{mean_val:.1f}%", f"±{std_val:.1f}%")
    
    # Performance Distribution
    st.markdown("### 📊 Performance Score Distributions")
    
    # Create subplots based on available performance columns
    n_cols = min(2, len(performance_cols))
    n_rows = (len(performance_cols) + n_cols - 1) // n_cols
    
    fig = make_subplots(
        rows=n_rows, cols=n_cols,
        subplot_titles=[col_names.get(col, col) for col in performance_cols[:n_rows*n_cols]]
    )
    
    for i, col in enumerate(performance_cols[:n_rows*n_cols]):
        row = i // n_cols + 1
        col_pos = i % n_cols + 1
        
        fig.add_trace(
            go.Histogram(x=df_latest[col], name=col_names.get(col, col), nbinsx=30, opacity=0.7),
            row=row, col=col_pos
        )
    
    fig.update_layout(height=300*n_rows, showlegend=False, title_text="Distribution of Performance Scores Across Districts")
    st.plotly_chart(fig, use_container_width=True)
    
    # State-wise Performance Analysis
    if 'State' in df_latest.columns:
        st.markdown("### 🏛️ State-wise Performance Rankings")
        
        state_performance = df_latest.groupby('State')[performance_cols].mean().round(2)
        
        if 'Overall_Performance' in performance_cols:
            state_performance['Overall_Rank'] = state_performance['Overall_Performance'].rank(ascending=False)
            state_performance = state_performance.sort_values('Overall_Performance', ascending=False)
            sort_col = 'Overall_Performance'
        else:
            sort_col = performance_cols[0]
            state_performance = state_performance.sort_values(sort_col, ascending=False)
        
        # Top and Bottom performing states
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🏆 Top 10 Performing States/UTs**")
            top_states = state_performance.head(10)
            
            fig_top = px.bar(
                x=top_states[sort_col], 
                y=top_states.index,
                orientation='h',
                title="Top 10 States by Performance",
                color=top_states[sort_col],
                color_continuous_scale='Viridis'
            )
            fig_top.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_top, use_container_width=True)
        
        with col2:
            st.markdown("**📉 Bottom 10 Performing States/UTs**")
            bottom_states = state_performance.tail(10)
            
            fig_bottom = px.bar(
                x=bottom_states[sort_col], 
                y=bottom_states.index,
                orientation='h',
                title="Bottom 10 States by Performance",
                color=bottom_states[sort_col],
                color_continuous_scale='Reds'
            )
            fig_bottom.update_layout(height=400, yaxis={'categoryorder': 'total descending'})
            st.plotly_chart(fig_bottom, use_container_width=True)


def show_performance_analysis(df_latest):
    """Display detailed performance analysis"""
    st.markdown('<div class="section-header">📊 Advanced Performance Analysis</div>', unsafe_allow_html=True)
    
    if len(df_latest) == 0:
        st.warning("No data available for analysis.")
        return
    
    # Performance Correlation Analysis
    performance_cols = []
    for col in ['Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance']:
        if col in df_latest.columns and df_latest[col].notna().any():
            performance_cols.append(col)
    
    if len(performance_cols) >= 2:
        st.markdown("### 🔗 Subject Performance Correlations")
        
        correlation_matrix = df_latest[performance_cols].corr()
        
        fig_corr = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix of Subject Performances",
            color_continuous_scale='RdBu'
        )
        fig_corr.update_layout(height=500)
        st.plotly_chart(fig_corr, use_container_width=True)
    
    # Performance vs School/Student Count Analysis
    if all(col in df_latest.columns for col in ['Number_Of_Schools_Surveyed', 'Overall_Performance']):
        st.markdown("### 🏫 Performance vs Survey Scale Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            size_col = 'Number_Of_Students_Surveyed' if 'Number_Of_Students_Surveyed' in df_latest.columns else None
            hover_data = []
            for col in ['State', 'District']:
                if col in df_latest.columns:
                    hover_data.append(col)
            
            fig_schools = px.scatter(
                df_latest,
                x='Number_Of_Schools_Surveyed',
                y='Overall_Performance',
                color='Overall_Performance',
                size=size_col,
                hover_data=hover_data,
                title="Performance vs Number of Schools Surveyed",
                color_continuous_scale='Viridis'
            )
            fig_schools.update_layout(height=400)
            st.plotly_chart(fig_schools, use_container_width=True)
        
        with col2:
            if 'Number_Of_Students_Surveyed' in df_latest.columns:
                fig_students = px.scatter(
                    df_latest,
                    x='Number_Of_Students_Surveyed',
                    y='Overall_Performance',
                    color='Overall_Performance',
                    size='Number_Of_Schools_Surveyed',
                    hover_data=hover_data,
                    title="Performance vs Number of Students Surveyed",
                    color_continuous_scale='Viridis'
                )
                fig_students.update_layout(height=400)
                st.plotly_chart(fig_students, use_container_width=True)


def show_district_mapping(df_latest):
    """Display district-level mapping visualization"""
    st.markdown('<div class="section-header">🗺️ District-Level Performance Mapping</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This section provides geographical visualization of district-level performance across India. 
    Due to the complexity of Indian district boundaries and the need for accurate geospatial data, 
    we present alternative visualizations that effectively show geographical patterns.
    """)
    
    if len(df_latest) == 0:
        st.warning("No data available for mapping.")
        return
    
    # State-wise heatmap
    if 'State' in df_latest.columns:
        st.markdown("### 🌡️ State-wise Performance Heatmap")
        
        performance_cols = []
        for col in ['Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance', 'Overall_Performance']:
            if col in df_latest.columns and df_latest[col].notna().any():
                performance_cols.append(col)
        
        if performance_cols:
            state_performance = df_latest.groupby('State')[performance_cols].mean()
            
            fig_heatmap = px.imshow(
                state_performance.T,
                aspect="auto",
                title="State-wise Performance Heatmap",
                color_continuous_scale='RdYlGn',
                labels=dict(x="States/UTs", y="Subjects", color="Performance %")
            )
            fig_heatmap.update_layout(height=400)
            st.plotly_chart(fig_heatmap, use_container_width=True)


def show_insights_and_recommendations(df_latest):
    """Display key insights and recommendations"""
    st.markdown('<div class="section-header">💡 Key Insights & Recommendations</div>', unsafe_allow_html=True)
    
    if len(df_latest) == 0:
        st.warning("No data available for generating insights.")
        return
    
    # Calculate key metrics for insights
    performance_cols = []
    for col in ['Overall_Performance', 'Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance']:
        if col in df_latest.columns and df_latest[col].notna().any():
            performance_cols.append(col)
    
    if not performance_cols:
        st.warning("No performance data available for insights.")
        return
    
    # Key Insights
    st.markdown("### 🔍 Key Findings")
    
    overall_mean = df_latest[performance_cols[0]].mean() if performance_cols else 0
    
    insights = [
        {
            "title": "📊 Overall Performance Landscape",
            "content": f"""
            - **National Average:** {overall_mean:.1f}% across all districts
            - **Performance Range:** {df_latest[performance_cols[0]].min():.1f}% to {df_latest[performance_cols[0]].max():.1f}%
            - **Standard Deviation:** {df_latest[performance_cols[0]].std():.1f}% indicating variation across districts
            - **Total Districts Analyzed:** {len(df_latest)}
            """
        }
    ]
    
    for insight in insights:
        with st.expander(insight["title"]):
            st.markdown(insight["content"])
    
    # Recommendations
    st.markdown("### 🎯 Strategic Recommendations")
    
    recommendations = [
        {
            "category": "🏫 Educational Infrastructure",
            "recommendations": [
                "Prioritize resource allocation to underperforming districts",
                "Establish teacher training centers in low-performing regions",
                "Implement technology-enabled learning solutions in remote areas",
                "Create district-wise mentorship programs pairing high and low-performing schools"
            ]
        },
        {
            "category": "📚 Curriculum & Pedagogy",
            "recommendations": [
                "Focus on curriculum enhancement for subjects showing lowest performance",
                "Develop competency-based learning modules aligned with NEP 2020",
                "Introduce peer learning and collaborative teaching methods",
                "Create subject-specific intervention programs for struggling students"
            ]
        },
        {
            "category": "📊 Monitoring & Evaluation",
            "recommendations": [
                "Establish quarterly performance tracking systems",
                "Implement early warning systems for declining performance trends",
                "Create state-wise performance dashboards for real-time monitoring",
                "Develop predictive models to identify at-risk districts"
            ]
        },
        {
            "category": "🤝 Policy & Governance",
            "recommendations": [
                "Launch targeted intervention programs for bottom performing districts",
                "Create incentive structures for high-performing schools and teachers",
                "Establish inter-state knowledge sharing platforms",
                "Develop region-specific educational policies addressing local challenges"
            ]
        }
    ]
    
    for rec in recommendations:
        with st.expander(rec["category"]):
            for item in rec["recommendations"]:
                st.markdown(f"• {item}")
    
    # Success Stories
    if 'State' in df_latest.columns and performance_cols:
        st.markdown("### 🌟 Success Stories & Best Practices")
        
        state_performance = df_latest.groupby('State')[performance_cols[0]].mean().sort_values(ascending=False)
        consistent_performers = state_performance.head(5)
        
        st.markdown("**States/UTs Leading in Educational Excellence:**")
        
        for i, (state, performance) in enumerate(consistent_performers.items(), 1):
            state_data = df_latest[df_latest['State'] == state]
            
            avg_schools = state_data['Number_Of_Schools_Surveyed'].mean() if 'Number_Of_Schools_Surveyed' in state_data.columns else 0
            avg_students = state_data['Number_Of_Students_Surveyed'].mean() if 'Number_Of_Students_Surveyed' in state_data.columns else 0
            
            st.markdown(f"""
            **{i}. {state}** - {performance:.1f}% Performance
            - Average schools per district: {avg_schools:.0f}
            - Average students surveyed: {avg_students:.0f}
            - Districts: {len(state_data)}
            """)
    
    # Call to Action
    st.markdown("### 🚀 Next Steps")
    
    st.markdown("""
    <div class="insight-box">
    <h4>Immediate Actions Required:</h4>
    
    1. **Data-Driven Decision Making:** Use this analysis to prioritize resource allocation
    2. **Stakeholder Engagement:** Share insights with state education departments
    3. **Continuous Monitoring:** Implement regular assessment cycles
    4. **Best Practice Sharing:** Facilitate knowledge transfer between high and low-performing regions
    5. **Technology Integration:** Leverage digital platforms for scalable interventions
    
    <h4>Long-term Vision:</h4>
    
    - Achieve 80%+ overall performance across all districts by 2030
    - Reduce inter-state performance gap to less than 10 percentage points
    - Establish India as a global leader in competency-based education
    </div>
    """, unsafe_allow_html=True)
    
    # Download Options
    st.markdown("### 📥 Export Data & Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Download State Performance Summary"):
            if 'State' in df_latest.columns and performance_cols:
                state_performance = df_latest.groupby('State')[performance_cols].mean()
                csv = state_performance.to_csv()
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="state_performance_summary.csv",
                    mime="text/csv"
                )
            else:
                st.warning("State performance data not available.")
    
    with col2:
        if st.button("📈 Download District Analysis"):
            available_cols = []
            for col in ['State', 'District', 'Overall_Performance', 'Math_Performance', 
                       'Science_Performance', 'SST_Performance', 'Language_Performance']:
                if col in df_latest.columns:
                    available_cols.append(col)
            
            if available_cols:
                district_summary = df_latest[available_cols]
                csv = district_summary.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="district_performance_analysis.csv",
                    mime="text/csv"
                )
            else:
                st.warning("District analysis data not available.")
    
    with col3:
        if st.button("🎯 Download Recommendations Report"):
            report_content = f"""
National Achievement Survey (NAS) - Class 8 Analysis Report
Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY:
- Total Districts Analyzed: {len(df_latest)}
- Performance Analysis: Based on available learning outcome data

KEY FINDINGS:
- Comprehensive analysis of educational performance across Indian districts
- Identification of high and low-performing regions
- Subject-wise performance variations

RECOMMENDATIONS:
- Targeted interventions for underperforming districts
- Best practice sharing between high and low-performing regions
- Technology integration for scalable educational improvements
- Enhanced monitoring and evaluation systems

For detailed analysis and recommendations, refer to the full dashboard.
"""
            
            st.download_button(
                label="Download Report",
                data=report_content,
                file_name="nas_analysis_report.txt",
                mime="text/plain"
            )


# Run the main application
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please check your data file and try again.")
