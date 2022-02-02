import tqdm as tqdm
from bs4 import BeautifulSoup
import requests as urlreq
import random
import threadpool
from requests.adapters import HTTPAdapter

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
]

GITHUB_URL_LIST = [
    "github.com",
    "gist.github.com",
    "assets-cdn.github.com",
    "raw.githubusercontent.com",
    "gist.githubusercontent.com",
    "cloud.githubusercontent.com",
    "camo.githubusercontent.com",
    "avatars.githubusercontent.com",
    "avatars0.githubusercontent.com",
    "avatars1.githubusercontent.com",
    "avatars2.githubusercontent.com",
    "avatars3.githubusercontent.com",
    "avatars4.githubusercontent.com",
    "avatars5.githubusercontent.com",
    "avatars6.githubusercontent.com",
    "avatars7.githubusercontent.com",
    "avatars8.githubusercontent.com",
    "github.global.ssl.fastly.net",
]

QUERY_DNS_SERVER = "https://ipaddress.com/website/"


def scrap_html(url):
    s = urlreq.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    s.headers['User-Agent'] = random.choice(USER_AGENT_LIST)
    response = ""
    try:
        response = s.get(url, timeout=15)
    except Exception as e:
        print(e)
    if response.ok is not True:
        print(url + ": null")
        return ""
    return response.content


HOST_IP_CONFIG = []


# 解析Response，获取dns ip addr
def get_dns_info(url, pbar):
    html_text = scrap_html(QUERY_DNS_SERVER + url)
    bsoup = BeautifulSoup(html_text, 'html.parser')
    ip_addr = bsoup.find(id="dnsinfo").next.contents[2].text
    pbar.update()
    HOST_IP_CONFIG.append(ip_addr + "  " + url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    max_threads = len(GITHUB_URL_LIST) if len(GITHUB_URL_LIST) < 20 else 20
    pool = threadpool.ThreadPool(max_threads)
    req_urls = []
    # 爬取网页信息
    with tqdm.tqdm(total=len(req_urls)) as pbar:
        for url in GITHUB_URL_LIST:
            req_urls.append(([url, pbar], None))
        requests_ = threadpool.makeRequests(get_dns_info, req_urls)
        for req in requests_:
            pool.putRequest(req)
        pool.wait()
    # 打印结果
    for hosts_item in HOST_IP_CONFIG:
        print(hosts_item)
