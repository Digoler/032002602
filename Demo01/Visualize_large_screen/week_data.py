"""
    @ author: 032002602陈俊龙
    @ Document description: 这个文件用于生成可视化大屏中的七天疫情数据
"""
import pyecharts.options as opts
from pyecharts.charts import Timeline, Bar
from pyecharts.globals import ThemeType

from Demo01.Visualize_large_screen import get_mainland_data
import datetime


total_data = {}
name_list = [
    "本土病例",
    "北京",
    "天津",
    "河北",
    "山西",
    "内蒙古",
    "辽宁",
    "吉林",
    "黑龙江",
    "上海",
    "江苏",
    "浙江",
    "安徽",
    "福建",
    "江西",
    "山东",
    "河南",
    "湖北",
    "湖南",
    "广东",
    "广西",
    "海南",
    "重庆",
    "四川",
    "贵州",
    "云南",
    "西藏",
    "陕西",
    "甘肃",
    "青海",
    "宁夏",
    "新疆",
]


# 格式化时间的函数，后续用于生成文件名
def format_time(date):
    date_year = int(date[0:4])
    date_month = int(date[4:6].lstrip('0'))
    date_day = int(date[6:8].lstrip('0'))
    date_time = datetime.datetime(date_year, date_month, date_day)
    return date_time


# 获取七天内的数据
def get_week_data(input_time: str):
    # 格式化时间格式
    date_year = int(input_time[0:4])
    date_month = int(input_time[4:6].lstrip('0'))
    date_day = int(input_time[6:8].lstrip('0'))
    date_time = datetime.datetime(date_year, date_month, date_day)

    # 生成七天内的数据
    for index in range(1, 8):
        if index == 1:
            file_day = str(date_time)[0:10]
            temp_month_time = str(date_time + datetime.timedelta(days=-index))[5:7].lstrip('0')
            temp_day_time = str(date_time + datetime.timedelta(days=-index))[8:10].lstrip('0')
            filename = file_day + f'-截至{temp_month_time}月{temp_day_time}日24时新型冠状病毒肺炎疫情最新情况.txt'
        else:
            file_day = str(date_time + datetime.timedelta(days=-index))[0:10]
            temp_month_time = str(date_time + datetime.timedelta(days=-index-1))[5:7].lstrip('0')
            temp_day_time = str(date_time + datetime.timedelta(days=-index-1))[8:10].lstrip('0')
        filename = file_day+f'-截至{temp_month_time}月{temp_day_time}日24时新型冠状病毒肺炎疫情最新情况.txt'
        f = open(file=f'C:/Users/ASUS/Desktop/疫情防控数据/{filename}', mode='r', encoding='utf-8')
        text = f.read()
        local_data = get_mainland_data.get_Local_data(text)

        # 格式化本土新增数据
        local_data = format_local_data(local_data)
        total_data[f'{file_day}'] = local_data
    return total_data


# 格式化本土新增数据，使其能够导入到柱状图中生成相应图表
def format_local_data(data: dict) -> list:
    data_list = []
    for name in name_list:
        temp = {'name': f'{name}', 'value': int(data[f'{name}'])}
        data_list.append(temp)
    return data_list


# 生成七天疫情数据图表（柱状图）
def get_week_chart(date: str) -> Bar:
    bar = (
        Bar(init_opts=opts.InitOpts(width='880px', height='600px', theme=ThemeType.PURPLE_PASSION))
            .add_xaxis(xaxis_data=name_list)    # 添加X轴
        # 添加Y轴，并设置条形的样式
            .add_yaxis(
            series_name="每日本土新增确诊",
            y_axis=total_data[f"{date}"],
            category_gap=5,
            color="#333300",
            label_opts=opts.LabelOpts(is_show=True),
        )
        # 配置全局样式
            .set_global_opts(
            # 配置标题样式
            title_opts=opts.TitleOpts(
                title="{}全国疫情数据".format(date), subtitle="数据来自中华人民共和国国家卫生健康委员会", pos_top='10%', pos_left='center',
                title_textstyle_opts=dict(font_size=36, font_weight='bolder'),
                subtitle_textstyle_opts=dict(font_size=25)
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="shadow"
            ),
            # 设值全局设置，更改 interval 的值，默认会采用标签不重叠的方式显示标签（也就是默认会将部分文字显示不全）可以设置为0强制显示所有标签，
            # 如果设置为1，表示隔一个标签显示一个标签，如果为3，表示隔3个标签显示一个标签，以此类推

            # 设置Y轴的样式
            yaxis_opts=opts.AxisOpts(
                name="数量",
                name_textstyle_opts=opts.TextStyleOpts(font_size=20, font_weight='bolder'),
                axislabel_opts=opts.LabelOpts(  # 坐标轴标签配置
                    font_size=10,  # 字体大小
                    font_weight='bolder'  # 字重
                ),
            ),
            # 设置X轴的样式
            xaxis_opts=opts.AxisOpts(
                name="地区",
                name_textstyle_opts=opts.TextStyleOpts(font_size=20, font_weight='bolder'),
                axislabel_opts=opts.LabelOpts(  # 坐标轴标签配置
                    font_size=8.5,  # 字体大小
                    font_weight='bolder',  # 字重
                    interval="0"
                ),
            ),
            # 设置不显示图例
            legend_opts=opts.LegendOpts(
                is_show=False,  # 是否显示图例
            ),
        )
        .set_series_opts(  # 自定义图表样式
            label_opts=opts.LabelOpts(
                is_show=True,
                font_style='oblique',
                font_weight='bolder',
                font_size=9.5,
            ),  # 是否显示数据标签
        )
    )
    return bar


# 生成七天数据柱形图的轮播图
def get_timeline(date_string: str):
    get_week_data(date_string)  # 获取七天内数据
    date_str = str(format_time(date_string))[0:10]

    # 生成轮播图对象
    timeline = Timeline(init_opts=opts.InitOpts(width="885px", height="580px", theme=ThemeType.PURPLE_PASSION))
    # 将数据导入到轮播图中，生成图表
    for index in range(1, 8):
        if index == 1:
            file_day = date_str
        else:
            sel_time = format_time(date_string)
            file_day = str(sel_time + datetime.timedelta(days=-index))[0:10]
        timeline.add(get_week_chart(date=file_day), time_point=str(file_day))
    # 设置轮播图的一些样式
    timeline.add_schema(is_auto_play=True, play_interval=1000, pos_left="15%",)
    return timeline
