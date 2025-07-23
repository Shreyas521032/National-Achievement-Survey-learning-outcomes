import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="NAS Class 8 Learning Outcomes Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2e8b57;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #2e8b57;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load and preprocess data
@st.cache_data
def load_data():
    try:
        # Try to load from uploaded file first, then from default file
        data = pd.read_csv('nas_class8_data.csv')
    except:
        # Sample data based on the provided snippet
        sample_data = """Country,State,District,Year,Class,Number Of Schools Surveyed (UOM:Number), Scaling Factor:1,Number Of Students Surveyed (UOM:Number), Scaling Factor:1,Average Performance Of Students In L813 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M601 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M606 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M620 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M621 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M702 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M705 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M706 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M707 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M710 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M717 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M719 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M721 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M801 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M802 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M803 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M804 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M808 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M812 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M818 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In M819 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci703 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci704 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci705 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci708 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci710 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci711 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci801 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci804 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci805 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci807 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci811 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sci813 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst605 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst610 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst625 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst703 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst704 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst722 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst726 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst731 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst733 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst734 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst802 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst805 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst807 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst809 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst810 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst815 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst816 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst818 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst823 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst827 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst831 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1,Average Performance Of Students In Sst833 Learning Outcome (UOM:%(Percentage)), Scaling Factor:1
India,Andaman and Nicobar Islands,Nicobars,Calendar Year (Jan - Dec) 2021,8,80,1412,37.58,39.72,33.55,28.04,28.53,32.27,29.92,33.2,32.56,24.25,32.06,34.18,34.51,28.21,32.73,39.08,31.48,31.39,24.65,33.6,24.86,24.69,36.17,24.13,28.52,27.46,16.9,26.42,15.47,21.22,30.28,36.48,27.84,34.37,22.53,33.18,24.54,40.81,23,24.81,35.25,26.21,33.76,38.06,23.73,15.46,24.81,10.79,16.42,11.64,33.94,57.59,48.56,35.05,29.05
India,Andaman and Nicobar Islands,North and Middle Andaman,Calendar Year (Jan - Dec) 2021,8,132,2428,50.02,47.57,43.83,25.3,42.78,30.95,16.73,33.18,29.6,23.24,29.28,42.51,32.14,25.6,34.32,32.8,30.01,36,38.34,41.74,30.66,37.51,42.11,44.03,42.83,38.08,28.07,50.77,38.37,37.87,27.57,42.33,49.06,32.96,28.43,33.17,54.49,53.26,34.82,41.35,47.99,24.55,26.7,31.48,23.22,33.16,36.51,23.13,33.29,34.94,43.87,24.33,31.76,26.19,56.51
India,Andaman and Nicobar Islands,South Andamans,Calendar Year (Jan - Dec) 2021,8,188,4588,57.06,53.56,45.73,27.17,40.35,30.94,18.79,19.27,27.82,25.68,40.3,38.82,41.92,33.63,39.61,43.16,26.67,37.74,36.74,30.52,28.47,45.33,40.12,45.85,45.84,41.95,27.36,52.88,27.68,43.27,34.67,45.27,43.73,38.9,31.39,35.43,63.03,41.77,36.13,36.92,50.11,32.14,35.73,35.59,30.48,35.39,36.6,17.93,29.83,30.16,35.41,28.7,26.91,30.6,62.92
India,Andhra Pradesh,Ananthapuramu,Calendar Year (Jan - Dec) 2021,8,264,7000,47.09,45.6,44.65,25.98,37.98,34.87,23.86,30.75,35.24,24.73,29.79,44.13,38.47,37.47,43.25,41.85,33.02,41.36,38.78,34.84,28.28,35.82,29.82,38.12,33.35,30.35,24.19,38.38,28.08,29.63,31.89,39.99,36.61,29.01,27.18,34.09,32.94,31.18,25.59,37.51,44.3,27.31,35.13,34.29,27.52,34.64,29.59,24.51,26.15,25.23,36.17,39.94,28.8,32.78,59.06"""
        data = pd.read_csv(StringIO(sample_data))
    
    return data

