# visualizations.py
"""
Visualization module for Advanced Data Analyst Project

Dependencies:
- pandas
- matplotlib
- seaborn
- plotly.express

This script creates advanced charts from processed data to showcase insights.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set style for seaborn
sns.set(style="whitegrid")

def load_data(filepath):
    """
    Load the cleaned and processed CSV data into a DataFrame.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Loaded data.
    """
    df = pd.read_csv(filepath)
    return df

def plot_time_series(df, date_col, value_col, title, output_file):
    """
    Plot a time series line chart.
    
    Args:
        df (pd.DataFrame): Data containing date and value columns.
        date_col (str): Name of date column.
        value_col (str): Name of value column.
        title (str): Chart title.
        output_file (str): Path to save PNG file.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df[date_col], df[value_col], marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel(date_col)
    plt.ylabel(value_col)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def plot_correlation_heatmap(df, output_file):
    """
    Plot a correlation heatmap of numerical columns.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        output_file (str): Path to save PNG file.
    """
    plt.figure(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def plot_interactive_scatter(df, x_col, y_col, color_col, title, output_html):
    """
    Create an interactive scatter plot with Plotly.
    
    Args:
        df (pd.DataFrame): DataFrame with data.
        x_col (str): Column name for x-axis.
        y_col (str): Column name for y-axis.
        color_col (str): Column name for color grouping.
        title (str): Plot title.
        output_html (str): Path to save HTML interactive plot.
    """
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=title,
                     hover_data=[x_col, y_col, color_col])
    fig.write_html(output_html)

def main():
    # Example usage:
    data_file = 'processed_data.csv'  # Adjust to your processed data file path
    
    # Load data
    df = load_data(data_file)
    
    # Plot time series: example columns - 'date' and 'sales'
    plot_time_series(df, 'date', 'sales', 'Sales Over Time', 'outputs/sales_time_series.png')
    
    # Plot correlation heatmap
    plot_correlation_heatmap(df, 'outputs/correlation_heatmap.png')
    
    # Interactive scatter: example columns - 'feature1', 'feature2', 'category'
    plot_interactive_scatter(df, 'feature1', 'feature2', 'category',
                             'Feature1 vs Feature2 by Category', 'outputs/scatter_plot.html')

if __name__ == '__main__':
    main()

