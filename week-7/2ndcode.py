import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

# Load data from CSV with encoding fix
df = pd.read_csv("sensor_data.csv", encoding="ISO-8859-1") 

# Drop any missing or invalid rows
df.dropna(inplace=True)

# Print first few rows to verify data
print(df.head())

# Extract temperature and humidity
X = df["Temperature (°C)"].values.reshape(-1, 1)  # Independent variable
y = df["Humidity (%)"].values  # Dependent variable

# Train Linear Regression Model
model = LinearRegression()
model.fit(X, y)

# Generate test temperature values (min to max)
temp_min, temp_max = df["Temperature (°C)"].min(), df["Temperature (°C)"].max()
test_temps = np.linspace(temp_min, temp_max, 100).reshape(-1, 1)

# Predict humidity for these temperatures
predicted_humidity = model.predict(test_temps)

# Plot scatter and trend line
fig = px.scatter(df, x="Temperature (°C)", y="Humidity (%)", title="Temperature vs Humidity")
fig.add_scatter(x=test_temps.flatten(), y=predicted_humidity, mode='lines', name="Regression Line")
fig.show()
