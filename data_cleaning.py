import pandas as pd
import numpy as np

def load_raw_data(filepath):
    """
    Load raw data from CSV file.
    In a real project, you could connect directly to a database
    and pull data, but for this project, CSVs simulate that.
    """
    df = pd.read_csv(filepath)
    print(f"Loaded raw data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def clean_data(df):
    """
    Clean and preprocess raw data:
    - Handle missing values
    - Convert data types
    - Create any new features if needed
    """
    
    # Example: Fill missing values for numeric columns with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        median_val = df[col].median()
        df[col].fillna(median_val, inplace=True)
        print(f"Filled missing values in numeric column '{col}' with median: {median_val}")
    
    # Example: Fill missing categorical columns with 'Unknown'
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col].fillna('Unknown', inplace=True)
        print(f"Filled missing values in categorical column '{col}' with 'Unknown'")
    
    # Example: Convert date columns (if any)
    # Assuming you have a column named 'transaction_date' in the data
    if 'transaction_date' in df.columns:
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
        # Fill missing dates with a default or drop rows
        df['transaction_date'].fillna(pd.Timestamp('2000-01-01'), inplace=True)
        print("Converted 'transaction_date' to datetime and filled missing with 2000-01-01")
    
    # Example: Create new feature 'year' extracted from transaction_date if exists
    if 'transaction_date' in df.columns:
        df['year'] = df['transaction_date'].dt.year
        print("Created new feature 'year' from 'transaction_date'")
    
    # Additional cleaning steps can go here as needed
    
    return df

def save_clean_data(df, output_filepath):
    """
    Save cleaned data to CSV for later use in visualization or modeling.
    """
    df.to_csv(output_filepath, index=False)
    print(f"Cleaned data saved to {output_filepath}")

if __name__ == "__main__":
    # Load your raw data file (update path as needed)
    raw_data_path = 'data/raw_data.csv'
    cleaned_data_path = 'data/cleaned_data.csv'

    raw_df = load_raw_data(raw_data_path)
    cleaned_df = clean_data(raw_df)
    save_clean_data(cleaned_df, cleaned_data_path)

