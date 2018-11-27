import random
import sqlite3
import time

from download_html import HtmlDownloader
from html_analyze import HtmlParser



def executeSQL(*args):
    conn = sqlite3.connect("CNKI.db")
    cursor = conn.cursor()
    if args.__len__()==2:
        re = cursor.execute(args[0], args[1])
        re=re.fetchall()
    elif args.__len__()==1:
        re=cursor.execute(args[0])
        re=re.fetchall()
    else:
        re=False
    conn.commit()
    cursor.close()
    conn.close()
    return re


class GetData:
    def __init__(self):
        self.url = "http://yuanjian.cnki.net/Search/ListResult"
        self.post_dict = {
            "searchType":"MulityTermsSearch",
            "ParamIsNullOrEmpty":True,
            "Islegal":True,
            "Content":"社会工作",
            "Order":1,
            "Page":1,
            "Year":2018,
        }

        self.xpath_keyword = {
            "title": {
                "xpath": '//div[@class="list-item"]//p[@class="tit clearfix"]/a[1]/@title',
            },  # 题目
            "author": {
                "xpath": '//div[@class="list-item"]//p[@class="source"]/span[1]/@title',
            },  # 作者
            "tutor": {
                "xpath": '//div[@class="list-item"]//p[@class="source"]/span[2]/@title',
            },  # 导师
            "school": {
                "xpath": '//div[@class="list-item"]//p[@class="source"]/span[3]/@title',
            },  # 导师
            # "document_type": {
            #     "xpath": '//div[@class="list-item"]//p[@class="source"]/span[4]/text()',
            # },  # 文献类型
            "keywords": {
                "xpath": '//div[@class="list-item"]//div[@class="info"]//p[@class="info_left left"]/a[1]/@data-key',
            },  # 关键字
            "download_times": {
                "xpath": '//div[@class="list-item"]//div[@class="info"]//p[@class="info_right right"]/span[1]/text()',
            },  # 下载次数
            "citations_times": {
                "xpath": '//div[@class="list-item"]//div[@class="info"]//p[@class="info_right right"]/span[2]/text()',
            },  # 引用次数
            "reorganization": [
                'title',
                # 'author', 'tutor', 'school',
                'keywords',
                # 'download_times', 'citations_times'
            ],
        }  # 主体数据的获取

        # self.xpath_index = {
        #     "index": {
        #         "xpath": "",
        #     },
        # }

        self.download_html = HtmlDownloader()
        self.html_analyze = HtmlParser()
        headers_dict = {
            "Connection": "keep - alive",
            "Accept": "text/html, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "http://yuanjian.cnki.net/Search/Result",
            "Origin": "http://yuanjian.cnki.net",
            "Host": "yuanjian.cnki.net",
        }
        self.download_html.set_headers(headers_dict)

    def get_data_by_index(self, index=1):
        try:
            print("准备抓取第{}页".format(index))
            self.post_dict["Page"] = index
            html_content = self.download_html.download_post_html(self.url, self.post_dict)
            # print(html_content)
            if not html_content:
                return False
            analyze_result = self.html_analyze.paser_xpath(html_content, self.xpath_keyword)
            # print(analyze_result)
            print("得到了{}条数据".format(analyze_result.__len__()))
            self.save_to_bd(analyze_result)
            return True
        except:
            return False

    def save_to_bd(self, data):  # 数据存储
        # print(data)
        if isinstance(data, list):
            for __, data_one in enumerate(data):
                inster_sql = 'INSERT INTO "info" ("id", "title", "keywords") VALUES (?, ?, ?)'
                pare = (time.time(), data_one["title"], data_one["keywords"])
                # print(inster_sql)
                result = executeSQL(inster_sql, pare)
                # print(result)

    def main(self):
        for i in range(1, 403 ):
            if self.get_data_by_index(i):
                time.sleep(20)
                continue
            else:
                break
        print("已经终止了爬虫", i)

if __name__ == '__main__':
    a = GetData()
    a.main()
    # a.get_data_by_index(15)
    # result = [{'title': '中职生养老护理专业能力的现状及提升效果研究', 'keywords': '中职生/养老护理/专业能力/社会工作'}]
    # a.save_to_bd(result)
