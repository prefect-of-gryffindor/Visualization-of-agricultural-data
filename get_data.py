import requests
import datetime
from openpyxl import load_workbook
from openpyxl import workbook
import json

url = "http://openapi.uml-tech.com/farm/getHistoryCanInfo"
header = {'Content-Type': 'application/json'}
excel = load_workbook('50_did.xlsx')
table = excel.get_sheet_by_name('Sheet1')
cell_range = table['c2':'c51']
wb = workbook()
ws = wb.active
count = 0
for cell in cell_range:
    body = "{    \"did\": \""+cell[0].value+"\"," \
              "    \"gpsEndTime\": \"20191231235959\"," \
              "    \"filterIfMissing\": true," \
              "    \"pageSize\": 10000," \
              "    \"pageType\": 0," \
              "    \"reversed\": false," \
              "    \"startRowkey\": \"a\"," \
              "    \"gpsStartTime\": \"20190101000000\"," \
              "    \"token\": \"92d4e3fef54e432a01127200365d039f\"," \
              "    \"vin\": \"\"\r\n}"
    response = requests.post(url=url , headers=header , data=body)
    count +=1
    print("这是向农机can数据接口的第：{0}次发送".format(count))
    if(response.status_code==200):
        print("请求成功")
        list = json.loads(response.text)['result']
        for j in range(len(list)):
            can_dict = list[j]['can']


    else:
        print("请求失败")
    print(response.text.encode('utf8'))

