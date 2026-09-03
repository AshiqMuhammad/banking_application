import streamlit as st
import pandas as pd
import joblib
from datetime import datetime


# Page settings
st.set_page_config(
    page_title="Banking Queue System",
    page_icon="🏦"
)


# ==============================
# PROJECT NAME
# ==============================

st.title("🏦 Banking Queue System")

st.write("Machine Learning Based Smart Banking Queue Management")


# ==============================
# TEAM MEMBERS
# ==============================

st.subheader("Team")

st.write("Muhammad Ashiq")
st.write("Hammad Behzad")
st.write("Muhammad Shahzad")
st.write("Imran Latif")


st.write("---")


# ==============================
# LOAD ML MODEL
# ==============================

model = joblib.load("bank_queue_model.pkl")


# ==============================
# BANKING SERVICE
# ==============================

st.header("🎫 Get Your Ticket")

service = st.selectbox(
    "Select Your Banking Service",
    [
        "Cash Deposit",
        "Cash Withdrawal",
        "Account Opening",
        "Loan Service",
        "Customer Support"
    ]
)


st.write("---")


# ==============================
# GET TICKET
# ==============================

if st.button("🎫 Get Ticket"):

    # Current time
    current_time = datetime.now()

    hour = current_time.hour
    minute = current_time.minute


    # ==============================
    # READ PREVIOUS CUSTOMER DATA
    # ==============================

    try:

        history = pd.read_csv("queue_data.csv")

        # Remove missing values
        history = history.dropna(
            subset=[
                "wait_time",
                "queue_length"
            ]
        )

        # Previous waiting time
        previous_waiting_time = history["wait_time"].mean()

        # Previous queue length
        previous_queue_length = history["queue_length"].mean()

    except:

        # Backup values
        previous_waiting_time = 10
        previous_queue_length = 5


    # ==============================
    # DATA FOR ML MODEL
    # ==============================

    customer_data = pd.DataFrame(
        [[
            hour,
            minute,
            previous_queue_length
        ]],
        columns=[
            "arrival_hour",
            "arrival_minute",
            "queue_length"
        ]
    )


    # ==============================
    # ML PREDICTION
    # ==============================

    prediction = model.predict(customer_data)

    waiting_time = prediction[0]

    # Prevent negative waiting time
    waiting_time = max(0, waiting_time)


    # ==============================
    # GENERATE TICKET NUMBER
    # ==============================

    ticket_number = int(previous_queue_length) + 1


    if service == "Cash Deposit":

        prefix = "A"

    elif service == "Cash Withdrawal":

        prefix = "A"

    elif service == "Account Opening":

        prefix = "B"

    elif service == "Loan Service":

        prefix = "C"

    else:

        prefix = "D"


    ticket = prefix + "-" + str(ticket_number).zfill(3)


    # ==============================
    # SHOW TICKET
    # ==============================

    st.success("🎉 Your Ticket Has Been Generated!")

    st.write("---")

    st.header("🎫 Your Ticket")

    st.title(ticket)

    st.write("Service:", service)

    st.write(
        "Estimated Waiting Time:",
        round(waiting_time, 2),
        "minutes"
    )

    st.info(
        "Please wait until your ticket number is called."
    )