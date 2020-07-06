from pymongo import MongoClient
from bson.objectid import ObjectId
import myutils
import pandas as pd
import json
import datetime

db_user = "admin"
db_pswd = "123456"
db_domain = "localhost"
db_port = "27017"
db_url = "mongodb://{}:{}@{}:{}/".format(db_user, db_pswd, db_domain, db_port)

conn = None


def find_by_id(idd, db_name="data", collection="car"):
    db = get_mongo_conn()[db_name]
    coll = db[collection]
    result = coll.find_one({"_id": idd})
    return result


def is_exist(idd, db_name="data", collection="car"):
    db = get_mongo_conn()[db_name]
    coll = db[collection]
    return coll.find_one({"_id": idd}, {"_id": 1})


def get_mongo_conn() -> MongoClient:
    global conn
    if conn is None:
        conn = MongoClient(db_url)
    return conn


def insert_data(db_name: str, collection: str, json_data):
    json_data["create_time"] = myutils.get_mongo_time()
    db = get_mongo_conn()[db_name]
    coll = db[collection]
    return coll.insert_one(json_data)


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
    for item in cursor:
        result = insert_data("data", "uniform", myutils.uni_form_data(item))
        print(item["_id"], "result", result, "transform success!")
    f_list = []
    e_list = []
    # for i in range(1, 20):
    #     t1 = myutils.get_mongo_time()
    #     v = find_by_id("100804245348")
    #     t2 = myutils.get_mongo_time()
    #     v2 = is_exist("100804245348")
    #     t3 = myutils.get_mongo_time()
    #     f_list.append(float(str(t2-t1)[-6:]))
    #     e_list.append(float(str(t3-t2)[-6:]))
    #     # print(f_list)
    #     # print(e_list)
    # print("find by id time:", sum(f_list)/len(f_list), " exist time : ", sum(e_list)/len(e_list))
    # print(cursor)
    # datetime.datetime.strftime()
    # for key in cursor:
    #     if type(cursor[key]) != str:
    #         print(key, type(cursor[key]))


if __name__ == "__main__":
    main()
