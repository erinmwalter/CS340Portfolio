import os
#building DAL class for AAC CRUD functions
from pymongo import MongoClient
class AnimalShelterDAL:
    #constructor
    #this takes the connection url in as an input and sets the function url to this url
    #this url will need to have username, password, and port already in it, in this format:
    #'mongodb://{username}:{password}@127.0.0.1:{port}'
    def __init__(self, url):
        self.url = url
    
    #alternate constructor
    #this constructor takes username, password, and port number as params
    #and will construct the connection url from these
    def __init__(self, username, password, port):
        self.url = f'mongodb://{username}:{password}@127.0.0.1:{port}'
            
    #print out all databases 
    #method is called for user to see all possible databases that they have access to
    def showAllDatabases(self):
        return (self.connection.list_database_names())
        
    #connection to verify login successful and DBs are shown 
    #takes in the database to choose as a parameter and sets
    #the database of the function equal to what is chosen.
    def connect(self, project):
        self.connection = MongoClient(self.url)
        #tries to see if able to connect to specified database
        try:
            self.db = self.connection[project]
           # print(self.db)
            return f'connected to database: {project}'
        except Exception:
            return f'Error-unable to connect to database: {project}: {Exception}'
               
    #method to insert ONE entry into DB
    #takes collection name and dictionary entry to insert into the collection as parameters
    #returns true if successful and false if unsuccessful
    def create(self, collection, entry):
        toReturn = False #defaults to false, will only return true if successfully inserts
        #first do a null check to make sure that entry isn't empty
        if entry is not None:
            try:
                #tries to find the collection and then insert
                self.db.validate_collection(collection)
                coll = self.db[collection]
                result = coll.insert_one(entry)
                toReturn = True
            except Exception:
                #if collection not found, throws exception
                print("No such collection")
        else:
            #if entry is empty, throws exception
            raise Exception("No data in entry param, unable to insert into db")
            
        return toReturn
    
    #will read one with given query params in entry, entry is dictionary
    #You can enter multiple parameters in here, for instance entry = {"id":1, "name":"Lucy", "type":"Dog"}
    #query must be in dictionary format for items in database to be read with given query
    def read(self, collection, entry):
        toReturn = '...'
        #if entry is not None:
        try:
            #tries to find collection then look for entries that match that entry query provided
            self.db.validate_collection(collection)
            coll = self.db[collection]
            foundItem = coll.find(entry,{"_id":0})
            toReturn = foundItem
            return toReturn
        except Exception:
            #if no collection found, throws exception
            print("No such collection")
            return Exception
        #else:
            #raise Exception("Animal Id param empty, unable to find by Id")
        #return Exception
    
    #function to update entries
    #collection parameter specifies which collection to find/update entries for
    #takes query as a parameter, which is a dictionary of key/value pairs to find items in database
    #that match to update
    #entry parameter is a dictionary of key/value pairs, and items that are found matching the query
    #will be updated to these entry values
    def update(self, collection, query, entry):
        toReturn = '....'
        if query is not None and entry is not None:
            #now try and find this in collection, also make sure collection valid
            try:
                #tries to find collection then look for entry
                self.db.validate_collection(collection)
                coll = self.db[collection]
                #uses provided query and updates all k/v pairs in entry param in db
                updatedItems = coll.update(query, {"$set": entry})
                toReturn = updatedItems
                return toReturn
            except Exception:
                #if no collection found, throws exception
                #returns this exception as well
                print("No such collection")
                return 'No such collection'
        elif entry is not None:
            #if query is empty, don't do this update as will do db wide update
            raise Exception("query param empty, no items to update")
            return Exception
        else:
            #if the entry is empty meaning there were no parameters given to update
            #then this will return the following 
            print("Nothing to update, entry is empty, exiting update method")
            return 'Nothing to update, entry is empty, exiting update method'
        
    #function to delete one entry by query
    #takes collection in as a param to specify which collection to use/delete from
    #takes a query which is a dictionary of key/value pair, will delete all that match
    #this query from the database.
    #this uses delete_many in case there are more than one that meet the query params
    #be careful with the params you choose!
    def delete(self, collection, query):
        #first do null check to make sure query not empty
        toReturn = "..."
        if query is not None:
            #now try and find this in collection, also make sure collection valid
            try:
                #tries to find collection then look for entry
                self.db.validate_collection(collection)
                coll = self.db[collection]
                result = coll.delete_many(query)
                toReturn = result.raw_result
                return toReturn
            except Exception:
                #if no collection found, throws exception and returns exception
                print("No such collection")
                return Exception
        else:
            #if query is empty, will not do delete and returns the following exception
            raise Exception("Query param empty, unable to delete since no query given") 
            return Exception