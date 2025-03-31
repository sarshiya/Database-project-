#!/usr/bin/env python3

import cgi
import json
import pandas as pd
import numpy as np
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns

# Function to execute database query
def execute_query(query):
    try:
        connection = pymysql.connect(
            host='bioed.bu.edu',
            user='arshiyas',
            password='Ar@021202',
            db='Team_11',
            port=4253)
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print("Error executing query:", e)
    finally:
        if connection:
            connection.close()

# Function to generate heatmap data with normalization
def generate_heatmap_data():
    # Query to fetch data from the database table
    query = "SELECT * FROM placenta_opioid_counts"

    # Load data from the database into a DataFrame
    try:
        counts_data = pd.DataFrame(execute_query(query))
    except Exception as e:
        print("Error fetching data from the database:", e)
        return None

    # Process data and return heatmap data
    try:
        # Extracting the data values from the DataFrame
        data_values = counts_data.iloc[:, 1:].values.astype(float)
        
        # Perform normalization
        data_values_normalized = (data_values - data_values.min()) / (data_values.max() - data_values.min())

        # For demonstration purposes, let's return the normalized data
        heatmap_data = data_values_normalized.tolist()  # Convert numpy array to list
        
        return heatmap_data
    except Exception as e:
        print("Error processing data:", e)
        return None

# Function to generate PCA plot data
def generate_pca_plot_data():
    # Query to fetch data from the database table
    query = "SELECT * FROM placenta_opioid_counts"

    # Load data from the database into a DataFrame
    try:
        counts_data = pd.DataFrame(execute_query(query))
    except Exception as e:
        print("Error fetching data from the database:", e)

    # Process data and return PCA plot data
    # Example: pca_data = process_pca(counts_data)

    # For demonstration purposes, let's return a placeholder PCA plot data
    pca_data = np.random.rand(50, 2)  # Placeholder data
    return pca_data

# Add CGI response header
print("Content-type: application/json\n")

# Parse form data
form = cgi.FieldStorage()

# Check if the 'action' parameter is provided
if 'action' in form:
    action = form['action'].value
    

    # Checking for the action parameter as 'generate_heatmap'
    if action == 'generate_heatmap':
        # Generate heatmap data
        heatmap_data = generate_heatmap_data()
        print(json.dumps({'heatmap_data': heatmap_data}))
    
    elif action == 'pca':
        # Generate PCA plot data
        pca_data = generate_pca_plot_data()
        print(json.dumps({'pca_data': pca_data.tolist()}))
    
    else:
        print(json.dumps({'error': 'Invalid action specified'}))
else:
    print(json.dumps({'error': 'Action parameter not provided'}))