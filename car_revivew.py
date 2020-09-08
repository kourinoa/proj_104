import requests
from bs4 import BeautifulSoup
import myutils
import json
from service import mongo_service
import time
import random
import datetime


def get_article():
    ss = myutils.get_session()
    # make header
    header = myutils.get_header()
    header["Accept"] = "application/json, text/plain, */*"
    header["Accept-Encoding"] = "gzip, deflate"
    header["Host"] = "www.carplushk.com"
    header["Accept-Language"] = "zh-tw"
    header["Referer"] = "http://www.carplushk.com/category/review/"
    header["Connection"] = "keep-alive"

    url = '''http://www.carplushk.com/wp-admin/admin-ajax.php?id=&post_id=4036&slug=review&canonical_url=http%3A%2F%20%20%20%20%20%2Fwww.carplushk.com%2Fcategory%2Freview%2F&posts_per_page=12&page={}&offset=25&post_type=post&repeater=template_1%20%20%20%20%20&seo_start_page=1&preloaded=false&preloaded_amount=0&cta[cta]=true&cta[cta_position]=after:12&cta[%20%20%20%20%20cta_repeater]=template_3&cta[cta_theme_repeater]=null&category=review&order=DESC&orderby=date&action=alm_get_posts&query_type=standard'''

    urlajax = url.format("0")
    print(urlajax)
    res = ss.get(url=urlajax, headers=header)
    data_dict = json.loads(res.text)
    try:
        total_post = int(data_dict["meta"]["totalposts"])
    except ValueError as err:
        print("*" * 50)
        print("total post is not a number")
    # for k in data_dict:
    #     print(k, " : ", data_dict[k])
    # soup = myutils.get_soup(data_dict["html"])
    # print(soup.prettify())

    # for s in soup.select("div.ajaxmoreblk a"):
    #     a = {"_id": s["href"], "title": s.text, "from": "http://www.carplushk.com", "type": "review"}
    #     article_list.append(a)
    # print(article_list)
    # result = mongo_service.insert_many("data", "car_article", article_list)
    # print(result)

    for i in range( int(total_post/12) + 1):
        article_list = []
        urlajax = url.format(i)
        res = ss.get(url=urlajax, headers=header)
        data_dict = json.loads(res.text)
        soup = myutils.get_soup(data_dict["html"])
        for s in soup.select("div.ajaxmoreblk a")[:-1]:
            a = {"_id": s["href"], "title": s.text, "from": "http://www.carplushk.com", "type": "review"}
            if not mongo_service.is_exist(idd=a["_id"], collection="car_article"):
                article_list.append(a)
            else:
                print(a["_id"], " already in article db")
        print(article_list)
        if len(article_list) > 0:
            result = mongo_service.insert_many("data", "car_article", article_list)
            print(result)


def get_article_content(url: str, ss):
    conn = mongo_service.get_mongo_conn()
    db = conn["data"]
    coll = db["car_article"]
    cursor = coll.find({})

    ss = myutils.get_session()
    header = myutils.get_header()
    header["Accept"] = "application/json, text/plain, */*"
    header["Accept-Encoding"] = "gzip, deflate"
    header["Host"] = "www.carplushk.com"
    header["Accept-Language"] = "zh-tw"
    header["Referer"] = "http://www.carplushk.com/category/review/"
    header["Connection"] = "keep-alive"
    count = 1
    for art_url in cursor:
        art_dict = {}
        print(art_url["_id"], "\n")
        art_dict["_id"] = art_url["_id"]
        res = ss.get(url=art_url["_id"], headers=header)
        soup = myutils.get_soup(res.text)
        content = soup.select_one("div.entry-content.single-page")
        pdate = content.select_one("div.postdayau").text
        art_dict["post_time"] = datetime.datetime.strptime(pdate.split("By")[0].strip(), "%d %b, %Y")
        print(art_dict["post_time"])
        main_content = ""
        for tag in content:
            if tag.name == "p":
                if tag.text.find("Text & Photo") == -1:
                    main_content += tag.text
                    main_content += "\n"
            elif tag.name == "h2":
                main_content += "=t{}=t\n".format(tag.string)
        art_dict["content"] = main_content
        print(art_dict)
        count += 1
        if count == 5:
            break
        time.sleep(random.randint(1, 5))


def test():
    print("test start ...")
    # get_article() # 取得文章連接及標題
    get_article_content("dfl", "dfs")

    # res = ss.get(url=url, headers=header)
    # soup = myutils.get_soup(res.text)
    # soup.select("div#catwholeblk2 ")
    # print(soup.prettify())


def main():
    try:
        test()
    except Exception as err:
        print(err)
        raise err


if __name__ == "__main__":
    main()
