# data_processing.py - Handle data retrieval and processing.

import pandas as pd
from animal_shelter import AnimalShelter  # Import the AnimalShelter class for database interaction

def get_data(filter_type):
    """
    Connects to MongoDB, retrieves data based on the specified filter type, 
    and returns it as a DataFrame.

    Parameters:
        filter_type (str): The type of rescue filter to apply.

    Returns:
        pd.DataFrame: A DataFrame containing the filtered data.
    """
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

    # Retrieve data from the MongoDB collection based on the query
    data = db.read(query)

    # Convert the retrieved data (list of dictionaries) to a pandas DataFrame
    df = pd.DataFrame.from_records(data)

    # Remove the '_id' column if it exists to avoid potential issues in display and processing
    if '_id' in df.columns:
        df.drop(columns=['_id'], inplace=True)

    return df  # Return the filtered data as a DataFrame

