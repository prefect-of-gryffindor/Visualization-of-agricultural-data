# import pymysql
# conn = pymysql.connect(host='bj-cdb-knrsiywz.sql.tencentcdb.com',
#                        port=6082,
#                        user='root',
#                        password='weizhi2017',
#                        database='bochuang_data')
# # ------------------行驶总里程数据查询-----------------------------------------
# totalmiles = []
# cur11 = conn.cursor(cursor=pymysql.cursors.DictCursor)
# sql11 = "select (@i:=@i+1)pm,did,mileage from job_statistic_data,(SELECT @i:=0)t WHERE statisticType='year' ORDER BY mileage DESC limit 0,5"
# cur11.execute(sql11)
# rows06 = cur11.fetchall()
# for item in rows06:
#     totalmiles.append(item)
# print(type(totalmiles))
# print(totalmiles)

data =[(1,2,3),(2,3,4)]
print(data[0])
print(data[0].value[1])