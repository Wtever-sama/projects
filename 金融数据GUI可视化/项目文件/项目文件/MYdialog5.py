from PyQt5.QtWidgets import QVBoxLayout,QDialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  
from PyQt5 import QtWidgets  
import pandas as pd

class MyDialog5(QDialog):    #移动平均线图 
    def __init__(self, text_to_display,fileName,parent=None): 
        super(MyDialog5, self).__init__(parent)
        self.text=text_to_display#全局变量 
        self.number=int(text_to_display)
        self.filename=fileName 
        self.setWindowTitle("Matplotlib 绘图对话框:移动平均线图")  
        #对于all股票的绘图 ，bar
        #创建第一个 matplotlib Figure 和 Canvas  
        self.fig5=Figure()
        self.canvas5 = FigureCanvas(self.fig5)  
        self.ax5= self.fig5.add_subplot(111)  
        self.ax5.set_title('线图')  
        # 有一个按钮pushButton_pic_type，点击后会调用 update_plot 方法 
        self.button_price_upandown=QtWidgets.QPushButton('绘图', self) 
        self.button_price_upandown.clicked.connect(self.update_plot)  
        # 布局  
        layout = QVBoxLayout(self)  
        layout.addWidget(self.canvas5)   
        layout.addWidget(self.button_price_upandown) 


    def update_plot(self):   
        df=pd.read_excel(self.filename)
        try: 
            fi_dfe1= df.loc[(df['股票代码'] ==self.number), ['收盘价']]#1002这支股收盘价数据
            day= df.loc[(df['股票代码'] ==self.number), ['日期']]#日期
            df2=pd.concat([day, fi_dfe1], axis=1)
            df2['lMA5'] = fi_dfe1['收盘价'].rolling(window=5).mean()
            df2['lMA10'] = fi_dfe1['收盘价'].rolling(window=10).mean()
            df2['lMA30'] = fi_dfe1['收盘价'].rolling(window=30).mean()

            golden_cross = ((df2['lMA5'].shift(1) < df2['lMA30'].shift(1)) & (df2['lMA5'] > df2['lMA30'])).idxmax() 
            golden_cross1 = ((df2['lMA5'].shift(1) < df2['lMA10'].shift(1)) & (df2['lMA5'] > df2['lMA10'])).idxmax()
            death_cross = ((df2['lMA5'].shift(1) > df2['lMA30'].shift(1)) & (df2['lMA5'] < df2['lMA30'])).idxmax() 
            death_cross1 = ((df2['lMA5'].shift(1) > df2['lMA10'].shift(1)) & (df2['lMA5'] < df2['lMA10'])).idxmax()

            self.ax5.clear()
            self.ax5.plot(df2['日期'], df2['lMA5'], label='5-Day MA', color='g')
            self.ax5.plot(df2['日期'], df2['lMA10'], label='10-Day MA', color='purple')  
            self.ax5.plot(df2['日期'], df2['lMA30'], label='30-Day MA', color='r')  
  
            # 标记交叉点 
            self.ax5.scatter(df2.loc[golden_cross1, '日期'], df2.loc[golden_cross1, 'lMA5'], color='red', label='Golden Cross of MA5&MA10') 
            self.ax5.scatter(df2.loc[golden_cross, '日期'], df2.loc[golden_cross, 'lMA5'], color='orange', label='Golden Cross of MA5&MA30')  
            self.ax5.scatter(df2.loc[death_cross1, '日期'], df2.loc[death_cross1, 'lMA5'], color='darkred', label='Death Cross of MA5&MA10', marker='x')
            self.ax5.scatter(df2.loc[death_cross, '日期'], df2.loc[death_cross, 'lMA5'], color='black', label='Death Cross of MA5&MA30', marker='x')  
    
            self.ax5.legend()  
            self.ax5.set_title('5日、10日和30日的移动平均线及其黄金和死亡交叉点',fontname='SimHei', fontsize=12)  
            self.ax5.set_xlabel('Date')  
            self.ax5.set_ylabel('Price') 
            # 刷新画布以显示新的图表  
            self.canvas5.draw() 
        except FileNotFoundError:  
            print("文件未找到，请检查文件路径是否正确。")  
