import requests
import json

proxy_api = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=4d9d6f7844ac4ff0ba9741196055ffb0&orderno=YZ20193105820IhjYI2&returnType=2&count=1"
response = requests.get(proxy_api)
data = json.loads(response.text)
data = data['RESULT'][0]

print(data['ip'])