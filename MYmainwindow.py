from PyQt5 import QtWidgets 
from UImainwindow import Ui_MainWindow 
from MYdialog1 import MyDialog1
from MYdialog2 import MyDialog2
from MYdialog3 import MyDialog3
from MYdialog4 import MyDialog4 
from MYdialog5 import MyDialog5
import pandas as pd
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):  
    def __init__(self):  
        super().__init__()  
        self.setupUi(self)  # 初始化UI窗口和控件 

        # 连接 choice_bt_2 的 clicked 信号到 open_file_dialog 槽函数 
        self.choice_bt_2.clicked.connect(self.open_file_dialog)
        #选择每支股票达到的最高价的柱状图的复选项
        self.checkBox_all_hi_price_3.clicked.connect(self.on_checkbox_changed2)#由于所有的checkbox后期改成了button,statechanged也改成clicked
        #所有开盘价均值柱状图的
        self.checkBox_open_mean_3.clicked.connect(self.on_checkbox_changed3)
        
        #移动平均线图
        self.checkBox_ma.clicked.connect(self.on_checkbox_changed5)
        #K线图
        self.checkBox_kline.clicked.connect(self.on_checkbox_changed1)
        #价格走势折线图
        self.checkBox_price_upandown.clicked.connect(self.on_checkbox_changed4)

    def open_file_dialog(self):  
        # 使用 QFileDialog 打开文件对话框进行预览（仅能预览）
        self.options = QtWidgets.QFileDialog.Options()  
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",  
                "All Files (*);;Text Files (*.txt)", options=self.options) 
        if self.fileName: 
            print("选择的文件:", self.fileName) 
            self.file_path_edt_2.setText(self.fileName)  
            # 读取Excel文件的前5行  
            df = pd.read_excel(self.fileName)  #, nrows=5
            # 将数据转换为字符串并显示在QTextEdit中  
            self.textEdit.setText(df.to_string()) 
    
    def on_checkbox_changed1(self):  #K线图 checkBox_kline
        text_to_pass = self.stock_read_lineedt.text()
        if not text_to_pass:
            print('请输入文本')
        else:
            dialog = MyDialog1(text_to_pass,self.fileName,self)  # 创建MyDialog1的实例  
            dialog.exec_()  # 显示对话框
    def on_checkbox_changed2(self):  #每支股票达到的最高价的柱状图   
        dialog = MyDialog2(self.fileName,self)  # 创建MyDialog2的实例  
        dialog.exec_()  # 显示对话框
    
    def on_checkbox_changed3(self): #所有开盘价均值柱状图的 checkBox_open_mean_3
        dialog = MyDialog3(self.fileName,self)  # 创建MyDialog3的实例  
        dialog.exec_()  # 显示对话框 
    def on_checkbox_changed4(self):  #移动平均线图 checkBox_ma
        # 获取 QLineEdit 中的文本 #此处获取的是用户想要看的股票代号
        text_to_pass = self.stock_read_lineedt.text()
        if not text_to_pass:
            print('请输入文本')
        else:
            dialog = MyDialog4(text_to_pass,self.fileName,self)  # 创建MyDialog4的实例  
            dialog.exec_()  # 显示对话框
    
    def on_checkbox_changed5(self): #价格走势折线图 checkBox_price_upandown
        text_to_pass = self.stock_read_lineedt.text()
        if not text_to_pass:
            print('请输入文本')
        else:
            dialog = MyDialog5(text_to_pass,self.fileName,self)  # 创建MyDialog5的实例  
            dialog.exec_()  # 显示对话框   
 