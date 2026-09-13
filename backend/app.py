import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask application
sales_predictor_api = Flask("SuperKart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_sales_prediction_model_v1_0.joblib")

# Root endpoint
@sales_predictor_api.get('/')
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

# Single prediction endpoint
@sales_predictor_api.post('/v1/predictsales')
def predict_sales():
    product_data = request.get_json()

    # Build sample with all features
    sample = {
        "Product_Weight": product_data["Product_Weight"],
        "Product_Sugar_Content": product_data["Product_Sugar_Content"],
        "Product_Allocated_Area": product_data["Product_Allocated_Area"],
        "Product_Type": product_data["Product_Type"],
        "Product_MRP": product_data["Product_MRP"],
        "Store_Id": product_data["Store_Id"],
        "Store_Size": product_data["Store_Size"],
        "Store_Location_City_Type": product_data["Store_Location_City_Type"],
        "Store_Type": product_data["Store_Type"],
        "Store_Age": product_data["Store_Age"],
        "FoodType": product_data["FoodType"],
        "Type_of_Food": product_data["Type_of_Food"]
    }

    input_data = pd.DataFrame([sample])
    predicted_sales = model.predict(input_data)[0]
    predicted_sales = round(float(predicted_sales), 2)

    return jsonify({"Predicted Sales": predicted_sales})

# Batch prediction endpoint
@sales_predictor_api.post('/v1/batchpredictsales')
def predict_sales_batch():
    file = request.files['file']
    input_data = pd.read_csv(file)

    predicted_values = model.predict(input_data)
    predicted_sales = [round(float(val), 2) for val in predicted_values]

    product_ids = input_data['id'].tolist()  # assumes 'id' column exists
    output_dict = dict(zip(product_ids, predicted_sales))

    return jsonify(output_dict)

if __name__ == '__main__':
    sales_predictor_api.run(debug=True)
