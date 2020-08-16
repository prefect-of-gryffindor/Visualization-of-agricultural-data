import requests
import datetime
import json
import xlwt
url = "http://openapi.uml-tech.com/farm/getHistoryCanInfo"

payload = "{    \"did\": \"860675040644856\"," \
          "    \"gpsEndTime\": \"20190701235959\"," \
          "    \"filterIfMissing\": true," \
          "    \"pageSize\": 10," \
          "    \"pageType\": 0," \
          "    \"reversed\": false," \
          "    \"startRowkey\": \"z\"," \
          "    \"gpsStartTime\": \"20190701000000\"," \
          "    \"token\":\"92d4e3fef54e432a01127200365d039f\"," \
          "    \"vin\": \"\"\r\n}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text)
list = json.loads(response.text)
print(list)
list = list["result"]
print(list)
print(list[0])
can_dict=list[0]["can"]
k=can_dict.keys()
v=can_dict.values()
for i in k:
    print(i)