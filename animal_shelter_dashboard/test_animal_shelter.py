from animal_shelter import AnimalShelter

# Database credentials
username = "newUsername"
password = "newPassword123"

# Instantiate the AnimalShelter class
db = AnimalShelter(username, password)

# Test data
valid_data = {
    "animal_id": "A123456",
    "animal_type": "Dog",
    "breed": "Labrador Retriever Mix",
    "name": "Buddy",
    "age_upon_outcome": "3 years",
    "outcome_type": "Adoption",
    "outcome_subtype": "Neutered",
    "date_of_birth": "2018-01-01",
    "sex_upon_outcome": "Male",
    "location_lat": 30.7128,
    "location_long": -97.5654,
    "age_upon_outcome_in_weeks": 156
}

invalid_data = {
    "animal_id": "A123456",
    "animal_type": "Dog",
    "breed": "Labrador Retriever Mix; DROP TABLE;",  # Potentially malicious data
    "name": "Buddy",
    "age_upon_outcome": "3 years",
    "outcome_type": "Adoption",
    "outcome_subtype": "Neutered",
    "date_of_birth": "2018-01-01",
    "sex_upon_outcome": "Male",
    "location_lat": 30.7128,
    "location_long": -97.5654,
    "age_upon_outcome_in_weeks": 156
}

updated_data = {
    "age_upon_outcome": "4 years",
    "outcome_type": "Transfer",
    "sex_upon_outcome": "Spayed Female"
}

invalid_update_data = {
    "outcome_type": "Transfer; DROP DATABASE;",  # Potentially malicious update
    "age_upon_outcome": "4 years",
    "sex_upon_outcome": "Spayed Female"
}

# Test Functions
def test_create_with_valid_data():
    print("\nTesting create method with valid data:")
    result = db.create(valid_data)
    print(f"Expected: True, Got: {result}")

def test_create_with_invalid_data():
    print("\nTesting create method with invalid data:")
    try:
        result = db.create(invalid_data)
        print(f"Expected: False, Got: {result}")
    except Exception as e:
        print(f"Validation Error: {str(e)}")

def test_update_with_valid_data():
    print("\nTesting update method with valid data:")
    query = {"animal_id": "A123456"}
    result = db.update(query, updated_data)
    print(f"Expected: True, Got: {result}")

def test_update_with_invalid_data():
    print("\nTesting update method with invalid data:")
    query = {"animal_id": "A123456"}
    try:
        result = db.update(query, invalid_update_data)
        print(f"Expected: False, Got: {result}")
    except Exception as e:
        print(f"Validation Error: {str(e)}")

def test_read_data():
    print("\nTesting read method:")
    query = {"animal_id": "A123456"}
    result = db.read(query)
    print(f"Expected: List of records, Got: {result}")

def test_delete_data():
    print("\nTesting delete method:")
    query = {"animal_id": "A123456"}
    result = db.delete(query)
    print(f"Expected: True if document exists, Got: {result}")

# Run tests
if __name__ == "__main__":
    # Test create method
    test_create_with_valid_data()
    test_create_with_invalid_data()

    # Test update method
    test_update_with_valid_data()
    test_update_with_invalid_data()

    # Test read method
    test_read_data()

    # Test delete method
    test_delete_data()
