import myutils
from bs4 import BeautifulSoup
import json
from service import mongo_service


def search_page(cata, input_data, action, url, ss):
    input_data["catb"] = cata
    print(input_data)

    search_header = myutils.get_header()
    search_header["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    search_header["Accept-Encoding"] = "br, gzip, deflate"
    search_header["Host"] = "tw.usedcar.yahoo.com"
    search_header["Accept-Language"] = "zh-tw"
    search_header["Referer"] = "https://tw.usedcar.yahoo.com/"
    search_header["Connection"] = "keep-alive"

    searchreq = ss.get(url + action, params=input_data, headers=search_header)
    print(searchreq.url)
    soup2 = myutils.get_soup(searchreq.text)
    total_car_num = soup2.select_one("div .infol.mei-u em").text
    meta_search(ss, searchreq.url, cata, total_car_num)
    # print("__________________________")
    # print(soup2.prettify())


def meta_search(ss, url, cata, total_car_num):
    search_header = myutils.get_header()
    search_header["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
    search_header["Accept"] = "*/*"
    search_header["Host"] = "tw.usedcar.yahoo.com"
    search_header["Accept-Language"] = "zh-tw"
    search_header["Accept-Encoding"] = "br,gzip,deflate"
    search_header["Origin"] = "https://tw.usedcar.yahoo.com"
    search_header["Referer"] = url
    search_header["Connection"] = "keep-alive"
    search_header["Content-Length"] = "56"
    search_header["X-Requested-With"] = "XMLHttpRequest"
    post_data = {"MIME 類型": "application/x-www-form-urlencoded; charset=UTF-8",
                 "cata": "000000515224",
                 "cateid": "000000515235",
                 "action": "dataPrepare"}
    req = ss.post(url="https://tw.usedcar.yahoo.com/search/search_services", headers=search_header, data=post_data)
    json_data = json.loads(req.text)
    print("meta search---------------------")
    # print(json_data)
    car_search(ss, url, cata, total_car_num)


def car_search(ss, url, cata, total_car_num):
    search_header = myutils.get_header()
    search_header["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
    search_header["Accept"] = "*/*"
    search_header["Host"] = "tw.usedcar.yahoo.com"
    search_header["Accept-Language"] = "zh-tw"
    search_header["Accept-Encoding"] = "br,gzip,deflate"
    search_header["Origin"] = "https://tw.usedcar.yahoo.com"
    search_header["Referer"] = url
    search_header["Connection"] = "keep-alive"
    search_header["Content-Length"] = "268"
    search_header["X-Requested-With"] = "XMLHttpRequest"
    post_data = {"MIME 類型": "application/x-www-form-urlencoded; charset=UTF-8",
                 "cata": "000000515224",
                 "catb": "000000515235",
                 "undedup": 0,
                 "unspc": 0,
                 "areaa": "tw",
                 "sort": 3,
                 "total": total_car_num,
                 "cp": 1,
                 "ppa": 30,
                 "pa": 10,
                 "type": "srplist",
                 "vmode": 0,
                 "action": "srplistquery"}
    req = ss.post(url="https://tw.usedcar.yahoo.com/search/search_services", headers=search_header, data=post_data)
    json_data = json.loads(req.text)
    print("car search---------------------")
    # print(json_data)

    for car in json_data["data"][1:2]:
        url = car["mlink"]
        r = ss.get(url, headers=myutils.get_header())
        print("get car detail : url", url)
        car_soup = myutils.get_soup(r.text)
        print(car_soup.prettify())
        # 車輛廠牌分類
        car_brand = [a.text for a in car_soup.select("div.itemhd a")]
        car["新舊"] = car_brand[0]
        car["車型"] = car_brand[1]
        car["廠牌"] = car_brand[2].replace("/", "sl")
        car["型號a"] = car_brand[3]
        car["型號"] = car_brand[4]
        # 車輛狀態
        car_status = []
        for i in car_soup.select("div#ycoptions ul#itemAttrs li")[0:3]:
            for j in i:
                car_status.extend(j.select("td"))
        print("car_status", car_status)
        for i in range(0, len(car_status), 2):
            if "hide" not in car_status[i]["class"]:
                car[car_status[i].text] = car_status[i + 1].text
        # 車輛配備
        car_equipment = car_soup.select("div#ycoptions ul#itemAttrs li.col2 td span")
        print("car_equipment", car_equipment)
        for i in car_equipment:
            car[i.text] = 1
        # 車輛圖案
        car_pic = car_soup.select_one("div#ycitemslideshow div.sft input")
        car_pic = car_pic["value"].replace("'", '"')  # 取value屬性的值，接着用雙引號取代單引號
        car_pic = json.loads(car_pic)  # 將文字轉成物件
        car_pic = [pic["i"] for pic in car_pic]
        print("car_pic", car_pic)
        car["pic"] = car_pic
        # get_picture(ss, car_pic["href"])
        # 寫入圖片到本地
        pic_path = "./pic/{}/{}/{}/{}/{}_{}_{}_{}".format(car["廠牌"], car["型號a"], car["型號"], car["auto_build_year"], car["廠牌"], car["型號a"], car["型號"], car["auto_build_year"])
        car["pic"] = []
        for i, pic in enumerate(car_pic):
            q = ss.get(url=pic, headers=myutils.get_header())
            car["pic"].append({"url": pic, "file_path": myutils.write_pic_file(pic_path + "_{}.jpg".format(i), q.content)})
        print(car)
        # car["_id"] = car.pop("mid")
        # car.remove_key("mid")
        # print(car)
        # mongo_service.insert_data("data", "car", car)


# def get_picture(ss, ref):
#     header = myutils.get_header()
#     header["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
#     header["Accept"] = "*/*"
#     header["Host"] = "tw.usedcar.yahoo.com"
#     header["Accept-Language"] = "zh-tw"
#     header["Accept-Encoding"] = "br,gzip,deflate"
#     header["Origin"] = "https://tw.usedcar.yahoo.com"
#     header["Referer"] = myutils.url_encoding(ref)
#     header["Connection"] = "keep-alive"
#     header["Content-Length"] = "110"
#     header["X-Requested-With"] = "XMLHttpRequest"
#     post_data = {"MIME 類型": "application/x-www-form-urlencoded; charset=UTF-8",
#                  "undedup": 0,
#                  "unspc": 0,
#                  "category_id": 12012841,
#                  "price": 2980000.00,
#                  "action": "itemADs"}
#     r = ss.post(url="https://tw.usedcar.yahoo.com/item/characteristic_item", headers=header, data=post_data)
#     print("get pic", json.loads(r.text)["data"])


def main():
    url = "https://tw.usedcar.yahoo.com"
    ss = myutils.get_session()
    req = ss.get(url=url, headers=myutils.get_header())
    soup = BeautifulSoup(req.text, "html.parser")
    # print(soup.prettify())
    # 車型
    car_type_list = soup.select("form select[name='catb'] option")
    car_type_dict = {t["value"]: t.text for t in car_type_list if len(t["value"]) > 0}
    # 廠牌
    brand_list = soup.select("form select[name='catid'] option")
    brand_dict = {t["value"]: t.text for t in brand_list if len(t["value"]) > 0}

    input_data = {i["name"]: i["value"] for i in soup.select("form input[type='hidden']")}
    print(brand_dict.values())
    action = soup.select_one("form")["action"]
    search_page("000000515235", input_data, action, url, ss)


if __name__ == "__main__":
    main()