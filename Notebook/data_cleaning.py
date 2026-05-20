import pandas as pd
import numpy as np

def run_real_estate_cleaning():
    print("Step 1: Initializing Relational Cleaning Pipeline...")
    
    # Load raw data
    try:
        clients = pd.read_csv("data/clients.csv")
        properties = pd.read_csv("data/properties.csv")
        print(f"Success: Loaded clients.csv ({len(clients)} rows) and properties.csv ({len(properties)} rows).")
    except FileNotFoundError as e:
        print(f"Error: Ensure files are placed properly in data/. Details: {e}")
        return

    print("Converting and aligning ID references...")
    # Force both linking columns to be clean, stripped string data types
    clients['client_id'] = clients['client_id'].astype(str).str.strip()
    properties['client_ref'] = properties['client_ref'].astype(str).str.strip()

    # Merge on client_id from clients and client_ref from properties
    print("Merging relational datasets...")
    df = pd.merge(clients, properties, left_on='client_id', right_on='client_ref', how='inner')
    print(f"Status: Datasets successfully merged! Combined rows: {len(df)}")

    # Remove duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    print(f"Status: Removed {initial_len - len(df)} duplicate records.")

    # Calculate Age dynamically for current year (2026)
    if 'date_of_birth' in df.columns:
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
        df['Age'] = 2026 - df['date_of_birth'].dt.year
        # Keep realistic home buyer age spectrum
        df = df[(df['Age'] >= 18) & (df['Age'] <= 100)]
        print("Success: Extracted buyer Age from date profiles.")
    else:
        df['Age'] = 35 

    # Clean text inconsistencies (Title Case strings so everything standardizes)
    categorical_cols = ['client_type', 'gender', 'country', 'region', 'acquisition_purpose', 'loan_applied', 'referral_channel']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown').astype(str).str.strip().str.title()

    # Handle numeric blanks safely using medians
    if 'satisfaction_score' in df.columns:
        df['satisfaction_score'] = df['satisfaction_score'].fillna(df['satisfaction_score'].median())
    if 'Age' in df.columns:
        df['Age'] = df['Age'].fillna(df['Age'].median()).astype(int)

    # Export clean master dataset
    output_path = "data/Parcl_Cleaned_Buyers.csv"
    df.to_csv(output_path, index=False)
    print(f"Success! Cleaned master dataset exported to: {output_path}\n")

if __name__ == "__main__":
    run_real_estate_cleaning()