# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_design_ui_4.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys  
from PyQt5 import QtWidgets    

from MYmainwindow import MainWindow

if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)  
    mainWindow = MainWindow()  # 创建 MainWindow 类的实例  
    mainWindow.show()  # 显示窗口  
    sys.exit(app.exec_())  # 进入主事件循环，等待用户操作
