import streamlit as st

# Page settings
st.set_page_config(
    page_title="Smart Banking System",
    page_icon="🏦"
)

# Project title
st.title("🏦 Welcome to My Banking Queue System")

st.write(
    "A Smart Banking Queue Management System "
    "using Machine Learning"
)

st.write("---")

# Team members
st.header("Our Team")

st.write("Muhammad Ashiq")
st.write("Hammad Behzad")
st.write("Muhammad Shahzad")
st.write("Imran Latif")

st.write("---")

st.success("Welcome to our project!")

st.write(
    "Please select the Banking page from the left side "
    "to get your ticket."
)