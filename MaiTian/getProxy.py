import requests
import json
response = requests.get(
            'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=4d9d6f7844ac4ff0ba9741196055ffb0&orderno=YZ20193105820IhjYI2&returnType=2&count=5')
data = json.loads(response.text)['RESULT']
url = 'http://www.baidu.com'
usage_list = []
for i in data:
    proxy = {i['ip'] : i['port']}
    response = requests.get(url,proxies=proxy)
    if response.status_code == 200:
        proxy = 'http://' +i['ip'] + ":" + i['port']
        usage_list.append(proxy)

for i in usage_list:
    print("'{}',".format(i))