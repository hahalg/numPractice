# coding=utf-8
# SQ数字编码练习
# 编写时间：2019-01-02 作者：SQ
# 主程序

import os
import random
import shelve
import sys
import time

import cv2
from pylab import mpl
from PyQt5.QtGui import *
# from PyQt5.QtWidgets import QAbstractItemView,QTableWidgetItem,QTableWidget,QDesktopWidget,QHeaderView
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
from SQUi_act_do_toolbuttom import *
# sys.path.append("..")
# from sqlib.sq_read_lib import readExcel
from sq_read_lib import readExcel

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
mpl.rcParams['figure.subplot.left'] = 0.03
mpl.rcParams['figure.subplot.bottom'] = 0.1
mpl.rcParams['figure.subplot.right'] = 0.99
mpl.rcParams['figure.subplot.top'] = 0.99       
 
class sq_win(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(sq_win,self).__init__() 
        self._data_init()
        self.setupUi(self)
        self._setClick()
        self.letsRun()

    def _setClick(self):
        '''设置点击事件'''
        self.pushButton_2.clicked.connect(self.letsRun)
        self.pushButton.clicked.connect(self.showAnalysis)
        for i in range(12):
            exec('self.toolButton_{}.clicked.connect(self.judgeRight)'.format(i+1))


    def _data_init(self):
        '''初始化数据'''
        self.plt = None
        self.showdatas = []
        self.trueNum = ''
        self.data = readExcel('numcode.xlsx','Sheet1')
        # print('data:',self.data)
        #打印sheet的名称，行数，列数
        # print(self.data.name,self.data.nrows,self.data.ncols)
        self.db = shelve.open("sq_shelve",writeback=True)
        m_mark = self.db.get('num',{}).get('sq','')
        if m_mark == '':
            self.db['num'] = {}
            self.db['num']['sq'] = '1'

    def letsRun(self):
        '''生成随机图'''
        self.showdatas,self.trueNum = self._getRandom()
        # print(self.showdatas,self.trueNum)
        self._rander(self.showdatas)
        self.label.setText(self.trueNum)
    
    def _appendData(self,num,type='normal'):
        '''记录下对错的结果'''
        m_nor,m_err = self.db['num'].get(self.trueNum,[0,0])
        if type=='err':
            m_err+=1
        else:
            m_nor+=1
        self.db['num'][self.trueNum]=[m_nor,m_err]
        # print(num,m_nor,m_err)

    def judgeRight(self):
        '''判断对错
        如果点击的值等于trueNum则对'''
        # 可以指向同一个事件，用 sender = self.sender() 得到是哪个控件触发的
        sender = self.sender()
        # print(sender.text() + ' was pressed')
        m_rv = self.showdatas.index(self.trueNum)+1
        # print(f'ture num is :{m_rv}')
        if sender.text()==str(m_rv):
            # print('you are right!')
            self._appendData(self.trueNum)
            m_file = f"photo/r.png"
        else:
            # print('you are stupid!')
            self._appendData(self.trueNum,type='err')
            m_file = f"photo/w.png"
        m_Img = QtGui.QPixmap(m_file)
        self.label_OK.setPixmap(m_Img)
        self.label_OK.setScaledContents(True)

        m_str = self.data.cell(int(self.trueNum),1).value
        self.setWindowTitle(self.trueNum+' '+m_str)
        self.label_13.setText(self.trueNum+' '+m_str)
        self._setGraphView()
        self.letsRun()

    def showAnalysis(self):
        '''显示分析窗口'''
        if self.plt is None:
            import matplotlib.pyplot as plt
            self.plt = plt
        else:
            self.plt.close()
        nor_colors = [ 'green', 'lightgreen', 'cyan', 'purple', 'orange', 'blue','brown','yellow','gray','pink','black','gold']
        err_color = 'red'

        m_num = 0
        self.plt.figure(figsize=(16,4))
        m_allcount = 0
        m_errs = {}
        while m_num< 100:
            m_Snum = str(m_num)
            if len(m_Snum)==1:
                m_Snum = '0'+m_Snum               
            m_nor,m_err = self.db['num'].get(m_Snum,[0,0])
            m_name = m_Snum #+ ' (' + str(m_err) + '/' + str(m_nor) + ')'
            m_count = m_nor+m_err
            m_allcount+=m_count
            x = [m_num,m_num]
            y = [0,m_nor]
            self.plt.plot(x, y, linewidth = 6,color=random.choice(nor_colors),alpha=0.8)
            y = [m_nor,m_count]
            self.plt.plot(x, y, linewidth = 6,color=err_color,alpha=0.8)
            self.plt.text(x[1] , m_count+0.2, str(m_name), ha='center', va='bottom')
            if m_err>0:
                m_errs[m_Snum]=m_err
            m_num+=1

        # 排序
        m_errs = sorted(m_errs.items(),key = lambda x:x[1],reverse = True)
        # print(m_errs)
        m_str = ''
        for err in m_errs:
            m_str=m_str+' '+err[0]
        self.plt.xlabel('Count:'+str(m_allcount)+' err:'+m_str)
        self.plt.grid(True) 
        self.plt.show()        

    def _setGraphView(self):
        ''' 显示右下角的正确图片'''
        x = self.graphicsView.width()
        # y = self.graphicsView.height()
        img = QtGui.QPixmap()
        img.load(f'photo/{self.trueNum}.jpg')
        item=QGraphicsPixmapItem(img)                      #创建像素图元
        item.setScale(x/img.width())
        scene=QGraphicsScene()                             #创建场景
        scene.addItem(item)
        self.graphicsView.setScene(scene)                        #将场景添加至视图

    def __del__(self):
        self.db.close()
        if self.plt is not None:
            self.plt.close()

    def _getRandom(self,num=12):
        '''生成num个随机数和一个真值'''
        m_list = range(100)
        m_rlist = random.sample(m_list, num)
        m_relist = []
        for m_nums in m_rlist:
            m_num = str(m_nums)
            if len(m_num)==1:
                m_num = '0'+m_num
            m_relist.append(m_num)
        return m_relist,random.choice(m_relist)
        
    def _rander(self,datalist):
        '''生成图片'''
        i = 0
        # print('label:',self.mLW_W,self.mLW_H)
        for data in datalist:
            i+=1
            m_file = f"photo/{data}.jpg"
            exec('self.toolButton_{}.setIcon(QIcon(m_file))'.format(i))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = sq_win()
    ui.show()
    sys.exit(app.exec_())
