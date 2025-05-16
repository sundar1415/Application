# Predict Air Quality Levels Using Advanced Machine Learning Algorithms For Environmental Insights

> A machine learning project to predict air pollutant concentrations based on environmental factors using regression algorithms for actionable environmental insights.

## 📌 Project Overview

Air pollution poses significant threats to human health, particularly affecting respiratory and cardiovascular systems. This project aims to **predict air pollutant levels**—such as CO, C6H6, NOx, and NO2—using environmental factors like **temperature** and **humidity**. The results help identify pollution trends and inform proactive environmental planning.

## 🎯 Objectives

* Predict pollutant levels using regression models.
* Analyze how environmental features (temperature, humidity) influence air quality.
* Identify peak pollution periods.
* Enhance model accuracy with feature engineering and evaluation.
* Visualize trends and extract actionable insights.

## 🧩 Dataset

* **Source:** [Kaggle - Air Quality Dataset](https://www.kaggle.com/)
* **Type:** Time-series, structured data
* **Size:** \~9,000 hourly measurements (2004–2005)
* **Features:** Date, Time, CO(GT), C6H6(GT), NOx(GT), NO2(GT), Temperature (T), Relative Humidity (RH)
* **Targets:** CO, C6H6, NOx, NO2

## 🛠️ Data Preprocessing

* Combined Date and Time into a unified DateTime column.
* Replaced invalid values (e.g., `-200`) with `NaN` and dropped them.
* Selected and renamed relevant columns.
* Aggregated data to daily averages.
* Ensured consistent formatting and data types.

## 📊 Exploratory Data Analysis (EDA)

* **Univariate:** Histograms, time-series plots for pollutants.
* **Bivariate:** Correlation between NOx and NO2, pollutant trends vs. time.
* **Key Insights:**

  * Peak pollution during evenings (likely traffic-related).
  * Strong NOx–NO2 correlation.
  * Seasonal trends observed.
  
## 🧠 Feature Engineering

* Extracted day, month, hour from DateTime.
* Aggregated to daily means.
* Standardized features.
* Derived optional interaction terms (e.g., pollutant ratios).

## 🤖 Model Building

* **Problem Type:** Regression
* **Algorithms Used:**

  * Linear Regression
  * Random Forest Regressor
* **Train/Test Split:** 80/20
* **Metrics:**

  * MAE (Mean Absolute Error)
  * RMSE (Root Mean Squared Error)
  * R² Score

> Random Forest performed well on structured, non-linear datasets.

## 📈 Results and visualization

* Time-series plots of pollutants.
* NOx vs NO2 scatter plot shows linear dependency.
* Temperature vs Humidity dual-axis visualization.
* Summary table of pollutant levels for initial days.
* Feature importance: Temperature and humidity heavily influence CO and C6H6.
  

## 🧰 Tools & Technologies

* **Language:** Python
* **IDE:** Google Colab
* **Libraries:**

  * `pandas`, `numpy` – Data processing
  * `matplotlib`, `seaborn` – Visualization
  * `sklearn` – ML models and metrics
* **Visualization:** Static plots via `matplotlib`, saved using `plt.savefig()`

## 👥 Team Members

| Name                 | Contribution              |
| -------------------- | ------------------------- |
| Meenakshi Sundaram R | EDA, Model Development    |
| Paranthaman R        | Data Cleaning             |
| GopiKrishnan J       | Feature Engineering       |
| Nanthitha K          | Documentation & Reporting |

## college name: Sri Ramanujar Engineering College

## 🔗 GitHub Repository

[https://github.com/sundar1415/project.git](https://github.com/sundar1415/project.git)

---

Would you like me to format this into a downloadable `.md` file or assist in pushing it to your GitHub repository?
