# -*- coding: utf-8 -*-
"""netflix_subscriptions.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nHT43ZygdHCY2BMc1Y-V8d62SOkuiEyK

Import Library
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_white"
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

"""Load Dataset"""

data = pd.read_csv('netflixSubscriptions.csv')
print(data.head())

print(data.describe())

"""Data Pre-processing"""

# Handling Missing Values
print(data.isnull().sum())

# Data Type Conversion
data['Time Period'] = pd.to_datetime(data['Time Period'], format='%d/%m/%Y')
print(data.head())

# Handling Duplicate Data
data.drop_duplicates(inplace=True)

# Handling Outliers
plt.figure(figsize=(8, 6))
plt.boxplot(data['Subscribers'])
plt.ylabel('Subscribers')
plt.title('Box Plot of Subscribers')
plt.show()

# Feature Engineering (Extracting Year, Quarter, Month)
data['Year'] = data['Time Period'].dt.year
data['Quarter'] = data['Time Period'].dt.quarter
data['Month'] = data['Time Period'].dt.month

# Correlation Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()

# Data Normalization (Min-Max Scaling)
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
data['Scaled_Subscribers'] = scaler.fit_transform(data[['Subscribers']])

"""Visualization and Correlation"""

fig = go.Figure()
fig.add_trace(go.Scatter(x=data['Time Period'],
                         y=data['Subscribers'],
                         mode='lines', name='Subscribers'))
fig.update_layout(title='Netflix Quarterly Subscriptions Growth',
                  xaxis_title='Date',
                  yaxis_title='Netflix Subscriptions')
fig.show()

# Calculate the quarterly growth rate
data['Quarterly Growth Rate'] = data['Subscribers'].pct_change() * 100

# Orange for positive growth, red for negative growth
data['Bar Color'] = data['Quarterly Growth Rate'].apply(lambda x: 'orange' if x > 0 else 'red')

# Plotting
fig = go.Figure()
fig.add_trace(go.Bar(
    x=data['Time Period'],
    y=data['Quarterly Growth Rate'],
    marker_color=data['Bar Color'],
    name='Quarterly Growth Rate'
))
fig.update_layout(title='Netflix Quarterly Subscriptions Growth Rate',
                  xaxis_title='Time Period',
                  yaxis_title='Quarterly Growth Rate (%)')
fig.show()

# Orange for positive growth, red for negative growth
data['Bar Color'] = yearly_growth.apply(lambda x: 'orange' if x > 0 else 'red')

# Plotting
fig = go.Figure()
fig.add_trace(go.Bar(
    x=data['Year'],
    y=yearly_growth,
    marker_color=data['Bar Color'],
    name='Yearly Growth Rate'
))
fig.update_layout(title='Netflix Yearly Subscriber Growth Rate',
                  xaxis_title='Year',
                  yaxis_title='Yearly Growth Rate (%)')
fig.show()

"""Using ARIMA to forecast the number of subscriptions of Netflix"""

time_series = data.set_index('Time Period')['Subscribers']

differenced_series = time_series.diff().dropna()

# Plot ACF and PACF of differenced time series
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
plot_acf(differenced_series, ax=axes[0])
plot_pacf(differenced_series, ax=axes[1])
plt.show()

"""ARIMA Model"""

p, d, q = 1, 1, 1
model = ARIMA(time_series, order=(p, d, q))
results = model.fit()
print(results.summary())

# Train model
future_steps = 5
predictions = results.predict(len(time_series), len(time_series) + future_steps - 1)
predictions = predictions.astype(int)

forecast = pd.DataFrame({'Original': time_series, 'Predictions': predictions})

"""Result"""

# Plot the original data and predictions
fig = go.Figure()

fig.add_trace(go.Scatter(x=forecast.index, y=forecast['Predictions'],
                         mode='lines', name='Predictions'))

fig.add_trace(go.Scatter(x=forecast.index, y=forecast['Original'],
                         mode='lines', name='Original Data'))

fig.update_layout(title='Netflix Quarterly Subscription Predictions',
                  title_x=0.5,
                  xaxis_title='Time Period',
                  yaxis_title='Subscribers',
                  legend=dict(x=0.1, y=0.9),
                  showlegend=True)

fig.show()

