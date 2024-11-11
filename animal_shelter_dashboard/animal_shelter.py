# animal_shelter.py - Define the AnimalShelter class to interact with the MongoDB database.

from pymongo import MongoClient  # Import MongoClient to connect to MongoDB
from bson.objectid import ObjectId  # Import ObjectId to handle MongoDB document IDs

class AnimalShelter(object):

    # Initializes the AnimalShelter object with connection details to MongoDB.
    def __init__(self, username, password):
        
        # Define the connection variables
        USER = username
        PASS = password
        HOST = 'localhost'  # MongoDB host address
        PORT = 27017        # MongoDB default port
        DB = 'AAC'          # Database name
        COL = 'animals'     # Collection name

        # Initialize the connection to MongoDB using the provided credentials
        self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}/?authSource={DB}')
        self.database = self.client[DB]  # Access the specified database
        self.collection = self.database[COL]  # Access the specified collection within the database

    # Create method - Inserts a new document into the collection. 
    def create(self, data):
        # Validate data before insertion
        if data is not None and self.validate_input(data):
            try:
                # Insert the document into the collection
                self.collection.insert_one(data)
                return True  # Return True if insertion is successful
            except Exception as e:
                print(f"An error occurred: {e}")
                return False  # Return False if an error occurs during insertion
        else:
            raise Exception("Nothing to save, or data failed validation")  # Raise an error if no data is provided or validation fails

    # Read method - Retrieves documents from the collection based on the specified query.
    def read(self, query):
        try:
            # Perform the query and retrieve matching documents
            cursor = self.collection.find(query)
            return list(cursor)  # Return the results as a list of documents
        except Exception as e:
            print(f"An error occurred: {e}")
            return []  # Return an empty list if an error occurs during retrieval

    # Update method - Updates a document in the collection based on the specified query and update data.
    def update(self, query, update_data):
        # Validate update_data before updating
        if query is not None and update_data is not None and self.validate_input(update_data):
            try:
                # Perform the update operation on the matched document
                result = self.collection.update_one(query, {'$set': update_data})
                return result.modified_count > 0  # Return True if at least one document was updated
            except Exception as e:
                print(f"An error occurred: {e}")
                return False  # Return False if an error occurs during update
        else:
            raise Exception("Query and update_data parameters must not be empty or failed validation")  # Raise an error if parameters are missing or validation fails

    # Delete method - Deletes a document from the collection based on the specified query.
    def delete(self, query):
        if query is not None:
            try:
                # Perform the delete operation on the matched document
                result = self.collection.delete_one(query)
                return result.deleted_count > 0  # Return True if a document was deleted
            except Exception as e:
                print(f"An error occurred: {e}")
                return False  # Return False if an error occurs during deletion
        else:
            raise Exception("Query parameter must not be empty")  # Raise an error if no query is provided

    # Validation method to validate input data before CRUD operations
    def validate_input(self, data):
        # Define expected data types and ranges for each field
        expected_fields = {
            'animal_id': str,
            'animal_type': str,
            'breed': str,
            'name': str,
            'age_upon_outcome': str,
            'outcome_type': str,
            'outcome_subtype': str,
            'date_of_birth': str,
            'sex_upon_outcome': str,
            'location_lat': float,
            'location_long': float,
            'age_upon_outcome_in_weeks': int
        }
        
        # Validate each field in the input data
        for field, field_type in expected_fields.items():
            if field in data:
                # Check data type
                if not isinstance(data[field], field_type):
                    print(f"Validation Error: {field} should be of type {field_type.__name__}.")
                    return False

                # Additional validation for specific types
                if field_type == float and not (-90 <= data[field] <= 90 if 'lat' in field else -180 <= data[field] <= 180):
                    print(f"Validation Error: {field} value out of valid range.")
                    return False
                if field_type == int and data[field] < 0:
                    print(f"Validation Error: {field} should be a positive integer.")
                    return False
                
                # Prevent injection attacks by sanitizing strings
                if field_type == str and ';' in data[field]:
                    print(f"Validation Error: {field} contains potentially malicious characters.")
                    return False

        return True
