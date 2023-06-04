#!/usr/bin/python3
# coding=utf-8

def getP(str, separator = " "):
    p = str.split(separator) 
    return {
        'x': int(p[0]),
        'y': int(p[1])
    }

def getLdir(number):
    map = {
        '0': 'N',
        '1': 'NE',
        '2': 'E',
        '3': 'SE',
        '4': 'S',
        '5': 'SW',
        '6': 'W',
        '7': 'NW'
    }

    return map.get(number, 'N')

