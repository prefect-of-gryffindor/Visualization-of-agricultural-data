# 最新点位信息：查询返回车辆最后上报的位置信息

import xlrd
import requests
import json
import xlwt

def getDataDids(filePath):
    fileDids=xlrd.open_workbook(filePath)
    sheet=fileDids.sheet_by_index(0)
    dataDids=sheet.col_values(2,1)  # 第3列，第2开始
    return(dataDids)

def responseGetOnline(dids):
    url="http://openapi.uml-tech.com/farm/getRealTime"
    payload=json.dumps(
        {
            "dids":dids,
            "showColums":"GPSLat,GPSLon",
            "token":"92d4e3fef54e432a01127200365d039f",
            "vins":""
        }
    )
    headers={'Content-Type':'application/json'}
    response=requests.request("POST",url,headers=headers,data=payload)
    # {
    #     "GPSLat": "30.842377",
    #     "gcjLat": "30.83999327144654",
    #     "GPSLon": "113.987177",
    #     "gcjLon": "113.99276471836312",
    #     "bdLon": "113.99360695262988",
    #     "bdLat": "30.84864538540465"
    # }   #返回示例，只要GPS经纬度即可
    GPSLat=response.json()['result'][0]['GPSLat']  #['data']['token']
    GPSLon=response.json()['result'][0]['GPSLon']
    return GPSLat,GPSLon

def getAll(dataDids):
    GPSLats=[]
    GPSLons=[]
    for index in range(len(dataDids)):
        #print(dataDids[index])
        GPSLat,GPSLon=responseGetOnline(dataDids[index])
        GPSLats.append(GPSLat)
        GPSLons.append(GPSLon)
    return GPSLats,GPSLons

 # 分段测试所用代码
    # for index in range(30,49,1):
    #     #print(dataDids[index])
    #     print(dataDids[index])
    #     print(type(dataDids[index]))
    #     GPSLat,GPSLon=responseGetOnline(dataDids[index])
    #     print(GPSLat,GPSLon)
    #     #GPSLats.append(GPSLat)
    #     #GPSLons.append(GPSLon)
    # return GPSLats,GPSLons

def saveToExcel(dataDids,GPSLats,GPSLons,path):
    rows=len(dataDids)
    workbook=xlwt.Workbook()
    sheet=workbook.add_sheet("sheet1")
    for row in range(rows):
        sheet.write(row,0,dataDids[row])
        sheet.write(row,1,GPSLats[row])
        sheet.write(row,2,GPSLons[row])
    workbook.save(path)
    print("写入EXCEL成功！")

if __name__=='__main__':
    #dids="860675041848407"
    # GPSLat,GPSLon=responseGetOnline(dids)
    dataDids = getDataDids("dataTractor1-50.xlsx")
    GPSLats,GPSLons=getAll(dataDids)
    print(dataDids,GPSLats,GPSLons)
    saveToExcel(dataDids,GPSLats,GPSLons,"ResultGetRealTime.xls") #注意必须是.xls，不能.xlsx