"""
    @ author: 0320020602陈俊龙
    @ Document description：这是数据统计接口，整个项目的接口也是这个文件，运行这个文件可以实现项目的三个功能三个功能
                            1. 爬取所有的页面数据
                            2. 爬取今天最新疫情数据并保存到Excel和生成图表
                            3. 生成可视化大屏
"""
import asyncio
from pyppeteer import launch
from lxml import etree
from Demo01.Spider.fetch_data_main import main as fetch_main
from Demo01.showdata.draw_data import main as draw_main
from draw_data import draw_today_data
from Demo01.setting import *
from Demo01.Visualize_large_screen.Big_Screen import main as screen_main


# 获取网页源代码
async def FetchUrl(url: str) -> str:
    # launch 方法新建一个 Browser 对象，然后赋值给 browser
    browser = await launch({'headless': True, 'dumpio': True, 'autoClose': True})

    # 调用 newPage方法相当于浏览器中新建了一个选项卡，同时新建了一个Page对象。
    page = await browser.newPage()

    # 绕过浏览器检测（关键步骤）
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                     '{ webdriver:{ get: () => false } }) }')

    # 设置 UserAgent
    await page.setUserAgent(
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.27')
    # Page 对象调用了 goto 方法就相当于在浏览器中输入了这个 URL，浏览器跳转到了对应的页面进行加载
    await page.goto(url)
    await asyncio.wait([page.waitForNavigation()], timeout=3)  # 等待页面加载完成

    # 页面加载完成之后再调用 content 方法，返回当前浏览器页面的源代码
    page_content = await page.content()

    await browser.close()
    return page_content


# 获取页面源代码
def get_page_source(text_url: str) -> str:
    # 创建事件循环，实现异步爬虫
    return asyncio.get_event_loop().run_until_complete(FetchUrl(text_url))


# -----获取最新一天的疫情通报信息-----
def get_today_url(html_txt):
    html_tree = etree.HTML(html_txt)  # 生成etree对象
    href = html_tree.xpath("/html/body/div[3]/div[2]/ul/li[1]/a/@href")  # 提取出页面源代码中的所有li对象
    url = "http://www.nhc.gov.cn" + "".join(href)   # 获取当天页面的url
    title = html_tree.xpath('/html/body/div[3]/div[2]/ul/li[1]/a/text()')   # 获取当天文本标题
    date = html_tree.xpath('/html/body/div[3]/div[2]/ul/li[1]/span/text()')  # 获取发布时间
    # 组成形成最终文件名
    filename = "".join(date) + '-' + "".join(title)
    return url, filename


#  获取每一天的发布内容
def get_each_day_content(html_txt: str) -> str:
    html_tree = etree.HTML(html_txt)
    text = html_tree.xpath('/html/body/div[3]/div[2]/div[3]//text()')   # 定位到文本所在的位置，进行提取
    day_text = "".join(text)    # xpath返回的是一个列表，我们需要把它拼接成字符串
    return day_text
# ----------------------------------------


# 保存文件到指定的目录
def save_file(path: str, filename: str, text: str):
    # 保存文件
    with open(path + filename + ".txt", 'w', encoding='utf-8') as f:
        f.write(text)


# 用户选择功能函数
def client_options():
    print("1: 获取所有的疫情数据")
    print("2: 获取当天最新疫情数据")
    print("3: 生成可视化大屏")
    option = input("please input one number to select your demand:")
    return option


# 主函数，用于向其他python文件暴露调用接口
def main():
    opt = client_options()  # 获取用户选择
    # 根据用户选择调用相应函数
    if opt == '1':
        fetch_main()   # 爬取所有数据
        draw_main()    # 提取所有数据
    elif opt == '2':
        # 获取当天最新疫情数据
        page_url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
        page_content = get_page_source(page_url)    # 获取当天页面的源代码
        # 获取当天页面的url和文件名
        today_url, filename = get_today_url(page_content)
        html = get_page_source(today_url)   # 获取当天页面的源代码
        content = get_each_day_content(html)    # 获取当日文本
        save_file(f'{TXT_SAVE_PATH}/', filename, content)   # 保存文件
        draw_today_data(filename)   # 将当天数据提取到Excel并生成图表
    elif opt == '3':
        # 生成可视化大屏
        screen_main()


if __name__ == '__main__':
    main()




