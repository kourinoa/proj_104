from pymongo import MongoClient
from bson.objectid import ObjectId


db_user = "admin"
db_pswd = "123456"
db_domain = "localhost"
db_port = "27017"
db_url = "mongodb://{}:{}@{}:{}/".format(db_user, db_pswd, db_domain, db_port)


def get_mongo_conn() -> MongoClient:
    return MongoClient(db_url)


def insert_data(db_name, collection: str, json_data):
    db = get_mongo_conn()[db_name]
    coll = db[collection]
    coll.insert_one(json_data)



def main():
    test = {"_id": "1", "name": "allen", "age": 88, "gender": "M"}
    insert_data("data", "person", test)
    cursor = get_mongo_conn().data.person.find({})
    print([d for d in cursor])


if __name__ == "__main__":
    main()