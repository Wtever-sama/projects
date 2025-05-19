# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:16:52 2024

@author: ASUS
"""

'''
 开盘、收盘价均值柱状图。
 总交易量柱状图。
 每支股票达到的最高价的柱状图。
 每支股票达到的最低价的柱状图。
 每支股票当年的复合涨跌幅组成的柱状图。
 每支股票的平均振幅组成的散点图。
 每支股票的平均换手率组成的柱状图。

'''
#数据的处理
import pandas as pd
import numpy as np
#？
#获得证券信息
#import akshare as ak(failed
#绘制图表
import matplotlib.pyplot as plt
from pylab import mpl
import mplfinance as mpf

plt.rcParams['font.sans-serif'] = ['SimHei']  # 对于Windows系统  
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

df=pd.read_excel('金融-精简化股市数据分析.xlsx')
#存储开盘、收盘价均值
lis_s=[]
lis_e=[]
#总交易量
lis_t=[]
#每支股票达到的最高价
lis_h=[]
#每支股票达到的最低价
lis_l=[]
#每支股票的平均振幅
lis_w=[]
for i in range(1001,1101,1):
    #开盘、收盘价均值
    filtered_df = df.loc[(df['股票代码'] == i), ['开盘价']] 
    values_df=filtered_df['开盘价'].mean()
    lis_s.append(values_df) 
    
    filtered_df1 = df.loc[(df['股票代码'] == i), ['收盘价']] 
    values_df1=filtered_df1['收盘价'].mean()
    lis_e.append(values_df1)
    #总交易量
    trade_df=df.loc[(df['股票代码'] == i), ['交易量']]
    vtd=trade_df['交易量'].sum()
    lis_t.append(vtd)
    #每支股票达到的最高价
    hi_filter=df.loc[(df['股票代码'])==i,['最高价']]
    max_price = pd.Series(hi_filter.get('最高价', [np.nan]), dtype=float).max()
    lis_h.append(max_price)
    #每支股票达到的最低价
    lo_filter=df.loc[(df['股票代码'])==i,['最低价']]
    min_price = pd.Series(lo_filter.get('最低价', [np.nan]), dtype=float).min()
    lis_l.append(min_price)

    #每支股票的平均振幅组成的散点图
    wave_filter=df.loc[(df['股票代码'])==i,['振幅']]
    av_wave = pd.Series(wave_filter.get('振幅', [np.nan]), dtype=float).mean()
    lis_w.append(av_wave)

#开盘、收盘价均值柱状图。
x=np.linspace(1001,1100,100)
plt.figure(figsize=(12,5))
plt.subplot(2, 2, 1)
plt.bar(x,lis_s,color='skyblue',label='Opening price',width=0.4)
plt.bar(x+0.4,lis_e,color='darkred',label='Closing price',width=0.4)
plt.legend()
plt.xlabel('股票代码',fontname='SimHei', fontsize=10)
plt.ylabel('价格',fontname='SimHei', fontsize=10)
plt.title('股市开盘价&收盘价均值柱状图',fontname='SimHei', fontsize=12)
plt.grid(axis='y')
#总交易量柱状图。
plt.subplot(2,2,2)
plt.bar(x,lis_t,color='darkblue',label='Total transaction volume',width=0.4)
plt.legend()
plt.xlabel('股票代码',fontname='SimHei', fontsize=10)
plt.ylabel('总交易量',fontname='SimHei', fontsize=10)
plt.title('总交易量柱状图',fontname='SimHei', fontsize=12)
#每支股票达到的最高价的柱状图。
plt.subplot(2,2,3)
plt.bar(x,lis_h,color='purple',label='Highest price',width=0.4)
plt.legend()
plt.xlabel('股票代码',fontname='SimHei', fontsize=10)
plt.ylabel('最高价',fontname='SimHei', fontsize=10)
plt.title('每支股票达到的最高价的柱状图',fontname='SimHei', fontsize=12)
#每支股票达到的最低价的柱状图。
plt.subplot(2,2,4)
plt.bar(x,lis_l,color='orange',label='Bottom price',width=0.4)
plt.legend()
plt.xlabel('股票代码',fontname='SimHei', fontsize=10)
plt.ylabel('最高价',fontname='SimHei', fontsize=10)
plt.title('每支股票达到的最低价的柱状图',fontname='SimHei', fontsize=12)
plt.tight_layout()
plt.show()
#每支股票的平均振幅组成的散点图
plt.figure(figsize=(12,5))
plt.subplot(1,1,1)
plt.scatter(x,lis_w,edgecolors='darkred',label='Average amplitude')
plt.legend()
plt.xlabel('股票代码',fontname='SimHei', fontsize=10)
plt.ylabel('平均振幅',fontname='SimHei', fontsize=10)
plt.title('每支股票的平均振幅组成的散点图',fontname='SimHei', fontsize=12)
plt.show()

'''
价格走势折线图：按照开盘价-收盘价-第二天开盘价的折线趋势。
 移动平均线图：5日、30日的移动平均线，采用不同标识，并标注出黄金和死亡交叉点。
 成交量变化图：用折线图或者柱状图表示股票每一天的成交量变化。
 涨跌幅散点图：利用散点来评估股票的涨跌情况。
 股票蜡烛图：股市常用的显示股票价格的图形。
 振幅折线图。
 换手率柱状图。
'''

fi_dfs0= df.loc[(df['股票代码'] == 1001), ['开盘价']]#过滤出1001股票的开盘价dataframe
fi_dfe0= df.loc[(df['股票代码'] == 1001), ['收盘价']]
fi_dfs=fi_dfs0.reset_index(drop=True)#重置行索引，开盘
fi_dfe=fi_dfe0.reset_index(drop=True)
n=fi_dfs.shape[0]#n代表天数

df_reseted=df.set_index('股票代码')
fdf0=df_reseted.loc['1001']#过滤出1001的信息
fdf=fdf0['日期']#日期作为信息单独提取
lis_p=[]#存储走势的y轴数据
for j in range(n):
    start=fi_dfs.iloc[j,0]
    end=fi_dfe.iloc[j,0]
    lis_p0=[start,end]
    lis_p+=lis_p0#按照开盘价-收盘价-第二天开盘价的1001折线趋势存储价格数据
x1=[]
for dat in fdf:
    x1.extend([dat]*2)#我们想要每个日期重复2次,重复日期并创建一个新的x轴列表x1 
#print(x1)
#由于y轴有原来两倍的数据，则x*2  (备用)
plt.figure(figsize=(12,5))
plt.plot(x1,lis_p,linestyle='--',label='Price trend',color='green',marker='o',markeredgecolor='orange')
plt.legend()
plt.xlabel('时间',fontname='SimHei', fontsize=10)
plt.ylabel('价格',fontname='SimHei', fontsize=10)
plt.title('价格走势折线图',fontname='SimHei', fontsize=12)
plt.show()

#移动平均线图：5日、10日、30日的移动平均线，采用不同标识，并标注出黄金和死亡交叉点
#MA=（C1+C2+C3+...+Cn)/N （ Ci：某日收盘价，N：移动平均周期 ）。
fi_dfe1= df.loc[(df['股票代码'] == 1002), ['收盘价']]#1002这支股收盘价数据
day= df.loc[(df['股票代码'] == 1002), ['日期']]#日期
df2=pd.concat([day, fi_dfe1], axis=1)
df2['lMA5'] = fi_dfe1['收盘价'].rolling(window=5).mean()
df2['lMA10'] = fi_dfe1['收盘价'].rolling(window=10).mean()
df2['lMA30'] = fi_dfe1['收盘价'].rolling(window=30).mean()
#print(df2['lMA5'],df2['lMA10'],df2['lMA30'])
golden_cross = ((df2['lMA5'].shift(1) < df2['lMA30'].shift(1)) & (df2['lMA5'] > df2['lMA30'])).idxmax() 
golden_cross1 = ((df2['lMA5'].shift(1) < df2['lMA10'].shift(1)) & (df2['lMA5'] > df2['lMA10'])).idxmax()
death_cross = ((df2['lMA5'].shift(1) > df2['lMA30'].shift(1)) & (df2['lMA5'] < df2['lMA30'])).idxmax() 
death_cross1 = ((df2['lMA5'].shift(1) > df2['lMA10'].shift(1)) & (df2['lMA5'] < df2['lMA10'])).idxmax()
plt.figure(figsize=(12, 6))  
#plt.plot(df2['日期'], df2['收盘价'], label='Close Price', alpha=0.5)  参考线 
plt.plot(df2['日期'], df2['lMA5'], label='5-Day MA', color='g')
plt.plot(df2['日期'], df2['lMA10'], label='10-Day MA', color='purple')  
plt.plot(df2['日期'], df2['lMA30'], label='30-Day MA', color='r')  
  
# 标记交叉点 
plt.scatter(df2.loc[golden_cross1, '日期'], df2.loc[golden_cross1, 'lMA5'], color='red', label='Golden Cross of MA5&MA10') 
plt.scatter(df2.loc[golden_cross, '日期'], df2.loc[golden_cross, 'lMA5'], color='orange', label='Golden Cross of MA5&MA30')  
plt.scatter(df2.loc[death_cross1, '日期'], df2.loc[death_cross1, 'lMA5'], color='darkred', label='Death Cross of MA5&MA10', marker='x')
plt.scatter(df2.loc[death_cross, '日期'], df2.loc[death_cross, 'lMA5'], color='black', label='Death Cross of MA5&MA30', marker='x')  
    
plt.legend()  
plt.title('5日、10日和30日的移动平均线及其黄金和死亡交叉点',fontname='SimHei', fontsize=12)  
plt.xlabel('Date')  
plt.ylabel('Price')  
plt.grid(True)  
plt.show()  

# 输出交叉点位置 
print(f"5日和10日黄金交叉点: {df.loc[golden_cross1, '日期']}")
print(f"5日和30日黄金交叉点: {df.loc[golden_cross, '日期']}")
print(f"5日和10日死亡交叉点: {df.loc[death_cross1, '日期']}")  
print(f"5日和30日死亡交叉点: {df.loc[death_cross, '日期']}")

#成交量变化图：用折线图或者柱状图表示股票每一天的成交量变化。
fi_dfdl= df.loc[(df['股票代码'] == 1003), ['交易量']]
day3= df.loc[(df['股票代码'] == 1003), ['日期']]#1003日期
df3=pd.concat([day3,fi_dfdl],axis=1)
plt.figure(figsize=(12,6))
plt.plot(df3['日期'],df3['交易量'],label='The daily volume of business of 1003 stock',color='green')
plt.xlabel('Date')
plt.ylabel('Deal')
plt.title('折线图表示股票每一天的成交量变化',fontname='SimHei', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

#涨跌幅散点图：利用散点来评估股票的涨跌情况
fi_dfw= df.loc[(df['股票代码'] == 1004), ['涨跌幅']]
day4= df.loc[(df['股票代码'] == 1004), ['日期']]#1004日期
df4=pd.concat([day4,fi_dfw],axis=1)
plt.figure(figsize=(12,6))
plt.scatter(df4['日期'],df4['涨跌幅'],label='The rise and fall of 1004 stock',color='orange')
plt.xlabel('Date')
plt.ylabel('涨跌',fontname='SimHei', fontsize=10)
plt.title('散点来评估1004股票的涨跌情况',fontname='SimHei', fontsize=12)
plt.legend()
plt.show()

#股票蜡烛图：股市常用的显示股票价格的图形
#df_reseted=df.set_index('股票代码')
filtered_df=df_reseted.loc['1007']
stock_hfq_df0=filtered_df.iloc[:,:6]
stock_hfq_df=stock_hfq_df0.set_index('日期')
stock_hfq_df.index.name = 'Time'
stock_hfq_df['Open']=stock_hfq_df['开盘价']
stock_hfq_df['Close']=stock_hfq_df['收盘价']
stock_hfq_df['High']=stock_hfq_df['最高价']
stock_hfq_df['Low']=stock_hfq_df['最低价']
stock_hfq_df['Volume']=stock_hfq_df['交易量']

stock_hfq_df=stock_hfq_df.drop(columns=['开盘价'])
stock_hfq_df=stock_hfq_df.drop(columns=['收盘价'])
stock_hfq_df=stock_hfq_df.drop(columns=['最高价'])
stock_hfq_df=stock_hfq_df.drop(columns=['最低价'])
stock_hfq_df=stock_hfq_df.drop(columns=['交易量'])
#print(stock_hfq_df)为日期为索引的数据结构，开盘价-交易量
#a=stock_hfq_df.index
#print(type(a))为<class 'pandas.core.indexes.datetimes.DatetimeIndex'>

mpf.plot(stock_hfq_df, 
         type='candle',
         style='yahoo',
         title = "Candlestick for 1007",
         ylabel = "price(CNY)",
         ylabel_lower = 'volume(shares)',
         volume = True,
         figratio = (12, 6))
mpf.show()

#振幅折线图。
fi_dfwave=df.loc[(df['股票代码']==1005),['振幅']]
day5=df.loc[(df['股票代码']==1005),['日期']]#1005日期
df5=pd.concat([day5,fi_dfwave],axis=1)
plt.figure(figsize=(12,6))
plt.plot(df5['日期'],df5['振幅'],label='amplitude of 1005 stock')
plt.xlabel('Date')
plt.ylabel('Wave')
plt.title('1005振幅折线图',fontname='SimHei', fontsize=12)
plt.legend()
plt.show()

#换手率柱状图。
fi_dfex=df.loc[(df['股票代码']==1006),['换手率']]
day6=df.loc[(df['股票代码']==1006),['日期']]
df6=pd.concat([day6,fi_dfex],axis=1)
plt.figure(figsize=(12,6))
plt.bar(df6['日期'],df6['换手率'],label='Turnover rate of 1006 stock')
plt.xlabel('Date')
plt.ylabel('换手率',fontname='SimHei', fontsize=10)
plt.title('1006股票换手率柱状图',fontname='SimHei', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()



