import requests
import datetime
import xlwt
import json

url_1 = "http://openapi.uml-tech.com/farm/getHistoryCanInfo"
url_2 = "http://openapi.uml-tech.com/farm/getHistoryGpsInfo"
header = {'Content-Type': 'application/json'}
dict = [
    "860675040778035",
    "WUZ21115BG100088",
    "862237044558679",
    "860675041723139",
    "860675041846369",
    "862237044104961",
    "862237044557200",
    "860675045986104",
    "BWZ1102005100033",
    "015127181207",
    "860675041729946",
    "862237044026834",
    "862237044146061",
    "860675041911387",
    "860675041938612",
    "862237044012636",
    "860675041727148",
    "862237044015969",
    "NJHYBVHAT0000352",
    "860675040512533",
    "860675040765925",
    "862237044558455",
    "862237044615149",
    "862237044007362",
    "860675040644856",
    "862237044544596",
    "862237044020233",
    "862237044071426",
    "860675041848407",
    "860675045977145",
    "NJHYKBOAU0000041",
    "862237044524705",
    "XJXY220200300130",
    "860675040631655",
    "862237044068174",
    "860675041774769",
    "860675045983689",
    "860675041728880",
    "NJHYTFQAT0000029",
    "862237044132103",
    "862237044036791",
    "015127180910",
    "NJHYBQSAU0000029",
    "NJHYEFDAT0000020",
    "862237044075377",
    "860675041725829",
    "862237044540990",
    "860675046024699",
    "862237044532583",
    "860675041912195",
]
list = []
count = 0
workbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet_1 = workbook.add_sheet('data',cell_overwrite_ok=True)
sheet_2 = workbook.add_sheet('data',cell_overwrite_ok=True)
begin = datetime.date(2019,7,1)
end  = datetime.date(2019,8,31)
delta = (end-begin).days+1
for i in dict:
    for j in range(delta):
        day = begin + datetime.timedelta(days=j)
        day=str(day).replace("-","")
        body_1 = "{    \"did\": \""+i+"\"," \
                  "    \"gpsEndTime\": \""+day+"235959\"," \
                  "    \"filterIfMissing\": true," \
                  "    \"pageSize\": 10," \
                  "    \"pageType\": 0," \
                  "    \"reversed\": false," \
                  "    \"startRowkey\": \"a\"," \
                  "    \"gpsStartTime\": \""+day+"000000\"," \
                  "    \"token\": \"92d4e3fef54e432a01127200365d039f\"," \
                  "    \"vin\": \"\"\r\n}"
        body_2 = "{    \"did\": \""+i+"\"," \
                  "    \"gpsEndTime\": \""+day+"235959\"," \
                  "    \"pageSize\": 10," \
                  "    \"pageType\": 1," \
                  "    \"reversed\": true," \
                  "   \"startRowkey\": \"a\"," \
                  "    \"gpsStartTime\": \""+day+"000000\"," \
                  "    \"token\": \"92d4e3fef54e432a01127200365d039f\"," \
                  "    \"vin\": \"\"}"
        response_1 = requests.post(url=url_1 , headers=header , data=body_1)
        response_2 = requests.post(url=url_2 , headers=header , data=body_2)
        count +=1
        print("这是向农机can数据接口的第：{0}次发送".format(count))
        if(response_1.status_code==200):
            list.append(count)
            print ("请求成功")
        else:
            print ("请求失败")
        print(response_1.text.encode('utf8'))
        print("这是向农机历史轨迹查询接口的第：{0}次发送".format(count))
        if(response_2.status_code==200):
            list.append(count)
            print ("请求成功")
        else:
            print ("请求失败")
        print(response_2.text.encode('utf8'))

