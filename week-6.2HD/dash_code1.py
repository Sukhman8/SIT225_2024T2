from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Select, Button, TextInput, DataTable, TableColumn
from bokeh.layouts import column, row
import pandas as pd
import numpy as np
import os
import time

# Function to Load Data
def load_data():
    files = sorted([f for f in os.listdir() if f.startswith("gyroscope_data") and f.endswith(".csv")])
    if files:
        return pd.read_csv(files[-1])  # Load latest CSV file
    return pd.DataFrame()

# Default Parameters
df = load_data()
num_samples = 300
start_idx = 0

# Column Data Source for Graph and Table
source = ColumnDataSource(df.iloc[start_idx:start_idx + num_samples])

# Create Initial Plot
p = figure(title="Gyroscope Data Visualization", x_axis_label="Time (ms)", y_axis_label="Sensor Value", width=800, height=400)
renderer = p.circle(x="Time(ms)", y="X", source=source, size=5, color="blue")  # Default to scatter plot

# Table Below Graph
columns = [
    TableColumn(field="Time(ms)", title="Time (ms)"),
    TableColumn(field="X", title="X"),
    TableColumn(field="Y", title="Y"),
    TableColumn(field="Z", title="Z")
]
data_table = DataTable(source=source, columns=columns, width=800, height=250)

# UI Elements
graph_select = Select(title="Select Graph Type", value="Scatter", options=["Scatter", "Line", "Distribution"])
axis_select = Select(title="Select Axis", value="X", options=["X", "Y", "Z"])
num_samples_input = TextInput(title="Number of Samples", value=str(num_samples))
prev_button = Button(label="⬅ Previous", button_type="primary")
next_button = Button(label="Next ➡", button_type="primary")
refresh_button = Button(label=" Refresh Data", button_type="success")

# Function to Compute Histogram Data for Distribution Plot
def compute_histogram(data, bins=20):
    hist, edges = np.histogram(data, bins=bins)
    return hist, edges

# Callback Function for Updating Graph
def update_graph():
    global renderer  # Needed to modify the existing renderer
    
    # Get selected axis and graph type
    selected_axis = axis_select.value
    graph_type = graph_select.value

    # Remove existing renderers
    p.renderers = []

    if graph_type == "Scatter":
        renderer = p.circle(x="Time(ms)", y=selected_axis, source=source, size=5, color="blue")

    elif graph_type == "Line":
        renderer = p.line(x="Time(ms)", y=selected_axis, source=source, line_width=2, color="red")

    elif graph_type == "Distribution":
        # Compute histogram
        hist, edges = compute_histogram(source.data[selected_axis], bins=20)
        
        # Create new ColumnDataSource for histogram
        hist_source = ColumnDataSource(data={"top": hist, "left": edges[:-1], "right": edges[1:]})
        
        # Plot histogram
        renderer = p.quad(top="top", bottom=0, left="left", right="right", source=hist_source, fill_color="green", line_color="black")

    # Update Plot Title
    p.title.text = f"{graph_type} Plot of {selected_axis} Axis"

# Callback Function for Updating Data
def update_data():
    global start_idx, num_samples, df
    try:
        num_samples = max(100, min(len(df), int(num_samples_input.value)))
    except ValueError:
        num_samples = 300  # Default if invalid input

    # Update Source Data
    source.data = df.iloc[start_idx:start_idx + num_samples].to_dict(orient="list")
    
    # Refresh the graph with new data
    update_graph()

# Navigation Callbacks
def prev_page():
    global start_idx
    start_idx = max(0, start_idx - num_samples)
    update_data()

def next_page():
    global start_idx
    start_idx = min(len(df) - num_samples, start_idx + num_samples)
    update_data()

# Live Data Refresh
def refresh_data():
    global df
    time.sleep(10)  # Simulate waiting for new data
    df = load_data()
    update_data()

# Assign Callbacks
num_samples_input.on_change("value", lambda attr, old, new: update_data())
axis_select.on_change("value", lambda attr, old, new: update_graph())
graph_select.on_change("value", lambda attr, old, new: update_graph())
prev_button.on_click(prev_page)
next_button.on_click(next_page)
refresh_button.on_click(refresh_data)

# Layout and Document
layout = column(
    row(graph_select, axis_select, num_samples_input),
    row(prev_button, next_button, refresh_button),
    p,
    data_table
)

curdoc().add_root(layout)
curdoc().title = "Gyroscope Dashboard"
