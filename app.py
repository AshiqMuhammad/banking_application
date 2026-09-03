import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import json
import random
import string
import os


# ==============================
# PAGE SETTINGS
# ==============================

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
# DAILY TICKET SYSTEM
# ==============================

counter_file = "daily_ticket_counter.json"

today = datetime.now().strftime("%Y-%m-%d")


# Check if counter file exists
if os.path.exists(counter_file):

    with open(counter_file, "r") as file:
        counter_data = json.load(file)

else:

    counter_data = {
        "date": today,
        "count": 0
    }


# If new day, start from 0
if counter_data["date"] != today:

    counter_data = {
        "date": today,
        "count": 0
    }


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

    # Increase today's ticket number
    counter_data["count"] += 1

    ticket_number = counter_data["count"]


    # Save today's counter
    with open(counter_file, "w") as file:
        json.dump(counter_data, file)


    # ==============================
    # CURRENT TIME
    # ==============================

    current_time = datetime.now()

    hour = current_time.hour
    minute = current_time.minute


    # ==============================
    # READ PREVIOUS DATA
    # ==============================

    try:

        history = pd.read_csv("queue_data.csv")

        history = history.dropna(
            subset=[
                "wait_time",
                "queue_length"
            ]
        )

        previous_queue_length = history[
            "queue_length"
        ].mean()

    except:

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

    waiting_time = max(0, waiting_time)


    # ==============================
    # RANDOM TICKET CODE
    # ==============================

    random_code = "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=4
        )
    )


    # ==============================
    # SERVICE PREFIX
    # ==============================

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


    # ==============================
    # FINAL TICKET
    # ==============================

    ticket = (
        prefix
        + "-"
        + str(ticket_number).zfill(3)
        + "-"
        + random_code
    )


    # ==============================
    # SHOW TICKET
    # ==============================

    st.success(
        "🎉 Your Ticket Has Been Generated!"
    )

    st.write("---")

    st.header("🎫 Your Ticket")

    st.title(ticket)

    st.write(
        "Service:",
        service
    )

    st.write(
        "Ticket Number:",
        ticket_number
    )

    st.write(
        "Estimated Waiting Time:",
        round(waiting_time, 2),
        "minutes"
    )

    st.info(
        "Please wait until your ticket number is called."
    )
