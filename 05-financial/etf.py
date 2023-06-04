import requests
import json
import datetime
from lxml import etree

# 获取基金详情
def getFundDetail(code):
    url = "http://fund.eastmoney.com/{}.html".format(code)
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    r = requests.get(url, header)
    html = r.content
    element = etree.HTML(html)
    type = element.xpath("//div[@class='infoOfFund']//tr[1]//td[1]//text()")
    money = element.xpath("//div[@class='infoOfFund']//tr[1]//td[2]//text()")
    manager = element.xpath("//div[@class='infoOfFund']//tr[1]//td[3]//text()")
    create_date = element.xpath("//div[@class='infoOfFund']//tr[2]//td[1]//text()")
    company = element.xpath("//div[@class='infoOfFund']//tr[2]//td[2]//text()")
    error = element.xpath("//div[@class='infoOfFund']//tr[3]//td[1]//text()")
    if len(error) > 0:
        error = error[-1]
    
    url = "http://fundf10.eastmoney.com/jjfl_{}.html".format(code)
    r = requests.get(url, header)
    html = r.content
    element = etree.HTML(html)
    cost = element.xpath("//div[@class='box'][4]//table[@class='w770 comm jjfl'][1]//tr[1]//td//text()")
    info = {
        'type': type[1],
        'money': float(money[1].replace("：", "").split('亿元', 1)[0]),
        'manager': manager[1],
        'create_date': create_date[1].replace("：", ""),
        'company': company[2]  + "管理有限公司",
        'error': error,
        'manage_cost': cost[1].replace("（每年）", ""),
        'host_cost': cost[3].replace("（每年）", "")
    }
    
    return info

# 获取指数基金
def getIndexFunds(keyword):
    url="http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?m=1&key={}&pageindex=0&pagesize=200".format(keyword)
    r = requests.get(url)
    content = json.loads(r.content)
    list = content["Datas"]
    return list

# 获取基金公司
def getFundCompany():
    company = []
    url="http://fund.eastmoney.com/Data/FundRankScale.aspx"
    r = requests.get(url)
    res = str(r.content[16:-1], 'utf-8')
    for item in res.split("["):
        items = item.rstrip('],').replace("'", "").split(',')
        if len(items) < 6:
            continue
        money = 0
        if len(items[7]) > 0:
            money = float(items[7])
        company.append({
            "code": items[0],
            "name": items[1],
            "create_date": items[2],
            "money": float(money),
        })
    return company

def getDayDiff(date):
    d1 = datetime.datetime.strptime(date, '%Y-%m-%d')
    d2 = datetime.datetime.now()
    return (d2 - d1).days

# top10的基金公司
company = getFundCompany()
company = sorted(company, key=lambda x: x["money"], reverse=1)
company = company[:10]
companys = {item["name"] : item for item in company}
    
list = getIndexFunds("上证50")
# print(len(list), companyInfo)
print('代码,基金名称,成立时间,基金规模,跟踪误差,基金公司规模,管理费,托管费,交易方式')
for item in list:
    fundInfo = getFundDetail(item['CODE'])
    if fundInfo['company'] not in companys:
#         print("000", item['CODE'], fundInfo['company'])
        continue
        
    # 第一个是排除名称里带有【分级】字样的 
    if '分级' in item['NAME']:
        continue
    # 第二个是剔除名称里带【增强】的 
    if '增强' in item['NAME']:
        continue
    # 第三个是剔除名称里带有【行业】的基金，
    if '行业' in item['NAME']:
        continue
    companyInfo = companys[fundInfo['company']]
    # 基金规模超过 2 亿
    if fundInfo['money'] < 2:
#         print("1111", item['CODE'], fundInfo['money'])
        continue
    # 成立年限超过 1 年
    if getDayDiff(fundInfo['create_date']) < 3 * 365:
#         print("2222", item['CODE'], fundInfo['create_date'])
        continue
    # 基金公司规模超过 1000 亿
    if companyInfo['money'] < 1000:
#         print("2222", item['CODE'], companyInfo['money'])
        continue
    print("{},{},{},{},{},{},{},{},{}".format(
        item['CODE'],
        item['NAME'],
        fundInfo['create_date'],
        "{} {}".format(fundInfo['money'], "亿元"),
        fundInfo['error'],
        "{} {}".format(companyInfo['money'], "亿元"),
        fundInfo['manage_cost'],
        fundInfo['host_cost'],
        fundInfo['type']
    ))
