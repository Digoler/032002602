"""
    @ author: 032002602陈俊龙
    @ Document description: 这个文件用于生成港澳台数据图表，并将各个图表组装成可视化大屏。
"""
import webbrowser

from pyecharts.charts import Page
from Demo01.Visualize_large_screen.week_data import *
from Demo01.Visualize_large_screen.map import *
from Demo01.Visualize_large_screen.top3_rank import *
# 获取港澳台相关数据需要从 HK_MAC_TW.py文件中导入自己写好的函数
from Demo01.Visualize_large_screen.HK_MAC_TW import get_increase_data


# 生成地图
def get_map(date):
    native_data = get_day_data(date)    # 获取本土新增数据
    # 格式化数据，使其能够导入到地图图表中
    sequence = list(zip(name_list[1:], native_data[1:]))
    selected_time = str(format_time(date))[0:10]
    # 生成地图
    m = map_visual_map(sequence, f'{selected_time}')
    return m


# --------------------------------------------------------------------
# 生成港澳台新增数量的柱状图
def get_HK_MAC_TW_data(input_time: str) -> Bar:
    all_data, today_data = get_increase_data(input_time)    # 获取相应数据
    c = (
        Bar(init_opts=opts.InitOpts(width="590px", height='290px', theme=ThemeType.PURPLE_PASSION))
        # 添加X轴和Y轴
            .add_xaxis(['香港', '澳门', '台湾省'])
            .add_yaxis("商家A", today_data, bar_max_width=50, bar_min_width=20)
        # 配置全局样式
            .set_global_opts(
            # 配置标签样式
            title_opts=opts.TitleOpts(
                title="港澳台今日新增病例",
                pos_left='center',  # 标题展示位置
                title_textstyle_opts=dict(color='#fff')  # 设置标题字体颜色
            ),
            # 配置Y轴样式
            yaxis_opts=opts.AxisOpts(
                name="数量",
                name_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight='bolder'),
                axislabel_opts=opts.LabelOpts(  # 坐标轴标签配置
                    font_size=10,  # 字体大小
                    font_weight='bolder'  # 字重
                ),
            ),
            # 配置X轴样式
            xaxis_opts=opts.AxisOpts(
                name="地区",
                name_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight='bolder'),
                axislabel_opts=opts.LabelOpts(  # 坐标轴标签配置
                    font_size=15,  # 字体大小
                    font_weight='bolder'  # 字重
                ),
            ),
            # 配置标签样式
            legend_opts=opts.LegendOpts(
                is_show=False,  # 是否显示图例
            ),
        )
            # 自定义图表样式
            .set_series_opts(
            label_opts=opts.LabelOpts(
                is_show=True,
                font_style='oblique',
                font_weight='bolder',   # 字重
                font_size=15,   # 字体大小
            ),  # 是否显示数据标签
        )
    )
    return c


# 生成港澳台累计确诊数量的柱状图
def get_HK_MAC_TW_cumulative(input_time: str) -> Bar:
    all_data, today_data = get_increase_data(input_time)    # 获取相关数据
    c = (
        Bar(init_opts=opts.InitOpts(width="590px", height='290px', theme=ThemeType.PURPLE_PASSION))
        # 添加X轴和Y轴
            .add_xaxis(['香港', '澳门', '台湾'])
            .add_yaxis("商家A", all_data, bar_max_width=50, bar_min_width=20)
        # 配置全局样式
            .set_global_opts(
            # 配置标题样式
            title_opts=opts.TitleOpts(title="港澳台累计确诊病例", pos_left='center', title_textstyle_opts=dict(color='#fff')),
            # 配置Y轴样式
            yaxis_opts=opts.AxisOpts(
                name="数量",
                name_textstyle_opts=opts.TextStyleOpts(font_size=15),
                axislabel_opts=opts.LabelOpts(  # 坐标轴标签配置
                    font_size=10,  # 字体大小
                    font_weight='bolder'  # 字重
                ),
            ),
            # 设置X轴样式
            xaxis_opts=opts.AxisOpts(
                name="地区",
                name_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight='bolder'),
                axislabel_opts=opts.LabelOpts(  # 坐标轴标签配置
                    font_size=10,  # 字体大小
                    font_weight='bolder'  # 字重
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
                # position="center",
                font_style='oblique',
                font_weight='bolder',
                font_size=15,
            ),  # 是否显示数据标签
        )
    )
    return c


# ----------------------------------------------------
def page_draggable_layout(date):
    page = Page(layout=Page.SimplePageLayout, interval=0)
    page.add(
        get_map(date),
        get_timeline(date),
        create_rank_pic(date),
        get_HK_MAC_TW_data(date),
        get_HK_MAC_TW_cumulative(date),
    )
    page.render('BigScreen.html')
    webbrowser.open_new_tab('BigScreen.html')


def main():
    global file_day
    input_date = input("请输入你要查询的日期（如20220909）：")
    get_day_data(input_date)
    page_draggable_layout(input_date)


if __name__ == "__main__":
    main()
