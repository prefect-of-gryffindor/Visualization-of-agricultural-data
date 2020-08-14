# -*- coding: UTF-8 -*-
import pymysql
import os
import json
from flask_cors import *

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from flask import Flask, request

app1 = Flask(__name__)


@app1.route('/')
def getcontent():
    conn = pymysql.connect(host='bj-cdb-knrsiywz.sql.tencentcdb.com',
                           port=6082,
                           user='root',
                           password='weizhi2017',
                           database='bochuang_data')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "SELECT * FROM work_data"
    cur.execute(sql)
    data = cur.fetchall()
    # print(data)
    para = []
    for i in data:
        #text = {'name': i[0], 'class': i[1], 'number': i[2], 'score': i[3]}
        # print(text)
        para.append(i)
    return json.dumps(para, ensure_ascii=False)
    return 'hello world'


if __name__ == '__main__':
    app1.run()  #有的电脑上 port 5000不能用（我的电脑可以）