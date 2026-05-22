# Real Estate Market Intelligence & Buyer Segmentation Portal

An interactive, production-ready data science web application engineered for **Parcl Co. Limited**. This platform aggregates customer behavioral logs, handles complex data preprocessing, and implements an optimized unsupervised Machine Learning pipeline to mathematically segment the consumer base into strategic profiles.

## Deployed Application
🔗 **Live Interactive App:** [manjeet-parcl-market-intelligence.streamlit.app](https://manjeet-parcl-market-intelligence.streamlit.app/)

---

## 🛠️ Technical Architecture & Pipeline

### 1. Data Aggregation & Preprocessing
* **Relational Alignment:** Restructured disparate consumer data arrays, resolving underlying data type conflicts and handling missing attributes.
* **Feature Scaling:** Applied `StandardScaler` to compute exact **Z-scores** across continuous behavioral variables, eliminating scalar bias prior to geometric modeling.

### 2. Machine Learning Engine
* **Algorithm:** Unsupervised **K-Means Clustering**.
* **Optimization:** Evaluated clusters using the Elbow Method and Silhouette Analysis to identify the mathematically optimal cluster numbers.
* **Outputs:** Successfully partitioned a portfolio of **3,118 consumer records** into four high-impact strategic profiles.

### 3. Business Intelligence Frontend
* Deployed a responsive dashboard built entirely with **Python**, **Streamlit**, and **Plotly**.
* **Dynamic Interactivity:** Implemented multi-dimensional sidebar filters (Country of Origin, Target Region, Acquisition Purpose) that force the underlying backend descriptive matrix to re-calculate in real time.

---

## 📊 Strategic Buyer Profiles Extracted

The system identifies and tracks consumer behavior across four core segments:
1. **Corporate Buyers:** High-volume institutional entities focused on commercial real estate and portfolio scaling.
2. **Luxury Investors:** Premium demographic targeting tier-one residential assets with premium lifestyle indicators.
3. **First-Time Buyers:** Emerging consumer sector characterized by specific loan utilization and domestic financial dependencies.
4. **Global Investors:** Cross-border capital allocators requiring hyper-targeted property recommendations and macro-market filtering.

---

## ⚙️ Core Stack & Libraries
* **Language:** Python 3.x
* **Modeling & Scaling:** `scikit-learn` (KMeans, StandardScaler)
* **Data Engineering:** `pandas`, `numpy`
* **Visualization Engine:** `plotly.express`, `matplotlib`, `seaborn`
* **Application Framework:** `streamlit`

---

## 🚀 Installation & Local Deployment

To run this repository locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone [https://github.com/manjeetrwt/Parcl_Buyer_Segmentation.git](https://github.com/manjeetrwt/Parcl_Buyer_Segmentation.git)
   cd Parcl_Buyer_Segmentation
