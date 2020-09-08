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

conn = None  # type: MongoClient
logger = myutils.get_logger(log_name="mongo_service")

def close_conn():
    if conn is not None:
        conn.close()


def find_by_id(idd, db_name="data", collection="car"):
    db = get_mongo_conn()[db_name]
    coll = db[collection]
    result = coll.find_one({"_id": idd})
    return result


def is_exist(idd, db_name="data", collection="car"):
    db = get_mongo_conn()[db_name]
    coll = db[collection]
    return coll.find_one({"_id": idd}, {"_id": 1}) is not None


def get_mongo_conn() -> MongoClient:
    global conn
    if conn is None:
        conn = MongoClient(db_url)
    return conn


def get_remote_mongo_conn(user=db_user, pswd=db_pswd, host=db_domain, port=db_port) -> MongoClient:
    return MongoClient("mongodb://{}:{}@{}:{}/".format(user, pswd, host, port))


def insert_data(db_name: str, collection: str, json_data):
    json_data["create_time"] = myutils.get_mongo_time()
    db = get_mongo_conn()[db_name]
    coll = db[collection]
    return coll.insert_one(json_data)


def insert_many(db_name: str, collection: str, json_data: list):
    for data in json_data:
        data["create_time"] = myutils.get_mongo_time()
    db = get_mongo_conn()[db_name]
    coll = db[collection]
    return coll.insert_many(json_data)


def update_date(db_name: str, collection: str, json_data):
    db = get_mongo_conn()[db_name]
    coll = db[collection]
    return coll.update_one({"_id": json_data["_id"]}, {"$set": json_data})


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


def test():
    remote_conn = get_remote_mongo_conn(user="tibame123", pswd="tibame", host="10.120.26.31", port="27017")
    # cursor = get_mongo_conn().data.uniform.find({"checked": {"$ne": 1}})  # .limit(10)
    # for item in cursor:
        ################################################
        # 檢查品牌
        # if item["brand"] not in myutils.brand_tmp:
        #     item["checked"] = 1
        #     update_date("data", "uniform", item)
        #     print(item["brand"])
        # if item["price"] is not None:
        #     str_price = str(item["price"])
        #     if item["price"] > 1000:
        #         print(item)
        ##############################################
        # #轉資料
        # item = myutils.uni_form_data(item)
        # a = insert_data("data", "uniform", item)
        # print(a, "success")
        #############################################
        # 寫遠端DB
        # collection = remote_conn["Allcars"]["usedcar"]
        # success = collection.insert_one(item)
        # print(success, "write success!")
        #############################################
        # 修復本地型號

    coll = get_mongo_conn()["data"]["car"]
    cursor = coll.find({"廠牌": "Mercedes-Benz[sl]賓士"}, {"型號": 1, "型號a": 1})
    count = 0
    for car in cursor:
        if car.get("型號", None) is None:
            update_data = {"_id": car["_id"], "型號": "fix_" + car["型號a"]}
            # print(update_data)
            # result = update_date("data", "car", update_data)
            logger.warn(str(car) + "no type")
        else:
            remote_coll = remote_conn["Allcars"]["usedcar_copy"]
            rcursor = remote_coll.find({"id": car["_id"], "source": "yahoo"})
            # print(rcursor.count(), "  ", rcursor)
            if rcursor.count() > 1:
                logger.warn("id: " + car["_id"] + "more than one data")
            else:
                remote_car = rcursor.next()
                type_str = car["型號"]
                if type_str.find("fix_") != -1:
                    type_str = type_str[4:]
                update_data2 = {"type": type_str}
                logger.info("update id: " + str(remote_car["_id"]) + " to " + str(update_data2))
                remote_coll.update({"_id": remote_car["_id"]}, {"$set": update_data2})
        # count += 1
        # if count == 10:
        #     break


def update_8891_car_type():
    # 取得公共資料庫中的8891 id，存入本地mongodb
    remote_conn = get_remote_mongo_conn(user="tibame123", pswd="tibame", host="10.120.26.31", port="27017")
    collection = remote_conn["Allcars"]["usedcar_copy"]
    cursor = collection.find({"brand": "Mercedes-Benz", "source": "8891"}, {"_id": 1, "id": 1})
    start_time = datetime.datetime.now()
    for item in cursor:
        if not is_exist(item["id"], collection="8891"):
            result = insert_data("data", "8891", {"_id": item["id"]})
            print(result, "insert data success!")
        else:
            print(item["id"], "already exist!")
    print("spend time :", datetime.datetime.now() - start_time)


def main():
    # test = {"_id": "1", "name": "allen", "age": 88, "gender": "M"}
    # insert_data("data", "person", test)
    try:
        test()
        # update_8891_car_type()
    except Exception as err:
        raise err
    finally:
        close_conn()
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