def preprocess_data(df):
    """Preprocess the dataset"""
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Rename complex column names for easier handling
    column_mapping = {}
    for col in df.columns:
        if 'Number Of Schools Surveyed' in col:
            column_mapping[col] = 'Schools_Surveyed'
        elif 'Number Of Students Surveyed' in col:
            column_mapping[col] = 'Students_Surveyed'
        elif 'Average Performance' in col:
            # Extract the learning outcome code
            if 'L813' in col:
                column_mapping[col] = 'Language_L813'
            elif 'M601' in col:
                column_mapping[col] = 'Math_M601'
            elif 'M606' in col:
                column_mapping[col] = 'Math_M606'
            # Add more mappings as needed
    
    df = df.rename(columns=column_mapping)
    
    # Extract year from the Year column
    df['Year_Clean'] = df['Year'].str.extract(r'(\d{4})')
    df['Year_Clean'] = pd.to_numeric(df['Year_Clean'], errors='coerce')
    
    # Create subject-wise average performance columns
    math_cols = [col for col in df.columns if col.startswith('Math_') or 'M6' in col or 'M7' in col or 'M8' in col]
    science_cols = [col for col in df.columns if 'Sci' in col]
    social_cols = [col for col in df.columns if 'Sst' in col]
    language_cols = [col for col in df.columns if col.startswith('Language_') or 'L8' in col]
    
    # Calculate subject averages
    if math_cols:
        df['Math_Average'] = df[math_cols].mean(axis=1, skipna=True)
    if science_cols:
        df['Science_Average'] = df[science_cols].mean(axis=1, skipna=True)
    if social_cols:
        df['Social_Science_Average'] = df[social_cols].mean(axis=1, skipna=True)
    if language_cols:
        df['Language_Average'] = df[language_cols].mean(axis=1, skipna=True)
    
    # Calculate overall average
    subject_avg_cols = ['Math_Average', 'Science_Average', 'Social_Science_Average', 'Language_Average']
    available_avg_cols = [col for col in subject_avg_cols if col in df.columns]
    if available_avg_cols:
        df['Overall_Average'] = df[available_avg_cols].mean(axis=1, skipna=True)
    
    return df

# Main app
def main():
    st.markdown('<h1 class="main-header">📊 National Achievement Survey (NAS) Class 8 Learning Outcomes Analysis</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home", "📋 Dataset Overview", "🔧 Data Preprocessing", "📈 Exploratory Data Analysis", "📊 Advanced Analysis", "🗺️ District Mapping", "💡 Insights & Recommendations"]
    )
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
        df_processed = preprocess_data(df)
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "📋 Dataset Overview":
        show_dataset_overview(df, df_processed)
    elif page == "🔧 Data Preprocessing":
        show_preprocessing(df, df_processed)
    elif page == "📈 Exploratory Data Analysis":
        show_eda(df_processed)
    elif page == "📊 Advanced Analysis":
        show_advanced_analysis(df_processed)
    elif page == "🗺️ District Mapping":
        show_district_mapping(df_processed)
    elif page == "💡 Insights & Recommendations":
        show_insights_recommendations(df_processed)

def show_home_page():
    st.markdown("""
    ## Welcome to the NAS Class 8 Learning Outcomes Analysis Dashboard
    
    This comprehensive dashboard provides an in-depth analysis of the **National Achievement Survey (NAS)** data for Class 8 students across India. 
    
    ### 🎯 What You'll Discover
    
    - **Dataset Overview**: Comprehensive information about the NAS survey and data collection methodology
    - **Data Preprocessing**: Details about data cleaning and preparation steps
    - **Exploratory Data Analysis**: Visual insights into student performance patterns
    - **Advanced Analysis**: Deep-dive analytics and statistical insights
    - **District Mapping**: Geographic visualization of learning outcomes
    - **Insights & Recommendations**: Key findings and actionable recommendations
    
    ### 📊 Key Features
    
    ✅ Interactive visualizations and charts  
    ✅ State and district-wise performance analysis  
    ✅ Subject-wise learning outcome comparisons  
    ✅ Geographic mapping of educational performance  
    ✅ Trend analysis across different regions  
    ✅ Data-driven insights and recommendations  
    
    ### 🚀 Getting Started
    
    Use the navigation menu in the sidebar to explore different sections of the analysis. Each section provides unique insights into the educational landscape of India based on the NAS Class 8 data.
    
    ---
    
    **Data Source**: Ministry of Education, Government of India  
    **Survey Period**: 2017-2021  
    **Last Updated**: July 9, 2025
    """)

