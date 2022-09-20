"""
    @ author: 032002602陈俊龙
    @ Document description: 这个文件用于生成可视化大屏中的地图
"""
from pyecharts import options as opts
from pyecharts.charts import Map
from Demo01.Visualize_large_screen import get_mainland_data
import datetime
from pyecharts.globals import ThemeType
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
local_data = []


# 获取当天全国本土新增数据
def get_day_data(input_time: str):
    # 对输入的时间进行格式化，后续用于生成文件名
    date_year = int(input_time[0:4])
    date_month = int(input_time[4:6].lstrip('0'))
    date_day = int(input_time[6:8].lstrip('0'))
    date_time = datetime.datetime(date_year, date_month, date_day)

    # 根据时间生成当天通报文件的文件名
    file_day = str(date_time)[0:10]
    temp_month_time = str(date_time + datetime.timedelta(days=-1))[5:7].lstrip('0')
    temp_day_time = str(date_time + datetime.timedelta(days=-1))[8:10].lstrip('0')
    filename = file_day + f'-截至{temp_month_time}月{temp_day_time}日24时新型冠状病毒肺炎疫情最新情况.txt'

    # 从文件中提取出数据
    f = open(file=f'C:/Users/ASUS/Desktop/疫情防控数据/{filename}', mode='r', encoding='utf-8')
    text = f.read()
    local_datas = (get_mainland_data.get_Local_data(text))
    local_datas = format_local_data(local_datas)
    return local_datas


# 格式化提取出来的数据，使其能够导入到Map图表中
def format_local_data(data: dict) -> list:
    data_list = []
    for name in name_list:
        temp = {'name': f'{name}', 'value': int(data[f'{name}'])}
        data_list.append(temp['value'])
    return data_list


# 生成地图图表
def map_visual_map(sequence, date) -> Map:
    # 设置地图的分段样式（本土各省份新增数量）
    pieces = [
        {'min': 500, 'color': '#660000'},
        {'max': 499, 'min': 250, 'color': '#FF0000'},
        {'max': 249, 'min': 200, 'color': '#FF8000'},
        {'max': 199, 'min': 150, 'color': '#ffff00'},
        {'max': 149, 'min': 100, 'color': '#80ff00'},
        {'max': 99, 'min': 50, 'color': '#00ffff'},
        {'max': 49, 'min': 40, 'color': '#a0a0a0'},
        {'max': 39, 'min': 30, 'color': '#ff9999'},
        {'max': 29, 'min': 20, 'color': '#99ff99'},
        {'max': 19, 'min': 10, 'color': '#9999ff'},
        {'max': 9, 'min': 1, 'color': '#ffe5cc'},
        {'max': 1, 'color': '#FFCCE5'}
    ]

    # 创建地图Map对象
    c = (
        # opts.InitOpts() 设置初始参数:width=画布宽,height=画布高
        Map(opts.InitOpts(width='885px', height='580px', theme=ThemeType.PURPLE_PASSION))
            .add(series_name=date, data_pair=sequence, maptype="china")  # 系列名称(显示在中间的名称 )、数据 、地图类型
            .set_global_opts(
            # 设置标题样式
            title_opts=opts.TitleOpts(
                title="全国疫情情况",  # 设置主标题
                subtitle=f'{date}更新',   # 设置副标题
                pos_left='center',  # 居中
                pos_top='10%',
                # 分别设置主标题和副标题的样式
                title_textstyle_opts=dict(font_size=70, font_weight='bolder', width=100, height=80),
                subtitle_textstyle_opts=dict(font_size=25)
            ),

            # 设置地图内的数据的样式
            visualmap_opts=opts.VisualMapOpts(
                pieces=pieces,
                is_piecewise=True,
                textstyle_opts=dict(color='white', font_size=15),
                item_width=30,
                item_height=15
            ),

            # 设置标签样式
            legend_opts=opts.LegendOpts(
                is_show=False,  # 是否显示图例
                pos_top='3%',  # 图例距离顶部的距离
                orient='horizontal'  # 图例水平布局
            ),
        )

        # 设置图表样式
        .set_series_opts(
            label_opts=opts.LabelOpts(
                color='#202020',
                font_size=10
            )
        )
    )
    return c


if __name__ == '__main__':
    pass
