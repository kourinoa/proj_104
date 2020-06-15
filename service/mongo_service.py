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


def see_result(cursor):

    title = ""
    content = ""
    result_set = [d for d in cursor]
    one = result_set[1:2]
    # print(one)
    for d in one:
        for key in d:
            # print(key)
            temp = str(d[key])
            l = len(temp)
            if len(temp) > 30:
                temp = temp[:27] + "..."
                l = 30
            if l < len(key):
                l = len(key)
            fmt = "{:" + str(l) + "s}"
            content += fmt.format(temp)
            content += " | "
            title += fmt.format(key)
            title += " | "

    print(title)
    print(content)
    for d in result_set[2:]:
        content = ""
        for one in d:
            temp = str(d[one])
            if len(temp) > 30:
                temp = temp[:30] + "..."
            content += temp
            content += " | "
        print(content)


def main():
    # test = {"_id": "1", "name": "allen", "age": 88, "gender": "M"}
    # insert_data("data", "person", test)
    cursor = get_mongo_conn().data.car.find({})
    see_result(cursor)


if __name__ == "__main__":
    main()
