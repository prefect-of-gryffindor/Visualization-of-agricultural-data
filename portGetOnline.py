import xlrd
import requests
import json
import xlwt

def getDataDids(filePath):
    fileDids=xlrd.open_workbook(filePath)
    sheet=fileDids.sheet_by_index(0)
    dataDids=sheet.col_values(2,1)  # 第3列，第2-52行（不含第52行）
    return(dataDids)

def responseGetOnline(dids,minute):
    url="http://openapi.uml-tech.com/farm/getOnline"
    payload=json.dumps(
        {
            "dids":dids,
            "onlineOffset": minute,
            "today": "",
            "token":"92d4e3fef54e432a01127200365d039f",
            "vins":""
        }
    )
    headers={'Content-Type':'application/json'}
    response=requests.request("POST",url,headers=headers,data=payload)
    result=response.json()['result']  #['data']['token']
    if result:
        print("有数据！")
        return "yes"
    else:
        print("sorry!")
        return "no"
    #return(result)

def getAll(dataDids):


if __name__=='__main__':
    dataDids=getDataDids("dataTractor1-50.xlsx")
    minute= -120 #前120分钟内是否登录过
    for index in range(len(dataDids)):
         responseGetOnline(dataDids[index],minute)
    # for index in range(48):
    #     responseGetOnline(dataDids[index])