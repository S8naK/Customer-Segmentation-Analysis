import streamlit as st
import numpy as np
import joblib

kmeans = joblib.load("kmeans_model.pkl")
scaler = joblib.load("scaler.pkl")

cluster_labels = {
    0: "RETAIN",
    1: "RE-ENGAGE",
    2: "NURTURE",
    3: "REWARD"
}

st.set_page_config(page_title="Customer Segmentation", page_icon="🧩", layout="centered")

st.title("🧩 Customer Segmentation App")
st.write("Enter customer details below to predict their segment:")

monetary_value = st.number_input("Total Spending (MonetaryValue) in British Pounds (£)", min_value=0.0, max_value=4000.0, value=1000.0, step=1.0)
frequency = st.number_input("Purchase Frequency (0-11)", min_value=0, max_value=12, value=3, step=1)
recency = st.number_input("Recency (days since last purchase)", min_value=0, max_value=400, value=30, step=1)

if st.button("Predict Segment"):
    features = np.array([[monetary_value, frequency, recency]])
    
    scaled_features = scaler.transform(features)
    
    cluster = kmeans.predict(scaled_features)[0]
    
    label = cluster_labels.get(cluster, f"Cluster {cluster}")
    
    st.success(f"Predicted Segment: {label}")

st.caption(
        "💡 Note: 'PAMPER', 'UPSELL', and 'DELIGHT' were special outlier clusters "
        "identified during analysis and are not part of live model predictions."
    )