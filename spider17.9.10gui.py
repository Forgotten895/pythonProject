#网络爬虫程序，爬取DF中文商城（http://www.dfrobot.com.cn/index.php）所有产品的sku名称与价格数据
import requests
from requests.exceptions import RequestException
import re
import pandas
import tkinter
import os
import time
import threading
from tkinter import scrolledtext
from tkinter import filedialog


if __name__ == '__main__':
    #function：获取一个网页的html源码
    # input：输入网页url链接
    # return: 返回html源码
    def get_one_page(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:  # 返回200即为获取数据正确
                # print("get ok")
                return response.text
            #print(response.status_code)
            return None
        except RequestException:
            #print("get err")
            return None


    # function：搜索下一页对应的页码
    # input：输入网页html源码
    # return: 返回搜索结果
    def parse_one_total_page(html):
        pattern = re.compile(
            '<a class="next" href=\'category-216-b0-min0-max0-attr0-(.*?)-goods_id-DESC.html\'>下一页</a>', re.S)
        items = re.findall(pattern, html)
        return items


    # function：搜索所有商品界面的所有商品超链接
    # input：输入网页html源码
    # return: 返回搜索结果
    def parse_one_index_page(html):
        pattern = re.compile('<div class="goodsItemh productBlock".*?href="(.*?)".*?</div>', re.S)
        items = re.findall(pattern, html)
        return items


    # function：搜索商品页面信息，sku，名称，价格，可以在增加
    # input：输入网页html源码
    # return: 返回搜索结果，字典形式
    def parse_one_goods_page(htmlGoods):
        patternGoods = re.compile(
            '<div class="goodsTitle">\n\t\t\t\t\t\t(.*?)\t.*?<font class="brief">.*?<div class="goodsMes" data-stock=".*?" data-price="(.*?)" data-promote=".*?" data-vip=".*?">.*?<div class="name">货号</div>.*?<div class="content2">(.*?)</div>',
            re.S)
        itemsGoods = re.findall(patternGoods, htmlGoods)
        for item in itemsGoods:
            yield {
                'mincheng': item[0],
                'jiage': item[1],
                'sku': item[2]
            }
        return itemsGoods


    new_total = []  # 全局列表变量，存储所有收到的数据以便存储到表格中

    # function：将存储所有数据的列表存储到表格中
    # input：
    # return:
    def write_to_file():
        df = pandas.DataFrame(new_total)
        # print(df)
        df.columns = ['SKU', '名称', '价格']  # 设定行名称
        df.to_excel('result.xlsx')  # 存储为excel文件

    def opendir():
        fname = filedialog.askopenfilename(parent=window, title=('打开文件'),initialdir=os.path.split(os.path.realpath(__file__))[0],filetypes=( ("Excel文件", "*.xlsx"), ("All files", "*.*")))
        #print(fname)
        os.startfile(fname)

    #function：按键按下后，子线程运行爬虫程序
    #input：
    #return:
    def run_proc():
        running = True
        page = 1
        lb.insert(tkinter.END, '==================================================\n')
        lb.insert(tkinter.END, str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' 获取总页数中...\n')
        #print('calculation page total...')

        while running:
            url = 'http://www.dfrobot.com.cn/category-216-b0-min0-max0-attr0-'+str(page)+'-goods_id-DESC.html'
            if parse_one_total_page(get_one_page(url)) ==[]: #每次翻页检测是否到了最后一页
                running = False

            #get_one_page_all(page) #获取每个索引页数据
            page += 1
        lb.insert(tkinter.END,str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' 总页数为:' + str(page - 1) + '\n')
        #print('page total is : ' + str(page - 1))
        lb.insert(tkinter.END,'==================================================\n')
        lb.insert(tkinter.END,str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' 已经爬取的页数有：\n')

        for pg in range(1,page):
            get_one_page_all(pg)  # 获取每个索引页数据
        lb.insert(tkinter.END,'\n==================================================\n')
        #print('save...')
        lb.insert(tkinter.END, str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' 输出表格文件...\n')
        write_to_file() #存储数据到表格
        #print('save done')
        lb.insert(tkinter.END, str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' 表格文件输出完成！\n\n')
        time.sleep(2)
        opendir()
        window.destroy()

    #function：设置窗口屏幕居中
    #input：
    #return:
    def center_window(root, width, height):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        #print(size)
        root.geometry(size)


    #function：先检索“所有商品”页面，将每一页的商品的超链接获取到，之后根据每个商品的超链接获取每个商品页面源码，然后抓取数据
    #input：所有商品预览页，每页20个商品
    #return:
    def get_one_page_all(page):
        url = 'http://www.dfrobot.com.cn/category-216-b0-min0-max0-attr0-'+str(page)+'-goods_id-DESC.html'
        html = get_one_page(url) #获取索引网页数据
        lb.insert(tkinter.END,str(page)+',')

        #print('main running page '+str(page))
        for item in parse_one_index_page(html):
            #print(item)
            goodsUrl = 'http://www.dfrobot.com.cn/'+item
            goodsHtml = get_one_page(goodsUrl)  #获取单个商品网页源码
            for item2 in parse_one_goods_page(goodsHtml):
                #print(item2)
                new_total.append([item2['sku'],item2['mincheng'],item2['jiage']]) #将抽取到的商品信息加到列表里面去



    def btStart():
        lb.insert(tkinter.END,str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+' 启动爬取线程\n')
        #print('Parent process %s.' % os.getpid())
        p = threading.Thread(target=run_proc,args=(),name='thread-refresh')
        p.setDaemon(True) #与主线程同生死
        #print('Child process will start.')
        p.start()
        #print('Child process end.')
        lb.insert(tkinter.END, str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' 爬取线程已启动\n')

    window = tkinter.Tk()
    center_window(window, 500, 400)

    window.title('DF爬虫')
    window.geometry('500x400')

    btStart = tkinter.Button(window,text=' 开始爬取数据',width=15,height=2,command=btStart)
    btStart.pack()

    # 滚动文本框
    lb = scrolledtext.ScrolledText(window,wrap=tkinter.WORD)
    lb.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True)

    window.mainloop()


