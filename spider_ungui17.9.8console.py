#网络爬虫程序，爬取DF中文商城（http://www.dfrobot.com.cn/index.php）所有产品的sku名称与价格数据
import requests
from requests.exceptions import RequestException
import re
import pandas

#function：获取一个网页的html源码
#input：输入网页url链接
#return: 返回html源码
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200: #返回200即为获取数据正确
            #print("get ok")
            return  response.text
        print(response.status_code)
        return None
    except RequestException:
        print("get err")
        return None

#function：搜索下一页对应的页码
#input：输入网页html源码
#return: 返回搜索结果
def parse_one_total_page(html):
    pattern = re.compile('<a class="next" href=\'category-216-b0-min0-max0-attr0-(.*?)-goods_id-DESC.html\'>下一页</a>',re.S)
    items = re.findall(pattern,html)
    return items

#function：搜索所有商品界面的所有商品超链接
#input：输入网页html源码
#return: 返回搜索结果
def parse_one_index_page(html):
    pattern = re.compile('<div class="goodsItemh productBlock".*?href="(.*?)".*?</div>',re.S)
    items = re.findall(pattern,html)
    return items

#function：搜索商品页面信息，sku，名称，价格，可以在增加
#input：输入网页html源码
#return: 返回搜索结果，字典形式
def parse_one_goods_page(htmlGoods):
    patternGoods = re.compile('<div class="goodsTitle">\n\t\t\t\t\t\t(.*?)\t.*?<font class="brief">.*?<div class="goodsMes" data-stock=".*?" data-price="(.*?)" data-promote=".*?" data-vip=".*?">.*?<div class="name">货号</div>.*?<div class="content2">(.*?)</div>',re.S)
    itemsGoods = re.findall(patternGoods,htmlGoods)
    for item in itemsGoods:
        yield {
            'mincheng':item[0],
            'jiage':item[1],
            'sku':item[2]
        }
    return itemsGoods

new_total=[]  #全局列表变量，存储所有收到的数据以便存储到表格中

#function：将存储所有数据的列表存储到表格中
#input：
#return:
def write_to_file():
    df = pandas.DataFrame(new_total)
    #print(df)
    df.columns = ['SKU', '名称', '价格'] #设定行名称
    df.to_excel('result.xlsx') #存储为excel文件

#function：先检索“所有商品”页面，将每一页的商品的超链接获取到，之后根据每个商品的超链接获取每个商品页面源码，然后抓取数据
#input：所有商品预览页，每页20个商品
#return:
def main(page):
    url = 'http://www.dfrobot.com.cn/category-216-b0-min0-max0-attr0-'+str(page)+'-goods_id-DESC.html'
    html = get_one_page(url) #获取索引网页数据
    print('main running page '+str(page))
    for item in parse_one_index_page(html):
        #print(item)
        goodsUrl = 'http://www.dfrobot.com.cn/'+item
        goodsHtml = get_one_page(goodsUrl)  #获取单个商品网页源码
        for item2 in parse_one_goods_page(goodsHtml):
            #print(item2)
            new_total.append([item2['sku'],item2['mincheng'],item2['jiage']]) #将抽取到的商品信息加到列表里面去

if __name__ == '__main__':
    running = True
    page = 1
    print('calculation page total...')
    while running:
        url = 'http://www.dfrobot.com.cn/category-216-b0-min0-max0-attr0-'+str(page)+'-goods_id-DESC.html'
        if parse_one_total_page(get_one_page(url)) ==[]: #每次翻页检测是否到了最后一页
            running = False
        main(page) #获取每个索引页数据
        page += 1
    print('page total is : '+str(page-1))
    print('save...')
    write_to_file() #存储数据到表格
    print('save done')



