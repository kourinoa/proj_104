import myutils
import json
import service.mongo_service as mongo_service

logger = myutils.get_logger("car_8891", "8891.log")


def get_new_car_brand():
    # print("start")
    url = "https://c.8891.com.tw"
    ss = myutils.get_session()
    # get https://c.8891.com.tw/Models
    res = ss.get(url=url + "/Models", headers=myutils.get_header())
    soup = myutils.get_soup(res.text)
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
    return new_car_brand_list


def get_pic_page_url(url: str):
    ss = myutils.get_session()
    req = ss.get(url=url, headers=myutils.get_header())
    soup = myutils.get_soup(req.text)
    url_list = [a["href"] for a in soup.select("div.jp-bg-color.mt10 a")]
    return url_list[1]


def get_new_car_type(url: str):
    header = myutils.get_header()
    header["referer"] = "https://c.8891.com.tw/Models"
    ss = myutils.get_session()
    res = ss.get(url=url, headers=header)
    brandsoup = myutils.get_soup(res.text)
    # 獲取車型清單
    car_type_dict = {t.text: t["href"] for t in
                     brandsoup.select("div.brand-list-main.IndexKindContent a.brand-list-type")}
    return car_type_dict


def get_new_car_pic(url: str):
    """

    :param url: 範例 https://c.8891.com.tw/audi/a1-sportback/HDPhoto.html
    :return: 該車型所有圖片url
    """
    pic_url_list = []  # 放圖片url
    ss = myutils.get_session()  # 可以換成requests.session()
    res = ss.get(url=url, headers=myutils.get_header())  # header裡只有user agent
    print("get response from", res.url)
    # print(req.text)
    scriptsoup = myutils.get_soup(res.text).find_all('script', type="text/javascript")
    for script in scriptsoup:
        # print(script)
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
                    # print(pidstr)
                    # 向https://c.8891.com.tw/photoLibrary-ajaxList.html 發出請求
                    r = ss.get(url=photo_lib_url + myutils.url_encoding(pidstr),
                               headers=myutils.get_header())  # 網址裡的,需要轉換編碼
                    # print(r.url, "photo rul result:")
                    # print(r.text)
                    try:
                        json_obj = json.loads(r.text)["data"]
                    except Exception as err:
                        print("error ", "~" * 20)
                        print(err)
                        print(r.text)

                    for photo_json in json_obj:
                        photo_url = photo_json["smallPic"].replace(r"\/", "/")  # 把反斜線弄掉
                        pic_url_list.append(photo_url)
                    pidstr = ""
                else:
                    pidstr += ","
    return pic_url_list


def get_used_car_page(url):
    logger.info("{} get url:{}".format(__name__, url))
    ss = myutils.get_session()
    res = ss.get(url=url, headers=myutils.get_header())
    soup = myutils.get_soup(res.text)
    logger.info(str(soup.prettify()))
    car = {}
    car_type = soup.select("div.breadcrumb a.NormalLink")
    print(car_type)
    car["brand"] = car_type[2].text
    if len(car_type) >= 5:
        car["type"] = car_type[4].text
    car["type2"] = car_type[3].text
    car["title"] = soup.select_one("div.right-info info-right-width div.infos-head-title span").text
    car["price"] = soup.select_one("div.car-price-box div#price b").text






def test():
    ################################################################
    # 新車抓圖範例
    # ss = myutils.get_session()
    # new_car_brand_list = get_new_car_brand()
    # print(new_car_brand_list)
    # count = 0
    # for brand in new_car_brand_list:
    #     car_type_dict = get_new_car_type(brand["link"])
    #     print(car_type_dict)
    #     count += 1
    #     if count == 2:
    #         break
    #     for t in car_type_dict:
    #         pic_url_list = get_new_car_pic(get_pic_page_url(car_type_dict[t]))
    #         print(t, "_" * 30)
    #         print(pic_url_list)
    #         for pic_url in pic_url_list:
    #             b = brand["brand"]
    #             if b.find("/") != -1:
    #                 b = b[:b.find("/")]
    #             pic_res = ss.get(url=pic_url, headers=myutils.get_header())
    #             file_path = "./pic/8891/{}/{}/{}".format(b, t, pic_url[pic_url.rfind("/"):])
    #             a = myutils.write_pic_file(file_path=file_path, pic=pic_res.content)
    #             print(a, "success")
    ###########################################################################
    # print(get_pic_page_url("https://c.8891.com.tw/daihatsu/coo/Summary.html"))
    local_conn = mongo_service.get_mongo_conn()
    local_coll = local_conn["data"]["8891"]
    cursor = local_coll.find({})

    domain = "https://auto.8891.com.tw/"

    for idd in cursor:
        url = "{}usedauto-infos-{}.html".format(domain, str(idd["_id"]))
        get_used_car_page(url)
        break


def main():
    test()


if __name__ == "__main__":
    main()
