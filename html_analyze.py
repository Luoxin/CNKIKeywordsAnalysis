# coding:utf-8
import json
import gzip
from bs4 import BeautifulSoup
import re
from urllib import parse
from urllib.parse import urljoin
from lxml import etree
import traceback



class HtmlParser(object):
    '''
    和解析相关的类
    '''
    def __init__(self):
        self.analysis_keywords=["gzip",'binary']

    def paser_xpath(self, html_content, xpath_dict):  # 解析页面
        '''
        利用xpath解析
        :param html_content:页面内容
        :param xpath_dict: xpath的解析列表
            {
                '解析的key':{
                    'xpath' : '' ,  # xpath  必须
                    'base_url':'',  # 要拼接的基础的url
                    'reserved_keywords'：[''],  # 存在则保留，和removed_keywords只能存在一个
                    'removed_keywords': [''],   # 存在则删除，和reserved_keywords只能存在一个
                }
                'binary':True,  # 需要对byte类型转换
                'reorganization':[],  # 重组
                "ChineseGarbled":True,  # 解决中文乱码的问题
            }
        :return: 解析结果的字典
        '''
        try:
            # 预处理
            if 'gzip' in xpath_dict:
                if xpath_dict['gzip']:
                    html_content = gzip.decompress(html_content)

            if 'binary' in xpath_dict:  # 处理二进制
                if xpath_dict['binary']:
                    html_content = str(html_content)[2:-1]
            # print(html_content)

            if 'ChineseGarbled' in xpath_dict:
                if xpath_dict['ChineseGarbled']:
                    html_content = self.chinese_garbled(html_content)

            soup = etree.HTML(html_content)
            result = self._paser_xpath_main(soup,xpath_dict)


            if 'reorganization' in xpath_dict:
               result = self.list_to_dict(result, xpath_dict)

            return result
        except:
            return None

    def chinese_garbled(self,data):
        def unicodetostr(s):
            strTobytes = []
            for i in s.split('\\x'):
                if i != '':
                    num = int(i, 16)
                    strTobytes.append(num)
            a = bytes(strTobytes).decode()
            return a

        def ti(m):
            s = str(m.group())
            a = unicodetostr(s)
            return a

        pat = re.compile(r'(\\x[0-9a-fA-F][0-9a-fA-F])+')
        return re.sub(pat, ti, data)

    def list_to_dict(self, result, xpath_dict):  # 把列表变成字典
        sgin = True
        # print(result)
        for __, val in enumerate(xpath_dict['reorganization']):  # 判断是否存在非法的字典
            if val not in result.keys():
                sgin = False
                break
        if sgin:
            val_len = result[xpath_dict['reorganization'][0]].__len__()  # 判断长度是否一样
            for __, val in enumerate(xpath_dict['reorganization']):
                if result[val].__len__() is not val_len:
                    sgin = False
                    break

        if sgin:
            temp_result = []
            for index in range(val_len):  # 重新组合
                temp_dict = dict()
                for __, val in enumerate(xpath_dict['reorganization']):
                    temp_dict[val] = result[val][index]
                temp_result.append(temp_dict)
                # print(temp_dict)
            result = temp_result

        return result

    def _paser_xpath_main(self,soup,xpath_dict):  # 根据xpath进行解析
        result_dict = {}
        for key, val in xpath_dict.items():
            if key in self.analysis_keywords:
                continue

            if isinstance(val,dict):
                result_dict[key] = self._paser_xpath_onekey(soup=soup, key=key, val=val)

        return result_dict


    def _paser_xpath_onekey(self, soup, key, val):  # 解析单个
        result=[]
        try:
            if 'base_url' in val:  # url需要拼接的
                '''
                如果是url则拼接
                ["xpath","url"]
                '''
                result_list = soup.xpath(val["xpath"])
                # print(result_list)
                for __, url in enumerate(result_list):
                    result.append(urljoin(val["base_url"], url))

            elif "xpath" in val :  # 不需要处理的
                # print(key, val["xpath"])
                result = soup.xpath(val["xpath"])
                # print(result)

            if 'unicode' in val:
                result=self.__decoding_unicode(result)

            #  对关键字做处理
            if 'reserved_keywords' in val:  # 存在才保留
                if isinstance(val["reserved_keywords"], list):
                    self.__reserved_keywords(result, val["reserved_keywords"])
                pass
            elif 'removed_keywords' in val:  # 存在则删除
                if isinstance(val["removed_keywords"], list):
                    self.__reserved_keywords(result, val["removed_keywords"])

        except Exception:
            result = ["Error", str(traceback.format_exc()), str(Exception.with_traceback())]

        return result

    def __decoding_unicode(self,data_list):  # 对Unicode解码
        result = []
        for __,data in enumerate(data_list):
            result.append(self.__decoding_unicode_one(data))
        return result

    def __decoding_unicode_one(self,data):  # 对单个数据Unicode解码
        # return data.encode('utf-8').decode('unicode_escape')
        # return data.
        pass

    def __reserved_keywords(self,data,reserved_keywords):  # 存在才保留
        for __,val in enumerate(data):
            if self.__reserved_keyword(data,val):
                continue
            else:
                data.remove(val)
        pass

    def __reserved_keyword(self, data, reserved_keywords):  # 存在才保留  单个处理
        for __,val in enumerate(reserved_keywords):
            if val in data:
                return True
            else:
                continue
        return False

    def __removed_keywords(self,data,removed_keywords):  # 存在则删除
        pass



