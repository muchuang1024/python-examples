#!/usr/bin/python3
# coding=utf-8

def getP(str, separator = " "):
    p = str.split(separator) 
    return {
        'x': int(p[0]),
        'y': int(p[1])
    }

