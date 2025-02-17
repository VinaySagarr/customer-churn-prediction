import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load("churn_model.pkl")

# Streamlit UI
st.title("🔮 Customer Churn Prediction App")
st.write("This app predicts whether a customer is likely to churn based on input features.")

# User Input Fields (All 23 features)
tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, step=1)
monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, step=0.1)
total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=10000.0, step=0.1)

gender = st.selectbox("Gender", ["Male", "Female"])
senior_citizen = st.selectbox("Senior Citizen", ["Yes", "No"])
partner = st.selectbox("Has Partner?", ["Yes", "No"])
dependents = st.selectbox("Has Dependents?", ["Yes", "No"])
phone_service = st.selectbox("Has Phone Service?", ["Yes", "No"])
multiple_lines = st.selectbox("Has Multiple Lines?", ["Yes", "No", "No phone service"])
online_security = st.selectbox("Online Security", ["Yes", "No", "Not applicable"])
online_backup = st.selectbox("Online Backup", ["Yes", "No", "Not applicable"])
device_protection = st.selectbox("Device Protection", ["Yes", "No", "Not applicable"])
tech_support = st.selectbox("Tech Support", ["Yes", "No", "Not applicable"])
streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "Not applicable"])
streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "Not applicable"])
paperless_billing = st.selectbox("Paperless Billing?", ["Yes", "No"])

# One-hot encoded categorical features
internet_service = st.selectbox("Internet Service Type", ["DSL", "Fiber optic", "No"])
contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
payment_method = st.selectbox("Payment Method", ["Bank Transfer", "Credit card (automatic)", "Electronic check", "Mailed check"])

# Convert categorical inputs to numeric
gender = 1 if gender == "Male" else 0
senior_citizen = 1 if senior_citizen == "Yes" else 0
partner = 1 if partner == "Yes" else 0
dependents = 1 if dependents == "Yes" else 0
phone_service = 1 if phone_service == "Yes" else 0
multiple_lines = {"Yes": 1, "No": 0, "No phone service": -1}[multiple_lines]
online_security = {"Yes": 1, "No": 0, "Not applicable": -1}[online_security]
online_backup = {"Yes": 1, "No": 0, "Not applicable": -1}[online_backup]
device_protection = {"Yes": 1, "No": 0, "Not applicable": -1}[device_protection]
tech_support = {"Yes": 1, "No": 0, "Not applicable": -1}[tech_support]
streaming_tv = {"Yes": 1, "No": 0, "Not applicable": -1}[streaming_tv]
streaming_movies = {"Yes": 1, "No": 0, "Not applicable": -1}[streaming_movies]
paperless_billing = 1 if paperless_billing == "Yes" else 0

# One-hot encoding for InternetService
internet_service_fiber = 1 if internet_service == "Fiber optic" else 0
internet_service_no = 1 if internet_service == "No" else 0

# One-hot encoding for Contract
contract_one_year = 1 if contract == "One year" else 0
contract_two_year = 1 if contract == "Two year" else 0

# One-hot encoding for PaymentMethod
payment_credit_card = 1 if payment_method == "Credit card (automatic)" else 0
payment_electronic_check = 1 if payment_method == "Electronic check" else 0
payment_mailed_check = 1 if payment_method == "Mailed check" else 0

# Create input feature array with all 23 features in correct order
input_features = np.array([[
    gender, senior_citizen, partner, dependents, tenure, phone_service, multiple_lines,
    online_security, online_backup, device_protection, tech_support, streaming_tv,
    streaming_movies, paperless_billing, monthly_charges, total_charges,
    internet_service_fiber, internet_service_no, contract_one_year, contract_two_year,
    payment_credit_card, payment_electronic_check, payment_mailed_check
]])

# Debugging: Print number of features
st.write("Number of features passed to model:", input_features.shape[1])

# Predict Button
if st.button("🔍 Predict Churn"):
    prediction = model.predict(input_features)

    if prediction[0] == 1:
        st.error("⚠️ This customer is **likely to churn!**")
    else:
        st.success("✅ This customer is **NOT likely to churn!**")
