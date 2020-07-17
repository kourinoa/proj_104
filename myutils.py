import requests
import datetime
import json
import os
from urllib import parse
from bs4 import BeautifulSoup


def url_encoding(url: str) -> str:
    return parse.quote(url)


def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def get_session() -> requests.session:
    return requests.session()


def get_header() -> dict:
    return {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.61 Safari/537.36"}


def get_jobid_by_url(job_url) -> str:
    a = job_url[job_url.rfind("/") + 1: job_url.rfind("?")]
    # print(a)
    return a


def get_mongo_time() -> datetime.datetime.utcnow:
    return datetime.datetime.utcnow()


def get_datetime_str() -> str:
    '''
    取得當前時間，mysql格式
    :return:
    '''
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_json_file(json_data, filename):
    try:
        with open("../dict/{}".format(filename), "w") as file:
            file.write(json.dumps(json_data, ensure_ascii=False))
    except FileNotFoundError as e:
        print(e)
        print(os.getcwd())


def write_pic_file(file_path: str, pic):
    d = file_path[0:file_path.rfind("/")]
    if not os.path.exists(d):
        os.makedirs(d)
    with open(file=file_path, mode="wb") as file:
        file.write(pic)
        return file_path


def write_text_file(file_path: str, content):
    d = file_path[0:file_path.rfind("/")]
    if not os.path.exists(d):
        os.makedirs(d)
    with open(file=file_path, mode="w") as file:
        file.write(content)


def uni_form_data(ori_data: dict) -> dict:
    key_mappping = {"廠牌": "brand", "型號a": "type", "mlink": "link",
                    "排氣量": "cc", "引擎燃料": "gas", "變速系統": "sys",
                    "外觀車色": "color", "auto_drive_km": "miles", "auto_build_year": "year",
                    "price": "price", "location": "locate", "poster": "seller",
                    "電動座椅": "auto_chair", "多媒體影音": "media", "倒車顯影": "back_screen",
                    "天窗": "window", "HID氙氣頭燈": "hid", "恆溫空調": "air_con",
                    "六安全氣囊以上": "safe_bag", "免鑰匙啟動": "keyless", "導航系統": "gps",
                    "LED頭燈": "led", "防滑循跡系統": "trc", "車道偏移警示": "ldws",
                    "自動煞車系統": "aeb", "定速": "ss", "抬頭顯示器": "hud", "_id": "id"}

    missing_key = ["power", "l_chair", "cd", "back_radar", "abs", "alu", "tcs", "acc", "auto_windows", "auto_side",
                   "alert", "tpms", "es", "isofix", "multi_wheel", "auto_park", "people", "silde_door", "female_used",
                   "turbo", "warranty", "fog_lights", "blind_spot", "electric_tailgate", "whole_window", "lcd",
                   "shift_paddles", "epb"]
    uniform_data = {}  # 重新整理過key值的資料
    for key in ori_data:
        # print("find key :", key, "result :", )
        if key_mappping.get(key, None) is not None:
            uniform_data[key_mappping[key]] = ori_data[key]
            # 去除廠牌的中文顯示
            if key == "廠牌":
                tmp = ori_data[key]
                uniform_data[key_mappping[key]] = tmp[:tmp.find("[sl]")]
            # 去除cc
            if key == "排氣量":
                tmp = ori_data[key]
                tmp = tmp.replace("cc", "")
                uniform_data[key_mappping[key]] = tmp
            if key == "price":
                tmp = ori_data[key]
                try:
                    tmp = tmp.replace(",", "").strip()
                    tmp = round(float(tmp) / 10000, 1)
                except ValueError as err:
                    print(tmp, "_" * 20)
                    tmp = None
                    # raise err
                uniform_data[key_mappping[key]] = tmp
    for mkey in missing_key:
        uniform_data[mkey] = None
    uniform_data["source"] = "yahoo"
    return uniform_data


brand_tmp = ["Alfa Romeo",
             "Aston Martin",
             "Audi",
             "Bentley",
             "BMW",
             "Bugatti",
             "Buick",
             "Cadillac",
             "Chery",
             "Chrysler",
             "Citroen",
             "CMC",
             "Daihatsu",
             "DFSK",
             "DS",
             "Ferrari",
             "Fiat",
             "Ford",
             "Honda",
             "Hyundai",
             "Infiniti",
             "IVECO",
             "Jaguar",
             "Kia",
             "Koenigsegg",
             "Lamborghini",
             "Land Rover",
             "Lexus",
             "Lotus",
             "Luxgen",
             "Mahindra",
             "Maserati",
             "Mazda",
             "McLaren",
             "Mercedes-Benz",
             "Mini",
             "Mitsubishi",
             "Morgan",
             "Nissan",
             "Opel",
             "Pagani",
             "Peugeot",
             "Porsche",
             "Proton",
             "Renault",
             "Rolls-Royce",
             "Saab",
             "Skoda",
             "Smart",
             "Ssangyong",
             "Subaru",
             "Suzuki",
             "Tesla",
             "Tobe",
             "Toyota",
             "Volkswagen",
             "Volvo",
             "Chevrolet",
             "Dodge",
             "Formosa",
             "Hummer",
             "Isuzu",
             "Jeep",
             "Volkswagen Commercial Vehicles"
             ]


def main():
    # a = ['54812', '54804', '54805', '54806', '54801', '54802', '54799', '65342', '49523']
    # tmp = ""
    # for i, j in enumerate(a):
    #     tmp += j
    #     if i % 4 == 0 or i % len(a) == 0:
    #         print(tmp)
    #         tmp = ""
    #     else:
    #         tmp += ","
    a = "adbdd"
    print(a[:a.find("/")])


if __name__ == "__main__":
    main()
