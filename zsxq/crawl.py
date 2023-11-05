# 请求url并打印结果

# 注意json 中int 必须为 string

import requests
import json

headers_group = {
  "accept": "application/json, text/plain, */*",
  "accept-encoding": "gzip, deflate, br",
  "accept-language": "zh-CN,zh;q=0.9",
  "cache-control": "no-cache",
  "cookie": "UM_distinctid=188126c9de5337-07a7abb9fd0331-1b525635-13c680-188126c9de61027; _ga=GA1.1.1002968551.1693924669; _ga_GDWQY4XZV0=GS1.1.1696917573.19.0.1696917573.0.0.0; zsxq_access_token=1549B62D-EC34-C9D1-18C4-9F0122DA1AD2_D1C6A4222B5F9CAF; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22225444245111%22%2C%22first_id%22%3A%2218824493cfa898-0c30cc82c2f499-1b525635-1296000-18824493cfb153a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fxiaobot.net%2F%22%7D%2C%22%24device_id%22%3A%2218824493cfa898-0c30cc82c2f499-1b525635-1296000-18824493cfb153a%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfy29va2llX2lkIjoiMTg4Mjk5NDAwMWE1MzJkOTktMWE3Zi05MTFmMmFhNjM3Y2FkLTIyNTQ0NDI0NTE1MTEtMTExIn0=%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22225444245111%22%7D%7D; abtest_env=product; zsxqsessionid=6fa9c7672e24dc2fada79e453adc229b; __cuid=00bdeb1fab624f0bbe899542d7d07fda; amp_fef1e8=169da19e-4836-4e96-9ee7-94eeabc53f18R...1he0d9b46.1he0d9b49.2.2.4",
  "dnt": 1,
  "origin": "https://wx.zsxq.com",
  "pragma": "no-cache",
  "referer": "https://wx.zsxq.com/",
  "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "macOS",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-site",
  "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
  "x-request-id": "820c80e29-2bf0-4d33-fb8d-3dc621004ad",
  "x-signature": "53998a061597cf1c91e06bd3a2f6fa7935ad2d73",
  "x-timestamp": "1698673871",
  "x-version": "2.45.0"
}

print(headers_group)

data = requests.get("https://api.zsxq.com/v2/groups/15552545485212/topics?scope=digests&count=20", headers=json.dump(headers_group)

# Serializing json
json_object = json.dumps(json.loads(data.text), indent=4, ensure_ascii=False)
 
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)