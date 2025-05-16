# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
st.title("🌍 Air Quality Analysis Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_air_quality.csv")

    # Combine Date and Time into DateTime column
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S', errors='coerce')
    df = df.dropna(subset=['DateTime'])

    # Replace -200 with NaN for air pollutant columns
    pollutants = ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
    df[pollutants] = df[pollutants].replace(-200, np.nan)

    # Drop rows with missing critical values
    df.dropna(subset=pollutants + ['T', 'RH'], inplace=True)

    return df

df = load_data()

# Sidebar filters
st.sidebar.header("📊 Filters")
start_date = st.sidebar.date_input("From Date", df['DateTime'].min().date())
end_date = st.sidebar.date_input("To Date", df['DateTime'].max().date())

filtered_df = df[(df['DateTime'].dt.date >= start_date) & (df['DateTime'].dt.date <= end_date)]

# Line plot for pollutant levels
st.subheader("📈 Air Pollutants Over Time")
selected_pollutants = st.multiselect("Choose pollutants to visualize", ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)'], default=['CO(GT)'])

if selected_pollutants:
    for pollutant in selected_pollutants:
        st.line_chart(filtered_df.set_index('DateTime')[pollutant])

# Correlation heatmap
st.subheader("📌 Correlation Between Variables")
numeric_cols = ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)', 'T', 'RH']
corr = filtered_df[numeric_cols].corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Raw data preview
st.subheader("📄 Raw Data Preview")
st.dataframe(filtered_df.head())
