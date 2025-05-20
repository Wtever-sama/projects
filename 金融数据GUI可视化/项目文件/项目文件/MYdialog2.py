from PyQt5.QtWidgets import QVBoxLayout,QDialog
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  
from matplotlib.figure import Figure
from PyQt5 import QtWidgets  

class MyDialog2(QDialog):  #每支股票达到的最高价的柱状图_all
    def __init__(self, fileName, parent=None):  #text是一个str
        super(MyDialog2, self).__init__(parent)
        self.filename=fileName 
        self.setWindowTitle("Matplotlib 绘图对话框")  
        #对于all股票的绘图 ，bar
        #创建第一个 matplotlib Figure 和 Canvas  
        self.fig2=Figure()
        self.canvas2 = FigureCanvas(self.fig2)  
        self.ax2 = self.fig2.add_subplot(111)  
        self.ax2.set_title('线图')  
        # 有一个按钮pushButton_pic_type，点击后会调用 update_plot 方法  
        self.btton_all_hi_price_3=QtWidgets.QPushButton('绘图', self)   
        self.btton_all_hi_price_3.clicked.connect(self.update_plot)  
        # 布局  
        layout = QVBoxLayout(self)  
        layout.addWidget(self.canvas2)   
        layout.addWidget(self.btton_all_hi_price_3) 

    def update_plot(self):   
        df=pd.read_excel(self.filename)
        try:  
            x=np.linspace(1001,1100,100)
            #每支股票达到的最高价
            lis_h=[]
            for i in range(1001,1101,1):
                #每支股票达到的最高价
                hi_filter=df.loc[(df['股票代码'])==i,['最高价']]
                max_price = pd.Series(hi_filter.get('最高价', [np.nan]), dtype=float).max()
                lis_h.append(max_price)

            self.ax2.clear()
            self.ax2.bar(x, lis_h, color='purple', label='highest price', width=0.4) 
            self.ax2.legend()  
            self.ax2.set_xlabel('股票代码', fontproperties='SimHei', fontsize=10)  
            self.ax2.set_ylabel('最高价', fontproperties='SimHei', fontsize=10)  
            self.ax2.set_title('每支股票达到的最高价的柱状图', fontproperties='SimHei', fontsize=12)   
              
            # 刷新画布以显示新的图表  
            self.canvas2.draw()  
        except FileNotFoundError:  
            print("文件未找到，请检查文件路径是否正确。") 