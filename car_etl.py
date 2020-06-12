import myutils
from bs4 import BeautifulSoup


def main():
    url = "https://tw.usedcar.yahoo.com"
    ss = myutils.get_session()
    req = ss.get(url=url, headers=myutils.get_header())
    soup = BeautifulSoup(req.text, "html.parser")
    print(soup.prettify())




if __name__ == "__main__":
    main()