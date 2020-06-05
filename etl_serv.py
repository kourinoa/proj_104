import myutils
from bs4 import BeautifulSoup
import time
import random
import json

ss = myutils.get_session()

def get_page():
    list_url = "https://www.104.com.tw/jobs/search/list?ro=0&kwop=7&keyword=AI&order=15&asc=0&page=10&mode=s&jobsource=2018indexpoc"


def get_soup(text) -> BeautifulSoup:
    return BeautifulSoup(text, "html.parser")


def get_total_page(text) -> int:
    """
    取得總頁數
    :param text: html
    :return: 總頁數 int
    """
    temp = text[text.rfind("totalPage"):]
    temp = temp[temp.find(":") + 1:temp.find(",")]
    # print("total", temp)
    return int(temp)
    # print(soup.prettify())
    # header = myutils.get_header()
    # header["Accept"]="Accept: application/json, text/javascript, */*; q=0.01"
    # header["Accept-Language"]= "zh-tw"
    # header["Host"]= "www.104.com.tw"
    # header["Referer"]= "https://www.104.com.tw/jobs/search/?ro=0&keyword=AI&jobsource=2018indexpoc"
    # header["Accept-Encoding"]= "br, gzip, deflate"
    # header["Connection"]= "keep-alive"
    # header["X-Requested-With"]= "XMLHttpRequest"
    # req2 = ss.get(url="https://www.104.com.tw/jobs/main/ajax/KeywordSuggest/mixSearch?kw=AI&scope=com&count=4",
    #               headers=header)
    # print(req2.content)
    # page = soup.select("select.page-select")
    # print(page)


def get_job_content(job_url):
    job_id = myutils.get_jobid_by_url(job_url)
    content_rul = "https://www.104.com.tw/job/ajax/content/" + job_id
# 製作header
    header = myutils.get_header()
    header["Accept"]="application/json, text/plain, */*"
    header["Accept-Language"]= "zh-tw"
    header["Host"]= "www.104.com.tw"
    header["Referer"]= job_url
    header["Accept-Encoding"]= "br, gzip, deflate"
    header["Connection"]= "keep-alive"
    req = ss.get(url=content_rul, headers=header)
    print(json.dumps(json.loads(req.text), indent=4, ensure_ascii=False))
    content_data = json.loads(req.text)
    job_content = {}
    job_content["jobName"] = content_data["data"]["header"]["jobName"]
    job_content["company_name"] = content_data["data"]["header"]["custName"]
    job_content["company_url"] = content_data["data"]["header"]["custUrl"]
    job_content["contact"] = content_data["data"]["contact"]




def main():
    req = ss.get(url="https://www.104.com.tw/jobs/search/?ro=0&keyword=AI&jobsource=2018indexpoc",
                 headers=myutils.get_header())

    soup = get_soup(req.text)
    total_page = get_total_page(req.text)
    job_data = {}
    for idx, bs in enumerate(soup.select("article div.b-block__left")):
        # print(bs)
        # print(idx, idx, idx)
        job = bs.select("a.js-job-link")
        for j in job:
            # print("url", j["href"], idx)
            if j["href"].find("hotjob_chr") == -1:
                job_data[myutils.get_jobid_by_url(j["href"])] = {"url": "https:" + j["href"], "job_name": j.text}
            # print("job_name", j.text)
        # print("-----------------")
    # print(job_data)
    for job in job_data:
        job_url = job_data[job]["url"]
        print(job_url)
        get_job_content(job_url)
        break
    # print(len([bs.select("a.js-job-link") for bs in soup.select("div.b-block__left")]))


if __name__ == "__main__":
    main()
