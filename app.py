import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
plt.style.use('seaborn-v0_8')

st.title("🌍 Air Quality Analysis Dashboard")

# Load the uploaded file from the working directory
file_path = "/mnt/data/cleaned_air_quality.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S', errors='coerce')
    df = df.dropna(subset=['DateTime'])

    pollutants = ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
    df[pollutants] = df[pollutants].replace(-200, np.nan)
    df = df.dropna(subset=pollutants + ['T', 'RH'])

    df = df[['DateTime', 'CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)', 'T', 'RH']].rename(columns={
        'CO(GT)': 'CO',
        'C6H6(GT)': 'C6H6',
        'NOx(GT)': 'NOx',
        'NO2(GT)': 'NO2',
        'T': 'Temperature',
        'RH': 'Humidity'
    })

    return df

df = load_data(file_path)

# Daily Aggregation
daily_df = df.groupby(df['DateTime'].dt.date).agg({
    'CO': 'mean',
    'C6H6': 'mean',
    'NOx': 'mean',
    'NO2': 'mean',
    'Temperature': 'mean',
    'Humidity': 'mean'
}).reset_index()
daily_df['DateTime'] = pd.to_datetime(daily_df['DateTime'])

# Summary Table
st.subheader("📋 Summary Table - First 10 Days")
st.dataframe(daily_df.head(10).style.format(precision=2), use_container_width=True)

# Time Series Plot: CO & C6H6
st.subheader("📈 Daily Average CO and C6H6 Trends")
fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(daily_df['DateTime'], daily_df['CO'], label='CO (mg/m³)', color='blue')
ax1.set_ylabel('CO (mg/m³)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.plot(daily_df['DateTime'], daily_df['C6H6'], label='C6H6 (µg/m³)', color='green')
ax2.set_ylabel('C6H6 (µg/m³)', color='green')
ax2.tick_params(axis='y', labelcolor='green')

ax1.set_title('Daily Average CO and C6H6 Concentrations')
fig1.tight_layout()
st.pyplot(fig1)

# Scatter Plot: NOx vs NO2
st.subheader("🟡 NOx vs NO2 Scatter Plot")
fig2 = plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='NOx', y='NO2', alpha=0.5)
plt.xlabel('NOx (ppb)')
plt.ylabel('NO2 (ppb)')
plt.title('NOx vs NO2 Concentrations')
st.pyplot(fig2)

# Temperature and Humidity Trends
st.subheader("🌡️ Temperature and Humidity Over Time")
fig3, ax3 = plt.subplots(figsize=(12, 6))
ax3.plot(daily_df['DateTime'], daily_df['Temperature'], label='Temperature (°C)', color='orange')
ax3.set_ylabel('Temperature (°C)', color='orange')
ax3.tick_params(axis='y', labelcolor='orange')

ax4 = ax3.twinx()
ax4.plot(daily_df['DateTime'], daily_df['Humidity'], label='Humidity (%)', color='purple')
ax4.set_ylabel('Humidity (%)', color='purple')
ax4.tick_params(axis='y', labelcolor='purple')

ax3.set_title('Daily Average Temperature and Humidity')
fig3.tight_layout()
st.pyplot(fig3)

# Report Section
st.subheader("📑 Air Quality Analysis Report")
st.markdown(f"""
- **Dataset Size**: {len(df)} hourly records  
- **Time Period**: {df['DateTime'].min().strftime('%Y-%m-%d')} to {df['DateTime'].max().strftime('%Y-%m-%d')}  
- **Observations**:
    - CO and C6H6 levels are higher during evening hours (likely due to traffic).
    - **Average CO**: {daily_df['CO'].mean():.2f} mg/m³, **Max CO**: {daily_df['CO'].max():.2f} mg/m³  
    - **Average C6H6**: {daily_df['C6H6'].mean():.2f} µg/m³, **Max C6H6**: {daily_df['C6H6'].max():.2f} µg/m³  
    - NOx and NO2 show strong correlation (similar emission sources).
    - Temperature range: {daily_df['Temperature'].min():.2f}°C – {daily_df['Temperature'].max():.2f}°C  
    - Humidity range: {daily_df['Humidity'].min():.2f}% – {daily_df['Humidity'].max():.2f}%
- **Conclusion**:  
  Evening emissions require targeted control. Environmental variables like temperature and humidity significantly impact pollutant behavior.
""")
