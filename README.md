# National Achievement Survey (NAS) Analysis Dashboard

A comprehensive Streamlit web application for analyzing the National Achievement Survey (NAS) dataset for Class 8 students across India. This dashboard provides detailed insights into learning outcomes, performance trends, and educational patterns from one of India's largest educational assessments.

## 🌟 Features

- **📋 Dataset Overview**: Comprehensive information about the NAS dataset, methodology, and collection process
- **🔧 Data Preprocessing**: Detailed view of data cleaning and transformation steps
- **📈 Exploratory Data Analysis**: Interactive visualizations of performance distributions and trends
- **📊 Performance Analysis**: Advanced analytics including correlations, regional comparisons, and district rankings
- **🗺️ District-Level Mapping**: Geographical visualization of performance patterns across India
- **💡 Insights & Recommendations**: Data-driven insights and strategic recommendations for educational improvement

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone this repository:
```bash
git clone <your-repository-url>
cd nas-analysis-dashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Ensure the dataset file `DATASETDATASCIENCE.csv` is in the same directory as the app

4. Run the Streamlit app:
```bash
streamlit run nas_streamlit_app.py
```

5. Open your browser and navigate to `http://localhost:8501`

## 📊 Dataset Information

**Source**: Ministry of Education, Government of India  
**Standardized By**: NDAP (National Data & Analytics Platform)  
**Coverage**: District-level data across all Indian states and UTs  
**Time Period**: 2017-2021  
**Subjects**: Mathematics, Science, Social Science, Language  

### Key Metrics Analyzed

- Overall performance scores across districts
- Subject-wise learning outcome assessments
- State and regional performance comparisons
- School and student survey statistics
- Competency-based evaluation results

## 🏗️ Application Structure

### Navigation Sections

1. **🏠 Home & Dataset Overview**
   - Dataset description and methodology
   - Key statistics and sample data preview
   - Data collection framework

2. **🔧 Data Preprocessing**
   - Column standardization process
   - Year extraction methodology
   - Subject classification and performance calculation
   - Data quality assessment

3. **📈 Exploratory Data Analysis**
   - National performance summaries
   - Distribution analysis across subjects
   - State-wise performance rankings
   - Learning outcome difficulty analysis

4. **📊 Performance Analysis**
   - Subject correlation analysis
   - Performance vs survey scale relationships
   - District-level performance rankings
   - State-specific distribution analysis

5. **🗺️ District-Level Mapping**
   - Regional performance heatmaps
   - Geographical pattern analysis
   - Interactive performance mapping
   - Regional comparison visualizations

6. **💡 Key Insights & Recommendations**
   - Critical findings and trends
   - Areas requiring intervention
   - Strategic recommendations
   - Success stories and best practices

## 📈 Key Insights

- **National Average**: Comprehensive performance metrics across all districts
- **Regional Disparities**: Significant variations in educational outcomes
- **Subject Performance**: Mathematics and Science showing specific patterns
- **Intervention Areas**: Districts requiring immediate educational support

## 🛠️ Technical Details

### Libraries Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib**: Static plotting
- **Seaborn**: Statistical visualization
- **Plotly**: Interactive visualizations

### Data Processing Pipeline

1. **Column Cleaning**: Standardization of column names
2. **Year Extraction**: Converting year strings to integers
3. **Subject Classification**: Grouping learning outcomes by subject
4. **Performance Calculation**: Computing aggregated scores
5. **Regional Mapping**: Adding geographical context

## 🎯 Use Cases

- **Educational Policy Making**: Data-driven policy decisions
- **Resource Allocation**: Identifying priority areas for investment
- **Performance Monitoring**: Tracking educational progress over time
- **Research & Analysis**: Academic research on educational outcomes
- **Stakeholder Reporting**: Comprehensive performance dashboards

## 📝 Deployment

### Local Development
```bash
streamlit run nas_streamlit_app.py
```

### Cloud Deployment

The application can be deployed on various platforms:

- **Streamlit Cloud**: Direct deployment from GitHub
- **Heroku**: Using Procfile and requirements.txt
- **AWS/GCP**: Container-based deployment
- **Railway/Render**: Modern deployment platforms

### Environment Variables

No additional environment variables required for basic functionality.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ministry of Education, Government of India** for providing the NAS dataset
- **NDAP** for data standardization and hosting
- **Streamlit Community** for the excellent framework
- **Open Source Contributors** for visualization libraries

## 📞 Support

For questions, issues, or suggestions:

- Create an issue on GitHub
- Contact the development team
- Check the documentation for troubleshooting

---

**Note**: This dashboard is designed for educational and research purposes. Please ensure compliance with data usage policies and regulations when using this application.

