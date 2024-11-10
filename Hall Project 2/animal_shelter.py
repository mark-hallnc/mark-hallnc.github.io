from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
#     def __init__(self):

        # Connection Variables
        #
#         USER = 'aacuser'
#         PASS = '12345SNHU'
        
        USER = username
        PASS = password
        HOST = 'localhost'
        # HOST = 'nv-desktop-services.apporto.com'
        PORT = 27017
        # PORT = 32210
        DB = 'AAC'
        COL = 'animals'
        #
        
        # # Initialize Connection
        self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}/?authSource={DB}')
        self.database = self.client[DB]
        self.collection = self.database[COL]

        # #
        # self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        # self.database = self.client['%s' % (DB)]
        # self.collection = self.database['%s' % (COL)]

    # Create method
    def create(self, data):
        if data is not None:
            try:
                self.collection.insert_one(data)  # data should be dictionary 
                return True
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

            
    # Read method
    def read(self, query):
        try:
            """Queries for documents from the specified MongoDB database and collection."""
            cursor = self.collection.find(query)
            return list(cursor)
        except Exception as e:
            print(f"An error occurred: {e}")
            return[]

        
    # Update method
    def update(self, query, update_data):
        if query is not None and update_data is not None:
            try:
                result = self.collection.update_one(query, {'$set': update_data})
                return result.modified_count > 0
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        else:
            raise Exception("Query and update_data parameters must not be empty")

            
    # Delete method
    def delete(self, query):
        if query is not None:
            try:
                result = self.collection.delete_one(query)
                return result.deleted_count > 0
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        else:
            raise Exception("Query parameter must not be empty")
