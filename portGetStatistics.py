import xlrd
# import xlwt
import requests
import json
import openpyxl
import datetime

def getdids():
    file1=xlrd.open_workbook("50辆农机.xlsx")
    sheet1=file1.sheet_by_index(0)
    Dids=sheet1.col_values(2,1)
    didsStr=""
    # print(type(Dids[1]))  # str
    for did in Dids:
        # print(did)
        if did==Dids[-1]:
            didsStr += did
        else:
            didsStr += did+","
    return didsStr



# 发送请求，并解析响应
def responseGetStatistics(paraDate, paraDid):
    url = "http://openapi.uml-tech.com/farm/getStatistics"
    # paraDid="WCHT201805C00008"
    payload = json.dumps(
        {
            "day": paraDate,
            "dids": paraDid,
            "token": "92d4e3fef54e432a01127200365d039f",
            "type": "month",
            "vins": ""
        }
    )
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)

    # "result": [
    #     {
    #         "avgDepth": 0.0,
    #         "avgPercentOfPass": 0.0,
    #         "did": "NJHYBVHAT0000352",
    #         "jobArea": 0.73,
    #         "jobTime": 20.7667,
    #         "mileage": 0.0
    #     }
    # ]

    # 设置默认值
    avgDepth = -100
    avgPercentOfPass = -100
    jobArea = -100
    jobTime = -100
    mileage = -100
    tempdataAll=[]
    if response.json()['result']:   # response.json()['result']是一个列表，元素为字典
        resultList=response.json()['result']
        # 获取得到result的字典
        for i in range(len(resultList)):
            result=resultList[i]
            did=result["did"]
            for k in result.keys():
                if k == "avgDepth":
                    avgDepth = result['avgDepth']
                elif k == "avgPercentOfPass":
                    avgPercentOfPass = result['avgPercentOfPass']
                elif k == "jobArea":
                    jobArea = result['jobArea']
                elif k == "jobTime":
                    jobTime = result['jobTime']
                elif k == "mileage":
                    mileage = result['mileage']

            tempDid = [did, "jobEquipment", "month", paraDate, avgDepth, avgPercentOfPass, jobArea, jobTime, mileage]
            tempdataAll.append(tempDid)
        return tempdataAll
    else:
        print("全空啦！")
        return tempdataAll

# 日期循环函数
def dateRange(paraBegin, paraEnd, paraStep):
    while paraBegin < paraEnd:
        yield paraBegin
        paraBegin += paraStep


if __name__=='__main__':
    dids=getdids()
    print(dids)

    begin = datetime.date(2019, 1, 1)
    end = datetime.date(2020, 1, 1)
    # step = datetime.timedelta(days=1)
    # step=datetime.timedelta(weeks=1)
    step=datetime.timedelta(days=31)  # 按月获取
    #datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    # date="20190101"
    dataAll = []
    workbook = openpyxl.Workbook()
    sheet = workbook.active  # 注意没有加()
    for date in dateRange(begin, end, step):
        dateStr = date.strftime("%Y%m%d")
        temp=responseGetStatistics(dateStr,dids)
        dataAll.append(temp)
        # print(temp)
        for j in temp:
            sheet.append(j)
        # sheet.append(temp)
    # print(dataAll)
    workbook.save("ResultGetStatisticsMonth.xlsx")
    print("写入EXCEL成功！")


