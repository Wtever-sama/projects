from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
import mplfinance as mpf 
import pandas as pd  
from PyQt5.QtWidgets import QVBoxLayout,QDialog
from PyQt5 import QtWidgets

class MyDialog1(QDialog):  #创建弹窗画K线图
    def __init__(self, text_to_display,fileName, parent=None):  #text是一个str
        super(MyDialog1, self).__init__(parent)
        #全局变量（用户输入的股票代码）
        self.number=int(text_to_display)
        self.fileName=fileName

        self.setWindowTitle("Matplotlib 绘图对话框:K线图")  
        #对于某一只股票的绘图 ，K线图
        #创建第一个 matplotlib Figure 和 Canvas  
        self.fig1= Figure()
        self.canvas1=FigureCanvas(self.fig1)  
        self.ax1 = self.fig1.add_subplot(211) 
        self.ax2 = self.fig1.add_subplot(212) 
        self.ax1.set_title('Candlestick for'+text_to_display) 
        self.ax2.set_title('Volume for'+text_to_display) 
        # 有一个按钮pushButton_pic_type，点击后会调用 update_plot 方法     
        self.button_kline = QtWidgets.QPushButton('绘图', self)   
        self.button_kline.clicked.connect(self.update_plot)
        # 布局  
        layout = QVBoxLayout(self)  
        layout.addWidget(self.canvas1)   
        layout.addWidget(self.button_kline) 
        #对于所有股票的绘图，柱状
   
    def update_plot(self): 
        df=pd.read_excel(self.fileName)
        try:
            filtered_df=df.loc[df['股票代码'] == self.number]
            stock_hfq_df0=filtered_df.iloc[:,:7]
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

            #stock_hfq_df[['Open','Close', 'High', 'Low', 'Close']].plot(kind='ohlc', ax=self.ax1)
            mpf.plot(stock_hfq_df,ax=self.ax1, type='candle', style='charles', volume=self.ax2)   
            plt.subplots_adjust(hspace=3.0)# 调整子图间距
 
            #self.ax1.plot(x, y)  
            self.ax1.set_xlabel('Date')  
            self.ax1.set_ylabel('price(CNY)')  
            self.ax2.set_xlabel('Date')  
            self.ax2.set_ylabel('Volume') 
            # 刷新画布以显示新的图表  
            self.canvas1.draw()  
        except FileNotFoundError:  
            print("文件未找到，请检查文件路径是否正确。")    