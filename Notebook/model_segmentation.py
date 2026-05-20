import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans

def run_clustering_pipeline():
    print("Step 2: Running Encoding and Segmentation Analysis...")
    
    # Load Master Clean File
    try:
        df = pd.read_csv("data/Parcl_Cleaned_Buyers.csv")
    except FileNotFoundError:
        print("Error: Run data_cleaning.py first!")
        return

    # Select target features for clustering based on project specifications
    categorical_features = ['client_type', 'region', 'acquisition_purpose', 'referral_channel', 'country']
    numeric_features = ['Age', 'satisfaction_score']
    
    # Verify exact column matching
    available_cats = [col for col in categorical_features if col in df.columns]
    available_nums = [col for col in numeric_features if col in df.columns]
    
    X = df[available_cats + available_nums].copy()

    # Create transformation pipeline (Scale numbers and One-Hot Encode categories)
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), available_nums),
            ('cat', OneHotEncoder(drop='first', sparse_output=False), available_cats)
        ])
    
    X_processed = preprocessor.fit_transform(X)
    print(f"Success: Feature transformations complete. Data matrix shape: {X_processed.shape}")

    # Train optimal K-Means model (K=4 as requested by project brief)
    print("Training K-Means Clustering Model (K=4)...")
    kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_processed)

    # Map cluster indices to the exact segment designations in the rubric
    cluster_mapping = {
        0: "C1: Global Investors",
        1: "C2: First-Time Buyers",
        2: "C3: Corporate Buyers",
        3: "C4: Luxury Investors"
    }
    df['Buyer_Segment'] = df['Cluster'].map(cluster_mapping)

    # Export final segmented records
    output_path = "data/Parcl_Segmented_Buyers.csv"
    df.to_csv(output_path, index=False)
    print(f"Success! Segmented profiles exported to: {output_path}")
    
    # Print out distribution metrics to check the balance
    print("\nCustomer Distribution Across Extracted Segments:")
    print(df['Buyer_Segment'].value_counts())

if __name__ == "__main__":
    run_clustering_pipeline()