import streamlit as st
import mysql.connector
import pandas as pd

# Database connection setup
conn = mysql.connector.connect(
    host="localhost",   
    user="root",   
    password="Yazh@2003#",  
    database="clinical_trial_mystery"  
)

cursor = conn.cursor()

# Load and Execute SQL Schema
sql_file_path = r"c:\Users\yazhini.selvakumar\Desktop\Think Solution\sql_mystery.sql"

try:
    with open(sql_file_path, "r") as file:
        schema_sql = file.read()

    # Execute each SQL command separately
    for statement in schema_sql.split(";"):
        if statement.strip():
            cursor.execute(statement)
    
    conn.commit()
except Exception as e:
    st.error(f"Error loading SQL schema: {e}")

# Streamlit app setup
st.title("SQL Mystery Challenge: Missing Drug Report")

st.write("Investigate the data, solve the clues, and uncover the mystery!")

# Display List of Tables in Database
st.markdown("## List of Tables in Database")

try:
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    table_list = [table[0] for table in tables]
    st.write(", ".join(table_list))  # Display tables in a clean format
except Exception as e:
    st.error(f"Error fetching table list: {e}")

# Custom SQL Query Section

custom_query = st.text_area("Enter your SQL query here:")
if st.button("Run Query"):
    
    try:
        cursor.execute(custom_query)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns = columns)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error: {e}")

# Hint System
st.markdown("## Need a Hint")

hints = st.radio(
    "Select a hint step:",
    ["Step 1", "Step 2", "Step 3", "Final Hint"]
)

hint_messages = {
    "Step 1": "Start by exploring the 'reports' table for missing entries in Phase 4.",
    "Step 2": "Check for researchers involved in 'Data Science'.",
    "Step 3": "Look for patients with a high drug response but marked 'Dropped Out'.",
    "Final Hint": "The missing report is linked to a researcher from the Data Science department who accessed Phase 4 reports."
}

# Display the selected hint
if hints in hint_messages:
    st.info(hint_messages[hints]) if hints != "Final Hint" else st.success(hint_messages[hints])

# Display hint correctly
if hints in hint_messages:
    if hints == "Final Hint":
        st.success(hint_messages[hints])
    else:
        st.info(hint_messages[hints])

