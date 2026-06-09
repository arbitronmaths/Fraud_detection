import streamlit as st
import pandas as pd
import joblib
import sqlite3
import matplotlib.pyplot as plt

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🛡️",
    layout="wide"
)


# -------------------------
# DATABASE
# -------------------------
conn = sqlite3.connect("fraud.db", check_same_thread=False)  #connection setup
cursor = conn.cursor()    

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_type TEXT,
    amount REAL,
    prediction INTEGER
)
""")

conn.commit()

#--------------
#LOAD MODEL
#--------------
model = joblib.load("fraud_detection_pipeline.pkl")

# -------------------------
# SIDEBAR
# -------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Prediction", "History"]
)

if page == "Prediction":
    st.title("Fraud Detection Prediction")

    st.markdown("Please enter the transaction details and use the predict button")

    st.divider()
    
    transaction_type = st.selectbox("Transaction Type", ["PAYMENT", "TRANSFER","CASH_OUT","DEPOSIT"])
    amount = st.number_input("Amount", min_value=0.0, value = 1000.0)
    oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value = 0.0, value=10000.0)
    newbalanceOrig = st.number_input("New Balance (Sender)", min_value = 0.0, value=9000.0)
    oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value = 0.0, value=0.0)
    newbalanceDest = st.number_input("New Balance (Receiver)", min_value = 0.0, value=0.0)

    if st.button("Predict"):
        input_data = pd.DataFrame([{
            "type": transaction_type,
            "amount": amount,
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "oldbalanceDest": oldbalanceDest,
            "newbalanceDest": newbalanceDest
        }])
        
        prediction = model.predict(input_data)[0]

        #save to databse
        cursor.execute("""
        INSERT INTO predictions (transaction_type, amount, prediction) 
        VALUES(?, ?, ?)""",(
            transaction_type,
            amount,
            int(prediction)
        ))

        conn.commit()

        #Result
        if int(prediction) == 1:
            st.subheader(f"Prediction:Fraudulent")
        else :
            st.subheader(f"Prediction:Not Fraudulent")

        if prediction == 1:
            st.error("This transaction is predicted to be fraudulent.")
        else:
            st.success("This transaction looks like not fraud.")

        #Risc Score
        try:
            probability = model.predict_proba(input_data)[0][1]
            
            st.subheader("Fraud Risk Score")

            st.progress(
                min(int(probability * 100), 100)
            )

            st.metric(
                "Risk Level",
                f"{probability * 100:.2f}%"
            )

        except:
            pass


#---------------------------
#HISTORY PAGE
#--------------------------

else:

    st.title("Prediction History")

    history = pd.read_sql_query("SELECT * FROM predictions", conn)

    if history.empty:
        st.info("No predictions made yet.")
    
    else:
        st.subheader("Your Prediction History is Here")
        st.dataframe(history)


        fraud_count = history["prediction"].value_counts()

        fig, ax = plt.subplots()
        fraud_count.plot(kind="bar", ax=ax)

        st.pyplot(fig)

