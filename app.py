import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Set page configuration
st.set_page_config(
    page_title="National Achievement Survey (NAS) Analysis",
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

# Data loading and caching
@st.cache_data
def load_data():
    """Load and preprocess the NAS dataset"""
    try:
        # Try to load from uploaded file first
        df = pd.read_csv('Dataset/National_Achievement_Survey_dataset.csv')
    except:
        st.error("Please ensure National_Achievement_Survey_dataset.csv is in the same directory as this script.")
        st.stop()
    
    return df


# Learning Outcomes Data
learning_outcomes_data = {
    "L813": "Read textual/non-textual materials with comprehension and identifies the details, characters, main idea and sequence of ideas and events while reading. Significance: Essential for developing strong reading comprehension and analytical skills, crucial for academic success and information processing.",
    "M601": "Solves problems involving large numbers by applying appropriate operations. Significance: Fundamental for building a strong mathematical foundation, enabling students to handle complex calculations and real-world quantitative problems.",
    "M606": "Solves problems on daily life situations involving addition and subtraction of fractions / decimals. Significance: Practical application of mathematical concepts, fostering problem-solving skills relevant to everyday scenarios like finance and measurements.",
    "M620": "Finds out the perimeter and area of rectangular objects in the surroundings like floor of the class room, surfaces of a chalk box etc. Significance: Develops spatial reasoning and practical geometry skills, useful in fields like architecture, engineering, and design.",
    "M621": "Arranges given/collected information in the form of table, pictograph and bar graph and interprets them. Significance: Crucial for data literacy, enabling students to organize, visualize, and understand information, a key skill in the data-driven world.",
    "M702": "Interprets the division and multiplication of fractions. Significance: Advances understanding of fractional arithmetic, vital for higher-level mathematics and scientific calculations.",
    "M705": "Solves problems related to daily life situations involving rational numbers. Significance: Enhances practical mathematical skills, allowing students to apply rational number concepts to real-world financial and measurement contexts.",
    "M706": "Uses exponential form of numbers to simplify problems involving multiplication and division of large numbers. Significance: Simplifies complex calculations, providing a powerful tool for scientific notation and understanding exponential growth/decay.",
    "M707": "Adds/subtracts algebraic expressions. Significance: Introduces foundational algebraic skills, essential for solving equations and understanding mathematical relationships.",
    "M710": "Solves problems related to conversion of percentage to fraction and decimal and vice versa. Significance: Develops versatility in numerical representation, critical for financial literacy, statistics, and data interpretation.",
    "M717": "Finds out approximate area of closed shapes by using unit square grid/graph sheet. Significance: Fosters estimation and approximation skills, useful in various practical applications where precise measurements are not always feasible.",
    "M719": "Finds various representative values for simple data from her/his daily life contexts like mean, median and mode. Significance: Introduces basic statistical concepts, enabling students to analyze and summarize data from their environment.",
    "M721": "Interprets data using bar graph. Significance: Enhances data visualization and interpretation skills, allowing students to draw conclusions from graphical representations.",
    "M801": "Generalizes properties of addition, subtraction, multiplication and division of rational numbers through patterns. Significance: Deepens understanding of number properties, crucial for advanced mathematical reasoning and abstract thinking.",
    "M802": "Finds rational numbers between two given rational numbers. Significance: Reinforces understanding of number density and rational number properties, important for number theory and advanced mathematics.",
    "M803": "Proves divisibility rules of 2, 3,4, 5, 6, 9 and 11. Significance: Develops number sense and logical reasoning, useful for mental math and understanding number theory.",
    "M804": "Finds squares, cubes, square roots and cube roots of numbers using different methods. Significance: Builds foundational skills in exponents and roots, essential for algebra, geometry, and various scientific calculations.",
    "M808": "Uses various algebraic identities in solving problems of daily life. Significance: Applies algebraic concepts to practical situations, enhancing problem-solving abilities in diverse contexts.",
    "M812": "Verifies properties of parallelogram and establishes the relationship between them through reasoning. Significance: Develops geometric reasoning and proof skills, fundamental for advanced geometry and spatial analysis.",
    "M818": "Finds surface area and volume of cuboidal and cylindrical object. Significance: Essential for understanding 3D shapes and their properties, with applications in engineering, design, and packaging.",
    "M819": "Draws and interprets bar charts and pie charts. Significance: Strengthens data visualization and interpretation skills, enabling effective communication of data insights.",
    "SCI703": "Classifies materials and organisms based on properties/characteristics. Significance: Develops observational and categorization skills, foundational for scientific inquiry and understanding biological and chemical diversity.",
    "SCI704": "Conducts simple investigation to seek answers to queries. Significance: Fosters scientific inquiry and experimental design skills, crucial for hands-on learning and problem-solving in science.",
    "SCI705": "Relates processes and phenomenon with causes. Significance: Promotes critical thinking and cause-and-effect reasoning, essential for understanding scientific principles and natural phenomena.",
    "SCI708": "Measures and calculates eg, temperature; pulse rate; speed of moving objects; time period of a simple pendulum, etc. Significance: Develops practical measurement and calculation skills, vital for experimental science and data collection.",
    "SCI710": "Plots and interprets graphs. Significance: Enhances data analysis and visualization skills, allowing students to understand trends and relationships in scientific data.",
    "SCI711": "Constructs models using materials from surroundings and explains their working. Significance: Encourages creativity and practical application of scientific knowledge, fostering hands-on learning and understanding of scientific principles.",
    "SCI801": "Differentiates materials, organism and processes. Significance: Refines classification and analytical skills, crucial for understanding the diversity and complexity of the natural world.",
    "SCI804": "Relates processes and phenomenon with causes. Significance: Deepens understanding of scientific causality, enabling students to explain and predict natural events.",
    "SCI805": "Explains processes and phenomenon. Significance: Develops clear and concise scientific communication skills, essential for conveying complex ideas.",
    "SCI807": "Measures angles of incidence and reflection, etc. Significance: Applies geometric principles to optics, fundamental for understanding light and its behavior.",
    "SCI811": "Applies learning of scientific concepts in day-to-day life. Significance: Connects classroom learning to real-world applications, making science relevant and practical.",
    "SCI813": "Makes efforts to protect environment. Significance: Fosters environmental awareness and responsibility, promoting sustainable practices and civic engagement.",
    "SST605": "Identifies latitudes and longitudes, eg, poles, equator, tropics, States/UTs of India and other neighboring countries on globe and the world map. Significance: Develops geographical literacy and spatial awareness, essential for understanding global locations and navigation.",
    "SST610": "Locates important historical sites, places on an outline map of India. Significance: Enhances historical and geographical knowledge, connecting historical events to their physical locations.",
    "SST625": "Describes the functioning of rural and urban local government bodies in sectors like health and education. Significance: Promotes civic knowledge and understanding of local governance, empowering students to engage with their communities.",
    "SST703": "Explains preventive actions to be undertaken in the event of disasters. Significance: Develops awareness of disaster preparedness and safety measures, crucial for personal and community well-being.",
    "SST704": "Describes formation of landforms due to various factors. Significance: Enhances understanding of geological processes and physical geography, explaining the Earth's diverse landscapes.",
    "SST722": "Explains the significance of equality in democracy. Significance: Fosters civic values and understanding of democratic principles, promoting social justice and human rights.",
    "SST726": "Describes the process of election to the legislative assembly. Significance: Educates students on democratic processes and electoral systems, encouraging informed participation in governance.",
    "SST731": "Explains the functioning of media with appropriate examples from newspapers. Significance: Develops media literacy and critical thinking about information sources, essential for navigating the modern information landscape.",
    "SST733": "Differentiates between different kinds of markets. Significance: Introduces economic concepts and market structures, providing foundational knowledge for understanding commerce and trade.",
    "SST734": "Traces how goods travel through various market places. Significance: Explains supply chains and economic flows, illustrating the journey of products from production to consumption.",
    "SST802": "Describes major crops, types of farming and agricultural practices in her/his own area/state. Significance: Connects students to local agriculture and food systems, fostering understanding of economic geography and sustainability.",
    "SST805": "Locates distribution of important minerals eg coal and mineral oil on the world map. Significance: Enhances geographical knowledge of natural resources and their global distribution, relevant to economics and environmental studies.",
    "SST807": "Justifies judicious use of natural resources. Significance: Promotes environmental stewardship and sustainable resource management, encouraging responsible consumption and conservation.",
    "SST809": "Draws interrelationship between types of farming and development in different regions of the world. Significance: Develops understanding of global economic patterns and the impact of agriculture on regional development.",
    "SST810": "Distinguishes the modern period from the medieval and the ancient periods through the use of sources. Significance: Fosters historical periodization and source analysis skills, crucial for understanding historical change and continuity.",
    "SST815": "Explains the origin, nature and spread of the revolt of 1857 and the lessons learned from it. Significance: Provides historical context on a pivotal event in Indian history, fostering understanding of colonial rule and resistance movements.",
    "SST816": "Analyses the decline of pre-existing urban centers and handicraft industries and the development of new urban centers and industries in India during the colonial period. Significance: Explores the economic and social impact of colonialism, highlighting historical transformations in urban and industrial landscapes.",
    "SST818": "Analyses the issues related to caste, women, widow remarriage, child marriage, social reforms and the laws and policies of colonial administration towards these issues. Significance: Examines social justice issues and historical reform movements, promoting critical awareness of social inequalities and legal frameworks.",
    "SST823": "Applies the knowledge of the Fundamental Rights to find out about their violation, protection and promotion in a given situation. Significance: Empowers students with knowledge of their rights and legal protections, fostering civic engagement and advocacy.",
    "SST827": "Describes the process of making a law (eg Domestic Violence Act, RTI Act, RTE Act). Significance: Educates students on legislative processes and the creation of laws, promoting understanding of legal frameworks and their societal impact.",
    "SST831": "Identifies the role of Government in providing public facilities such as water, sanitation, road, electricity etc, and recognizes their availability. Significance: Promotes understanding of public services and government responsibilities, fostering civic awareness and engagement with local infrastructure.",
    "SST833": "Draws bar diagram to show population of different countries/India/states. Significance: Develops data visualization skills in a geographical context, enabling students to represent and interpret demographic data."
}

def show_learning_outcomes():
    st.markdown("<div class=\"section-header\">🎯 Detailed Learning Outcomes</div>", unsafe_allow_html=True)
    st.markdown("""
    This section provides a detailed breakdown of each learning outcome assessed in the NAS survey, 
    along with its significance in the broader educational context.
    """, unsafe_allow_html=False)

    subject_categories = {
        "L": "Language",
        "M": "Mathematics",
        "SCI": "Science",
        "SST": "Social Science"
    }

    for prefix, subject_name in subject_categories.items():
        st.markdown(f"### {subject_name} Learning Outcomes")
        for lo_code, lo_description in learning_outcomes_data.items():
            if lo_code.startswith(prefix):
                parts = lo_description.split(". Significance: ")
                description = parts[0]
                significance = parts[1] if len(parts) > 1 else "N/A"
                
                st.markdown(f"**{lo_code}:** {description}")
                st.info(f"**Significance:** {significance}")


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
    
    # Extract year from the Year column
    df['Year'] = df['Year'].astype(str).str.extract(r'(\d{4})').astype(int)
    
    # Identify subject-specific columns
    math_cols = [col for col in df.columns if '_In_M' in col]
    science_cols = [col for col in df.columns if '_In_Sci' in col]
    sst_cols = [col for col in df.columns if '_In_Sst' in col]
    language_cols = [col for col in df.columns if '_In_L' in col]
    
    # Calculate subject-wise performance scores
    df['Math_Performance'] = df[math_cols].mean(axis=1)
    df['Science_Performance'] = df[science_cols].mean(axis=1)
    df['SST_Performance'] = df[sst_cols].mean(axis=1)
    df['Language_Performance'] = df[language_cols].mean(axis=1)
    df['Overall_Performance'] = df[['Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance']].mean(axis=1)
    
    return df, math_cols, science_cols, sst_cols, language_cols

# Main application
def main():
    # Title
    st.markdown('<h1 class="main-header">📊 National Achievement Survey (NAS) Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    sections = [
        "🏠 Home & Dataset Overview",
        "🎯 Detailed Learning Outcomes",
        "🔧 Data Preprocessing",
        "📈 Exploratory Data Analysis",
        "📊 Performance Analysis",
        "💡 Key Insights & Recommendations"
    ]
    
    selected_section = st.sidebar.selectbox("Choose a section:", sections)
    
    # Load and preprocess data
    df = load_data()
    df_processed, math_cols, science_cols, sst_cols, language_cols = preprocess_data(df)
    
    # Filter data for 2021 (most recent year)
    df_2021 = df_processed[df_processed['Year'] == 2021].copy()
    
    if selected_section == "🏠 Home & Dataset Overview":
        show_home_and_overview(df, df_processed)
    elif selected_section == "🔧 Data Preprocessing":
        show_preprocessing(df, df_processed, math_cols, science_cols, sst_cols, language_cols)
    elif selected_section == "📈 Exploratory Data Analysis":
        show_eda(df_2021)
    elif selected_section == "📊 Performance Analysis":
        show_performance_analysis(df_2021)
    elif selected_section == "🗺️ District-Level Mapping":
        show_district_mapping(df_2021)
    elif selected_section == "💡 Key Insights & Recommendations":
        show_insights_and_recommendations(df_2021)
    elif selected_section == "🎯 Detailed Learning Outcomes":
        show_learning_outcomes()

def show_home_and_overview(df, df_processed):
    """Display home page and dataset overview"""
    st.markdown('<div class="section-header">🏠 Welcome to NAS Analysis Dashboard</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This interactive dashboard provides comprehensive analysis of the **National Achievement Survey (NAS)** 
    for students across India. Explore learning outcomes, performance trends, and educational insights 
    from one of India's largest educational assessments.
    """, unsafe_allow_html=False)
    
    # Dataset Overview
    st.markdown('<div class="section-header">📋 About the Dataset</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        
        **Data Source:** Ministry of Education, Government of India  
        **Standardized By:** NDAP (National Data & Analytics Platform)  
        **Hosted By:** NDAP  
        
        #### Overview
        The National Achievement Survey (NAS) is a large-scale assessment conducted across India to evaluate 
        the learning outcomes of students in various classes. The District Report for
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
        """, unsafe_allow_html=False)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📅 Year Range", "2017 - 2021")
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
        st.metric("Districts Covered", f"{df['District'].nunique():,}")
    with col3:
        st.metric("States/UTs", f"{df['State'].nunique()}")
    with col4:
        st.metric("Learning Outcomes", f"{len([col for col in df.columns if 'Learning_Outcome' in col])}")
    
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
        """, unsafe_allow_html=False)
    
    with col2:
        st.markdown("""
        #### Impact & Applications  
        - **Policy Development:** Informs educational policy decisions
        - **Teacher Training:** Identifies areas for professional development
        - **Curriculum Enhancement:** Guides curriculum design and improvement
        - **Resource Allocation:** Helps prioritize educational investments
        """, unsafe_allow_html=False)

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
            for col in math_cols[:5]:  # Show first 5
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
    """, unsafe_allow_html=False)
    
    # Show sample calculations
    sample_district = df_processed.iloc[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Sample District Performance:**")
        st.markdown("**District:** {sample_district['District']}, {sample_district['State]}")
        st.metric("Math Performance", f"{sample_district['Math_Performance']:.2f}%")
        st.metric("Science Performance", f"{sample_district['Science_Performance']:.2f}%")
    
    with col2:
        st.markdown("**Calculated Scores:**")
        st.markdown("&nbsp;")  # Spacing
        st.metric("SST Performance", f"{sample_district['SST_Performance']:.2f}%")
        st.metric("Overall Performance", f"{sample_district['Overall_Performance']:.2f}%")
    
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
    display_cols = ['Country', 'State', 'District', 'Year', 'Number_Of_Schools_Surveyed', 
                   'Number_Of_Students_Surveyed', 'Math_Performance', 'Science_Performance', 
                   'SST_Performance', 'Language_Performance', 'Overall_Performance']
    
    st.dataframe(df_processed[display_cols].head(10), use_container_width=True)

def show_eda(df_2021):
    """Display exploratory data analysis"""
    st.markdown('<div class="section-header">📈 Exploratory Data Analysis (2021 Data)</div>', unsafe_allow_html=True)
    
    # National Summary Statistics
    st.markdown("### 📊 National Performance Summary")
    
    performance_cols = ['Overall_Performance', 'Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance']
    summary_stats = df_2021[performance_cols].describe()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Overall Performance", 
                 f"{summary_stats.loc['mean', 'Overall_Performance']:.1f}%",
                 f"±{summary_stats.loc['std', 'Overall_Performance']:.1f}%")
    
    with col2:
        st.metric("Mathematics", 
                 f"{summary_stats.loc['mean', 'Math_Performance']:.1f}%",
                 f"±{summary_stats.loc['std', 'Math_Performance']:.1f}%")
    
    with col3:
        st.metric("Science", 
                 f"{summary_stats.loc['mean', 'Science_Performance']:.1f}%",
                 f"±{summary_stats.loc['std', 'Science_Performance']:.1f}%")
    
    with col4:
        st.metric("Social Science", 
                 f"{summary_stats.loc['mean', 'SST_Performance']:.1f}%",
                 f"±{summary_stats.loc['std', 'SST_Performance']:.1f}%")
    
    with col5:
        st.metric("Language", 
                 f"{summary_stats.loc['mean', 'Language_Performance']:.1f}%",
                 f"±{summary_stats.loc['std', 'Language_Performance']:.1f}%")
    
    # Performance Distribution
    st.markdown("### 📊 Performance Score Distributions")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Overall Performance', 'Mathematics', 'Science', 'Social Science'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Overall Performance
    fig.add_trace(
        go.Histogram(x=df_2021['Overall_Performance'], name='Overall', nbinsx=30, opacity=0.7),
        row=1, col=1
    )
    
    # Mathematics
    fig.add_trace(
        go.Histogram(x=df_2021['Math_Performance'], name='Math', nbinsx=30, opacity=0.7),
        row=1, col=2
    )
    
    # Science
    fig.add_trace(
        go.Histogram(x=df_2021['Science_Performance'], name='Science', nbinsx=30, opacity=0.7),
        row=2, col=1
    )
    
    # Social Science
    fig.add_trace(
        go.Histogram(x=df_2021['SST_Performance'], name='SST', nbinsx=30, opacity=0.7),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Distribution of Performance Scores Across Districts")
    st.plotly_chart(fig, use_container_width=True)
    
    # State-wise Performance Analysis
    st.markdown("### 🏛️ State-wise Performance Rankings")
    
    state_performance = df_2021.groupby('State')[performance_cols].mean().round(2)
    state_performance['Overall_Rank'] = state_performance['Overall_Performance'].rank(ascending=False)
    state_performance = state_performance.sort_values('Overall_Performance', ascending=False)
    
    # Top and Bottom performing states
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🏆 Top 10 Performing States/UTs**")
        top_states = state_performance.head(10)
        
        fig_top = px.bar(
            x=top_states['Overall_Performance'], 
            y=top_states.index,
            orientation='h',
            title="Top 10 States by Overall Performance",
            color=top_states['Overall_Performance'],
            color_continuous_scale='Viridis'
        )
        fig_top.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        st.markdown("**📉 Bottom 10 Performing States/UTs**")
        bottom_states = state_performance.tail(10)
        
        fig_bottom = px.bar(
            x=bottom_states['Overall_Performance'], 
            y=bottom_states.index,
            orientation='h',
            title="Bottom 10 States by Overall Performance",
            color=bottom_states['Overall_Performance'],
            color_continuous_scale='Reds'
        )
        fig_bottom.update_layout(height=400, yaxis={"categoryorder": "total descending"})
        st.plotly_chart(fig_bottom, use_container_width=True)
    
    # Subject-wise State Comparison
    st.markdown("### 📚 Subject-wise State Performance Comparison")
    
    # Select states for comparison
    selected_states = st.multiselect(
        "Select states to compare:",
        options=state_performance.index.tolist(),
        default=state_performance.head(5).index.tolist(),
        max_selections=10
    )
    
    if selected_states:
        comparison_data = state_performance.loc[selected_states, ['Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance']]
        
        fig_comparison = go.Figure()
        
        for subject in comparison_data.columns:
            fig_comparison.add_trace(go.Bar(
                name=subject.replace('_Performance', ''),
                x=comparison_data.index,
                y=comparison_data[subject],
                text=comparison_data[subject].round(1),
                textposition='auto'
            ))
        
        fig_comparison.update_layout(
            title="Subject-wise Performance Comparison",
            xaxis_title="States/UTs",
            yaxis_title="Performance Score (%)",
            barmode='group',
            height=500
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Learning Outcome Analysis
    st.markdown("### 🎯 Most Challenging Learning Outcomes")
    
    learning_outcome_cols = [col for col in df_2021.columns if col.startswith('Average_Performance') and 'Learning_Outcome' in col]
    topic_performance = df_2021[learning_outcome_cols].mean().sort_values(ascending=True)
    
    # Clean up the names for better readability
    topic_performance.index = topic_performance.index.str.replace('Average_Performance_Of_Students_In_', '').str.replace('_Learning_Outcome', '')
    
    hardest_topics = topic_performance.head(15)
    easiest_topics = topic_performance.tail(15)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔴 Most Challenging Topics**")
        fig_hard = px.bar(
            x=hardest_topics.values,
            y=hardest_topics.index,
            orientation='h',
            title="15 Most Difficult Learning Outcomes",
            color=hardest_topics.values,
            color_continuous_scale='Reds'
        )
        fig_hard.update_layout(height=500, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_hard, use_container_width=True)
    
    with col2:
        st.markdown("**🟢 Best Performing Topics**")
        fig_easy = px.bar(
            x=easiest_topics.values,
            y=easiest_topics.index,
            orientation='h',
            title="15 Best Performing Learning Outcomes",
            color=easiest_topics.values,
            color_continuous_scale='Greens')
        fig_easy.update_layout(height=500, yaxis={'categoryorder': 'total descending'})
def show_performance_analysis(df_2021):
    """Display detailed performance analysis"""
    st.markdown('<div class="section-header">📊 Advanced Performance Analysis</div>', unsafe_allow_html=True)
    
    # Performance Correlation Analysis
    st.markdown("### 🔗 Subject Performance Correlations")
    
    performance_cols = ['Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance']
    correlation_matrix = df_2021[performance_cols].corr()
    
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
    st.markdown("### 🏫 Performance vs Survey Scale Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_schools = px.scatter(
            df_2021,
            x='Number_Of_Schools_Surveyed',
            y='Overall_Performance',
            color='Overall_Performance',
            size='Number_Of_Students_Surveyed',
            hover_data=['State', 'District'],
            title="Performance vs Number of Schools Surveyed",
            color_continuous_scale='Viridis'
        )
        fig_schools.update_layout(height=400)
        st.plotly_chart(fig_schools, use_container_width=True)
    
    with col2:
        fig_students = px.scatter(
            df_2021,
            x='Number_Of_Students_Surveyed',
            y='Overall_Performance',
            color='Overall_Performance',
            size='Number_Of_Schools_Surveyed',
            hover_data=['State', 'District'],
            title="Performance vs Number of Students Surveyed",
            color_continuous_scale='Viridis'
        )
        fig_students.update_layout(height=400)
        st.plotly_chart(fig_students, use_container_width=True)
    
    # District Performance Analysis
    st.markdown("### 🏘️ District-Level Performance Analysis")
    
    # Top and bottom performing districts
    district_performance = df_2021.groupby(['State', 'District'])['Overall_Performance'].mean().reset_index()
    district_performance = district_performance.sort_values('Overall_Performance', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🏆 Top 20 Performing Districts**")
        top_districts = district_performance.head(20)
        top_districts['State_District'] = top_districts['District'] + ', ' + top_districts['State']
        
        fig_top_districts = px.bar(
            top_districts,
            x='Overall_Performance',
            y='State_District',
            orientation='h',
            title="Top 20 Districts by Overall Performance",
            color='Overall_Performance',
            color_continuous_scale='Greens'
        )
        fig_top_districts.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_top_districts, use_container_width=True)
    
    with col2:
        st.markdown("**📉 Bottom 20 Performing Districts**")
        bottom_districts = district_performance.tail(20)
        bottom_districts['State_District'] = bottom_districts['District'] + ', ' + bottom_districts['State']
        
        fig_bottom_districts = px.bar(
            bottom_districts,
            x='Overall_Performance',
            y='State_District',
            orientation='h',
            title="Bottom 20 Districts by Overall Performance",
            color='Overall_Performance',
            color_continuous_scale='Reds'
        )
        fig_bottom_districts.update_layout(height=600, yaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_bottom_districts, use_container_width=True)
    
    # Performance Distribution by State
    st.markdown("### 📈 Performance Distribution by State")
    
    selected_state = st.selectbox(
        "Select a state to view district-wise performance distribution:",
        options=sorted(df_2021['State'].unique())
    )
    
    state_data = df_2021[df_2021['State'] == selected_state]
    
    if len(state_data) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_state_dist = px.box(
                state_data,
                y=['Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance'],
                title=f"Subject Performance Distribution in {selected_state}"
            )
            fig_state_dist.update_layout(height=400)
            st.plotly_chart(fig_state_dist, use_container_width=True)
        
        with col2:
            fig_state_districts = px.bar(
                state_data.sort_values('Overall_Performance', ascending=True),
                x='Overall_Performance',
                y='District',
                orientation='h',
                title=f"District Performance in {selected_state}",
                color='Overall_Performance',
                color_continuous_scale='Viridis'
            )
            fig_state_districts.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_state_districts, use_container_width=True)
        
        # State statistics
        st.markdown(f"**📊 {selected_state} Statistics:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Districts", len(state_data))
        with col2:
            st.metric("Avg Performance", f"{state_data["Overall_Performance"].mean():.1f}%")
        with col3:
            st.metric("Best District", f"{state_data.loc[state_data['Overall_Performance'].idxmax(), 'District']}")
        with col4:
            st.metric("Schools Surveyed", f"{state_data['Number_Of_Schools_Surveyed'].sum():,}")

def show_district_mapping(df_2021):
    """Display district-level mapping visualization"""
    st.markdown('<div class="section-header">🗺️ District-Level Performance Mapping</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This section provides geographical visualization of district-level performance across India. 
    Due to the complexity of Indian district boundaries and the need for accurate geospatial data, 
    we present alternative visualizations that effectively show geographical patterns.
    """, unsafe_allow_html=False)
    
    # State-wise heatmap
    st.markdown("### 🌡️ State-wise Performance Heatmap")
    
    # Create state performance matrix
    state_performance = df_2021.groupby('State')[['Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance', 'Overall_Performance']].mean()
    
    fig_heatmap = px.imshow(
        state_performance.T,
        aspect="auto",
        title="State-wise Performance Heatmap",
        color_continuous_scale='RdYlGn',
        labels=dict(x="States/UTs", y="Subjects", color="Performance %")
    )
    fig_heatmap.update_layout(height=400)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Interactive scatter plot with geographical regions
    st.markdown("### 🌍 Regional Performance Analysis")
    
    # Define geographical regions (simplified)
    region_mapping = {
        'North': ['Delhi', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Punjab', 'Rajasthan', 'Uttarakhand', 'Uttar Pradesh', 'Chandigarh', 'Ladakh'],
        'South': ['Andhra Pradesh', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Telangana', 'Puducherry', 'Andaman and Nicobar Islands', 'Lakshadweep'],
        'East': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal'],
        'West': ['Goa', 'Gujarat', 'Maharashtra', 'Dadra and Nagar Haveli and Daman and Diu', 'Nagpur'],
        'Central': ['Chhattisgarh', 'Madhya Pradesh']
    }
    
    # Add region information
    df_2021_with_region = df_2021.copy()
    df_2021_with_region["Region"] = df_2021_with_region["State"].apply(
        lambda x: next((region for region, states in region_mapping.items() if x in states), 'Other')
    )
    df_2021_with_region["Region"] = df_2021_with_region["Region"].astype(str)    
    # Regional performance scatter plot
    fig_regional = px.scatter(
        df_2021_with_region,
        x='Math_Performance',
        y='Science_Performance',
        color='Region',
        size='Overall_Performance',
        hover_data=['State', 'District', 'SST_Performance', 'Language_Performance'],
        title="Regional Performance Distribution (Math vs Science)",
        size_max=20
    )
    fig_regional.update_layout(height=500)
    st.plotly_chart(fig_regional, use_container_width=True)
    
    # District performance by region
    st.markdown("### 📊 Regional Performance Comparison")
    
    regional_stats = df_2021_with_region.groupby('Region')[[
        'Overall_Performance', 'Math_Performance', 'Science_Performance', 
        'SST_Performance', 'Language_Performance'
    ]].agg(['mean', 'std', 'count']).round(2)
    
    # Flatten column names
    regional_stats.columns = [f"{col[1]}_{col[0]}" for col in regional_stats.columns]
    regional_stats = regional_stats.reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_regional_bar = px.bar(
            regional_stats,
            x='Region',
            y='mean_Overall_Performance',
            error_y='std_Overall_Performance',
            title="Average Overall Performance by Region",
            color='mean_Overall_Performance',
            color_continuous_scale='Viridis'
        )
        fig_regional_bar.update_layout(height=400)
        st.plotly_chart(fig_regional_bar, use_container_width=True)
    
    with col2:
        fig_regional_subjects = go.Figure()
        subjects = ['Math_Performance', 'Science_Performance', 'SST_Performance', 'Language_Performance']
        
        for subject in subjects:
            fig_regional_subjects.add_trace(go.Bar(
                name=subject.replace('_Performance', ''),
                x=regional_stats['Region'],
                y=regional_stats[f'mean_{subject}'],
                error_y=dict(type='data', array=regional_stats[f'std_{subject}'])
            ))
        
        fig_regional_subjects.update_layout(
            title="Subject-wise Regional Performance",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig_regional_subjects, use_container_width=True)
    
    # Top districts by region
    st.markdown("### 🏆 Top Performing Districts by Region")
    
    selected_region = st.selectbox(
        "Select a region to view top performing districts:",
        options=sorted(df_2021_with_region['Region'].unique())
    )
    
    if selected_region != 'Other':
        region_data = df_2021_with_region[df_2021_with_region['Region'] == selected_region]
        top_districts_region = region_data.nlargest(10, 'Overall_Performance')
        
        fig_top_region = px.bar(
            top_districts_region,
            x='Overall_Performance',
            y='District',
            orientation='h',
            title=f"Top 10 Districts in {selected_region} Region",
            color='Overall_Performance',
            color_continuous_scale='Greens',
            hover_data=['State']
        )
        fig_top_region.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_top_region, use_container_width=True)
    
    # Performance density map alternative
    st.markdown("### 📍 Performance Density Visualization")
    
    st.markdown("""
    **Note:** For a complete geographical mapping experience with actual district boundaries, 
    you would need to integrate with geospatial libraries like GeoPandas and obtain 
    Indian district shapefiles from sources like:
    
    - **Survey of India** - Official mapping agency
    - **DataMeet** - Open data community with Indian administrative boundaries
    - **Natural Earth** - Public domain map dataset
    
    The current implementation provides comprehensive performance analysis through 
    alternative visualizations that effectively communicate geographical patterns.
    """, unsafe_allow_html=False)
    
    # Create a simple coordinate-based visualization
    # This is a simplified representation - in a real implementation, you'd use actual coordinates
    st.markdown("#### Simulated Geographical Distribution")
    
    # Create mock coordinates for demonstration (in real implementation, use actual lat/long)
    np.random.seed(42)
    df_2021_coords = df_2021.copy()
    df_2021_coords['lat'] = np.random.uniform(8, 37, len(df_2021))  # India's latitude range
    df_2021_coords['lon'] = np.random.uniform(68, 97, len(df_2021))  # India's longitude range
    
    fig_map = px.scatter_mapbox(
        df_2021_coords.sample(100),  # Sample for performance
        lat='lat',
        lon='lon',
        color='Overall_Performance',
        size='Overall_Performance',
        hover_data=['State', 'District'],
        color_continuous_scale='RdYlGn',
        size_max=15,
        zoom=4,
        title="District Performance Distribution (Simulated Coordinates)"
    )
    
    fig_map.update_layout(
        mapbox_style="open-street-map",
        height=500,
        margin={"r":0,"t":30,"l":0,"b":0}
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.info("""
    💡 **Implementation Note:** The above map uses simulated coordinates for demonstration. 
    For production use, integrate with actual district coordinate data and consider using 
    libraries like Folium or Plotly with real geospatial data.
    """, unsafe_allow_html=False)

def show_insights_and_recommendations(df_2021):
    """Display key insights and recommendations"""
    st.markdown('<div class="section-header">💡 Key Insights & Recommendations</div>', unsafe_allow_html=True)
    
    # Calculate key metrics for insights
    overall_mean = df_2021['Overall_Performance'].mean()
    math_mean = df_2021['Math_Performance'].mean()
    science_mean = df_2021['Science_Performance'].mean()
    sst_mean = df_2021['SST_Performance'].mean()
    language_mean = df_2021['Language_Performance'].mean()
    
    state_performance = df_2021.groupby('State')['Overall_Performance'].mean().sort_values(ascending=False)
    top_state = state_performance.index[0]
    bottom_state = state_performance.index[-1]
    
    # Key Insights
    st.markdown("### 🔍 Key Findings")
    
    insights = [
        {
            "title": "📊 Overall Performance Landscape",
            "content": f"""- **National Average:** {overall_mean:.1f}% across all districts
            - **Performance Range:** {df_2021['Overall_Performance'].min():.1f}% to {df_2021['Overall_Performance'].max():.1f}%
            - **Standard Deviation:** {df_2021['Overall_Performance'].std():.1f}% indicating significant variation
            - **Districts Above Average:** {len(df_2021[df_2021['Overall_Performance'] > overall_mean])} out of {len(df_2021)} ({len(df_2021[df_2021['Overall_Performance'] > overall_mean])/len(df_2021)*100:.1f}%)
            """
        },
        {
            "title": "📚 Subject-wise Performance Analysis",
            "content": f"""- **Strongest Subject:** {'Language' if language_mean == max(math_mean, science_mean, sst_mean, language_mean) else 'Mathematics' if math_mean == max(math_mean, science_mean, sst_mean, language_mean) else 'Science' if science_mean == max(math_mean, science_mean, sst_mean, language_mean) else 'Social Science'} ({max(math_mean, science_mean, sst_mean, language_mean):.1f}%)
            - **Most Challenging Subject:** {'Language' if language_mean == min(math_mean, science_mean, sst_mean, language_mean) else 'Mathematics' if math_mean == min(math_mean, science_mean, sst_mean, language_mean) else 'Science' if science_mean == min(math_mean, science_mean, sst_mean, language_mean) else 'Social Science'} ({min(math_mean, science_mean, sst_mean, language_mean):.1f}%)
            - **Subject Performance Gap:** {max(math_mean, science_mean, sst_mean, language_mean) - min(math_mean, science_mean, sst_mean, language_mean):.1f} percentage points
            - **Mathematics Performance:** {math_mean:.1f}% (Critical for STEM education)
            """
        },
        {
            "title": "🏛️ Regional Disparities",
            "content": f"""- **Top Performing State/UT:** {top_state} ({state_performance.iloc[0]:.1f}%)
            - **Lowest Performing State/UT:** {bottom_state} ({state_performance.iloc[-1]:.1f}%)
            - **Performance Gap:** {state_performance.iloc[0] - state_performance.iloc[-1]:.1f} percentage points
            - **States Above National Average:** {len(state_performance[state_performance > overall_mean])} out of {len(state_performance)}
            """
        }
    ]
    
    for insight in insights:
        with st.expander(insight["title"]):
            st.markdown(insight["content"])
    
    # Critical Areas Needing Attention
    st.markdown("### ⚠️ Critical Areas Needing Attention")
    
    # Find districts with very low performance
    low_performing_districts = df_2021[df_2021['Overall_Performance'] < (overall_mean - df_2021['Overall_Performance'].std())]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔴 Districts Requiring Immediate Intervention**")
        st.markdown(f"**Count:** {len(low_performing_districts)} districts")
        st.markdown(f"**Criteria:** Performance below {(overall_mean - df_2021['Overall_Performance'].std()):.1f}%")
        
        if len(low_performing_districts) > 0:
            worst_districts = low_performing_districts.nsmallest(10, 'Overall_Performance')[[
                'State', 'District', 'Overall_Performance'
            ]]
            st.dataframe(worst_districts, use_container_width=True)
    
    with col2:
        st.markdown("**📈 High-Performing Districts (Best Practices)**")
        high_performing_districts = df_2021[df_2021['Overall_Performance'] > (overall_mean + df_2021['Overall_Performance'].std())]
        st.markdown(f"**Count:** {len(high_performing_districts)} districts")
        st.markdown(f"**Criteria:** Performance above {(overall_mean + df_2021['Overall_Performance'].std()):.1f}%")
        
        if len(high_performing_districts) > 0:
            best_districts = high_performing_districts.nlargest(10, 'Overall_Performance')[[
                'State', 'District', 'Overall_Performance'
            ]]
            st.dataframe(best_districts, use_container_width=True)
    
    # Recommendations
    st.markdown("### 🎯 Strategic Recommendations")
    
    recommendations = [
        {
            "category": "🏫 Educational Infrastructure",
            "recommendations": [
                "Prioritize resource allocation to districts performing below 30% in overall assessment",
                "Establish teacher training centers in underperforming regions",
                "Implement technology-enabled learning solutions in remote areas",
                "Create district-wise mentorship programs pairing high and low-performing schools"
            ]
        },
        {
            "category": "📚 Curriculum & Pedagogy",
            "recommendations": [
                f"Focus on {'Mathematics' if math_mean < 35 else 'Science' if science_mean < 35 else 'Social Science'} curriculum enhancement as it shows lowest national average",
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
                "Launch targeted intervention programs for bottom 20% performing districts",
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
    st.markdown("### 🌟 Success Stories & Best Practices")
    
    # Find states with consistent high performance
    consistent_performers = state_performance.head(5)
    
    st.markdown("**States/UTs Leading in Educational Excellence:**")
    
    for i, (state, performance) in enumerate(consistent_performers.items(), 1):
        state_data = df_2021[df_2021['State'] == state]
        avg_schools = state_data['Number_Of_Schools_Surveyed'].mean()
        avg_students = state_data['Number_Of_Students_Surveyed'].mean()
        
        st.markdown(f"""**{i}. {state}** - {performance:.1f}% Overall Performance
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
            csv = state_performance.to_csv()
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="state_performance_summary.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Download District Analysis"):
            district_summary = df_2021[[
                'State', 'District', 'Overall_Performance', 'Math_Performance', 
                'Science_Performance', 'SST_Performance', 'Language_Performance'
            ]]
            csv = district_summary.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="district_performance_analysis.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("🎯 Download Recommendations Report"):
            report_content = f"""National Achievement Survey (NAS) Analysis Report
            Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            EXECUTIVE SUMMARY:
            - National Average Performance: {overall_mean:.1f}%
            - Total Districts Analyzed: {len(df_2021)}
            - Performance Range: {df_2021['Overall_Performance'].min():.1f}% - {df_2021['Overall_Performance'].max():.1f}%
            
            TOP PERFORMING STATES:
            {chr(10).join([f"{i+1}. {state}: {perf:.1f}%" for i, (state, perf) in enumerate(state_performance.head(5).items())])}
            
            CRITICAL INTERVENTION REQUIRED:
            {len(low_performing_districts)} districts performing below {(overall_mean - df_2021['Overall_Performance'].std()):.1f}%
            
            For detailed analysis and recommendations, refer to the full dashboard.
            """
            
            st.download_button(
                label="Download Report",
                data=report_content,
                file_name="nas_analysis_report.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()

