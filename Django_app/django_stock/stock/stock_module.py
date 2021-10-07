import requests
import json
import pandas as pd
import os
import yfinance as yf
from bs4 import BeautifulSoup
import requests
import time
from .stock_data import data_about_stock

class stock():
    
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
    
        
    def under_over_stock(symbol):
        company = company()
        df_stocks = []
        for comp in company:
            url = f'https://www.set.or.th/set/companyhighlight.do?symbol={comp}&ssoPageId=5&language=en&country=US'
            df = pd.read_html(url)
            df = df[0]
            df.columns = df.columns.get_level_values(0)
            eps = df[df['Period as of'] == 'EPS (Baht)']
            PE_ratio = df[df['Period as of'] == 'P/E']
            current_price = df[df['Period as of'] == 'Last Price(Baht)']
            df_stocks.append({
                'Ticket':comp,
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
        df['value_label'] = np.where(df['over_under_ratio'] < 1.0,'under','Fair or over','not value'),
        # np.Wheredf['over_under_ratio'] =='inf','not dividend')
        df['value percentage'] = abs(df['over_under_ratio'] - 1)*100
        over_under = df.to_json(orient='records')
        return over_under
