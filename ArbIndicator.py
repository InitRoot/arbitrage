# -*- coding: utf-8 -*-
"""
 ******************************* INFORMATION ***************************

 ***********************************************************************
  
 ** BTC Arbitrage Indicator - Indicates likely arbitrage trades between bitcoin exchanges. 
 ** 
 ** @author   Bartho Horn, Frans Botes
 ** @date     Dec 2017
 ** @param    Requires setup of two exchanges, locally and internationally
 ** @return   Likely trades
 ** @setup    pip install forex-python, ccxt
 **
      
 ***********************************************************************
 """

"""  ******************************* IMPORTS *************************** """
import ccxt 
import time
import altcoin
import operator
from forex_python.converter import CurrencyRates
currency = CurrencyRates()


"""  ******************************** SETUP **************************** """
intCurrency = 'EUR'
locCurrency = 'ZAR'
delay = 5 # setup delay in seconds for fetching market data, 2s on LUNO is seen as DDOS attack
coinsSet = ['BTC','BCH','LTC','XRP','ETH','DASH','ZEC'] #everything on altcoin as at DEC17
coinsSet2 = ['BTC','ETH'] 
ex1Prices = {"BTC":0,"BCH":0,"LTC":0,"XRP":0,"ETH":0,"DASH":0,"ZEC":0} #KRAKEN
ex2Prices = {"BTC":0,"BCH":0,"LTC":0,"XRP":0,"ETH":0,"DASH":0,"ZEC":0} #ALTCOIN
ex3Prices = {"BTC":0,"ETH":0} #LUNO, is not used to calculate spreads, just an indicator.
exSpreads = {"BTC":0,"BCH":0,"LTC":0,"XRP":0,"ETH":0,"DASH":0,"ZEC":0} 
feesPerc = 5 #percentage of fees
maxval = ''


"""  
************************ CURRENCY CONVERSION ********************** 
** Setup conversion rates for currencies.

*******************************************************************
"""
EURZAR = currency.get_rate(intCurrency,locCurrency) #updated daily 3PM CET as per package page



"""  
**************************** BTC EXCHANGE ************************ 
** Load market data from both exchanges. 

*******************************************************************
"""

def getKrakenPrices(type): 
    print()
    print("### KraKen ###")
    kraken = ccxt.kraken()
    #kraken_markets = kraken.load_markets()              #load markets on kraken
    #kraken_symbols = kraken.symbols
    #kraken_currencies = kraken.currencies   
    global kraken_tickers
    for c in coinsSet:     
        try: 
            kraken_tickers = kraken.fetch_ticker(c + "/" + intCurrency) #extract die ticker prys in plaas van die orderbooks. Sodat konstant oor exchanges is. ook minder API counter hits
            
            if kraken_tickers == None:              
                while kraken_tickers == None:
                    pass
                    time.sleep(20)
                    kraken_tickers = kraken.fetch_ticker(c + "/" + intCurrency) #extract die ticker prys in plaas van die orderbooks. Sodat konstant oor exchanges is. ook minder API counter hits
               #kraken_bid = EURZAR*(kraken_orderbook['bids'][0][0] if len (kraken_orderbook['bids']) > 0 else None)
                
            kraken_ask = EURZAR*(kraken_tickers[type])
            ex1Prices[c] = (kraken_ask)
            print("Unit: " + c + " ; Prices: " + str(ex1Prices[c]))
            time.sleep(delay) #extraction is unstable, have to implement delay
               
               
        except:
            print("Timeout exception. Waiting....")
            time.sleep(20)



def getLunoPrices(type): 
    print()
    print("### Luno ###")
    luno = ccxt.luno()
    
    global luno_tickers
    luno_tickers = None
    while luno_tickers == None:
        try: 
            luno_tickers = luno.fetch_ticker('BTC' + "/" + locCurrency) 
            #print(luno_tickers)
            time.sleep(2)
        except:
            print("Timeout exception. Waiting....")
            time.sleep(10)
               
        luno_ask = (luno_tickers[type])
        ex3Prices['BTC'] = (luno_ask)
        print("Unit: " + 'BTC' + " ; Prices: " + str(ex3Prices['BTC']))
       



def getaltCoinSellPrices(): #custom code for altcoin used as they do not offer a proper api
    print()
    print("### AltcoinTrader ###")
    altcoin.fetchfromAlt()
    for c in coinsSet:
        altcoin_ask = altcoin.getSellPrice(c)
        ex2Prices[c] = (altcoin_ask)
        print("Unit: " + c + " ; Prices: " + str(ex2Prices[c]))
        time.sleep(1)



def getSpreads():
    print()
    print("### Spreads ###")
    for coin in coinsSet:
        unit1 = float(ex1Prices[coin]) #buyKraken
        unit2 = float(ex2Prices[coin]) #sellAltcoin
        spread = ((unit2 - unit1)/unit1)*100
        exSpreads[coin] = spread
        print("Unit: " + coin + " ; Spread Alt" + str(spread))
       
    

def getSpreadsKraken():
    print()
    print("### Spreads ###")
    for coin in coinsSet2:
        unit1 = float(ex1Prices[coin]) #buyKraken
        unit2 = float(ex3Prices[coin]) #sellAltcoin
        spread = ((unit2 - unit1)/unit1)*100
        exSpreads[coin] = spread
        print("Unit: " + coin + " ; Spread Lun" + str(spread))
    
    
def selectCoins():
    print()
    maxval = (max(zip(exSpreads.values(), exSpreads.keys())))
    print("Highest %: " + str(maxval))
    


"""  
**************************** MAIN ************************ 
** Main program logic to calculate spread and identify
** best returning coin for international trade.

**********************************************************
"""

print("########### BTC Arbitrage Indicator ###########")
while True:     
    print()
    print("Gathering prices.... @" + (time.strftime("%d/%m/%Y")) + " " + (time.strftime("%H:%M:%S")))     
    getaltCoinSellPrices()
    getKrakenPrices('bid')
    getLunoPrices('bid')
    getSpreads()
    getSpreadsKraken()
    selectCoins()
   # writeDataCSV()
    time.sleep(60)
    print("###########################################")
    
    

    
    
    
    
    
    
    
    
    
    
    