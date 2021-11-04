#!/usr/bin/env python
# -*- coding:utf-8 -*-
import xlsxwriter

def write_chart(workbook,worksheet,name,cate_name,cate_val,col):
    #name 设置折线图表格的标题 以及 设置折线图的纵轴名称  cate_name 系列的名字，列表形式：[row,col]用于读取excel中的某个值
    #cate_vale [start_row,start_col,end_row,end_col]
    #col  在哪一列进行折线图的绘画
    chart = workbook.add_chart({'type': 'line'})
    chart.set_title({'name': name})
    chart.set_x_axis({'name': ['sheet_test', cate_name[0], cate_name[1]]})
    chart.set_y_axis({'name': name})
    chart.add_series({
        'marker': {'type': 'diamond'},
        'name': ['sheet_test', cate_name[0], cate_name[1]],
        # 'categories': ['sheet_test', 0, 0, 0, 5],
        'values': ['sheet_test', cate_val[0], cate_val[1], cate_val[2], cate_val[3]],
    })
    worksheet.insert_chart(cate_val[2] + 1, col, chart)

