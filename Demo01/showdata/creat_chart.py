"""
    @ author: 032002602陈俊龙
    @ Document description: 这个文件用于在Excel文件中批量生成图表
"""
import openpyxl
from openpyxl.chart import (
    Reference,
    label
)


#   生成图表函数
def myChart(excel_name):
    # 打开Excel文件
    wb = openpyxl.load_workbook(excel_name)

    # 遍历所有的sheet
    for SheetName in wb.sheetnames:
        sheet = wb[f'{SheetName}']
        # 划定数据的范围
        values = openpyxl.chart.Reference(sheet, min_row=1, min_col=2, max_row=32, max_col=2)  # 设置数据区域
        data_chart = openpyxl.chart.BarChart()

        # 调整图表的样式
        data_chart.legend = None
        data_chart.showGridLines = False    # 设置不显示网格线
        data_chart.dLbls = label.DataLabelList()
        data_chart.dLbls.showVal = True
        data_chart.varyColors = True
        data_chart.width = 25
        data_chart.height = 14
        data_chart.title = f'{SheetName}'
        data_chart.x_axis.title = '省份'
        data_chart.y_axis.title = '数量'

        # 划定X轴标签名范围
        categs = openpyxl.chart.Reference(sheet, min_col=1, min_row=1, max_row=32, max_col=1)

        # 往图表对象中添加数据
        data_chart.add_data(data=values)
        data_chart.set_categories(categs)

        # 将图表添加到指定sheet中
        sheet.add_chart(data_chart, 'D1')

        # 保存图表
        wb.save(excel_name)

