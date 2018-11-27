import sqlite3
from collections import Counter

import jieba
import jieba.analyse

class DB_sqlite:
    def __init__(self, db_path):
        self.db_path = db_path

    def executeSQL(self, *args):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if args.__len__() == 2:
                re = cursor.execute(args[0], args[1])
                re = re.fetchall()
                if re.__len__() == 0:
                    re = True
                else:
                    re = (True, re)
            elif args.__len__() == 1:
                re=cursor.execute(args[0])
                re = re.fetchall()
                if re.__len__() == 0:
                    re = (True,)
                else:
                    re = (True, re)
            else:
                re = (False,)
            conn.commit()
            cursor.close()
            conn.close()
            return re
        except:
            return (False,)

class DataProcess:
    def __init__(self):
        self.db = DB_sqlite("CNKI.db")

    def get_data(self):
        select_sql = "SELECT * FROM info"
        result = self.db.executeSQL(select_sql)
        print(result)
        insert_sql = 'INSERT INTO "save" ("title", "keywords") VALUES (?, ?)'
        for val in result:
            parse = (val[1], val[2])
            result = self.db.executeSQL(insert_sql, parse)
            print(result)

    def analyze_keywords(self):  # 根据词频统计信息
        select_sql = "SELECT keywords FROM save"
        status,result = self.db.executeSQL(select_sql)
        keywords = []
        if status:
            for val in result:
                keywords += str(val[0]).split("/")
        if keywords.__len__() == 0:
            return False
        else:
            print(Counter(keywords))

    def analyze_all(self):  # 根据词频统计信息
        select_sql = "SELECT * FROM save"
        status,result = self.db.executeSQL(select_sql)
        keywords = []
        if status:
            for val in result:
                keywords += [str(val[0])]
                keywords += str(val[1]).split("/")
        if keywords.__len__() == 0:
            return False
        else:
            keywords_str = " ".join(keywords)
            self.get_wordcount_by_string(keywords_str)

    def analyze_title(self):  # 根据标题统计信息
        select_sql = "SELECT title FROM save"
        status,result = self.db.executeSQL(select_sql)
        keywords = []
        if status:
            for val in result:
                keywords += [str(val[0])]
                # keywords += str(val[1]).split("/")
        if keywords.__len__() == 0:
            return False
        else:
            keywords_str = " ".join(keywords)
            self.get_wordcount_by_string(keywords_str)

    def get_wordcount_by_string(self, data):
        # seg_list = jieba.cut(data, cut_all=False)
        # print("Default Mode: " + "/ ".join(seg_list))
        keywords = jieba.analyse.extract_tags(data, topK=200, withWeight=True)
        for item in keywords:
            print(item[0], item[1])


if __name__ == '__main__':
    a = DataProcess()
    a.analyze_title()