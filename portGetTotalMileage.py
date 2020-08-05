import xlrd
import requests
import json
import xlwt

def getDataDids(filePath):
    fileDids=xlrd.open_workbook(filePath)
    sheet=fileDids.sheet_by_index(0)
    dataDids=sheet.col_values(2,1)  # 第3列，第2开始
    return(dataDids)

def responseGetTotalMileage(dids):
    print(dids)
    url="http://openapi.uml-tech.com/farm/getTotalMileage"
    payload=json.dumps(
        {
            "dids":dids,
            "token":"92d4e3fef54e432a01127200365d039f",
            "vins":""
        }
    )
    headers={'Content-Type':'application/json'}
    response=requests.request("POST",url,headers=headers,data=payload)
    # "result": [
    #     {
    #         "860675041728880": 0.0
    #     }
    # ],
    if response.json()['result']:
        result=response.json()['result'][0]  #['data']['token']
        for i in result:
            mileage=result[i]
            print(mileage)
    else:
        mileage=0  # 返回为空时自动补为0
        print(mileage)
    return mileage

def getAll(dataDids):
    mileages=[]
    for index in range(len(dataDids)):
        mileage=responseGetTotalMileage(dataDids[index])
        #print(mileage)
        mileages.append(mileage)
    return mileages

    # for index in range(5):
    #     did=dataDids[index]
    #     mileage=responseGetTotalMileage(did)
    #     #mileage=responseGetTotalMileage(dataDids[index])
    #     #print(mileage)
    #     mileages.append(mileage)
    # return mileages

def saveToExcel(dataDids,mileages,path):
    rows=len(dataDids)
    workbook=xlwt.Workbook()
    sheet=workbook.add_sheet("sheet1")
    for row in range(rows):
        sheet.write(row,0,dataDids[row])
        sheet.write(row,1,mileages[row])
    workbook.save(path)
    print("写入EXCEL成功！")

if __name__=='__main__':
    dataDids=getDataDids("dataTractor1-50.xlsx")
    mileages=getAll(dataDids)
    saveToExcel(dataDids,mileages,"ResultGetTotalMileage.xls")
