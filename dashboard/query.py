import os
from dotenv import load_dotenv
import pandas as pd
from requests import request
from pyathena import connect
import pandas as pd
import os

# Load environment variables
load_dotenv()

# Connect to Athena
conn = connect(
    s3_staging_dir=os.environ["AWS_S3_URI"],  # Replace with your S3 bucket for Athena query results
    region_name=os.environ["AWS_DEFAULT_REGION"]
)

def query_athena(sql_query):
    # Execute the query and load the results into a Pandas DataFrame
    df = pd.read_sql(sql_query, conn)
    return df

df = query_athena("SELECT * FROM \"phone-data\".\"phone-data\" limit 100;")

df = df[["_timestamp", "location-speed", "location-latitude", "location-longitude"]]

print(df)