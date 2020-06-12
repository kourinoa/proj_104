import requests
import datetime
import json
import os

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


def get_datetime_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_json_file(json_data, filename):
    try:
        with open("../dict/{}".format(filename), "w") as file:
            file.write(json.dumps(json_data, ensure_ascii=False))
    except FileNotFoundError as e:
        print(e)
        print(os.getcwd())


def main():
    print(get_datetime_str())


if __name__ == "__main__":
    main()
