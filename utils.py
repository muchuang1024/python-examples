#!/usr/bin/python3
# coding=utf-8

def getP(str, separator = " "):
    p = str.split(separator) 
    return {
        'x': p[0],
        'y': p[1]
    }

