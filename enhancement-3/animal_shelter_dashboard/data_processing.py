# data_processing.py - Handle data retrieval and processing.

import pandas as pd
from animal_shelter import AnimalShelter  # Import the AnimalShelter class for database interaction
import time

def get_data(filter_type):
   
    # Database connection credentials
    username = "newUsername"
    password = "newPassword123"

    # Initialize the AnimalShelter object with authentication
    db = AnimalShelter(username, password)

    # Define filter queries based on the selected filter type
    query = {}
    if filter_type == 'Water Rescue':
        query = {
            "animal_type": "Dog",
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]}
        }
    elif filter_type == 'Mountain or Wilderness Rescue':
        query = {
            "animal_type": "Dog",
            "breed": {"$in": ["German Shepherd", "Belgian Malinois", "Bloodhound", "Rottweiler"]}
        }
    elif filter_type == 'Disaster or Individual Tracking':
        query = {
            "animal_type": "Dog",
            "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound"]}
        }
    elif filter_type == 'Reset':
        query = {}  # No filter applied, retrieves all records

    # Record the start time before executing the query
    # For verification of query performance
    start_time = time.time()

    # Retrieve data from the MongoDB collection based on the query
    data = db.read(query)

    # Calculate and print the query execution time
    # For verification of query performance
    execution_time = time.time() - start_time
    print(f"Query executed in: {execution_time:.4f} seconds")

    # Convert the retrieved data (list of dictionaries) to a pandas DataFrame
    df = pd.DataFrame.from_records(data)

    # Remove the '_id' column if it exists to avoid potential issues in display and processing
    if '_id' in df.columns:
        df.drop(columns=['_id'], inplace=True)

    return df  # Return the filtered data as a DataFrame

