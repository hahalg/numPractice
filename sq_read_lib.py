# -*- coding: utf-8-*-  

import xlrd

def readExcel(filename,sheetname=''):
        #文件位置
        ExcelFile=xlrd.open_workbook(filename)
        #获取目标EXCEL文件sheet名
        # print(ExcelFile.sheet_names())
        #若有多个sheet，则需要指定读取目标sheet例如读取sheet2
        #sheet2_name=ExcelFile.sheet_names()[1]
        #获取sheet内容【1.根据sheet索引2.根据sheet名称】
        #sheet=ExcelFile.sheet_by_index(1)
        if not sheetname=='':
                sheet=ExcelFile.sheet_by_name(sheetname)
        else:
                sheet=ExcelFile.sheet_by_index(0)
        #打印sheet的名称，行数，列数
        #     print(sheet.name,sheet.nrows,sheet.ncols)
        return sheet