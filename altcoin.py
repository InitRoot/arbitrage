#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 11:15:14 2017

@author: admin
"""
import requests


def fetchfromAlt():
    global result
    result = requests.get("https://www.altcointrader.co.za/api/v3/live-stats").json()
    
    if result == None:        
        while result == None:
            result = requests.get("https://www.altcointrader.co.za/api/v3/live-stats").json()
            time.sleep(20)
   


def getSellPrice(coinType): #ek kry die idee die exchange is deermekaar met buy and sell??
    sellPrice = result[coinType]['Buy'] if result else None
    return sellPrice



def getBuyPrice(coinType):
    buyPrice = result[coinType]['Sell'] if result else None
    return buyPrice