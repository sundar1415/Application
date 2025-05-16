import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
st.title("🌍 Air Quality Analysis Dashboard")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("cleaned_air_quality.csv")

        # Combine Date and Time
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S', errors='coerce')
        df = df.dropna(subset=['DateTime'])

        # Replace -200 with NaN for pollutants
        pollutants = ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
        df[pollutants] = df[pollutants].replace(-200, np.nan)
        df = df.dropna(subset=pollutants + ['T', 'RH'])

        # Rename for clarity
        df = df[['DateTime', 'CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)', 'T', 'RH']]
        df.columns = ['DateTime', 'CO', 'C6H6', 'NOx', 'NO2', 'Temperature', 'Humidity']

        return df
    except Exception as e:
        st.error(f"❌ Error loading the dataset: {e}")
        return pd.DataFrame()

# Load the cleaned dataset
df = load_data()

if not df.empty:
    st.success("✅ Data loaded successfully!")

    # Daily aggregation
    daily_df = df.groupby(df['DateTime'].dt.date).mean(numeric_only=True).reset_index()
    daily_df['DateTime'] = pd.to_datetime(daily_df['DateTime'])

    # CO and Benzene
    st.subheader("📊 CO and C6H6 over Time")
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(daily_df['DateTime'], daily_df['CO'], label='CO (mg/m³)', color='blue')
    ax1.set_ylabel('CO', color='blue')
    ax2 = ax1.twinx()
    ax2.plot(daily_df['DateTime'], daily_df['C6H6'], label='C6H6 (µg/m³)', color='green')
    ax2.set_ylabel('C6H6', color='green')
    ax1.set_xlabel("Date")
    ax1.set_title("CO and Benzene (C6H6) Levels")
    st.pyplot(fig1)

    # NOx vs NO2
    st.subheader("📈 NOx vs NO2 Scatter")
    fig2, ax = plt.subplots(figsize=(6, 5))
    sns.scatterplot(data=df, x='NOx', y='NO2', ax=ax, alpha=0.6)
    ax.set_title("NOx vs NO2")
    st.pyplot(fig2)

    # Temperature and Humidity
    st.subheader("🌡️ Daily Temperature and Humidity")
    fig3, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(daily_df['DateTime'], daily_df['Temperature'], color='orange', label='Temperature')
    ax2 = ax1.twinx()
    ax2.plot(daily_df['DateTime'], daily_df['Humidity'], color='purple', label='Humidity')
    ax1.set_title("Temperature & Humidity Over Time")
    st.pyplot(fig3)

    # Data preview
    st.subheader("🧾 First Few Rows of Data")
    st.dataframe(df.head())

else:
    st.warning("⚠️ Please make sure 'cleaned_air_quality.csv' is present in the working directory.")
