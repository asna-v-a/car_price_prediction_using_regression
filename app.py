import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load the trained model
with open('C:/Users/asnav/Documents/MachineLearningProjects/car_price_prediction_using_regression/notebook/car_price_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load feature names used during training
with open('C:/Users/asnav/Documents/MachineLearningProjects/car_price_prediction_using_regression/notebook/feature_columns.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

# Streamlit App UI
st.title("Car Price Prediction App")
st.write("Enter the details of the car to predict its price.")

# Input fields for car features
year = st.number_input("Year of Manufacture", min_value=2000, max_value=2025, step=1)
kms_driven = st.number_input("Kilometers Driven", min_value=0, step=500)
fuel_type = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'CNG'])
seller_type = st.selectbox("Seller Type", ['Dealer', 'Individual'])
transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])
owner = st.selectbox("Owner Type", ['First Owner', 'Second Owner', 'Third Owner'])

# Convert categorical inputs to match model encoding
fuel_dict = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}
seller_dict = {'Dealer': 0, 'Individual': 1}
transmission_dict = {'Manual': 0, 'Automatic': 1}
owner_dict = {'First Owner': 0, 'Second Owner': 1, 'Third Owner': 2}

# Create DataFrame for input
df_input = pd.DataFrame([[year, kms_driven, fuel_dict[fuel_type], 
                          seller_dict[seller_type], transmission_dict[transmission], 
                          owner_dict[owner]]], 
                        columns=['Year', 'Kilometers_Driven', 'Fuel_Type', 
                                 'Seller_Type', 'Transmission', 'Owner_Type'])

# Ensure all columns from training exist
for col in feature_columns:
    if col not in df_input.columns:
        df_input[col] = 0  # Add missing columns with default value

df_input = df_input[feature_columns]  # Reorder columns to match training

# Predict button
if st.button("Predict Price"):
    if df_input.shape[0] > 0:  # Ensure input is not empty
        prediction = model.predict(df_input)
        st.success(f"Estimated Car Price: ₹{prediction[0]:,.2f}")
    else:
        st.error("Invalid input. Please check your values.")