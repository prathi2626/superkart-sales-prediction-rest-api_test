import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend (replace with your Codespaces URL if not using Docker networking)
BACKEND_URL = "http://backend:7860"

# Title
st.title("SuperKart Sales Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for product/store features
Product_Weight = st.number_input("Product Weight", min_value=0.0, step=0.1)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Regular", "Low Sugar", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, step=0.01)
Product_Type = st.text_input("Product Type")
Product_MRP = st.number_input("Product MRP", min_value=0.0, step=0.1)
Store_Id = st.text_input("Store Id")
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "Large"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.text_input("Store Type")
Store_Age = st.number_input("Store Age", min_value=0, step=1)
FoodType = st.text_input("FoodType")
Type_of_Food = st.text_input("Type of Food")

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_Type": Product_Type,
    "Product_MRP": Product_MRP,
    "Store_Id": Store_Id,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Store_Age": Store_Age,
    "FoodType": FoodType,
    "Type_of_Food": Type_of_Food
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predictsales", json=input_data.to_dict(orient='records')[0])
    if response.status_code == 200:
        prediction = response.json()['Predicted Sales']
        st.success(f"Predicted Sales: {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/batchpredictsales", files={"file": uploaded_file})
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)
        else:
            st.error("Unable to connect to the prediction API.")
