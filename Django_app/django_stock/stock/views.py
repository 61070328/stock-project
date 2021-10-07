from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
import pandas as pd
from .models import Trader
import json
from .stock_module import stock

from yahoo_fin.stock_info import get_live_price, get_data

# import time
import yfinance as yf

# def index(request):
#     return HttpResponse('Hello')
    
def symbol_company(request):
    company = [
        {'Name':'JMART.BK','Symbol':'JMART'},
        {'Name':'DELTA.BK','Symbol':'DELTA'},
        {'Name':'ADVANC.BK','Symbol':'ADVANC'},
        {'Name':'ALT.BK','Symbol':'ALT'},
        {'Name':'AIT.BK','Symbol':'AIT'},
        {'Name':'DIF.BK','Symbol':'DIF'},
        {'Name':'DTAC.BK','Symbol':'DTAC'},
        {'Name':'INTUCH.BK','Symbol':'INTUCH'},
        {'Name':'JTS.BK','Symbol':'JTS'},
        {'Name':'SIS.BK','Symbol':'SIS'},
        {'Name':'SYNEX.BK','Symbol':'SYNEX'},
        {'Name':'THCOM.BK','Symbol':'THCOM'},
        {'Name':'TRUE.BK','Symbol':'TRUE'},
        {'Name':'HUMAN.BK','Symbol':'HUMAN'},
        {'Name':'FORTH.BK','Symbol':'FORTH'}
    ]
    my_object = stock()
    monetary = my_object.MonetaryPolicy()


    return render(request, 'base.html', {'company': company,
    'monetary':monetary})


def stock_info(request, Symbol):
    data = yf.Ticker(Symbol+'.BK')
    information = data.info
    text = {'info':'54580',
    'ask':'d;dlf'}
    return render(request, 'stock_overview.html',\
      {'Symbol':Symbol})


def stockholder(request, Symbol):
      #list รายชื่อของผู้ถือหุ้นแต่ละบริษัท
  stockholder = []
  url_stockholder = f'https://www.set.or.th/set/companyholder.do?symbol={Symbol}&ssoPageId=6&language=th&country=TH'
  holder =pd.read_html(url_stockholder)  
  for row in holder[2].iterrows():
    list_name = {
            'id': row[0],
            'Stockholder' : row[1][1],
            'Amount_stock':row[1][2],
            'Percent' :row[1][3],
              }
    stockholder.append(list_name)  

  return render(request, 'stock_overview.html', {'stockholder': stockholder})


