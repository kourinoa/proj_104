from json.decoder import JSONDecodeError
from collections import defaultdict
import myutils
from bs4 import BeautifulSoup
import time
import random
import json
from service import job_service
from urllib import parse
import pandas as pd

ss = myutils.get_session()
first_url = "https://www.104.com.tw/jobs/search/?ro=0&keyword={}&jobsource=2018indexpoc"
keyword = "AI"

def get_page(page_num: int) -> dict:
    header = myutils.get_header()
    header["Accept"] = "application/json, text/javascript, */*; q=0.01"
    header["Accept-Encoding"] = "gzip, deflate, br"
    header["Accept-Language"] = "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    header["Connection"] = "keep-alive"
    header["Host"] = "www.104.com.tw"
    header["Referer"] = first_url + "&order=1"
    header["Sec-Fetch-Dest"] = "empty"
    header["Sec-Fetch-Mode"] = "cors"
    header["Sec-Fetch-Site"] = "same-origin"
    header["X-Requested-With"] = "XMLHttpRequest"
    global keyword

    list_url = "https://www.104.com.tw/jobs/search/list?ro=0&kwop=7&keyword={}&order=15&asc=0&page={}&mode=s&jobsource=2018indexpoc"
    list_url = list_url.format(keyword, str(page_num))
    print("get page ", list_url)
    req = ss.get(url=list_url, headers=header)
    jd = json.loads(req.text)
    print(list_url, "status", jd["status"])
    # print(jd["data"]["list"])
    job_dict = {
        myutils.get_jobid_by_url(job["link"]["job"]): {"job_name": job["jobName"], "url": "https:" + job["link"]["job"]}
        for job in jd["data"]["list"]}
    # print(job_dict)
    return job_dict


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
    header["Accept"] = "application/json, text/plain, */*"
    header["Accept-Language"] = "zh-tw"
    header["Host"] = "www.104.com.tw"
    header["Referer"] = job_url
    header["Accept-Encoding"] = "br, gzip, deflate"
    header["Sec-Fetch-Dest"] = "empty"
    header["Sec-Fetch-Mode"] = "cors"
    header["Sec-Fetch-Site"] = "same-origin"
    header["Connection"] = "keep-alive"
    req = ss.get(url=content_rul, headers=header)
    # print(json.dumps(json.loads(req.text), indent=4, ensure_ascii=False))
    try:
        content_data = json.loads(req.text)
    except JSONDecodeError as err:
        print(err)
        print(job_url)
        print(req.text)
    job_content = {}
    job_content["id"] = job_id
    job_content["job_name"] = content_data["data"]["header"]["jobName"]
    job_content["url"] = job_url
    job_content["company_name"] = content_data["data"]["header"]["custName"]
    job_content["company_url"] = content_data["data"]["header"]["custUrl"]
    job_content["contact"] = content_data["data"]["contact"]
    job_content["skill"] = content_data["data"]["condition"]["specialty"]
    job_content["job_detail"] = content_data["data"]["jobDetail"]["jobDescription"]
    print("get content url:", job_url, "success")
    return job_content


def do_search(key_word: str, page_num):
    global first_url
    page_num = int(page_num)
    if key_word is None or len(key_word) == 0:
        return "error keyword"
    if page_num is None:
        return "page_num"
    # 取得第一頁資料
    first_page_url = first_url.format(key_word)
    req = ss.get(url=first_page_url,
                 headers=myutils.get_header())
    soup = get_soup(req.text)
    job_data = {}
    for idx, bs in enumerate(soup.select("article div.b-block__left")):
        # print(bs)
        # print(idx, idx, idx)
        job = bs.select("a.js-job-link")
        for j in job:
            # print("url", j["href"], idx)
            if j["href"].find("hotjob_chr") == -1:
                job_data[myutils.get_jobid_by_url(j["href"])] = {"url": "https:" + j["href"], "job_name": j.text}

    job_result = []
    for job in job_data:
        job_url = job_data[job]["url"]
        # print(job_url)
        job_content = get_job_content(job_url)
        job_service.add_job(job_content)
        job_result.append(job_content)
    # 取得第二頁以後資料
    key_word = parse.quote(key_word)
    first_url = first_url.format(key_word)
    if page_num != 0:
        for i in range(2, page_num + 1):
            job_data = get_page(keyword=key_word, page_num=i)
            for job in job_data:
                job_url = job_data[job]["url"]
                # print(job_url)
                sleep_time = random.uniform(1, 2)
                print("sleep {} sec".format(sleep_time))
                time.sleep(sleep_time)
                job_content = get_job_content(job_url)
                job_service.add_job(job_content)
                job_result.append(job_content)
    myutils.write_json_file(job_result, str(int(time.time())) + "job.json")


def main():
    global first_url
    global keyword
    first_url = first_url.format(keyword)
    page_num = 1

    req = ss.get(url=first_url,
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
    print(job_data)

    job_result = []
    for job in job_data:
        job_url = job_data[job]["url"]
        # print(job_url)
        job_content = get_job_content(job_url)
        job_service.add_job(job_content)
        job_result.append(job_content)

    for i in range(2, page_num + 1):
        job_data = get_page(i)
        for job in job_data:
            job_url = job_data[job]["url"]
            # print(job_url)
            sleep_time = random.uniform(1, 2)
            print("sleep {} sec".format(sleep_time))
            time.sleep(sleep_time)
            job_content = get_job_content(job_url)
            job_service.add_job(job_content)
            job_result.append(job_content)
    # print(len([bs.select("a.js-job-link") for bs in soup.select("div.b-block__left")]))
    # 計算技能名稱出現次數
    skill_dict = defaultdict(lambda: 0)
    for job in job_result:
        for skill in job["skill"]:
            skill_dict[skill["description"]] += 1

    print(skill_dict)
    with open("./dict/skill.txt", "a") as file:
        file.write(json.dumps(skill_dict))


def test():
    filename = "1591868886job.json"
    json_data = json.load(open("./dict/{}".format(filename), "r"))
    print(json_data[1:2])
    skill_dict = defaultdict(lambda: 0)
    # 計算技能出現次數
    for job in json_data:
        for skill in job["skill"]:
            skill_dict[skill["description"]] += 1
    print(skill_dict)
    for job in json_data:
        con_str = ""
        for k, v in job["contact"].items():
            con_str += "{}: {} ".format(k, v)
        job["contact"] = con_str
        # 沒有技能要求的職位全部技能標註0
        if len(job["skill"]) == 0:
            for skill in skill_dict:
                job[skill] = 0
        # 職位有要求的技能標註1，否則標註0
        for skill in skill_dict:
            for s in job["skill"]:
                if skill in s.values():
                    job[skill] = 1
                else:
                    job[skill] = 0
        job["skill"] = None

    # print(json_data)

    df = pd.read_json(json.dumps(json_data))
    df.fillna(0)
    df.to_csv("./dict/{}.csv".format(filename[:filename.find(".")]), encoding="utf_8_sig")
    print(df[1:2])


if __name__ == "__main__":
    # main()
    test()
