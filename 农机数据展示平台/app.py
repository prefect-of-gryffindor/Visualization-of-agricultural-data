from flask import Flask
from flask import render_template  # 渲染
import pymysql
from flask import jsonify

def select_statistics(select_sql):
    """查询语句"""
    # 建立数据库连接
    db=pymysql.connect(
        host="bj-cdb-knrsiywz.sql.tencentcdb.com",
        port=6082,
        user="root",
        passwd="weizhi2017",
        db="bochuang_data",
        charset="utf8"
    )
    # 创建游标对象，并使查询结果以字典格式输出（列表嵌套字典，否则默认是元组嵌套元组）
    cur=db.cursor(cursor=pymysql.cursors.DictCursor)
    # excute()执行sql
    cur.execute(select_sql)
    # 使用fetchall()获取所有查询结果
    data=cur.fetchall()
    # 关闭游标
    cur.close()
    # 关闭数据库连接
    db.close()
    return data

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
    #jobFlag = [] #0-非作业，1-作业，2-暂停
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

    # ---------------------------------车辆类型SQL查询----------------------------------------
    cartype = []  # 车辆类型名
    carnum = []  # 车辆各类型数量统计
    # 连接mysql，括号内是服务器地址, 端口号, 用户名，密码，存放数据的数据库
    cur8 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql8 = "SELECT vehicleModelName,COUNT(*) FROM job_statistic_data GROUP BY vehicleModelName"
    cur8.execute(sql8)
    rows = cur8.fetchall()
    for item in rows:
        cartype.append(item['vehicleModelName'])
        carnum.append(item['COUNT(*)'])

    # ------------------车辆在线数据查询-----------------------------------------
    cur9 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql9 = "SELECT DISTINCT did FROM `work_data` where jobFlag='1' OR jobVehicleStatus='3'OR jobVehicleStatus='1'OR jobVehicleStatus='2'"
    cur9.execute(sql9)
    rows01 = cur9.fetchall()
    car_online = len(rows01)

    # ------------------作业车辆数据查询-----------------------------------------
    cur10 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql10 = "SELECT DISTINCT did FROM `work_data` WHERE jobFlag='1'"
    cur10.execute(sql10)
    rows02 = cur10.fetchall()
    car_work = len(rows02)

    # -------底部排名表开始
    # ------------------行驶总里程数据查询-----------------------------------------
    totalmiles = []
    cur11 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql11 = "select (@i:=@i+1)pm,did,mileage from job_statistic_data,(SELECT @i:=0)t WHERE statisticType='year' ORDER BY mileage DESC limit 0,5"
    cur11.execute(sql11)
    rows06 = cur11.fetchall()
    for item in rows06:
        totalmiles.append(item)

    # ------------------作业时长数据查询-----------------------------------------
    totaltime = []
    cur12 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql12 = "select (@i:=@i+1)pm,did,jobTime from job_statistic_data,(SELECT @i:=0)t WHERE statisticType='year' ORDER BY jobTime DESC limit 0,5"
    cur12.execute(sql12)
    rows07 = cur12.fetchall()
    for item in rows07:
        totaltime.append(item)

    # ------------------行驶最高时速数据查询-----------------------------------------
    cur13 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql13 = "select did,gpsSpeed from work_data ORDER BY gpsSpeed DESC  "
    cur13.execute(sql13)
    rows08 = cur13.fetchall()
    dids01 = []
    gpsSpeed = []
    count008 = 0
    for i in range(len(rows08)):
        if i == 0:
            count008 += 1
            dids01.append(rows08[i]['did'])
            gpsSpeed.append(rows08[i]['gpsSpeed'])
        elif rows08[i]['did'] != rows08[i - 1]['did']:
            count008 += 1
            dids01.append(rows08[i]['did'])
            gpsSpeed.append(rows08[i]['gpsSpeed'])
        if count008 == 5:
            break

    # ------------------累计油耗数据查询-----------------------------------------
    cur14 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql14 = "select did,totalFuelConsumption from work_data ORDER BY totalFuelConsumption DESC"
    cur14.execute(sql14)
    rows09 = cur14.fetchall()
    dids = []
    totalFuelConsumption = []
    count09 = 0
    for i in range(len(rows09)):
        if i == 0:
            count09 += 1
            dids.append(rows09[i]['did'])
            totalFuelConsumption.append(rows09[i]['totalFuelConsumption'])
        elif rows09[i]['did'] != rows09[i - 1]['did']:
            count09 += 1
            dids.append(rows09[i]['did'])
            totalFuelConsumption.append(rows09[i]['totalFuelConsumption'])
        if count09 == 5:
            break


    # # ------------------作业亩数数据查询-----------------------------------------
    # cur11 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # sql11 = "SELECT sum(jobArea) FROM `job_statistic_data` WHERE jobArea!='-100'"
    # cur11.execute(sql11)
    # rows03 = cur11.fetchall()
    # farm_area = rows03[0]['sum(jobArea)']
    #
    # # ------------------作业里程数据查询-----------------------------------------
    # cur12 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # sql12 = "SELECT sum(mileage) FROM `job_statistic_data` WHERE mileage!='-100'"
    # cur12.execute(sql12)
    # rows04 = cur12.fetchall()
    # miles = rows04[0]['sum(mileage)']
    #
    # # ------------------作业时长数据查询-----------------------------------------
    # cur13 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # sql13 = "SELECT sum(jobTime) FROM `job_statistic_data` WHERE jobTime!='-100'"
    # cur13.execute(sql13)
    # rows05 = cur13.fetchall()
    # jobtime = rows05[0]['sum(jobTime)']
   #---------------------------------------------------
    sql_month = "SELECT * FROM job_statistic_data WHERE statisticType='mont' AND statisticDate='201912'"
    res_month = select_statistics(sql_month)
    # !！开始 计算总亩数、总时长、总里程，提出-100无效值
    vehicle_model = []
    total_area = 0
    total_time = 0
    total_mileage = 0
    for i in range(len(res_month)):
        vehicle = res_month[i]
        temp_vehicle = vehicle['vehicleModelName']
        temp_area = vehicle['jobArea']
        temp_time = vehicle['jobTime']
        temp_mileage = vehicle['mileage']
        if temp_vehicle not in vehicle_model:
            vehicle_model.append(temp_vehicle)
        total_area += temp_area
        total_time += temp_time
        total_mileage += temp_mileage

    num_vehicle_area = []
    num_vehicle_time = []
    num_vehicle_mileage = []
    for j in range(len(vehicle_model)):
        temp_vehicle1 = vehicle_model[j]
        temp_num_area = 0
        temp_num_time = 0
        temp_num_mileage = 0
        for k in range(len(res_month)):
            if res_month[k]['vehicleModelName'] == temp_vehicle1:
                temp_num_area += res_month[k]['jobArea']
                temp_num_time += res_month[k]['jobTime']
                temp_num_mileage += res_month[k]['mileage']
        num_vehicle_area.append(temp_num_area)
        num_vehicle_time.append(temp_num_time)
        num_vehicle_mileage.append(temp_num_mileage)

        # cur12 = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # sql12 = "SELECT did,gpsSpeed FROM work_data ORDER BY gpsSpeed DESC"
        # cur12.execute(sql12)
        # data12 = cur12.fetchall()
        # dids = []
        # gpsSpeeds = []
        # count12 = 0
        # for i in range(len(data12)):
        #     if i==0:
        #         count12+=1
        #         dids.append(data12[i]['did'])
        #         gpsSpeeds.append(data12[i]['gpsSpeed'])
        #     elif data12[i]['did']!=data12[i-1]['did']:
        #         count12+=1
        #         dids.append(data12[i]['did'])
        #         gpsSpeeds.append(data12[i]['gpsSpeed'])
        #     if count12==5:
        #         break

        #
        # cur1.close()
        # cur2.close()
        # cur3.close()
        # cur4.close()
        # cur5.close()
        # cur6.close()
        # cur7.close()
        # cur8.close()
        # cur9.close()
        # cur10.close()
        # cur11.close()
        # cur12.close()
        # cur13.close()
        # cur14.close()
        # # conn.close()



    return render_template('index.html',did = did,GPSDateTime = GPSDateTime , numOfUsedSatellites = numOfUsedSatellites ,
                           num1 = num1 , num2 = num2,
                           province = province , pro_total = pro_total , pro_1 =pro_1 , pro_2 = pro_2, pro_3 = pro_3,
                           pro_4 = pro_4 , pro_5 = pro_5 , pro_6 = pro_6, pro_7 = pro_7 , pro_8 = pro_8 , pro_9 = pro_9 ,
                           pro_10 = pro_10 , cartype = cartype , carnum = carnum , car_online = car_online , car_work = car_work ,
                           total_area=total_area,total_time=total_time,total_mileage=total_mileage,vehicle_model=vehicle_model,
                           num_vehicle_area=num_vehicle_area,num_vehicle_time=num_vehicle_time,num_vehicle_mileage=num_vehicle_mileage ,
                           totalmiles = totalmiles , totaltime = totaltime , dids01 = dids01 , gpsSpeed = gpsSpeed ,
                           dids = dids , totalFuelConsumption = totalFuelConsumption)
    # 把index.html文件读进来，再交给浏览器

@app.route('/')
def tt():
    return news()


@app.route('/t1')
def text1():
    # sql_work_data="SELECT did GPSDateTime, numOfUsedSatellites, GPSLat,GPSLon,altitude,direction,GPSModuleStatus,gpsSpeed FROM work_data"
    # 车辆信息表
    sql_machine="SELECT * FROM agricultural_machine_data"
    res_machine=select_statistics(sql_machine)
    group_name=[]
    vehicle_model_name=[]
    for i in range(len(res_machine)):
        vehicle = res_machine[i]
        temp_group_name = vehicle['GroupName']
        temp_vehicle_model_name=vehicle['vehicleModelName']
        if temp_group_name not in group_name:
            group_name.append(temp_group_name)
        if temp_vehicle_model_name not in vehicle_model_name:
            vehicle_model_name.append(temp_vehicle_model_name)
    # return render_template('HTML_t1.html',res_machine=res_machine)
    return render_template('text_1.html',res_machine=res_machine)

@app.route('/t4')
def text4():
    return render_template('text_4.html')


if __name__ == '__main__':
    app.run()  # 127.0.0.1 回路 自己返回自己
