#!/usr/bin/env python3

import cgi
import json
import pymysql

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

def generate_whole_table():
    # Construct SQL query to fetch the entire table
    query = "SELECT * FROM placenta_opioid_meta;"
    return execute_query(query)

def generate_searched_table(sample_id):
    # Construct SQL query to fetch table based on user input sample ID
    query = f"SELECT * FROM placenta_opioid_meta WHERE sample_id REGEXP '{sample_id}';"
    result = execute_query(query)
    if result:
        return result  # Return the result if data is found
    else:
        return {"error": "No data found for the sample ID."}  # Return an error message if no data found

# Function to generate filtered table based on user filters
def generate_filtered_table(filters):
    # Initialize an empty list to store the filter conditions
    conditions = []

    # Check each filter option and construct the corresponding SQL query
    if 'Batch' in filters:
        batch_value = filters['Batch']
        if batch_value == 'all':
            conditions.append("1=1")  # No filter applied for 'all'
        else:
            conditions.append(f"Batch = '{batch_value}'")

    if 'OPIOIDCONTROL' in filters:
        opioid_control_value = filters['OPIOIDCONTROL']
        if opioid_control_value == 'all':
            conditions.append("1=1")  # No filter applied for 'all'
        else:
            conditions.append(f"OPIOIDCONTROL = '{opioid_control_value}'")

    if 'SEX' in filters:
        sex_value = filters['SEX']
        if sex_value == 'All':
            conditions.append("1=1")  # No filter applied for 'All'
        else:
            conditions.append(f"SEX = '{sex_value}'")

    if 'Race' in filters:
        race_value = filters['Race']
        if race_value == 'All':
            conditions.append("1=1")  # No filter applied for 'All'
        else:
            conditions.append(f"Race = '{race_value}'")

    if 'Ethnicity' in filters:
        ethnicity_value = filters['Ethnicity']
        if ethnicity_value == 'All':
            conditions.append("1=1")  # No filter applied for 'All'
        else:
            conditions.append(f"Ethnicity = '{ethnicity_value}'")

    if 'OPIOIDTYPE' in filters:
        opioid_type_value = filters['OPIOIDTYPE']
        if opioid_type_value == 'All':
            conditions.append("1=1")  # No filter applied for 'All'
        else:
            conditions.append(f"OPIOIDTYPE = '{opioid_type_value}'")

    # Combine all filter conditions using 'AND' operator
    where_clause = " AND ".join(conditions)

    # Construct the SQL query with the filter conditions
    query = f"SELECT * FROM placenta_opioid_meta WHERE {where_clause};"

    # Execute the SQL query and return the result
    return execute_query(query)

def generate_heatmap():
    query = """
        SELECT gene_id, GROUP_CONCAT(count SEPARATOR ',') AS counts
        FROM counts 
        GROUP BY gene_id;
    """
    result = execute_query(query)

    heatmap_data = []
    for row in result:
        gene_id, counts_str = row
        counts = [float(x) for x in counts_str.split(',')]
        heatmap_data.append([gene_id] + counts)

    return heatmap_data
print("Content-type: application/json\n")

form = cgi.FieldStorage()

if "action" not in form:
    print(json.dumps({"error": "Please provide an action."}))
else:
    action = form.getvalue("action")

    if action == "resetOptions":
        reset_options()
        print(json.dumps({"message": "Options reset successfully."}))

    elif action == "search":
        sample_id = form.getvalue("sampleId")
        if sample_id:
            result = search(sample_id)
            if result:
                print(json.dumps(result))
            else:
                print(json.dumps({"error": "Failed to fetch data for the sample ID."}))
        else:
            print(json.dumps({"error": "Please provide a sample ID for search."}))

    elif action == "applyFilter":
        variance_value = form.getvalue("varianceValue")
        if variance_value:
            apply_filter(variance_value)
            print(json.dumps({"message": "Filter applied successfully."}))
        else:
            print(json.dumps({"error": "Please provide a variance value for filtering."}))

    elif action == "generateContent":
        generate_content()
        print(json.dumps({"message": "Content generated successfully."}))

    elif action == "generateTable":
        result = generate_whole_table()  # Call function to generate the entire table
        print(json.dumps(result))  # Print the result as JSON
    elif action == "generate_heatmap":
        result = generate_heatmap()
        print(json.dumps(result))
