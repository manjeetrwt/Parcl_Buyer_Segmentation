import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Set Page Configuration Layout
st.set_page_config(page_title="Parcl Co. | Market Intelligence", layout="wide", initial_sidebar_state="expanded")

# Custom Minimalist Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    div.block-container { padding-top: 2rem; }
    h1, h2, h3 { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    </style>
""", unsafe_allow_html=True)

# 2. Data Loading Function
@st.cache_data
def load_segmented_data():
    try:
        data = pd.read_csv("data/Parcl_Segmented_Buyers.csv")
        return data
    except Exception as e:
        st.error(f"Error loading master segmented file: {e}")
        return None

df = load_segmented_data()

if df is not None:
    # 3. Streamlit Sidebar Header and Global Filter Engine
    st.sidebar.header("Parcl Co. Intelligent Filters")
    st.sidebar.markdown("Use the parameters below to filter market intelligence segments.")
    
    # Extract Unique Clean List values for drop-downs
    countries = ["All"] + sorted(df['country'].dropna().unique().tolist())
    regions = ["All"] + sorted(df['region'].dropna().unique().tolist())
    purposes = ["All"] + sorted(df['acquisition_purpose'].dropna().unique().tolist())
    client_types = ["All"] + sorted(df['client_type'].dropna().unique().tolist())
    
    # Define Select Boxes
    selected_country = st.sidebar.selectbox("Country of Origin", countries)
    selected_region = st.sidebar.selectbox("Target Geographic Region", regions)
    selected_purpose = st.sidebar.selectbox("Acquisition Purpose", purposes)
    selected_client = st.sidebar.selectbox("Client Structure Type", client_types)
    
    # Process Filter Logic Mask
    filtered_df = df.copy()
    if selected_country != "All":
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    if selected_region != "All":
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    if selected_purpose != "All":
        filtered_df = filtered_df[filtered_df['acquisition_purpose'] == selected_purpose]
    if selected_client != "All":
        filtered_df = filtered_df[filtered_df['client_type'] == selected_client]

    # 4. Main App Layout Headers
    st.title("Real Estate Market Intelligence Portal")
    st.subheader("AI-Driven Buyer Segmentation & Investment Profiling — Parcl Co. Limited")
    st.markdown("---")
    
    # Summary Dashboard Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Analyzed Portfolio Records", f"{len(filtered_df):,}")
    m2.metric("Average Strategic Buyer Age", f"{int(filtered_df['Age'].mean()) if len(filtered_df)>0 else 0} Years")
    m3.metric("Avg Satisfaction Index", f"{filtered_df['satisfaction_score'].mean():.2f}/5.0" if len(filtered_df)>0 else "0.00")
    m4.metric("Active Market Sectors", filtered_df['region'].nunique() if len(filtered_df)>0 else 0)
    
    st.markdown("---")

    # 5. Core Visual Matrix Layout Rows
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.subheader("Panel 1: Buyer Segmentation Overview")
        segment_counts = filtered_df['Buyer_Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Volume']
        
        fig_pie = px.pie(
            segment_counts, 
            values='Volume', 
            names='Segment',
            hole=0.4,
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Purples_r
        )
        fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    with row1_col2:
        st.subheader("Panel 2: Investor Financial Behavior")
        if len(filtered_df) > 0 and 'loan_applied' in filtered_df.columns:
            loan_profile = filtered_df.groupby(['Buyer_Segment', 'loan_applied']).size().reset_index(name='Volume')
            fig_bar = px.bar(
                loan_profile, 
                x='Buyer_Segment', 
                y='Volume', 
                color='loan_applied',
                barmode='group',
                template="plotly_dark",
                labels={'loan_applied': 'Financing Applied'},
                color_discrete_map={'Yes': '#9b5de5', 'No': '#f15bb5', 'Unknown': '#5c677d'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No categorical financing matrices map to current filter sets.")

    st.markdown("---")
    
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.subheader("Panel 3: Geographic Distribution")
        if len(filtered_df) > 0:
            geo_profile = filtered_df.groupby(['region', 'Buyer_Segment']).size().reset_index(name='Volume')
            fig_geo = px.bar(
                geo_profile,
                y='region',
                x='Volume',
                color='Buyer_Segment',
                barmode='stack',
                template="plotly_dark",
                orientation='h',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_geo, use_container_width=True)

    with row2_col2:
        st.subheader("Panel 4: Segment Descriptive Statistics")
        if len(filtered_df) > 0:
            summary_stats = filtered_df.groupby('Buyer_Segment').agg({
                'Age': 'mean',
                'satisfaction_score': 'mean',
                'client_id': 'count'
            }).rename(columns={
                'Age': 'Average Age',
                'satisfaction_score': 'Mean Satisfaction',
                'client_id': 'Total Count'
            }).reset_index()
            
            # Format display numbers neatly
            summary_stats['Average Age'] = summary_stats['Average Age'].round(1)
            summary_stats['Mean Satisfaction'] = summary_stats['Mean Satisfaction'].round(2)
            
            st.dataframe(summary_stats, use_container_width=True, hide_index=True)
        else:
            st.info("No baseline statistic records for current filters.")