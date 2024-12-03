import streamlit as st
import pandas as pd
import plotly.express as px
import time
from query import query_athena

# Streamlit title
st.title("Data Visualization")

# Refresh interval (in seconds)
REFRESH_INTERVAL = 10

# Main app loop
while True:
    
    sql = """
    SELECT "_timestamp", "accelerometer-x", "accelerometer-y" 
    FROM "phone-data"."phone-data"
    ORDER BY "_timestamp" DESC
    LIMIT 100;
    """
    
    # Query Athena for data
    df = query_athena(sql)
    
    df = df.sort_values(by="_timestamp")

    # Check if the DataFrame is not empty
    if not df.empty:
        # Melt the DataFrame to reshape for line plot
        df_melted = df.melt(id_vars=["_timestamp"], value_vars=["accelerometer-x", "accelerometer-y"], 
                            var_name="Axis", value_name="Value")

        # Create a line plot with different colors for each column
        fig = px.line(
            df_melted, 
            x="_timestamp", 
            y="Value", 
            color="Axis",  # Different color for each axis
            title="Accelerometer Data (X and Y Axes)"
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        # Display the original table
        st.subheader("Data Table")
        st.write(df)
    else:
        st.write("No data available.")

    # Refresh every REFRESH_INTERVAL seconds
    time.sleep(REFRESH_INTERVAL)
    st.rerun()