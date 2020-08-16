from flask import Flask
from flask import render_template  # 渲染
import pymysql

app = Flask(__name__)


@app.route('/index')  # 主页地址,“装饰器”
def news():
    conn = pymysql.connect(host='bj-cdb-knrsiywz.sql.tencentcdb.com',
                           port=6082,
                           user='root',
                           password='weizhi2017',
                           database='bochuang_data')
    cur1 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql1 = "SELECT * FROM work_data"
    cur1.execute(sql1)
    data = cur1.fetchall()
    #获取做右上角折线图所需数据
    did = []
    GPSDateTime = []
    numOfUsedSatellites = []
    jobFlag = [] #0-非作业，1-作业，2-暂停
    for i in range(len(data)):
        if i==0:
            did.append(data[i]['did'])
            GPSDateTime.append(data[i]['GPSDateTime'])
            numOfUsedSatellites.append(data[i]['numOfUsedSatellites'])
        elif data[i]['did']!=data[i-1]['did'] and data[i]['numOfUsedSatellites']==data[i-1]['numOfUsedSatellites']:
            did.append(data[i]['did'])
            GPSDateTime.append(data[i]['GPSDateTime'])
            numOfUsedSatellites.append(data[i]['numOfUsedSatellites'])
        elif data[i]['numOfUsedSatellites']!=data[i-1]['numOfUsedSatellites']:
            did.append(data[i]['did'])
            GPSDateTime.append(data[i]['GPSDateTime'])
            numOfUsedSatellites.append(data[i]['numOfUsedSatellites'])

    #获取按照jobflag的值分类的农机数
    cur2 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql2 = "SELECT DISTINCT did FROM work_data WHERE jobFlag='1'"
    cur2.execute(sql2)
    did_1 = cur2.fetchall()
    did_jF_1 = []
    for i in did_1:
        did_jF_1.append(i['did'])
    #jobFlag=0
    cur3 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql3 = "SELECT DISTINCT did FROM work_data WHERE jobFlag='0'"
    cur3.execute(sql3)
    did_0 = cur3.fetchall()
    did_jF_0 = []
    for i in did_0:
        if i['did'] not in did_jF_1:
            did_jF_0.append(i['did'])
    #vehicleModelName=拖拉机，TS804A，抛秧机，GF80(4LZ-8，甘蔗机，玉米机，4HZJ-2500，潍柴动力测试，勇猛玉米机车型，5AQ1
    cur4 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql4 = "SELECT did,vehicleModelName FROM agricultural_machine_data"
    cur4.execute(sql4)
    data4 = cur4.fetchall()
    num1 = [0,0,0,0]
    num2 = [0,0,0,0]
    for i in data4:
        if i['vehicleModelName']=='甘蔗机' and (i['did'] in did_jF_1):
            num1[0]+=1
        elif i['vehicleModelName']=='甘蔗机' and (i['did'] in did_jF_0):
            num2[0]+=1
        elif i['vehicleModelName']=='玉米机' and (i['did'] in did_jF_1):
            num1[1]+=1
        elif i['vehicleModelName']=='玉米机' and (i['did'] in did_jF_0):
            num2[1]+=1
        elif i['vehicleModelName']=='拖拉机' and (i['did'] in did_jF_1):
            num1[2]+=1
        elif i['vehicleModelName']=='拖拉机' and (i['did'] in did_jF_0):
            num2[2]+=1
        elif i['vehicleModelName']=='GF80(4LZ-8' and (i['did'] in did_jF_1):
            num1[3]+=1
        elif i['vehicleModelName']=='GF80(4LZ-8' and (i['did'] in did_jF_0):
            num2[3]+=1


        #获取地图可视化数据
        cur5 = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql5 = "SELECT did,province FROM farm_info_pro"
        cur5.execute(sql5)
        data5 = cur5.fetchall()

        #获取不重复province
        cur6 = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql6 = "SELECT DISTINCT province FROM farm_info_pro"
        cur6.execute(sql6)
        pro = cur6.fetchall()#五个元素，即五个省份中文名称
        province = []
        for i in pro:
            province.append(i['province'])

        #获取每个省份的对应总作业农机数
        pro_total = []
        pro_1 = []#五个元素，即五个省份对应的作业甘蔗机数
        pro_2 = []#...对应玉米机数
        pro_3 = []#...对应抛秧机数
        pro_4 = []#...对应拖拉机数
        pro_5 = []#...勇猛玉米机车型
        pro_6 = []#...潍柴动力测试
        pro_7 = []#...TS804A
        pro_8 = []#...GF80(4LZ-8
        pro_9 = []#...4HZJ-2500
        pro_10 = []#...5AQ1
        cur7 = conn.cursor(cursor=pymysql.cursors.DictCursor)
        for i in province:
            sql7 = "SELECT DISTINCT did FROM farm_info_pro WHERE province='%s'"%i
            cur7.execute(sql7)
            pro_t = cur7.fetchall()
            pro_total.append(len(pro_t))#五个元素，即五个省份对应的总作业农机数
            count_1 = 0
            count_2 = 0
            count_3 = 0
            count_4 = 0
            count_5 = 0
            count_6 = 0
            count_7 = 0
            count_8 = 0
            count_9 = 0
            count_10 = 0
            for j in pro_t:
                for z in data4:
                    if j['did']==z['did'] and z['vehicleModelName']=='甘蔗机':
                        count_1+=1
                    elif j['did']==z['did'] and z['vehicleModelName']=='玉米机':
                        count_2+=1
                    elif j['did'] == z['did'] and z['vehicleModelName'] == '抛秧机':
                        count_3+=1
                    elif j['did'] == z['did'] and z['vehicleModelName'] == '拖拉机':
                        count_4+=1
                    elif j['did'] == z['did'] and z['vehicleModelName'] == '勇猛玉米机车型':
                        count_5+=1
                    elif j['did'] == z['did'] and z['vehicleModelName'] == '潍柴动力测试':
                        count_6+=1
                    elif j['did'] == z['did'] and z['vehicleModelName'] == 'TS804A':
                        count_7+=1
                    elif j['did'] == z['did'] and z['vehicleModelName'] == 'GF80(4LZ-8':
                        count_8+=1
                    elif j['did'] == z['did'] and z['vehicleModelName'] == '4HZJ-2500':
                        count_9+=1
                    elif j['did'] == z['did'] and z['vehicleModelName'] == '5AQ1':
                        count_10+=1
            pro_1.append(count_1)
            pro_2.append(count_2)
            pro_3.append(count_3)
            pro_4.append(count_4)
            pro_5.append(count_5)
            pro_6.append(count_6)
            pro_7.append(count_7)
            pro_8.append(count_8)
            pro_9.append(count_9)
            pro_10.append(count_10)


    return render_template('index_test1.html',did = did,GPSDateTime = GPSDateTime , numOfUsedSatellites = numOfUsedSatellites ,
                           num1 = num1 , num2 = num2,
                           province = province , pro_total = pro_total , pro_1 =pro_1 , pro_2 = pro_2, pro_3 = pro_3,
                           pro_4 = pro_4 , pro_5 = pro_5 , pro_6 = pro_6, pro_7 = pro_7 , pro_8 = pro_8 , pro_9 = pro_9 ,
                           pro_10 = pro_10)
    # 把index.html文件读进来，再交给浏览器

@app.route('/')
def tt():
    return news()


@app.route('/t1')
def text1():
    return render_template('text_1.html')

@app.route('/t4')
def text4():
    return render_template('text_4.html')


if __name__ == '__main__':
    app.run()  # 127.0.0.1 回路 自己返回自己
