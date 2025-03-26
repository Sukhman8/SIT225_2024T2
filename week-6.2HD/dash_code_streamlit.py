import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

# Function to Load Data (with dynamic updates)
def load_data():
    files = sorted([f for f in os.listdir() if f.startswith("gyroscope_data") and f.endswith(".csv")])
    if files:
        return pd.read_csv(files[-1])  # Load the latest CSV file
    return pd.DataFrame()  # Empty DataFrame if no file found

# Initialize session state variables
if "start_idx" not in st.session_state:
    st.session_state.start_idx = 0

df = load_data()

# Sidebar Controls
st.sidebar.header(" Graph Controls")

# Dropdown for selecting graph type
graph_type = st.sidebar.selectbox("Select Graph Type", ["Scatter", "Line", "Distribution"])

# Dropdown for selecting axis (X, Y, Z)
axis = st.sidebar.selectbox("Select Axis", ["X", "Y", "Z", "All"])

# Input for number of samples
num_samples = st.sidebar.text_input("Enter Number of Samples", value="300")

# Ensure valid input
try:
    num_samples = int(num_samples)
    num_samples = max(100, min(len(df), num_samples))  # Restrict within range
except ValueError:
    st.sidebar.error("Please enter a valid number")
    num_samples = 300

# Navigation Buttons
col1, col2 = st.sidebar.columns(2)
if col1.button("⬅ Previous"):
    st.session_state.start_idx = max(0, st.session_state.start_idx - num_samples)
if col2.button("Next ➡"):
    st.session_state.start_idx = min(len(df) - num_samples, st.session_state.start_idx + num_samples)

# Subset Data
subset_df = df.iloc[st.session_state.start_idx:st.session_state.start_idx + num_samples]

# Create Graph Based on Selection
st.title(" Gyroscope Data Visualization")
st.write("Real-time visualization of gyroscope sensor readings.")

if graph_type == "Distribution":
    fig = px.histogram(subset_df, x=axis, title="Distribution Plot")
else:
    fig = px.scatter(subset_df, x="Time(ms)", y=axis, title=f"{graph_type} Plot") if graph_type == "Scatter" else px.line(subset_df, x="Time(ms)", y=axis, title=f"{graph_type} Plot")

st.plotly_chart(fig, use_container_width=True)

# Display Summary Table Below the Graph
st.write("### Data Summary")
st.write(subset_df.describe())

# Display Data Table
st.write("### Raw Data")
st.dataframe(subset_df)

# Live Update every 10 seconds
st.sidebar.write(" Data updates every 10 seconds")
if st.sidebar.button("Refresh Data"):
    time.sleep(10)  # Simulate waiting for new data
    df = load_data()
    st.rerun()
