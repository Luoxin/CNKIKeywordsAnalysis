import urllib.request
from contextlib import closing
import requests
import random
# from getproxy import GetProxy
from tqdm import tqdm

class HtmlDownloader:
    '''
    和下载相关的类
    '''

    def __init__(self):
        # user_agent
        self.user_agent=[
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        ]
        self.headers = {}

    def set_headers(self, headers_dict):
        if isinstance(headers_dict, dict):
            for key, val in headers_dict.items():
                self.headers[key] = val


    def download_html(self, url):
        '''
        下载碰面
        :param url: 需要下载的地址
        :return: 页面内容或None
        '''
        try:
            # url=url.encode("utf-8")
            # print("准备下载页面"+url)

            self.headers['User-Agent'] = random.choice(self.user_agent)
            # headers = {'User-Agent': ua.random}

            req_timeout = 20
            request = urllib.request.Request(url, headers=self.headers)
            # print(request)
            response = urllib.request.urlopen(request, None, req_timeout)  # 这里会有一个返回值 是我们的响应
            # print(response.getcode())
            # 我们判断如果不是200就返回None 否则就返回数据就
            if response.getcode() != 200:
                return None

            # 从响应中读取页面数据并返回
            return response.read()
        except :
            return None

    def download_post_json(self, url, post_dict):  # post请求，json格式
        return requests.post(url, data=post_dict).json()

    def download_post_html(self, url, post_dict):  # post请求，html格式
        return requests.post(url, post_dict).text


    def download_file(self,url, fileName):
        '''
        下载文件
        :param url: 下载地址
        :param fileName: 文件名
        :return:
        '''
        with closing(requests.get(url, stream=True)) as response:
            chunk_size = 1024  # 单次请求最大值
            content_size = int(response.headers['content-length'])  # 内容体总大小
            with open(fileName, "wb") as file:
                # 有进度条显示
                # for data in tqdm(response.iter_content(chunk_size=chunk_size),unit_scale=True,ncols=80,total=int(content_size/1024)+1,desc="{} downloading......".format(fileName),unit="b"):
                # 无进度条显示
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)

        print(f"{fileName}下载完成")


if __name__ == '__main__':
    # HtmlDownloader()
    # g = GetProxy()
    # g.init()
    # g.load_plugins()
    # g.grab_web_proxies()
    # g.validate_web_proxies()

    print(g.valid_proxies)