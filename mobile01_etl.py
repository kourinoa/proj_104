import myutils
import datetime
from service import mongo_service
domain = "https://www.mobile01.com/"


def get_car_country_url_list(ss) -> list:
    url = domain + "forumtopic.php?c=21"
    res = ss.get(url=url, headers=myutils.get_header())
    soup = myutils.get_soup(res.text)
    # print(soup.prettify())
    car_country = soup.select("div.u-gapNextV--lg ul.c-filter li a")
    url_data = []
    for a in car_country:
        url_dict = {"_id": domain + a["href"].replace("&amp;", "&"), "country_name": a.text}
        url_data.append(url_dict)
    return url_data


def get_brand_url(url: str, ss) -> list:
    res = ss.get(url=url, headers=myutils.get_header())
    soup = myutils.get_soup(res.text)
    brand_list = soup.select("div.u-gapNextV--lg ul.c-filter li a")
    return [{"brand": brand.text, "url": domain + brand["href"]} for brand in brand_list if
            brand["href"].find("forum") == -1]


def get_artical_url(url: str, ss) -> list:
    res = ss.get(url=url, headers=myutils.get_header())
    soup = myutils.get_soup(res.text)
    # 總頁數
    tmp = soup.select("div.l-navigation__item.l-navigation__item--min ul.l-pagination li")
    total_page = max([int(a.text) for a in tmp if a.text != ""])  # type:int
    # print([a.text for a in total_page])
    # 文章列表取得
    # 文章區塊，包含作者、最後回應、回覆數
    artical_block_list = soup.select("div.l-listTable__tbody div.l-listTable__tr")
    for art in artical_block_list:
        artical_title = {}
        # print(art.prettify())
        title = art.select_one("div.c-listTableTd__title a.c-link.u-ellipsis")
        # print(title.text, title["href"])
        artical_title["title"] = title.text
        artical_title["url"] = domain + title["href"]
        # 發文用戶、時間 最後回覆用戶、時間
        time_data = art.select("div.l-listTable__td.l-listTable__td--time")
        post_user = time_data[0].select_one("a").text
        post_time = datetime.datetime.strptime(time_data[0].select_one("div.o-fNotes").text, "%Y-%m-%d %H:%M")
        artical_title["post_user"] = post_user
        artical_title["post_time"] = post_time
        last_resp_user = time_data[1].select_one("a").text
        last_resp_time = datetime.datetime.strptime(time_data[1].select_one("div.o-fNotes").text, "%Y-%m-%d %H:%M")
        artical_title["last_resp_user"] = last_resp_user
        artical_title["last_resp_time"] = last_resp_time
        # 總回覆數
        resp_count = art.select_one("div.l-listTable__td.l-listTable__td--count div").text
        artical_title["resp_count"] = int(resp_count)
        print(artical_title)
        print("_"*30)


def test():
    ss = myutils.get_session()
    url_data = get_car_country_url_list(ss)
    print(url_data)
    for country_url in url_data[1:]:
        print("request url:", country_url["_id"])
        brand_url = get_brand_url(country_url["_id"], ss)
        country_url["brandList"] = brand_url

        print(country_url)
        a = mongo_service.insert_data("data", "mobile_car_cy", country_url)
        print(a, "success")
        # for brand in country_url["brandList"]:
        #     print("request brand", brand["brand"])
        #     get_artical_url(brand["url"], ss)
        #     break
        # break


def main():
    try:
        test()
    except Exception as err:
        raise err
    finally:
        pass


if __name__ == "__main__":
    main()