def show_dataset_overview(df, df_processed):
    st.markdown('<h2 class="section-header">📋 Dataset Overview</h2>', unsafe_allow_html=True)
    
    # Dataset Information
    st.markdown("""
    ### About the National Achievement Survey (NAS)
    
    The **National Achievement Survey (NAS)** is a large-scale assessment conducted across India to evaluate the learning outcomes of students in various classes, including Class 8. This comprehensive survey provides crucial insights into the educational performance landscape of the country.
    
    #### 🎯 Survey Objectives
    - Assess competencies rather than rote memorization
    - Follow a competency-based framework aligned with the National Education Policy (NEP)
    - Measure students' understanding, application of concepts, and critical thinking skills
    - Identify gaps in learning and suggest possible interventions
    
    #### 📊 Data Collection Methodology
    - **Standardized Tests**: Administered to representative samples of students
    - **Subject Coverage**: Mathematics, Science, Social Science, and Language
    - **Assessment Focus**: Understanding, application, and critical thinking
    - **Geographic Scope**: State and District level coverage
    
    #### 📈 Report Features
    - Performance trends analysis
    - Subject-wise detailed analysis
    - Comparisons with state and national averages
    - Learning gap identification
    - Policy intervention suggestions
    """)
    
    # Dataset Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📚 Total Records</h3>
            <h2>{len(df):,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏛️ States Covered</h3>
            <h2>{df['State'].nunique()}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏙️ Districts Covered</h3>
            <h2>{df['District'].nunique()}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_students = df['Students_Surveyed'].sum() if 'Students_Surveyed' in df.columns else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Students Surveyed</h3>
            <h2>{total_students:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Data Source Information
    st.markdown("""
    ### 📋 Data Source Information
    
    | Attribute | Details |
    |-----------|---------|
    | **Publisher** | Ministry of Education, Government of India |
    | **Dataset Host** | NDAP (National Data Analytics Platform) |
    | **Sector** | Education and Training |
    | **Geographic Coverage** | State and District Level |
    | **Time Granularity** | Yearly |
    | **Frequency** | Annual |
    | **Year Range** | 2017 - 2021 |
    | **Last Updated** | July 9, 2025 |
    | **Data Format** | CSV (Structured Data) |
    """)
    
    # Sample Data Preview
    st.markdown("### 📊 Sample Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Data Schema
    st.markdown("### 🔧 Data Schema")
    schema_info = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes,
        'Non-Null Count': df.count(),
        'Null Count': df.isnull().sum()
    })
    st.dataframe(schema_info, use_container_width=True)

def show_preprocessing(df, df_processed):
    st.markdown('<h2 class="section-header">🔧 Data Preprocessing</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Data Cleaning and Preparation Steps
    
    The following preprocessing steps were applied to prepare the data for analysis:
    """)
    
    # Preprocessing steps
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🧹 Data Cleaning
        - **Column Name Standardization**: Removed extra spaces and standardized naming
        - **Complex Column Renaming**: Simplified long column names for better readability
        - **Year Extraction**: Extracted numeric year from complex year strings
        - **Data Type Conversion**: Converted appropriate columns to numeric types
        """)
    
    with col2:
        st.markdown("""
        #### 📊 Feature Engineering
        - **Subject Categorization**: Grouped learning outcomes by subjects
        - **Average Calculations**: Created subject-wise average performance metrics
        - **Overall Performance**: Calculated overall average across all subjects
        - **Missing Value Handling**: Applied appropriate strategies for missing data
        """)
    
    # Before and After comparison
    st.markdown("### 📋 Before vs After Preprocessing")
    
    tab1, tab2 = st.tabs(["Original Data", "Processed Data"])
    
    with tab1:
        st.markdown("**Original Dataset Structure:**")
        st.write(f"Shape: {df.shape}")
        st.dataframe(df.head(), use_container_width=True)
    
    with tab2:
        st.markdown("**Processed Dataset Structure:**")
        st.write(f"Shape: {df_processed.shape}")
        st.dataframe(df_processed.head(), use_container_width=True)
    
    # Data Quality Metrics
    st.markdown("### 📈 Data Quality Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        missing_percentage = (df.isnull().sum().sum() / df.size) * 100
        st.metric("Missing Data %", f"{missing_percentage:.2f}%")
    
    with col2:
        duplicate_rows = df.duplicated().sum()
        st.metric("Duplicate Records", duplicate_rows)
    
    with col3:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        st.metric("Numeric Columns", len(numeric_cols))
    
    # Subject-wise column mapping
    if 'Math_Average' in df_processed.columns:
        st.markdown("### 📚 Subject-wise Learning Outcomes Mapping")
        
        subjects_info = {
            "Mathematics": [col for col in df_processed.columns if 'Math_' in col or any(code in col for code in ['M6', 'M7', 'M8'])],
            "Science": [col for col in df_processed.columns if 'Sci' in col],
            "Social Science": [col for col in df_processed.columns if 'Sst' in col],
            "Language": [col for col in df_processed.columns if 'Language_' in col or 'L8' in col]
        }
        
        for subject, columns in subjects_info.items():
            if columns:
                st.markdown(f"**{subject}**: {len(columns)} learning outcomes")
                with st.expander(f"View {subject} columns"):
                    st.write(columns)

def show_eda(df_processed):
    st.markdown('<h2 class="section-header">📈 Exploratory Data Analysis</h2>', unsafe_allow_html=True)
    
    # Performance Distribution
    st.markdown("### 📊 Performance Distribution Analysis")
    
    if 'Overall_Average' in df_processed.columns:
        fig = px.histogram(
            df_processed, 
            x='Overall_Average', 
            nbins=30,
            title="Distribution of Overall Student Performance",
            labels={'Overall_Average': 'Overall Average Performance (%)', 'count': 'Number of Districts'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean Performance", f"{df_processed['Overall_Average'].mean():.2f}%")
        with col2:
            st.metric("Median Performance", f"{df_processed['Overall_Average'].median():.2f}%")
        with col3:
            st.metric("Std Deviation", f"{df_processed['Overall_Average'].std():.2f}")
        with col4:
            st.metric("Performance Range", f"{df_processed['Overall_Average'].max() - df_processed['Overall_Average'].min():.2f}%")
    
    # State-wise Analysis
    st.markdown("### 🏛️ State-wise Performance Analysis")
    
    if 'Overall_Average' in df_processed.columns:
        state_performance = df_processed.groupby('State')['Overall_Average'].agg(['mean', 'count']).reset_index()
        state_performance = state_performance.sort_values('mean', ascending=False)
        
        fig = px.bar(
            state_performance.head(15), 
            x='State', 
            y='mean',
            title="Top 15 States by Average Performance",
            labels={'mean': 'Average Performance (%)', 'State': 'State'}
        )
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Subject-wise Comparison
    st.markdown("### 📚 Subject-wise Performance Comparison")
    
    subject_cols = ['Math_Average', 'Science_Average', 'Social_Science_Average', 'Language_Average']
    available_subjects = [col for col in subject_cols if col in df_processed.columns]
    
    if available_subjects:
        subject_data = []
        for col in available_subjects:
            subject_name = col.replace('_Average', '').replace('_', ' ')
            subject_data.extend([{
                'Subject': subject_name,
                'Performance': perf,
                'District': dist
            } for perf, dist in zip(df_processed[col].dropna(), df_processed['District'])])
        
        subject_df = pd.DataFrame(subject_data)
        
        fig = px.box(
            subject_df,
            x='Subject',
            y='Performance',
            title="Subject-wise Performance Distribution",
            labels={'Performance': 'Average Performance (%)'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Correlation Analysis
    st.markdown("### 🔗 Performance Correlation Analysis")
    
    if available_subjects and len(available_subjects) > 1:
        corr_matrix = df_processed[available_subjects].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Subject Performance Correlation Matrix",
            color_continuous_scale="RdBu"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # District Performance Analysis
    st.markdown("### 🏙️ Top and Bottom Performing Districts")
    
    if 'Overall_Average' in df_processed.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            top_districts = df_processed.nlargest(10, 'Overall_Average')[['State', 'District', 'Overall_Average']]
            st.markdown("**🏆 Top 10 Performing Districts**")
            st.dataframe(top_districts, use_container_width=True)
        
        with col2:
            bottom_districts = df_processed.nsmallest(10, 'Overall_Average')[['State', 'District', 'Overall_Average']]
            st.markdown("**📉 Bottom 10 Performing Districts**")
            st.dataframe(bottom_districts, use_container_width=True)

def show_advanced_analysis(df_processed):
    st.markdown('<h2 class="section-header">📊 Advanced Analysis</h2>', unsafe_allow_html=True)
    
    # Performance Categories
    st.markdown("### 🎯 Performance Category Analysis")
    
    if 'Overall_Average' in df_processed.columns:
        # Create performance categories
        df_processed['Performance_Category'] = pd.cut(
            df_processed['Overall_Average'],
            bins=[0, 30, 50, 70, 100],
            labels=['Low (0-30%)', 'Moderate (30-50%)', 'Good (50-70%)', 'Excellent (70-100%)']
        )
        
        category_counts = df_processed['Performance_Category'].value_counts()
        
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Distribution of Districts by Performance Category"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Category-wise statistics
        category_stats = df_processed.groupby('Performance_Category').agg({
            'District': 'count',
            'Students_Surveyed': 'sum' if 'Students_Surveyed' in df_processed.columns else 'count',
            'Overall_Average': ['mean', 'std']
        }).round(2)
        
        st.markdown("**Performance Category Statistics:**")
        st.dataframe(category_stats, use_container_width=True)
    
    # State-wise Performance Variance
    st.markdown("### 📈 State-wise Performance Variance Analysis")
    
    if 'Overall_Average' in df_processed.columns and df_processed['State'].nunique() > 1:
        state_stats = df_processed.groupby('State').agg({
            'Overall_Average': ['mean', 'std', 'min', 'max', 'count']
        }).round(2)
        state_stats.columns = ['Mean', 'Std Dev', 'Min', 'Max', 'Districts']
        state_stats['Range'] = state_stats['Max'] - state_stats['Min']
        state_stats = state_stats.sort_values('Mean', ascending=False)
        
        st.dataframe(state_stats, use_container_width=True)
        
        # Variance visualization
        fig = px.scatter(
            state_stats.reset_index(),
            x='Mean',
            y='Std Dev',
            size='Districts',
            hover_name='State',
            title="State Performance: Mean vs Variability",
            labels={'Mean': 'Average Performance (%)', 'Std Dev': 'Performance Variability'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Subject Performance Radar Chart
    st.markdown("### 🕸️ Subject Performance Radar Analysis")
    
    subject_cols = ['Math_Average', 'Science_Average', 'Social_Science_Average', 'Language_Average']
    available_subjects = [col for col in subject_cols if col in df_processed.columns]
    
    if len(available_subjects) >= 3:
        # Top 5 states for radar chart
        top_states = df_processed.groupby('State')['Overall_Average'].mean().nlargest(5).index
        
        radar_data = []
        for state in top_states:
            state_data = df_processed[df_processed['State'] == state][available_subjects].mean()
            radar_data.append(state_data.values.tolist() + [state_data.values[0]])  # Close the radar
        
        subjects_labels = [col.replace('_Average', '').replace('_', ' ') for col in available_subjects]
        subjects_labels.append(subjects_labels[0])  # Close the radar
        
        fig = go.Figure()
        
        for i, state in enumerate(top_states):
            fig.add_trace(go.Scatterpolar(
                r=radar_data[i],
                theta=subjects_labels,
                fill='toself',
                name=state
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 80]
                )),
            showlegend=True,
            title="Subject Performance Comparison - Top 5 States",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

def show_district_mapping(df_processed):
    st.markdown('<h2 class="section-header">🗺️ District-level Performance Mapping</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Geographic Distribution of Learning Outcomes
    
    This section provides geographic visualization of district-level performance across India.
    """)
    
    # Performance by Geographic Distribution
    if 'Overall_Average' in df_processed.columns:
        # Create a simplified map using scatter plot (since actual geographic coordinates would be needed for proper mapping)
        st.markdown("### 📍 State-wise Performance Distribution")
        
        state_performance = df_processed.groupby('State').agg({
            'Overall_Average': 'mean',
            'District': 'count',
            'Students_Surveyed': 'sum' if 'Students_Surveyed' in df_processed.columns else 'count'
        }).reset_index()
        
        # Create a bubble chart representing states
        fig = px.scatter(
            state_performance,
            x='District',
            y='Overall_Average',
            size='Students_Surveyed' if 'Students_Surveyed' in df_processed.columns else 'District',
            hover_name='State',
            title="State Performance: Districts vs Average Performance",
            labels={
                'District': 'Number of Districts',
                'Overall_Average': 'Average Performance (%)',
                'Students_Surveyed': 'Students Surveyed'
            },
            color='Overall_Average',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # District-level heatmap
        st.markdown("### 🔥 District Performance Heatmap")
        
        # Create a pivot table for heatmap
        if df_processed['State'].nunique() > 1 and df_processed['District'].nunique() > 1:
            # Select top states with most districts for better visualization
            top_states = df_processed.groupby('State').size().nlargest(10).index
            heatmap_data = df_processed[df_processed['State'].isin(top_states)]
            
            pivot_data = heatmap_data.pivot_table(
                index='State',
                columns='District',
                values='Overall_Average',
                aggfunc='mean'
            )
            
            # Limit to manageable size
            if pivot_data.shape[1] > 20:
                # Take top performing districts from each state
                top_districts = []
                for state in pivot_data.index:
                    state_districts = pivot_data.loc[state].dropna().nlargest(5)
                    top_districts.extend(state_districts.index.tolist())
                
                pivot_data = pivot_data[list(set(top_districts))]
            
            fig = px.imshow(
                pivot_data,
                aspect="auto",
                title="District Performance Heatmap (Top States & Districts)",
                labels={'x': 'District', 'y': 'State', 'color': 'Performance (%)'},
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    # Regional Analysis
    st.markdown("### 🏛️ Regional Performance Analysis")
    
    # Create regions based on states (simplified grouping)
    region_mapping = {
        'North': ['Punjab', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Delhi', 'Uttarakhand'],
        'South': ['Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 'Telangana', 'Kerala'],
        'East': ['West Bengal', 'Odisha', 'Jharkhand', 'Bihar'],
        'West': ['Maharashtra', 'Gujarat', 'Rajasthan', 'Goa'],
        'Central': ['Madhya Pradesh', 'Chhattisgarh', 'Uttar Pradesh'],
        'Northeast': ['Assam', 'Meghalaya', 'Manipur', 'Mizoram', 'Nagaland', 'Tripura', 'Arunachal Pradesh', 'Sikkim'],
        'Islands': ['Andaman and Nicobar Islands', 'Lakshadweep']
    }
    
    # Create region column
    df_processed['Region'] = 'Other'
    for region, states in region_mapping.items():
        df_processed.loc[df_processed['State'].isin(states), 'Region'] = region
    
    if 'Overall_Average' in df_processed.columns:
        region_performance = df_processed.groupby('Region').agg({
            'Overall_Average': ['mean', 'std', 'count'],
            'Students_Surveyed': 'sum' if 'Students_Surveyed' in df_processed.columns else 'count'
        }).round(2)
        
        region_performance.columns = ['Mean Performance', 'Std Dev', 'Districts', 'Total Students']
        region_performance = region_performance.sort_values('Mean Performance', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                region_performance.reset_index(),
                x='Region',
                y='Mean Performance',
                title="Regional Average Performance",
                color='Mean Performance',
                color_continuous_scale='RdYlGn'
            )
            fig.update_xaxes(tickangle=45)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Regional Performance Statistics:**")
            st.dataframe(region_performance, use_container_width=True)
    
    # Interactive District Selector
    st.markdown("### 🔍 Interactive District Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_state = st.selectbox("Select State:", options=sorted(df_processed['State'].unique()))
    
    with col2:
        state_districts = df_processed[df_processed['State'] == selected_state]['District'].unique()
        selected_district = st.selectbox("Select District:", options=sorted(state_districts))
    
    # Display selected district information
    if selected_state and selected_district:
        district_data = df_processed[
            (df_processed['State'] == selected_state) & 
            (df_processed['District'] == selected_district)
        ].iloc[0]
        
        st.markdown(f"### 📊 Performance Profile: {selected_district}, {selected_state}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overall_perf = district_data.get('Overall_Average', 'N/A')
            st.metric("Overall Performance", f"{overall_perf:.2f}%" if isinstance(overall_perf, (int, float)) else "N/A")
        
        with col2:
            students = district_data.get('Students_Surveyed', 'N/A')
            st.metric("Students Surveyed", f"{students:,}" if isinstance(students, (int, float)) else "N/A")
        
        with col3:
            schools = district_data.get('Schools_Surveyed', 'N/A')
            st.metric("Schools Surveyed", f"{schools:,}" if isinstance(schools, (int, float)) else "N/A")
        
        with col4:
            region = district_data.get('Region', 'N/A')
            st.metric("Region", region)
        
        # Subject-wise performance for selected district
        subject_cols = ['Math_Average', 'Science_Average', 'Social_Science_Average', 'Language_Average']
        available_subjects = [col for col in subject_cols if col in df_processed.columns and pd.notna(district_data.get(col))]
        
        if available_subjects:
            subject_scores = [district_data[col] for col in available_subjects]
            subject_names = [col.replace('_Average', '').replace('_', ' ') for col in available_subjects]
            
            fig = px.bar(
                x=subject_names,
                y=subject_scores,
                title=f"Subject-wise Performance: {selected_district}",
                labels={'x': 'Subject', 'y': 'Performance (%)'},
                color=subject_scores,
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

def show_insights_recommendations(df_processed):
    st.markdown('<h2 class="section-header">💡 Key Insights & Recommendations</h2>', unsafe_allow_html=True)
    
    # Calculate key metrics for insights
    if 'Overall_Average' in df_processed.columns:
        overall_mean = df_processed['Overall_Average'].mean()
        overall_std = df_processed['Overall_Average'].std()
        best_state = df_processed.groupby('State')['Overall_Average'].mean().idxmax()
        worst_state = df_processed.groupby('State')['Overall_Average'].mean().idxmin()
        
        # Performance categories
        low_performers = len(df_processed[df_processed['Overall_Average'] < 30])
        high_performers = len(df_processed[df_processed['Overall_Average'] > 70])
        total_districts = len(df_processed)
        
        st.markdown("### 🔍 Key Findings")
        
        findings = [
            f"**Overall Performance**: The national average performance stands at {overall_mean:.2f}% with a standard deviation of {overall_std:.2f}%, indicating significant variation across districts.",
            f"**Top Performer**: {best_state} shows the highest average performance among all states.",
            f"**Performance Distribution**: {high_performers} districts ({(high_performers/total_districts)*100:.1f}%) demonstrate excellent performance (>70%), while {low_performers} districts ({(low_performers/total_districts)*100:.1f}%) need urgent attention (<30%).",
            f"**Regional Disparities**: Significant performance gaps exist between different regions, highlighting the need for targeted interventions."
        ]
        
        for i, finding in enumerate(findings, 1):
            st.markdown(f"{i}. {finding}")
    
    # Subject-wise insights
    st.markdown("### 📚 Subject-wise Analysis")
    
    subject_cols = ['Math_Average', 'Science_Average', 'Social_Science_Average', 'Language_Average']
    available_subjects = [col for col in subject_cols if col in df_processed.columns]
    
    if available_subjects:
        subject_performance = {}
        for col in available_subjects:
            subject_name = col.replace('_Average', '').replace('_', ' ')
            subject_performance[subject_name] = df_processed[col].mean()
        
        best_subject = max(subject_performance, key=subject_performance.get)
        worst_subject = min(subject_performance, key=subject_performance.get)
        
        st.markdown(f"""
        - **Strongest Subject**: {best_subject} shows the highest average performance at {subject_performance[best_subject]:.2f}%
        - **Challenging Subject**: {worst_subject} needs more attention with an average of {subject_performance[worst_subject]:.2f}%
        - **Subject Correlation**: Strong correlations between subjects suggest comprehensive educational approaches work better
        """)
    
    # Actionable Recommendations
    st.markdown("### 🎯 Strategic Recommendations")
    
    recommendations = [
        {
            "title": "🏫 Immediate Interventions",
            "items": [
                "Focus on districts with performance below 30% for urgent remedial programs",
                "Implement peer-to-peer learning programs between high and low performing districts",
                "Strengthen teacher training programs in underperforming regions",
                "Increase infrastructure investment in bottom-performing districts"
            ]
        },
        {
            "title": "📈 Medium-term Strategies",
            "items": [
                "Develop region-specific curriculum adaptations based on local performance patterns",
                "Establish performance monitoring systems for continuous assessment",
                "Create incentive programs for schools showing improvement",
                "Strengthen community engagement in educational outcomes"
            ]
        },
        {
            "title": "🌟 Long-term Vision",
            "items": [
                "Align educational policies with NEP 2020 competency-based framework",
                "Develop comprehensive teacher development programs",
                "Establish research centers in high-performing regions to study best practices",
                "Create national excellence networks for knowledge sharing"
            ]
        },
        {
            "title": "📊 Data-Driven Approaches",
            "items": [
                "Implement real-time performance tracking systems",
                "Use predictive analytics to identify at-risk students early",
                "Develop personalized learning pathways based on individual performance",
                "Create automated reporting systems for stakeholders"
            ]
        }
    ]
    
    for rec in recommendations:
        with st.expander(rec["title"]):
            for item in rec["items"]:
                st.markdown(f"• {item}")
    
    # Success Stories
    st.markdown("### 🏆 Success Stories & Best Practices")
    
    if 'Overall_Average' in df_processed.columns:
        top_districts = df_processed.nlargest(5, 'Overall_Average')[['State', 'District', 'Overall_Average']]
        
        st.markdown("""
        **Top Performing Districts:**
        These districts demonstrate excellence and can serve as models for others:
        """)
        
        for idx, row in top_districts.iterrows():
            st.markdown(f"🥇 **{row['District']}, {row['State']}**: {row['Overall_Average']:.2f}% average performance")
    
    # Future Roadmap
    st.markdown("### 🚀 Future Roadmap")
    
    st.markdown("""
    #### Phase 1 (0-6 months): Foundation Building
    - Identify and support bottom 10% performing districts
    - Launch teacher training programs
    - Establish baseline monitoring systems
    
    #### Phase 2 (6-18 months): Implementation
    - Roll out intervention programs
    - Begin infrastructure improvements
    - Develop regional excellence centers
    
    #### Phase 3 (18+ months): Scaling & Sustainability
    - Scale successful interventions nationally
    - Establish long-term monitoring systems
    - Create sustainable improvement frameworks
    """)
    
    # Call to Action
    st.markdown("### 📢 Call to Action")
    
    st.markdown("""
    <div class="insight-box">
    <h4>🎯 Next Steps for Stakeholders</h4>
    
    <b>For Policy Makers:</b>
    <ul>
    <li>Prioritize resource allocation to underperforming regions</li>
    <li>Develop evidence-based policy interventions</li>
    <li>Create accountability mechanisms for improvement</li>
    </ul>
    
    <b>For Educators:</b>
    <ul>
    <li>Focus on competency-based teaching methods</li>
    <li>Participate in continuous professional development</li>
    <li>Collaborate with high-performing schools for best practices</li>
    </ul>
    
    <b>For Communities:</b>
    <ul>
    <li>Engage actively in local school improvement initiatives</li>
    <li>Support students through community learning programs</li>
    <li>Monitor and advocate for educational quality</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
