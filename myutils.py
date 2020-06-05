import requests


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


def main():
    get_jobid_by_url("http://www.104.com.tw/job/6iq7d?jobsource=2018indexpoc")


if __name__ == "__main__":
    main()
