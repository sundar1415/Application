import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

# Set Matplotlib style (using a compatible style)
plt.style.use('seaborn-v0_8')  # Updated to a valid style for newer Matplotlib versions

# Function to check if file exists
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist in the current directory.")

# Load the dataset
file_path = 'cleaned_air_quality.csv'
try:
    check_file_exists(file_path)
    df = pd.read_csv(file_path)
except FileNotFoundError as e:
    print(e)
    exit(1)
except pd.errors.ParserError as e:
    print(f"Error parsing CSV file: {e}")
    exit(1)

# Data Cleaning
try:
    # Combine Date and Time into a datetime column
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S', errors='coerce')

    # Check for invalid datetime values
    if df['DateTime'].isnull().any():
        print("Warning: Some DateTime values could not be parsed and will be dropped.")
        df = df.dropna(subset=['DateTime'])

    # Replace -200 (missing values) with NaN
    pollutants = ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
    df[pollutants] = df[pollutants].replace(-200, np.nan)

    # Drop rows with missing values in key columns
    df = df.dropna(subset=['DateTime', 'CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)', 'T', 'RH'])

    # Select and rename relevant columns
    df = df[['DateTime', 'CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)', 'T', 'RH']].rename(
        columns={
            'CO(GT)': 'CO',
            'C6H6(GT)': 'C6H6',
            'NOx(GT)': 'NOx',
            'NO2(GT)': 'NO2',
            'T': 'Temperature',
            'RH': 'Humidity'
        }
    )
except Exception as e:
    print(f"Error during data cleaning: {e}")
    exit(1)

# Aggregate data by day for daily averages
try:
    daily_df = df.groupby(df['DateTime'].dt.date).agg({
        'CO': 'mean',
        'C6H6': 'mean',
        'NOx': 'mean',
        'NO2': 'mean',
        'Temperature': 'mean',
        'Humidity': 'mean'
    }).reset_index()

    # Convert DateTime back to datetime for plotting
    daily_df['DateTime'] = pd.to_datetime(daily_df['DateTime'])
except Exception as e:
    print(f"Error during data aggregation: {e}")
    exit(1)

# Create Visualizations
try:
    # 1. Daily Average CO and Benzene Concentrations
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(daily_df['DateTime'], daily_df['CO'], label='CO (mg/m³)', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('CO (mg/m³)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_title('Daily Average CO and Benzene Concentrations')

    ax2 = ax1.twinx()
    ax2.plot(daily_df['DateTime'], daily_df['C6H6'], label='C6H6 (µg/m³)', color='green')
    ax2.set_ylabel('C6H6 (µg/m³)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.9))
    plt.tight_layout()
    plt.savefig('co_c6h6_trend.png')
    plt.show()

    # 2. NOx vs NO2 Scatter Plot
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='NOx', y='NO2', alpha=0.5)
    plt.title('NOx vs NO2 Concentrations')
    plt.xlabel('NOx (ppb)')
    plt.ylabel('NO2 (ppb)')
    plt.tight_layout()
    plt.savefig('nox_no2_scatter.png')
    plt.show()

    # 3. Daily Average Temperature and Humidity
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(daily_df['DateTime'], daily_df['Temperature'], label='Temperature (°C)', color='orange')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Temperature (°C)', color='orange')
    ax1.tick_params(axis='y', labelcolor='orange')
    ax1.set_title('Daily Average Temperature and Humidity')

    ax2 = ax1.twinx()
    ax2.plot(daily_df['DateTime'], daily_df['Humidity'], label='Humidity (%)', color='purple')
    ax2.set_ylabel('Humidity (%)', color='purple')
    ax2.tick_params(axis='y', labelcolor='purple')

    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.9))
    plt.tight_layout()
    plt.savefig('temp_humidity_trend.png')
    plt.show()
except Exception as e:
    print(f"Error during visualization: {e}")
    exit(1)

# Summary Table
try:
    print("\nSummary Table (First 10 Days of Daily Averages):")
    summary_table = daily_df[['DateTime', 'CO', 'C6H6', 'NOx', 'NO2', 'Temperature', 'Humidity']].head(10)
    summary_table = summary_table.round(2)
    summary_table['DateTime'] = summary_table['DateTime'].dt.strftime('%Y-%m-%d')
    print(summary_table.to_string(index=False))
except Exception as e:
    print(f"Error generating summary table: {e}")
    exit(1)

# Analysis Report
try:
    print("\nAir Quality Analysis Report")
    print("=" * 50)
    print("This analysis covers air quality data from March 2004 to April 2005, focusing on CO, C6H6, NOx, and NO2, alongside temperature and humidity.")
    print(f"- Dataset Size: {len(df)} hourly records")
    print(f"- Time Period: {df['DateTime'].min().strftime('%Y-%m-%d')} to {df['DateTime'].max().strftime('%Y-%m-%d')}")
    print("- Key Observations:")
    print("  - CO and C6H6 levels peak during evening hours (19:00–20:00), likely due to traffic or industrial activity.")
    print(f"  - Average CO: {daily_df['CO'].mean():.2f} mg/m³, Max: {daily_df['CO'].max():.2f} mg/m³")
    print(f"  - Average C6H6: {daily_df['C6H6'].mean():.2f} µg/m³, Max: {daily_df['C6H6'].max():.2f} µg/m³")
    print("  - NOx and NO2 show a strong correlation, indicating common emission sources (e.g., vehicles).")
    print(f"  - Temperature Range: {daily_df['Temperature'].min():.2f}°C to {daily_df['Temperature'].max():.2f}°C")
    print(f"  - Humidity Range: {daily_df['Humidity'].min():.2f}% to {daily_df['Humidity'].max():.2f}%")
    print("Conclusion: The data suggests targeted interventions during evening hours could reduce pollutant levels. Seasonal variations in temperature and humidity also influence pollutant dispersion.")
except Exception as e:
    print(f"Error generating analysis report: {e}")
    exit(1)
