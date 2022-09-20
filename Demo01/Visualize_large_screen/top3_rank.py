"""
    @ author: 032002602陈俊龙
    @ Document description: 这个文件用于生成可视化大屏中的排行榜
"""
import datetime
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

from Demo01.Visualize_large_screen import get_mainland_data
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


# ---------------本土新增Top3--------------------
# 获取本土今日新增的数据
def get_day_data_1(input_time: str):
    # 格式化时间格式
    date_year = int(input_time[0:4])
    date_month = int(input_time[4:6].lstrip('0'))
    date_day = int(input_time[6:8].lstrip('0'))
    date_time = datetime.datetime(date_year, date_month, date_day)
    file_day = str(date_time)[0:10]

    # 根据日期生成文件名
    temp_month_time = str(date_time + datetime.timedelta(days=-1))[5:7].lstrip('0')
    temp_day_time = str(date_time + datetime.timedelta(days=-1))[8:10].lstrip('0')
    filename = file_day + f'-截至{temp_month_time}月{temp_day_time}日24时新型冠状病毒肺炎疫情最新情况.txt'
    f = open(file=f'C:/Users/ASUS/Desktop/疫情防控数据/{filename}', mode='r', encoding='utf-8')
    text = f.read()

    # 获取数据并格式化数据
    local_datas = (get_mainland_data.get_Local_data(text))
    local_datas = format_local_data_1(local_datas)
    return local_datas


# 按照Bar类型需要传入的数据类型对数据进行格式化
def format_local_data_1(data: dict) -> dict:
    data_list = {}
    for name in name_list:
        data_list[name] = int(data[name])
    return data_list


# 生成排名信息，将元组解包
def get_rank(tuple_: tuple):
    name = tuple_[0]
    value = tuple_[1]
    return name, value


# 创建柱状图排行榜Top3
def create_rank_pic(input_time: str) -> Bar:
    today_data = get_day_data_1(input_time) # 获取今日新增数据
    data = sorted(today_data.items(), key=lambda x: x[1], reverse=True)  # 对字典按值进行排序，返回的是一个元组

    # 获取与排名有关的数据
    first, second, third = data[1:4]
    first_name, first_value = get_rank(first)
    second_name, second_value = get_rank(second)
    third_name, third_value = get_rank(third)
    rank_name = [third_name, second_name, first_name]
    rank_value = [third_value, second_value, first_value]

    # 初始化柱状图
    c = (
        Bar(init_opts=opts.InitOpts(width="590px", height='290px', theme=ThemeType.PURPLE_PASSION))
        # 添加X轴和Y轴
            .add_xaxis(rank_name)
            .add_yaxis("商家A", rank_value, category_gap=80, bar_max_width=100, bar_min_width=20)
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        # 配置全局样式
            .set_global_opts(
            title_opts=opts.TitleOpts(title="本土新增病例Top3", pos_left='center', title_textstyle_opts=dict(color='#fff')),
            legend_opts=opts.LegendOpts(
                is_show=False,  # 是否显示图例
                pos_left='right',  # 图例显示位置
                pos_top='3%',  # 图例距离顶部的距离
                orient='horizontal'  # 图例水平布局
            ),
            # 设置Y轴的样式
            yaxis_opts=opts.AxisOpts(
                name="地区",
                name_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight='bolder'),
                axislabel_opts=opts.LabelOpts(  # 坐标轴标签配置
                    font_size=10,  # 字体大小
                    font_weight='bolder'  # 字重
                ),
            ),
            # 设置X轴的样式
            xaxis_opts=opts.AxisOpts(
                name="数量",
                name_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight='bolder'),
                axislabel_opts=opts.LabelOpts(  # 坐标轴标签配置
                    font_size=10,  # 字体大小
                    font_weight='bolder'  # 字重
                ),
            )
        )
        # 设置图表样式
        .set_series_opts(  # 自定义图表样式
            label_opts=opts.LabelOpts(
                is_show=True,
                position="right",
                font_style='oblique',
                font_weight='bolder',
                font_size=15,
            ),  # 是否显示数据标签
        )
    )
    return c
