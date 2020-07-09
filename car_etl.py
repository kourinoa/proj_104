import myutils
from bs4 import BeautifulSoup
import json
from service import mongo_service
import time
import random


def search_page(cata, input_data, action, url, ss, kw=""):
    if len(kw) == 0:
        input_data["catb"] = cata
    input_data["kw"] = kw
    print(input_data)

    search_header = myutils.get_header()
    search_header["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    search_header["Accept-Encoding"] = "br, gzip, deflate"
    search_header["Host"] = "tw.usedcar.yahoo.com"
    search_header["Accept-Language"] = "zh-tw"
    search_header["Referer"] = "https://tw.usedcar.yahoo.com/"
    search_header["Connection"] = "keep-alive"

    searchreq = ss.get(url + action, params=input_data, headers=search_header)
    print("search page", searchreq.url)
    soup2 = myutils.get_soup(searchreq.text)
    total_car_num = soup2.select_one("div .infol.mei-u em").text
    print("total num:", total_car_num)
    meta_search(kw, ss, searchreq.url, cata, total_car_num)
    # print("__________________________")
    # print(soup2.prettify())


def meta_search(kw, ss, url, cata, total_car_num):
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
                 "cateid": cata,
                 "action": "dataPrepare"}
    req = ss.post(url="https://tw.usedcar.yahoo.com/search/search_services", headers=search_header, data=post_data)
    json_data = json.loads(req.text)
    print("meta search---------------------")
    # print(json_data)
    car_search(ss, url, cata, total_car_num, kw)


