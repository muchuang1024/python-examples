#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding=utf-8

import requests
import time
import json
import os
from selenium import webdriver
from lxml import etree

PAGE_URL = 'http://map.amap.com/subway/index.html?&1100'
DATA_URL = 'http://map.amap.com/service/subway?srhdata='
HEADER  = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}


def fetchAllCity(url, header):
    r = requests.get(url, header)
    html = r.content
    element = etree.HTML(html)
    options = element.xpath("//a[@class='city']")
    
    cities = []
    for option in options:
        city = {
            'id': option.get('id'),
            'name': option.get('cityname')
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
    path = './city/'
    if not os.path.exists(path):
        os.mkdir(path)
    for cityData in citiesData:
        print(cityData, type(cityData))
        f = open(path + cityData['i'] + '.json', 'w')
        f.write(str(cityData))

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
    browser.find_element_by_id(id).click()
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
            'x': station.get('x'),
            'y': station.get('y')
         }

    return result

def formatCityData(apiData, domData):
   # string to json 
   data = apiData
   lines = data['l']
   for lidx, line in enumerate(lines):
        for sidx, stop in enumerate(line['st']):
           # 开通的站
           if line['st'][sidx] == '1':
                line['st'][sidx]['lp'] = domData['st'][stop['si']]['lp'];
        data['l'][lidx] = line

   return data

def main():
    cities = fetchAllCity(PAGE_URL, HEADER)
    citiesData = parseAllCityData(cities)
    saveData(citiesData)

if __name__ == '__main__':
    main()
