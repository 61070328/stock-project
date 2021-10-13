import requests
import json
import pandas as pd
import os
import yfinance as yf
from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import urllib.request as urllib2
from .stock_data import data_about_stock

class stock:
    def __init__(self, Symbol):
        self.ticker = Symbol

    def MonetaryPolicy(self):
    #ข้อมูลอัตราเงินเฟ้อ และอัตราการขยายตัวทางเศรษฐกิจ
        url = 'https://www.bot.or.th/Thai/MonetaryPolicy/MonetPolicyComittee/MPR/Pages/default.aspx'
        df = pd.read_html(url)
        df = df[0].iloc[:,:4]
        df = df.dropna()
        df.columns = df.iloc[0]
        df = df.drop(0)
        year = int(time.strftime('%Y')) + 543
        gdp = df[df['ร้อยละ'] == 'อัตราการขยายตัวทางเศรษฐกิจ']
        Inflation = df[df['ร้อยละ'] == 'อัตราเงินเฟ้อทั่วไป']
        core_Inflation = df[df['ร้อยละ'] == 'อัตราเงินเฟ้อพื้นฐาน']
        monetary = {
            'GDP': gdp[[str(year)]].values[0][0],
            'Inflation' : Inflation[[str(year)]].values[0][0],
            'core Inflation' : core_Inflation[[str(year)]].values[0][0]
        }
        return monetary
    
        
    def under_over_stock(self, Symbol):
        compa = data_about_stock().company()
        df_stocks = []
        for comp in compa:
            name = comp.get('Symbol')
            url = f'https://www.set.or.th/set/companyhighlight.do?symbol={name}&ssoPageId=5&language=en&country=US'
            df = pd.read_html(url)
            df = df[0]
            df.columns = df.columns.get_level_values(0)
            eps = df[df['Period as of'] == 'EPS (Baht)']
            PE_ratio = df[df['Period as of'] == 'P/E']
            current_price = df[df['Period as of'] == 'Last Price(Baht)']
            df_stocks.append({
            'Ticket':name,
            'current_price':current_price.iloc[:,-1].values[0],
            'PE_ratio' : PE_ratio.iloc[:,-1].values[0],
            'EPS': eps.iloc[:,-1].values[0]
            })
        df = pd.DataFrame(df_stocks)
        df = df.set_index('Ticket')
        df = df.replace({'-':0.0,np.nan:0.0})
        df = df.astype(float)
        PE_ratio_mean = df.PE_ratio.mean()
        df['Fair_market'] = PE_ratio_mean * df['EPS']
        df['over_under_ratio'] = df['current_price'] / df['Fair_market']

        #create new column to store and show a label of under and over valued stock technology.
        df['value_label'] = np.where(df['over_under_ratio'] < 1.0,'under','over')
        df['value_label'] = np.where(df['over_under_ratio'] == np.inf,'not value',df['value_label'] )
        # np.Wheredf['over_under_ratio'] =='inf','not dividend')
        df['value percentage'] = abs(df['over_under_ratio'] - 1)*100
        ticket = df.loc[Symbol]
        under_over = {
            'Ticket' : Symbol,
            'Label' : ticket['value_label'],
            'Percent' : ticket['value percentage'],
        }
        return under_over

    def finance_balance(self, Symbol):
        Balance = []
        # ticker of company
        url = f'https://www.set.or.th/set/companyfinance.do?type=balance&symbol={Symbol}&language=th&country=TH'
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)
        table = soup.select('table')[2]
        for tr in table.find_all('tr'):
            left = tr.find('td',attrs={'style':'text-align:left;'})
            right = tr.find('td',attrs={'style':'text-align:right;'})
            header = tr.find('td',attrs={'class':'topic-bf'})
            if header:
                Balance.append({
                    'Name':header.text,
                    'Unit' : '-',
                    'category':'header'
                })
            # company_finan.append(comp.upper())
            elif left != None or right != None:
                Balance.append({
                    'Name':left.text,
                    'Unit' : right.text,
                    'category':'content'
                })
            else:
                pass
        return Balance

    def income_statement(self, Symbol):
  # Income Statement งบกำไรขาดทุนเบ็ดเสร็จ ของแต่ละ บริษัท
  # data show on table about financial
        income_statement = []
        url = f'https://www.set.or.th/set/companyfinance.do?type=income&symbol={Symbol}&language=th&country=TH'
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)
        table = soup.select('table')[2]
        for tr in table.find_all('tr'):
            left = tr.find('td',attrs={'style':'text-align:left;'})
            right = tr.find('td',attrs={'style':'text-align:right;'})
            header = tr.find('td',attrs={'class':'topic-bf'})
            if header:
                income_statement.append({
                'Name':header.text,
                'Unit' : '-',
                'category':'header'
            })
            # company_finan.append(comp.upper())
            elif left != None or right != None:
                income_statement.append({
                'Name':left.text,
                'Unit' : right.text,
                'category':'content'
            })
            else:
                pass
        return income_statement
    def cashflow(self,Symbol):
        cashflow = []
        #งบกระแสเงินสด
        url = f'https://www.set.or.th/set/companyfinance.do?type=cashflow&symbol={Symbol}&language=th&country=TH'
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)
        table = soup.select('table')[2]
        for tr in table.find_all('tr'):
            left = tr.find('td',attrs={'style':'text-align:left;'})
            right = tr.find('td',attrs={'style':'text-align:right;'})
            header = tr.find('td',attrs={'class':'topic-bf'})
            if header:
                cashflow.append({
                'Name':header.text,
                'Unit' : '-',
                'category':'header'
            })
            # company_finan.append(comp.upper())
            elif left != None or right != None:
                cashflow.append({
                    'Name':left.text,
                    'Unit' : right.text,
                    'category':'content'
            })
            else:
                pass
        return cashflow

    def stockholder(self,Symbol):
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

        return stockholder

    def settrade_compare(self):
    #ภาพรวมราคาหุ้นในกลุ่มอุตสาหกรรมเดียวกัน
        sector_compare = []
        url = 'https://www.settrade.com/C04_08_stock_sectorcomparison_p1.jsp?txtSymbol=JMART&ssoPageId=18&selectPage=8'
        data = pd.read_html(url,header=0)
        df = data[0]
        for data in df.iterrows():
            x = {
                'ID':data[1][0],
                'Symbol':data[1][1],
                'High':data[1][2],
                'Low':data[1][3],
                'Change':	data[1][4] ,
                '%Change':data[1][5],
                'Volume':data[1][6],
                'Value (Mil B.)':data[1][7]
            }
            sector_compare.append(x)
        return sector_compare
