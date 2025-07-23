-----

# 📊 National Achievement Survey (NAS) Dashboard

[](https://www.python.org/downloads/)
[](https://streamlit.io/)
[](https://opensource.org/licenses/MIT)

An interactive and insightful dashboard for analyzing the National Achievement Survey learning outcomes. This tool provides a comprehensive exploration of student performance across various subjects, states, and districts in India, offering data-driven insights for educators, policymakers, and researchers.

🔗 **Live Deployed Project:** [https://shreyas-national-achievement-survey.streamlit.app](https://shreyas-national-achievement-survey.streamlit.app/)

## ✨ Key Features

  * **🏠 Home & Overview:** Get a high-level summary of the dataset, its source, methodology, and key statistics.
  * **🔧 Data Preprocessing:** Understand the steps taken to clean and prepare the raw data for analysis, including column standardization and feature engineering.
  * **📈 Exploratory Data Analysis (EDA):** Visualize national performance summaries, score distributions, and state-wise rankings with interactive charts.
  * **📊 Performance Analysis:** Dive deep into subject correlations, performance vs. survey scale, and detailed district-level comparisons.
  * **🗺️ Geographical Insights:** Analyze regional performance patterns through heatmaps, scatter plots, and simulated geographical maps.
  * **💡 Insights & Recommendations:** Access auto-generated key findings, critical areas for intervention, and strategic recommendations for educational improvement.
  * **🎯 Learning Outcomes:** Explore a detailed breakdown of every learning outcome assessed in the survey, along with its educational significance.
  * **📥 Data Export:** Download processed data summaries (state-wise, district-wise) and a generated recommendations report in CSV or TXT format.

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

  * Python 3.9 or higher
  * `pip` package manager

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/nas-dashboard.git
    cd nas-dashboard
    ```

2.  **Create and activate a virtual environment (recommended):**

    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Dataset

1.  This application requires the `National_Achievement_Survey_dataset.csv` file.
2.  Create a folder named `Dataset` in the root directory of the project.
3.  Place the `National_Achievement_Survey_dataset.csv` file inside the `Dataset` folder.

The final file structure should look like this:

```
nas-dashboard/
├── Dataset/
│   └── National_Achievement_Survey_dataset.csv
├── app.py
├── requirements.txt
└── README.md
```

### Running the Application

Once the setup is complete, run the following command in your terminal:

```bash
streamlit run app.py
```

Your web browser will open a new tab with the running Streamlit dashboard.

## 🛠️ Technologies Used

  * **Core Framework:** [Streamlit](https://streamlit.io/)
  * **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
  * **Data Visualization:** [Plotly](https://plotly.com/python/), [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/)

## 📄 Code Structure

The main application logic is contained within `app.py`. The code is organized into modular functions for clarity and maintainability:

  * `main()`: The entry point of the application, handling page navigation and flow control.
  * `load_data()`: Loads the dataset from the CSV file and includes Streamlit's caching for performance.
  * `preprocess_data()`: Cleans column names, extracts features, and calculates aggregate performance scores.
  * `show_*()` functions (e.g., `show_home_and_overview`, `show_eda`): Each function is responsible for rendering a specific section/page of the dashboard.

## 🤝 Contributing

Contributions are welcome\! If you have suggestions for improvements or want to add new features, please follow these steps:

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📜 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

-----
