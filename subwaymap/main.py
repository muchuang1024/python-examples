#!/usr/bin/python
# coding=utf-8

import requests
import time
import json
import ast
import os
import utils
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree

PAGE_URL = 'http://map.amap.com/subway/index.html?&1100'
DATA_URL = 'http://map.amap.com/service/subway?srhdata='
HEADER  = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}


def fetchAllCity(url, header):
    r = requests.get(url, header)
    html = r.content
    element = etree.HTML(html)
    options = element.xpath("//a[contains(@class, 'city')]")
    
    cities = []
    for option in options:
        city = {
            'id': option.get('id'),
            'name': option.get('cityname'),
            'text': option.text
        }
        cities.append(city)

    return cities

def parseAllCityData(cities):
    # 启动一个chrome浏览器
    browser = webdriver.Chrome()
    browser.get(PAGE_URL)
    data = [];
    for city in cities:
        data.append(parseCityData(city, browser))
    return data 

def saveData(citiesData):
    path = './data/'
    if not os.path.exists(path):
        os.mkdir(path)
    for cityData in citiesData:
        f = open(path + cityData['name'] + '.json', 'w')
        # dict to json; json to str
        f.write(str(json.dumps(cityData)))

def parseCityData(city, browser):
    apiData   = parseCityDataFromApi(city)
    domData   = parseCityDataFromDom(city, browser)

    return    formatCityData(apiData, domData)

def parseCityDataFromApi(city):
    url =  DATA_URL + "{}_drw_{}.json".format(city['id'], city['name'])
    print(url)
    r = requests.get(url)
    #  字符串转json(ast.literal_eval())
    return eval(r.text.encode('utf-8'))
    

def parseCityDataFromDom(city, browser):
    id = city['id']
    # hidden 元素需要手动hover后才能执行，下面那种方式完全自动化了，因此采用下面的做法
    # element = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.ID, id)))
    # element.click()
    menu = browser.find_element_by_css_selector(".more-city")
    el   = browser.find_element_by_id(id)
    # hover 隐藏菜单然后点击
    webdriver.common.action_chains.ActionChains(browser).move_to_element(menu).click(el).perform()
    # 等ajax请求加载完
    time.sleep(2)
    element = etree.HTML(browser.page_source)
    # lines = element.xpath("//g[@id='g-line']/path")
    # stations = element.xpath("//g[@id='g-station']/circle")
    stationNames = element.xpath("//g[@id='g-station-name']/g/text")
    result = {
        'st': {}
    }

    for station in stationNames:
         sid =  station.get('id').split('-')[1]
         # 站点名称坐标
         result['st'][sid] = {}
         result['st'][sid]['lp'] = {
            'x': int(station.get('x')),
            'y': int(station.get('y'))
         }

    return result

def formatCityData(apiData, domData):
   # string to json 
   data = {
        'name': apiData['s'],
        'l': [],
   }
   lines = apiData['l']
   # list get index and value
   for lidx, line in enumerate(lines):
        labelp = []
        p = []
        for val in line['lp']:
            labelp.append(utils.getP(val))
        for val in line['c']:
            p.append(utils.getP(val))
        l  = {
            'name': line['ln'],
            'p': p,
            'labelp': labelp,
            'st': [],
            'la': line['la']
        }
        for sidx, stop in enumerate(line['st']):
           # 开通的站
           if line['st'][sidx]['su'] == '1':
                labelp  = domData['st'][stop['si']]['lp'];
                st = {
                    'name': stop['n'],
                    'p': utils.getP(stop['p']),
                    'labelp': labelp,
                    'strans': stop['t'] 
                }
                l['st'].append(st)
        data["l"].append(l)

   return data


def main():
    cities = fetchAllCity(PAGE_URL, HEADER)
    print(cities)
    citiesData = parseAllCityData(cities)
    saveData(citiesData)

if __name__ == '__main__':
    main()
