"""
    @ author: 032002602陈俊龙
    @ Document description: 这个文件用于获取港澳台相关数据
"""
import re
import datetime


# 使用正则表达式来提取数据
def draw_data_use_re(content: str):
    data_list = []  # 存储港澳台数据的列表
    info = re.search(r'香港特别行政区.*', content).group()  # 正则获取港澳台有关的文本数据
    info_list = info.split('，')  # 将提取到的文本进行切割，获取到每个地方的文本数据
    # 循环，顺序香港，澳门，台湾的有关数据
    for index in range(0, len(info_list), 2):
        num = re.search(r'[0-9]+', info_list[index]).group()  # 提取出数字
        data_list.append(int(num))  # 提取出的数字的str类型，需要转换为int类型
    return data_list


def get_increase_data(input_time: str):
    # 与时间格式的有关操作---------------------
    date_year = int(input_time[0:4])
    date_month = int(input_time[4:6].lstrip('0'))
    date_day = int(input_time[6:8].lstrip('0'))
    date_time = datetime.datetime(date_year, date_month, date_day)
    file_day = str(date_time)[0:10]
    temp_month_time = str(date_time + datetime.timedelta(days=-1))[5:7].lstrip('0')
    temp_day_time = str(date_time + datetime.timedelta(days=-1))[8:10].lstrip('0')
    # --------------------------------------------------------------
    # 获取今日有关数据-------------------------------------------------
    filename = file_day + f'-截至{temp_month_time}月{temp_day_time}日24时新型冠状病毒肺炎疫情最新情况.txt'
    f = open(file=f'C:/Users/ASUS/Desktop/疫情防控数据/{filename}', mode='r', encoding='utf-8')
    text = f.read()
    today_data = draw_data_use_re(text)
    # 获取昨日有关数据-------------------------------------------------
    temp_month_time2 = str(date_time + datetime.timedelta(days=-2))[5:7].lstrip('0')
    temp_day_time2 = str(date_time + datetime.timedelta(days=-2))[8:10].lstrip('0')
    file_day = str(date_time + datetime.timedelta(days=-1))[0:10]
    filename = file_day + f'-截至{temp_month_time2}月{temp_day_time2}日24时新型冠状病毒肺炎疫情最新情况.txt'
    f = open(file=f'C:/Users/ASUS/Desktop/疫情防控数据/{filename}', mode='r', encoding='utf-8')
    text = f.read()
    yesterday_data = draw_data_use_re(text)
    # 计算，得到港澳台每日新增数量----------------------------------------
    increase_data = []
    for index in range(0, len(today_data)):
        increase_data.append(today_data[index] - yesterday_data[index])
    return today_data, increase_data
