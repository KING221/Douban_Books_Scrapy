#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.request, urllib.parse
import time
import numpy as np
from bs4 import BeautifulSoup
import xlwt

def get_page(tag_list):
    page_num = 1
    try_times = 0
    book_list = []
    hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
       {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

    while(1):
        url = 'https://book.douban.com/tag/' + urllib.parse.quote(tag_list) + '?start=' + str((page_num-1)*20) + '&type=T'
        time.sleep(np.random.rand() * 3)
        try:
            req = urllib.request.Request(url, headers=hds[page_num % len(hds)])
            res = urllib.request.urlopen(req).read()
        except (urllib.request.HTTPError, urllib.request.URLError) as e:
            print(e)
            continue
        print('正在输出第 %d 页内容'%(page_num))

        soup = BeautifulSoup(res, 'lxml')
        list_soup = soup.find('div', id='subject_list')

        try_times += 1
        if try_times == 3 : break

        for book_info in list_soup.find_all('li', 'subject-item'):
            title = book_info.select('ul > li > div.info > h2 > a')[0].text.strip().replace('\n\n\n    \n       ','')
            try:
                author_info = book_info.select('ul > li > div.info > div.pub')[0].text.strip().split('/')[0]
            except:
                author_info = '作者/译者： 暂无'
            try:
                rating = book_info.select('ul > li > div.info > div.star.clearfix > span.rating_nums')[0].text.strip()
            except:
                rating = '暂无评分显示'
            try:
                people = book_info.select('ul > li > div.info > div.star.clearfix > span.pl')[0].text.strip()
            except:
                people = '低于10人评价'
            book_list.append([title, author_info, rating, people])
        page_num += 1
    return book_list

def print_excel(book_list, tag_list):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet =book.add_sheet('%s'%(tag_list),cell_overwrite_ok=True)
    count = 0
    for bl in book_list:
        sheet.write(count, 0, bl[0])
        sheet.write(count, 1, bl[1])
        sheet.write(count, 2, bl[2])
        sheet.write(count, 3, bl[3])
        count +=1
    book.save(r'D:\豆瓣书单.xls')

def main():
    tag_list = '互联网'
    book_list = get_page(tag_list)
    print_excel(book_list, tag_list)

if __name__ == '__main__':
    main()
