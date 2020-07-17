import myutils


def test():
    domain = "https://www.mobile01.com/"
    url = domain + "forumtopic.php?c=21"
    ss = myutils.get_session()
    req = ss.get(url=url, headers=myutils.get_header())
    soup = myutils.get_soup(req.text)
    # print(soup.prettify())
    car_catagroy = soup.select(("div.u-gapNextV--lg ul.c-filter li"))
    print(car_catagroy)


def main():
    try:
        test()
    except Exception as err:
        raise err
    finally:
        pass


if __name__ == "__main__":
    main()