# Douban_Books_Scrapy
## 项目简介
  利用Python3来爬取豆瓣某一分类图书下的所有内容（见下图），包括书名，作者，评分等信息，最后用Excel 存储这部分数据。
  
## 设计思路图
![PIC](https://github.com/KING221/Douban_Books_Scrapy/blob/master/豆瓣图书分类信息.png)


## 网页抓取
  urllib，伪装浏览器，time，while循环，try-except判断，if-else判断
 
 “互联网”分类图书的第一页地址不是 https://book.douban.com/tag/互联网?start=0&type=T ，而是 https://book.douban.com/tag/%E4%BA%92%E8%81%94%E7%BD%91?start=0&type=T 才对。
 
```
import urllib.request, urllib.parse

tag_list = '互联网'

def get_page(tag_list):

    url = 'https://book.douban.com/tag/' + urllib.parse.quote(tag_list) + '?start=' + str((page_num-1)*20) + '&type=T'

```

这一部分值得说的内容是，伪装浏览器：

```req = urllib.request.Request(url, headers=hds[page_num % len(hds)])```

首先用列表定义了一些headers，然后在request时，利用取余的得数来对headers进行随机选取；

还有就是时间间隔的设置，利用numpy里的random方法，从0~1之间随机取出一个随机数，再将随机数×5，得到一个随机时间间隔。

## 解析页面
  BeautifulSoup，try-except判断，append方法
  
  最后第三步，由于是创建表格，所以会用到openpyxl库。
  
  创建表格后，利用for循环和append方法，将书单信息输出到表格，保存后关闭即可。
  
  首先我们用美味汤处理先前的响应内容，得到了一个list_soup。
  
  list_soup会带有subject_list，也就是图书的信息列表。如果没有这个列表，则可以判定，本页没有内容，循环可以停止了（```if list_soup == None : break```）。
  
  随后用了```for book_info in list_soup.find_all('li', 'subject-item')``` 找出所有的```subject-item```。
  
  再对这个```subject-item```操作，由于信息太多，我在这里只列出一部分信息寻找方法：
  
  书名：``` title = book_info.select('ul > li > div.info > h2 > a')[0].text.strip().replace('\n\n\n    \n       ','')```
  
  用CSS选择器定位到标题位置。如果不加后面那段的话，得到的会是一个列表。
  
  我用了```[0].text``` 将列表处理成了字符串，```strip```处理掉空格。随后我观察到有的书名和副标题之间有```'\n\n\n    \n       '```这样的字符串，所以用```replace```去掉。
  
  对于一部分信息，有缺失的可能性，比如作者信息，所以要用```try-except```判断。至于提取作者信息则是：   
  
  ```author_info = book_info.select('ul > li > div.info > div.pub')[0].text.strip().split('/')[0]```
  
  前面部分类似书名操作，得到的信息是：
  
  吴军 / 电子工业出版社 / 2011-8 / 55.00元 
  
  所以我用斜杠进行分隔，取出第一个字符串，就是作者名。
  
  
  ```book_list.append([title, author_info, rating, people])```
  
  将这些内容用```append```方法存储到空列表里。


## 存储数据
openpyxl，for循环，append方法

## 结果展示
![PIC](https://github.com/KING221/Douban_Books_Scrapy/blob/master/微信截图_20190823132514.png)
