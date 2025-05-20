from PyQt5.QtWidgets import QVBoxLayout,QDialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  
from PyQt5 import QtWidgets  
import numpy as np  
import pandas as pd

class MyDialog3(QDialog):  #开盘价均值柱状图_all
    def __init__(self, fileName, parent=None):  #text是一个str
        super(MyDialog3, self).__init__(parent)
        self.filename= fileName
        self.setWindowTitle("Matplotlib 绘图对话框")  
        #对于all股票的绘图 ，bar
        #创建第一个 matplotlib Figure 和 Canvas  
        self.fig3= Figure()
        self.canvas3 =FigureCanvas(self.fig3)  
        self.ax3 = self.fig3.add_subplot(111)  
        self.ax3.set_title('线图')  
        # 有一个按钮pushButton_pic_type，点击后会调用 update_plot 方法  
        self.open_mean_3=QtWidgets.QPushButton('绘图', self)  
        self.open_mean_3.clicked.connect(self.update_plot)  
        # 布局  
        layout = QVBoxLayout(self)  
        layout.addWidget(self.canvas3)   
        layout.addWidget(self.open_mean_3) 

    def update_plot(self):    
        df=pd.read_excel(self.filename)
        try:  
            x=np.linspace(1001,1100,100)
            #每支股票达到的最高价
            lis_s=[]
            for i in range(1001,1101,1):
                #开盘、收盘价均值
                filtered_df = df.loc[(df['股票代码'] == i), ['开盘价']] 
                values_df=filtered_df['开盘价'].mean()
                lis_s.append(values_df) 

            self.ax3.clear()
            self.ax3.bar(x, lis_s, color='skyblue', label='Opening price', width=0.4) 
            self.ax3.legend()  
            self.ax3.set_xlabel('股票代码', fontproperties='SimHei', fontsize=10)  
            self.ax3.set_ylabel('价格',fontname='SimHei', fontsize=10)  
            self.ax3.set_title('股市开盘价&收盘价均值柱状图',fontname='SimHei', fontsize=12)  
            # 刷新画布以显示新的图表  
            self.canvas3.draw()  
        except FileNotFoundError:  
            print("文件未找到，请检查文件路径是否正确。")  