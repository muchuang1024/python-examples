#!/usr/bin/python3
# coding=utf-8

import requests
#from selenium import webdriver
from lxml import etree

def fetchHtml(url, header):
    r = requests.get(url, headers=header)
    return r.text

def parseHtml(html):
    element = etree.HTML(html)
    options = element.xpath("//a[@class='city']")
    print(options)

    for option in options:
        q = ''.join([option.get('id'), '_info_', option.get('cityname')])
        print(q)

def main():
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    url = 'http://map.amap.com/subway/index.html?&1100'
    html = fetchHtml(url, header)
    parseHtml(html)
    

if __name__ == '__main__':
    main()
