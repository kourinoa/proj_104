import myutils
from bs4 import BeautifulSoup


def get_soup(text) -> BeautifulSoup:
    return BeautifulSoup(text, "html.parser")


def main():
    ss = myutils.get_session()
    req = ss.get(url="https://www.104.com.tw/jobs/search/?ro=0&keyword=AI&jobsource=2018indexpoc",
                 headers=myutils.get_header())
    soup = get_soup(req.text)
    for bs in soup.select("article div.b-block__left"):
        print(bs.prettify())
        print("-----------------")
        job = bs.select("a.js-job-link")
        for j in job:
            print("url", j["href"])
            print("job_name", j.text)
        print("-----------------")
        # print(len([bs.select("a.js-job-link") for bs in soup.select("div.b-block__left")]))


if __name__ == "__main__":
    main()
