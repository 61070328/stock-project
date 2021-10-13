from django.shortcuts import render
from django.http import  JsonResponse
from django.shortcuts import render, redirect
import pandas as pd
import numpy as np
import json
from bs4 import BeautifulSoup
import requests
import time
import urllib.request as urllib2
from .stock_module import stock
from .stock_data import data_about_stock
from ..fusioncharts import FusionCharts
from ..fusioncharts import FusionTable
from ..fusioncharts import TimeSeries
from yahoo_fin.stock_info import get_live_price, get_data

# import time
import yfinance as yf

# def index(request):
#     return HttpResponse('Hello')
    
def symbol_company(request):
    
    symbol = data_about_stock().company()
    monetary = stock(symbol).MonetaryPolicy()

    return render(request, 'base.html', {'company': symbol,
    'monetary':monetary, })


def stock_info(request, Symbol):
    data = yf.Ticker(Symbol+'.BK')
    information = data.info
    stocks = stock(Symbol) # class จาก file stock_module เพื่อเข้าสู่ฟังก์ชั่นที่ทำการเขียนไว้
    monetary = stocks.MonetaryPolicy() # GDP Market
    under_over = stocks.under_over_stock(Symbol)
    balance = stocks.finance_balance(Symbol) #งบแสดงฐานการเงินแบบเต็มของล่าสุด
    income = stocks.income_statement(Symbol) # งบกำไรขาดทุนเบ็ดเสร็จ แสดงที่การเงิน
    stockholder = stocks.stockholder(Symbol) # รายชื่อผู้ถือหุ้น
    
    return render(request, 'stock_overview.html',{
      'Symbol':Symbol,
      'monetary':monetary,
      'balance':balance,
      'stockholder':stockholder,
      'under':under_over,
      }
      )

def stock_financial(request, Symbol):
    stocks = stock(Symbol) # class จาก file stock_module เพื่อเข้าสู่ฟังก์ชั่นที่ทำการเขียนไว้
    balance = stocks.finance_balance(Symbol) #งบแสดงฐานการเงินแบบเต็มของล่าสุด
    income = stocks.income_statement(Symbol) # งบกำไรขาดทุนเบ็ดเสร็จ แสดงที่การเงิน
    stockholder = stocks.stockholder(Symbol) # รายชื่อผู้ถือหุ้น
def finance_chart(request):
    stock = yf.Ticker('JMART.BK')
    infor = stock.history(period="5y")
    infor = infor.reset_index().round(4)
    infor['Date'] = pd.to_datetime(infor['Date']).dt.date.astype(str)
    infor = infor.rename(columns={"Date": "t", "Close": "y"})
    data = infor[['t','y']].to_dict('records')
    fusionTable = FusionTable(schema, data)
    timeSeries = TimeSeries(fusionTable)

    # Wrapper constructor parameters
    # charttype, chartID, width, height, renderAt, data format, TimeSeries object

    fcChart = FusionCharts("timeseries", "MyFirstChart" , "700", "450", "chart-container", "json", timeSeries)

    # Returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    return render(request,'base.html', {'output':fcChart.render()})
    
def chart(request):
    return render(request,'base.html')

