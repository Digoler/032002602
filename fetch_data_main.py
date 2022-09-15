import asyncio
from pyppeteer import launch
import os
from lxml import etree
import random
import time


# 获取每一个有防控数据页面的内容（即页面源代码）
def get_page_source(text_url: str) -> str:
    # 创建事件循环，实现异步爬虫
    return asyncio.get_event_loop().run_until_complete(FetchUrl(text_url))


# 获取每一页面的url(共42页)
def get_page_url() -> list:
    url_list = []  # 用来保存42个页面的42个url
    for page in range(1, 42):
        if page == 1:   # 第一页的时候，页面的url比较特殊，我们单独拿出来保存
            url_list.append('http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml')
        else:   # 剩下的页面的url有规律，我们直接用 lambda匿名函数生成即可
            # 拼接成完整的url
            url_list.append(lambda page: 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_' + str(page) + '.shtml')
    return url_list


# 通过xpath数据解析来提取出我们想要的文件名（以页为单位进行存储）
def get_filenames(html_txt: str):
    file_list = []  # 定义一个列表用来存储当前页的24个文件名
    html_tree = etree.HTML(html_txt)    # 生成etree对象
    li_list = html_tree.xpath("/html/body/div[3]/div[2]/ul/li")  # 提取出页面源代码中的所有li对象
    # 遍历每一个li对象，进行文件名提取
    for li in li_list:
        file = "".join(li.xpath("./a/text()"))  # 获取页面中每个文件的名称,xpath返回的是一个列表，我们需要给它拼接成字符串
        date = "".join(li.xpath('./span/text()'))   # 为了保证文件名的唯一性，我还在文件名里面加上了发布日期
        file_name = date + "-" + file   # 连接形成完整的文件名
        file_list.append(file_name)  # 加入到文件名列表中
    return file_list


# 获取每一个页面(目前共42页)的24条url
def get_link_url(html_txt: str) -> list:
    day_urls = []  # 定义一个用来存储所有页面内24条url的列表
    html_tree = etree.HTML(html_txt)    # 生成etree对象
    li_list = html_tree.xpath("/html/body/div[3]/div[2]/ul/li")  # 提取出页面源代码中的所有li对象
    for li in li_list:
        day_url = li.xpath('./a/@href')  # 对每个li对象，分别提取出它里面的 a 标签的属性值
        day_url = "http://www.nhc.gov.cn" + "".join(day_url[0])  # 由于提取到的href是相对于网页的相对路径，我们需要拼接成完整的url
        day_urls.append(day_url)
    return day_urls


#  获取每一天的发布内容
def get_each_day_content(html_txt: str) -> str:
    html_tree = etree.HTML(html_txt)
    text = html_tree.xpath('/html/body/div[3]/div[2]/div[3]//text()')   # 定位到文本所在的位置，进行提取
    day_text = "".join(text)    # xpath返回的是一个列表，我们需要把它拼接成字符串
    return day_text


# 保存文件到指定的目录
def save_file(path: str, filename: str, text: str):
    if not os.path.exists(path):
        os.makedirs(path)
    # 保存文件
    with open(path + filename + ".txt", 'w', encoding='utf-8') as f:
        f.write(text)


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
    #
    await browser.close()
    return page_content


if "__main__" == __name__:
    start = time.time()  # 设置时间戳，查看程序运行时间
    page_urls = get_page_url()    # 获取42个页面的url
    for url in page_urls:   # 遍历每一个疫情通报页面
        page_text = get_page_source(url)    # 这一步是获取疫情通报页面的页面源代码
        time.sleep(random.randint(3, 6))    # 设计一个随机的程序睡眠时间，让程序更好地模仿人进行爬取页面数据
        filenames = get_filenames(page_text)    # 提取出当前疫情通报页面的所有文件名
        index = 0   # 设置文件名索引
        links = get_link_url(page_text)  # 获取当前疫情通报页面的24条url
        # ----------获取这个页面24天的疫情通报内容文本----------
        for link in links:
            html = get_page_source(link)    # 获取这一天的页面源代码
            content = get_each_day_content(html)    # 从页面源代码中提取出我们需要的文本
            print(filenames[index] + "爬取成功")    # 程序运行情况提示
            save_file('C:/Users/ASUS/Desktop/数据防控数据1/', filenames[index], content)  # 保存文件到指定文件夹
            index = index + 1
        # ---------------------------------------- --------
        print("-----" * 20)  # 爬取完一页所设置的标识情况，方便观察程序运行情况
    end = time.time()
    print(f"所有内容爬取完成，所用时间：{end - start}s")
