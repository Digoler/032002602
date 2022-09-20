"""
    @ author: 032002602陈俊龙
    @ Document description: 这个文件用于获取本土新增的数据，用于生成可视化大屏地图中的数据
"""
import re

province_name = ['福建', '河北', '河南', '湖南', '湖北', '广东', '北京', '上海', '天津', '重庆', '四川', '黑龙江', '内蒙古', '西藏', '宁夏', '浙江', '山东',
                 '安徽', '江西', '山西', '吉林', '江苏', '云南', '贵州', '陕西', '甘肃', '青海', '辽宁', '广西', '新疆', '海南']


# 检验省份名字是否正确的函数
def verify_name(name_str):
    area_name = ''
    for name in province_name:
        if name in name_str:
            area_name = name
            break
    return area_name


# 改进一下字典，没有病例的省份的值设为0
def refine_dict(dictionary):
    for province in province_name:
        if province not in dictionary:
            dictionary[province] = 0
    return dictionary


# 获取本土新增数据
def get_Local_data(content):
    area_num = {}
    if re.search(r"[^\u4e00-\u9fa5]本土病例.*。", content) is None:
        area_num['本土病例'] = 0
        return area_num
    else:
        information = (re.search(r"[^\u4e00-\u9fa5]本土病例.*。", content)).group()

        all_increase = (re.search(r'\d+', information)).group()  # all_increase 为本土新增的病例数
        area_num[(re.search(r'本土病例', information)).group()] = all_increase

        # 获取出每个省份新增人数的信息
        province_increase = (re.search(r'（.*?）', information)).group()

        # 解决文本格式不一致的问题,比如说xx省x例，其中xx市几例；xx省x例，其中xx市x例
        if '；' in province_increase:
            increase_list = province_increase.split('；')
        else:
            increase_list = province_increase.split('，')

        for area_increase in increase_list:
            area_name = re.search(r'[\u4e00-\u9fa5]+', area_increase).group()
            # 解决出现类似：本土新增x例（均在福建）的问题
            if re.search(r'[0-9]+', area_increase) is None:
                area_name = verify_name(area_name)
                area_num[area_name] = all_increase
            else:
                area_name = verify_name(area_name)
                increase_num = re.search(r'[0-9]+', area_increase).group()
                area_num[area_name] = increase_num
        return refine_dict(area_num)
