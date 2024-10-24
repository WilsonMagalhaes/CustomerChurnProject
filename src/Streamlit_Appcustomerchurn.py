# -*- coding: utf-8 -*-
"""DeployCustomerChurn.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HpeaaPjXLz5zLNdpdRa4CNiRgnLsp0o-
"""

import streamlit as st
import joblib
from transformxfunctionFinal import transformX
import pandas as pd

full_pipeline = joblib.load("full_pipeline.pkl")
categorical_columns = joblib.load("categorical_columns.pkl")
categorical_columns_two_options = joblib.load("categorical_columns_two_options.pkl")
model = joblib.load("abFinal.pkl")
optimal_threshold = joblib.load("optimal_threshold.pkl")

# Load the machine learning model (replace with your specific loading logic)
#model = full_pipeline.load_model()

def make_prediction(data):
    """Makes predictions using the loaded model."""
    processed_data = transformX(data, categorical_columns, categorical_columns_two_options, full_pipeline)  # Process data using treatment.py functions
    y_probs = model.predict_proba(processed_data)[:, 1]
    y_pred_opt = (y_probs >= optimal_threshold).astype(int)
    #prediction = model.predict(processed_data)
    return y_pred_opt

st.title("Machine Learning Model Deployment")
st.subheader("Input User Information and Monthly Charge")

st.write("If you wish to upload a csv file, go to the bottom of the page")

# User input section
gender = st.selectbox("Gender", ["Female", "Male"])
senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
partner = st.selectbox("Partner", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["No", "Yes"])
tenure = st.number_input("Tenure (number of months)", min_value=0, max_value=100, step=1)
phone_service = st.selectbox("Phone Service", ["No", "Yes"])
multiple_lines = st.selectbox("Multiple Lines", ["No phone service", "No", "Yes"])
internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
payment_method = st.selectbox("Payment Method", [
    "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
])
monthly_charge = st.number_input("Monthly Charge", format="%.2f", min_value=0.0, max_value=500.0, step=10.0)
total_charges = st.number_input("Total Charges", format="%.2f", min_value=0.0, max_value=10000.0, step=100.0)
tenure_MonthlyCharges = tenure * monthly_charge


# Button to trigger prediction
if st.button("Predict"):
    if senior_citizen == "Yes":
        senior_citizen = 1
    else:
        senior_citizen = 0
    # Combine user input and other relevant data into a dictionary
    data = {
    "gender": gender,
    "SeniorCitizen": senior_citizen,
    "Partner": partner,
    "Dependents": dependents,
    "tenure": tenure,
    "PhoneService": phone_service,
    "MultipleLines": multiple_lines,
    "InternetService": internet_service,
    "OnlineSecurity": online_security,
    "OnlineBackup": online_backup,
    "DeviceProtection": device_protection,
    "TechSupport": tech_support,
    "StreamingTV": streaming_tv,
    "StreamingMovies": streaming_movies,
    "Contract": contract,
    "PaperlessBilling": paperless_billing,
    "PaymentMethod": payment_method,
    "MonthlyCharges": monthly_charge,
    "TotalCharges": total_charges,
    "Tenure_MonthlyCharges": tenure_MonthlyCharges    
    }
    df = pd.DataFrame([data])
    # Make prediction using the defined function
    prediction = make_prediction(df)
    if prediction == 0.0:
        prediction = "Client is likely to churn"
    else:
        prediction = "Client is not expected to churn"
    # Display prediction results
    st.write("Prediction:")
    st.success(prediction)  # Use success for positive outcomes (optional)

st.write("Below, you can also predict multiple customers by selecting a csv file with the customers informations")
st.write("Be careful with the file's columns, as wel as their input, they must be spelled properly")
st.write("For more information, click on the button below. You will see the column names and their possible inputs")
information = """
gender : ["Female", "Male"] \n
SeniorCitizen : ["No", "Yes"]\n
Partner : ["Yes", "No"]\n
Dependents : ["No", "Yes"]\n
tenure : A numeric value (e.g., between 0 and 100, representing the number of months)\n
PhoneService : ["No", "Yes"]\n
MultipleLines : ["No phone service", "No", "Yes"]\n
InternetService : ["DSL", "Fiber optic", "No"]\n
OnlineSecurity : ["No", "Yes", "No internet service"]\n
OnlineBackup : ["Yes", "No", "No internet service"]\n
DeviceProtection : ["No", "Yes", "No internet service"]\n
TechSupport : ["No", "Yes", "No internet service"]\n
StreamingTV : ["No", "Yes", "No internet service"]\n
StreamingMovies : ["No", "Yes", "No internet service"]\n
Contract : ["Month-to-month", "One year", "Two year"]\n
PaperlessBilling : ["Yes", "No"]\n
PaymentMethod : ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]\n
MonthlyCharges : Numeric input (representing the monthly charges)\n
TotalCharges : Numeric input (representing the total charges)\n
Tenure_MonthlyCharges : Derived feature (tenure multiplied by monthly charges)
"""
button = st.button("Click to Show Information")
placeholder = st.empty()
hideButton = False
if button:
    placeholder.write(information)
    hideButton = True

if hideButton:
    button = st.button("Click to Hide Information")
    if button:
      placeholder.empty()

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df_initial = pd.read_csv(uploaded_file)
    # Display the DataFrame in Streamlit
    if st.button('Predic File'):
      predictions = make_prediction(df_initial)
      predictions = ["Client is likely to churn" if prediction == 1 else "Client is not expected to churn" for prediction in predictions]
      df_predictions = pd.DataFrame(predictions, columns=['Prediction'])
      df_initial['Prediction'] = df_predictions['Prediction']
      df_initial.to_csv('predictions.csv', index=False)
      #st.write(df_initial)  
      csv_file = df_initial.to_csv(index=False).encode()
      st.download_button(
      label="Download Predictions",
      data=csv_file,
      file_name="predictions.csv",
      mime="text/csv"
      )
