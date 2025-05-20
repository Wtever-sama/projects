from PyQt5.QtWidgets import QVBoxLayout,QDialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  
from PyQt5 import QtWidgets  
import pandas as pd

class MyDialog4(QDialog):  #价格走势折线图
    def __init__(self,text_to_display,fileName, parent=None): 
        super(MyDialog4, self).__init__(parent)
        self.number=int(text_to_display)#全局变量
        self.filename=fileName
        self.setWindowTitle("Matplotlib 绘图对话框")  
        #对于all股票的绘图 ，bar
        #创建第一个 matplotlib Figure 和 Canvas  
        self.fig4 = Figure() 
        self.canvas4 =  FigureCanvas(self.fig4)
        self.ax4 = self.fig4.add_subplot(111)  
        self.ax4.set_title('线图')  
        # 有一个按钮pushButton_pic_type，点击后会调用 update_plot 方法  
        self.button_ma=QtWidgets.QPushButton('绘图', self) 
        self.button_ma.clicked.connect(self.update_plot) 
        # 布局  
        layout = QVBoxLayout(self)  
        layout.addWidget(self.canvas4)  
        layout.addWidget(self.button_ma)   

    def update_plot(self):  
        df=pd.read_excel(self.filename)
        try:    
            fi_dfs0= df.loc[(df['股票代码'] == self.number), ['开盘价']]#过滤出1001股票的开盘价dataframe
            fi_dfe0= df.loc[(df['股票代码'] == self.number), ['收盘价']]
            fi_dfs=fi_dfs0.reset_index(drop=True)#重置行索引，开盘
            fi_dfe=fi_dfe0.reset_index(drop=True)
            n=fi_dfs.shape[0]#n代表天数
            fdf0=df.loc[df['股票代码'] == self.number]#过滤出代号的信息
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
            
            self.ax4.clear()
            self.ax4.plot(x1, lis_p, linestyle='--',label='Price trend',color='green',marker='o',markeredgecolor='orange') 
            self.ax4.legend()  
            self.ax4.set_xlabel('时间',fontname='SimHei', fontsize=10)  
            self.ax4.set_ylabel('价格',fontname='SimHei', fontsize=10)  
            self.ax4.set_title('价格走势折线图',fontname='SimHei', fontsize=12)  
            # 刷新画布以显示新的图表  
            self.canvas4.draw()  
        except FileNotFoundError:  
            print("文件未找到，请检查文件路径是否正确。")  