def car_search(ss, url, cata, total_car_num, kw):
    each_page = 30
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
                 "catb": cata,
                 "undedup": 0,
                 "unspc": 0,
                 "areaa": "tw",
                 "sort": 3,
                 "total": total_car_num,
                 "cp": 1,
                 "ppa": each_page,
                 "pa": 10,
                 "type": "srplist",
                 "vmode": 0,
                 "action": "srplistquery",
                 "kw": kw}
    if len(kw) > 0:
        post_data["catid"] = "000000515224"
    print("car search---------------------")
    # print(json_data)
    total_page = (int(total_car_num) // each_page) + 1
    for page in range(1, total_page + 1):
        print("total_page:", total_page, "current page :", page)
        post_data["cp"] = page
        try:
            req = ss.post(url="https://tw.usedcar.yahoo.com/search/search_services", headers=search_header,
                          data=post_data)
            json_data = json.loads(req.text)
        except Exception as err:
            print("-" * 30)
            file_path = "./err/msg/{}.txt".format(kw + str(page))
            myutils.write_text_file(file_path=file_path, content=req.text)
            # error_log = {
            #     "err": err,
            #     "data": file_path
            # }
            # mongo_service.insert_data(collection="err", db_name="data", json_data=json.dumps(error_log))
            # raise err
        try:
            for car in json_data["data"][1:]:
                if mongo_service.is_exist(car["mid"]) is not None:
                    print("cat id {} already existed".format(car["mid"]))
                    continue
                url = car["mlink"]
                r = ss.get(url, headers=myutils.get_header())
                print("get car detail : url", url)
                car_soup = myutils.get_soup(r.text)
                # print(car_soup.prettify())
                # 車輛廠牌分類
                car_brand = [a.text for a in car_soup.select("div.itemhd a")]
                car["新舊"] = car_brand[0]
                car["車型"] = car_brand[1]
                car["廠牌"] = car_brand[2].replace("/", "[sl]")
                if len(car_brand) > 3:
                    car["型號a"] = car_brand[3]
                    if len(car_brand) > 4:
                        car["型號"] = car_brand[4]
                # 車輛狀態
                car_status = []
                for i in car_soup.select("div#ycoptions ul#itemAttrs li")[0:3]:
                    for j in i:
                        car_status.extend(j.select("td"))
                # print("car_status", car_status)
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
                if len(car_pic) > 0:
                    car_pic = json.loads(car_pic)  # 將文字轉成物件
                    car_pic = [pic["i"] for pic in car_pic]
                # print("car_pic", car_pic)
                car["pic"] = car_pic
                # get_picture(ss, car_pic["href"])

                # 寫入圖片到本地
                # print(car)
                download_pic(ss, car)
                car["_id"] = car.pop("mid")
                # car.remove_key("mid")
                # print(car)
                mongo_service.insert_data("data", "car", car)
                item_sleep_time = random.uniform(0, 2)
                print("item sleep :", item_sleep_time)
                time.sleep(item_sleep_time)
            page_sleep_time = random.uniform(0, 5)
            print("page sleep :", page_sleep_time)
            time.sleep(page_sleep_time)
        except Exception as err:
            print("-" * 20)
            # print(car)
            # print("car pic", car_pic)
            error_log = {
                "err": err,
                "data": car
            }
            mongo_service.insert_data(collection="err", json_data=error_log, db_name="data")
            # raise err


def download_pic(ss, car):
    pic_path = "./pic/{}/{}/{}/{}/{}/{}_{}_{}_{}".format(car["廠牌"], car.get("型號a", "0"), car.get("型號", "0"),
                                                         car["auto_build_year"], car["mid"],
                                                         car["廠牌"], car.get("型號a", "0"), car.get("型號", "0"),
                                                         car["auto_build_year"])
    car_pic = car.pop("pic")
    car["pic"] = []
    for i, pic in enumerate(car_pic):
        q = ss.get(url=pic, headers=myutils.get_header())
        car["pic"].append({"url": pic, "file_path": myutils.write_pic_file(pic_path + "_{}.jpg".format(i), q.content)})


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

def yahoo_car():
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
    print(car_type_dict)
    print(brand_dict)
    action = soup.select_one("form")["action"]
    print("input data", input_data)
    for brand in brand_dict:
        search_page("000000515224", input_data, action, url, ss, kw=brand)


def test():
    print("start")
    url = "https://c.8891.com.tw"
    ss = myutils.get_session()
    # get https://c.8891.com.tw/Models
    req = ss.get(url=url+"/Models", headers=myutils.get_header())
    soup = myutils.get_soup(req.text)
    # print(soup.select("div.scroll-area"))
    # 獲取車輛品牌清單
    new_car_brand_list = []
    for a in soup.select("div.scroll-area li"):
        new_car_brand = {}
        new_car_brand["country"] = a["country"]
        new_car_brand["brand_id"] = a["id"]
        atag = a.select_one("a")
        new_car_brand["brand"] = atag.text.strip()
        new_car_brand["link"] = url + atag["href"]
        new_car_brand_list.append(new_car_brand)
        # print("-" * 20)
        # print(a)
        # print("-"*20)
        # print()
    # soup.select("scroll-area")
    # print(new_car_brand_list)
    #########################################################################
    #########################################################################
    #########################################################################
    #########################################################################
    header = myutils.get_header()
    header["referer"] = "https://c.8891.com.tw/Models"
# sec-fetch-dest: document
# sec-fetch-mode: navigate
# sec-fetch-site: same-origin
# sec-fetch-user: ?1
# service-worker-navigation-preload: true
# upgrade-insecure-requests: 1
    for brand in new_car_brand_list:
        req = ss.get(url=brand["link"], headers=header)
        brandsoup = myutils.get_soup(req.text)
        # 獲取車型清單
        car_type_dict = {t.text: t["href"] for t in brandsoup.select("div.brand-list-main.IndexKindContent a.brand-list-type")}
        print(car_type_dict)
        for key in car_type_dict:
            car_summary_url = car_type_dict[key]
            car_photo_url = car_summary_url.replace("Summary", "HDPhoto")
            req = ss.get(url="https://c.8891.com.tw/audi/a1-sportback/HDPhoto.html", headers=myutils.get_header())
            print(req.url)
            # print(req.text)
            scriptsoup = myutils.get_soup(req.text).find_all('script', type="text/javascript")
            for script in scriptsoup:
                print(script)
                tmp = str(script)
                if tmp.find("InitData") != -1:
                    # print(tmp.index(": ["), tmp.index("]"))
                    pid_str = tmp[tmp.index(": [") + 3: tmp.index("]")]
                    pid_list = pid_str.split(",")
                    print(pid_list)
                    photo_lib_url = "https://c.8891.com.tw/photoLibrary-ajaxList.html?pid="
                    pidstr = ""
                    for idx, pid in enumerate(pid_list):
                        pidstr += pid
                        # 一次獲取多少張圖片的網址
                        num_of_photo = 7
                        if idx % num_of_photo == 0 or idx % len(pid_list) == 0:
                            print(pidstr)
                            r = ss.get(url=photo_lib_url + myutils.url_encoding(pidstr), headers=myutils.get_header())
                            print(r.url, "photo rul result:")
                            # print(r.text)
                            try:
                                json_obj = json.loads(r.text)["data"]
                            except Exception as err:
                                print("error ", "~"*20)
                                print(err)
                                print(r.text)

                            for photo_json in json_obj:
                                photo_url = photo_json["smallPic"].replace(r"\/", "/")
                                # photo_req = ss.get(url=photo_url, headers=myutils.get_header())
                                # file_path = photo_url[photo_url.rfind("/"):]
                                # result = myutils.write_pic_file("./pic/8891"+file_path, photo_req.content)
                                # print("write pic", result, "success!")
                            print(json_obj)
                            pidstr = ""
                        else:
                            pidstr += ","
                        # break
            break
        break


def main():
    # test()
    ss = myutils.get_session()
    q = ss.get(url="https://auto.8891.com.tw/usedauto-infos-2445162.html", headers=myutils.get_header())
    print(myutils.get_soup(q.text).prettify())
    req = ss.get(url="https://p2.8891.com.tw/m223511/v9202/2020/06/23/1592916865015878_765_575_2445162.jpg", headers=myutils.get_header())
    a = myutils.write_pic_file("./pic/123.jpg", req.content)
    print(a)



if __name__ == "__main__":
    main()
