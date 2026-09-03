import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Page settings
st.set_page_config(
    page_title="Banking Queue",
    page_icon="🎫"
)

st.title("🏦 Banking Queue System")

st.write(
    "Get your ticket and let our Machine Learning model "
    "estimate your waiting time."
)

st.write("---")

# Load ML model
model = joblib.load("bank_queue_model.pkl")

# Select service
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

# Get ticket
if st.button("🎫 Get Ticket"):

    # Current time
    current_time = datetime.now()

    hour = current_time.hour
    minute = current_time.minute

    # ------------------------------------------------
    # IMPORTANT:
    # Customer does NOT enter queue length.
    # We use previous customer information.
    # ------------------------------------------------

    # Read previous customer data
    try:
        history = pd.read_csv("queue_data.csv")

        # Calculate average waiting time
        previous_waiting_time = history["wait_time"].mean()

        # Calculate previous average queue length
        previous_queue_length = history["queue_length"].mean()

    except:
        # Backup values if history file is unavailable
        previous_waiting_time = 10
        previous_queue_length = 5

    # ------------------------------------------------
    # Give previous queue information to ML model
    # ------------------------------------------------

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

    # ML prediction
    prediction = model.predict(customer_data)

    waiting_time = prediction[0]

    # Prevent negative time
    waiting_time = max(0, waiting_time)

    # ------------------------------------------------
    # Generate ticket
    # ------------------------------------------------

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

    # ------------------------------------------------
    # Show result
    # ------------------------------------------------

    st.success("🎉 Your Ticket Has Been Generated!")

    st.write("---")

    st.header("🎫 Your Ticket")

    st.title(ticket)

    st.write("**Service:**", service)

    st.write(
        "**Estimated Waiting Time:**",
        round(waiting_time, 2),
        "minutes"
    )

    st.info(
        "Please wait until your ticket number is called."
    )