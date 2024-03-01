import random

from faker import Faker
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ServerSelectionTimeoutError, InvalidOperation

NUMBER_OF_RECORDS = 10

def seed_database(db, number):
    """
    Seed the database with a given NUMBER_OF_RECORDS.

    Args:
        db: The database object to seed.
        number: The number of cat records to seed.

    Returns:
        None
    """

    # Set of features for a random choice
    features1 = ["ходить в капці", "ходить в лоток", "ходить навкруги"]
    features2 = ["дає себе гладити", "не дає себе гладити", "може погладити"]
    features3 = ["чорний", "рудий", "білий", "сірий", "тигр смугастий"]

    # creating and inserting a record with fake data
    for _ in range(number):
        fake = Faker()
        name = fake.name().split()[0]
        age = fake.random_int(min=1, max=15)
        features = [
            random.choice(features1),
            random.choice(features2),
            random.choice(features3),
        ]
        try:
            db.cats.insert_one(
                {
                    "name": name,
                    "age": age,
                    "features": features,
                }
            )
        except ServerSelectionTimeoutError:
            print("Unable to connect to the server.")
            client.close()
            return


    print(f"{NUMBER_OF_RECORDS} recordes were added to the database")


def print_all(db):
    """
    Function to print all elements retrieved from the 'cats' collection in the given database.

    Args:
    - db: The database to retrieve data from.

    Returns:
    - None
    """    
    try:
        result = db.cats.find({})
        for el in result:
            print(el)
    except ServerSelectionTimeoutError:
        print("Unable to connect to the server.")
        client.close()

def print_one(db):
    """
    Function to retrieve and print information about a pet from the database.

    Args:
    db: The database object to query.

    Returns:
    None
    """
    pet_name = input("Enter pet name: ").title()
    
    try:
        result = db.cats.find_one({"name": pet_name})
        if result is None:
            print("No such pet")
        else:
            print(result)
    except ServerSelectionTimeoutError:
        print("Unable to connect to the server.")
        client.close()

def update_age(db):
    """
    Update the age of a cat in the database.

    Args:
        db: The database object.

    Returns:
        None
    """    
    try:
        pet_name = input("Enter pet name: ").title()
        new_age = int(input("Enter new age: "))

        db.cats.update_one({"name": pet_name}, {"$set": {"age": new_age}})
        result = db.cats.find_one({"name": pet_name})
        if result is None:
            print("No such pet")
        else:
            print(result)
    except (ValueError, UnboundLocalError):
        print("Wrong age")
        client.close()
    except ServerSelectionTimeoutError:
        print("Unable to connect to the server.")
        client.close()

def add_feature(db):
    """
    Function to add a new feature to a pet in the database.

    Args:
    - db: The database object.

    Returns:
    - None
    """
    pet_name = input("Enter pet name: ").title()
    new_feature = input("Enter new feature: ")
    try:
        db.cats.update_one({"name": pet_name}, {"$push": {"features": new_feature}})
        result = db.cats.find_one({"name": pet_name})
        if result is None:
            print("No such pet")
        else:
            print(result)
    except ServerSelectionTimeoutError:
        print("Unable to connect to the server.")

def delete_record(db):
    """
    Function to delete a record from the database based on the provided pet name.
    The function takes a database object as a parameter.
    This function does not return anything.
    """
    pet_name = input("Enter pet name: ").title()
    try:
        result = db.cats.find_one({"name": pet_name})
        if result is None:
            print("No such pet")
        else:
            db.cats.delete_one({"name": pet_name})
            result = db.cats.find_one({"name": pet_name})
            if result is None:
                print("Record deleted")
            else:
                print("There is an error")
    except ServerSelectionTimeoutError:
        print("Unable to connect to the server.")
        client.close()

def delete_all_records(db):
    """
	Function to delete all records in the given database.

	Args:
	    db: The database to delete records from.

	Returns:
	    None
	"""

    try:
        result = db.cats.find({})
        if len(list(result)) == 0:
            print("Database is empty")
        else:
            db.cats.delete_many({})
            result = db.cats.find({})
            if len(list(result)) == 0:
                print("All records deleted")
            else:
                print("There is an error")
    except ServerSelectionTimeoutError:
        print("Unable to connect to the server.")

if __name__ == "__main__":
    # connecting to a running docker container
    uri = 'mongodb://localhost:27015/'
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.module_06

    #performing tasks one-by-one
    seed_database(db, NUMBER_OF_RECORDS)

    print_all(db)

    print_one(db)

    update_age(db)

    add_feature(db)

    delete_record(db)

    delete_all_records(db)

    #closing the connection
    try:
        client.close()
    except InvalidOperation:
        print("Client already closed")
    