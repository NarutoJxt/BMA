# -*- coding=utf-8 -*-
import os
import time
import unicodedata
import urllib

import requests
from lxml.etree import  HTML
from urllib.request import urlretrieve

from spider import settings
from spider.postgresql import PostgreSql


class BookSpider:
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    img_path = "/home/lx/PycharmProjects/Myheart/spider/img/"
    def __init__(self,db):
        self.session = requests.Session()
        self.db = db
    def parse_category(self):
        """
        :summary 获取分类及地址
        :return:
        """
        main_url = "http://www.pdfbook.cn/"
        response = self.session.get(main_url,headers=self.headers)
        if response.status_code == 200:
            response = HTML(response.text)
            a_node = response.xpath("//div[@id='NavBlock']//ul//a")
            for a in a_node[0:1]:
                href = a.xpath("./@href")[0]
                category = a.xpath("./text()")[0]
                self.parse_book_by_category(category,href)
    def parse_book_by_category(self,category,url):
        response = self.session.get(url,headers=self.headers)
        if response.status_code == 200:
            response = HTML(response.text)
            lis = response.xpath("//ul[@class='image_box c']/li")
            for li in lis[0:1]:
                boor_url = li.xpath(".//a/@href")[0]
                book_title = li.xpath(".//a/@title")[0]
                book_img_url = li.xpath(".//a/img/@src")[0]
                filename = book_title +"."+ book_img_url.split(".")[-1]
                urlretrieve(book_img_url,filename)
    def parse_book_detail(self,book_url):
        response = self.session.get(book_url,headers=self.headers)
        if response.status_code == 200:
            response = HTML(response.text)
class BookSpiderNew:
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    img_path = "/home/lx/PycharmProjects/Myheart/spider/img/"
    def __init__(self,db):
        self.session = requests.Session()
        self.db = db
    def start_parse(self):
        for items in self.parse_book_base_info():
            for item in items:
                img_url, book_real_url = self.parse_book_detail(book_url=item["book_href"])
                img_path = self.save_book_cover_img(item["title"],img_url)
                book_id = self.save_book_base_info(item,img_path)
                sections = self.parse_book_section(book_real_url)
                self.save_book_section(sections,book_id)

    def parse_book_base_info(self):
        """
        :summary get some base information of all books
        :return:
        """
        base_url = "http://www.mingyuege.com"
        main_url = "http://www.mingyuege.com/modules/article/fulllistfree.php?page=17"
        response = self.session.get(main_url, headers=self.headers)
        response.encoding = "gbk"
        while True:
            if response.status_code == 200:
                response = HTML(response.text)
                trs = response.xpath("//table[@id='fomtb']//tr")[1:-1]
                items = []
                for tr in trs:
                    try:
                        category = tr.xpath(".//td[1]//span/text()")[0][1:-1]
                    except IndexError as e:
                        print(tr.xpath(".//td[1]//span/text()"))
                    title = tr.xpath(".//td[2]//span[@class='toplist_bookname']//text()")[0]
                    status = tr.xpath(".//td[3]//text()")[0]
                    author = tr.xpath(".//td[4]//text()")[0]
                    length = tr.xpath(".//td[5]//text()")[0]
                    book_href = tr.xpath(".//td[2]/span/a/@href")[0]
                    item = {
                        "category": category,
                        "title": title,
                        "status": status,
                        "author": author,
                        "length": length,
                        "book_href": book_href
                    }
                    items.append(item)
                yield items
            else:
                break
            next_path = response.xpath("//a[@class='next']/@href")
            if next_path:
                next_page_url = base_url + next_path[0]
                response = self.session.get(next_page_url, headers=self.headers)
                response.encoding = "gbk"
                time.sleep(1)
            else:
                break

    def get_category(self,category):
        sql = """
        select id from category
        where category = %s
        """
        res = self.db.pg_query_data(sql,params=[category])
        if res:
            return res[0]
        else:
            sql = """
            insert into category(category)
            values(%s)
            returning id
            """
            res = self.db.pg_insert_data(sql,params=[category])
        return res

    def check_book_existed_by_title(self,title):
        """
        :summary check current book whether is in the book table by title
        :param title: str the book's title
        :return: int if exists return an int more than 0 else return 0
        """
        sql = """
        select id from book
        where book_name = %s
        """
        res = self.db.pg_query_data(sql,params=[title])
        return res[0] if res else 0

    def save_book_cover_img(self,title,img_url):
        """
        :summary save book cover
        :param title: str the book's name
        :param img_url:  the url of  book's cover
        :return:
        """
        img_path = self.img_path + title + "." + img_url.split(".")[-1]
        if not os.path.exists(img_path):
            try:
                urlretrieve(img_url, img_path)
            except urllib.error.HTTPError as e:
                print("封面不存在")
                img_path = "/home/lx/PycharmProjects/Myheart/spider/img/base.jpg"
        return img_path

    def save_book_base_info(self,item,img_path):
        """
        :summary save book some base information
        :param item: dict book's base info
        :param img_path: str the file path book's cover is saved
        :return: book_id if success return an number more than 0 else return 0
        """
        title = item["title"]
        category = item["category"]
        author = item["author"]
        length = item["length"]
        status = item["status"]
        category_id = self.get_category(category)
        sql = """
                 insert into book(book_name,category_id,author,character_length,status,img_path)
                 values (%s,%s,%s,%s,%s,%s)
                 returning id
            """
        book_exists_res = self.check_book_existed_by_title(item['title'])
        book_id = 0
        if not book_exists_res:
            res = self.db.pg_insert_data(sql, params=[title, category_id, author, length, status, img_path])
            if res:
                print("%s 插入成功"%(title))
                book_id = res
            else:
                print("%s 插入失败"%(title))
        else:
            book_id = book_exists_res
        return book_id

    def parse_book_section(self,book_content_url):
        """
        :summary save book's all section
        :param book_content_url: str the book content page's url
        :return: items {
                    volume_name:[
                        {'section':'xxxx','content':''},
                    ]
                }
        """
        response = self.session.get(book_content_url,headers=self.headers)
        if response.status_code == 200:
            response.encoding = "gbk"
            response = HTML(response.text)
            volumes = response.xpath("//div[@class='dirbox']")[0]
            all_node = volumes.getchildren()[0].getchildren()
            current_volume = "第一卷"
            items = {}
            for node in all_node:
                if node.tag == "dt":
                    current_volume = node.xpath("./text()")[0]
                elif node.tag == "dd":
                    if not items.get(current_volume):
                        items[current_volume] = []
                    section = node.xpath(".//text()")[1]
                    section_url = node.xpath("./a/@href")[0]
                    content = self.parse_section_content(section_url)
                    item = {
                        "section":section,
                        "content":content
                    }
                    items[current_volume].append(item)
            return items
    def check_volumn_exists(self,volume,section,book_id):
        """
        :summary check the book's volume whether is in database
        :param volume: str the book's volume
        :param section: str the section of book's volume
        :param book_id: int book's id
        :return: int id of the book's section
        """
        sql = """
            select id from book_detail
            where book_id = %s and volume = %s and section = %s
        """
        res = self.db.pg_query_data(sql,[book_id,volume,section])
        return res

    def save_book_section(self,items,book_id):
        """
        :summary save the book's all section
        :param items: dict all section's info
        :param book_id: int the book's id in database
        :return:
        """
        sql = """
            insert into book_detail(book_id,volume,section,content)
            values (%s,%s,%s,%s)
        """

        for key in items.keys():
            sections = items[key]
            for section in sections:
                content = section["content"]
                section_name = section["section"]
                res = self.check_volumn_exists(key,section_name,book_id)
                if not res:
                    res = self.db.pg_insert_data(sql, [book_id, key, section_name, content])
                    if res:
                        print("%s:%s-%s 已保存到数据库中"%(book_id,key,section_name))
                    else:
                        print("%s:%s-%s 未保存"%(book_id,key,section_name))
                else:
                    print("%s:%s-%s 已存在" % (book_id, key, section_name))

    def parse_section_content(self,section_url):

        section_url_prefix = "http://www.mingyuege.com/modules/article/"
        section_full_url = section_url_prefix + section_url
        response = self.session.get(section_full_url,headers=self.headers)
        response.encoding = "gbk"
        if response.status_code == 200:
            response = HTML(response.text)
            content = response.xpath("//td[@id='table_container']//text()")
            for index in range(len(content)):
                content[index] = unicodedata.normalize('NFKC', content[index])
            return content

    def parse_book_detail(self,book_url):
        response = self.session.get(book_url,headers=self.headers)
        response.encoding = "utf-8"
        if response.status_code == 200:
            response = HTML(response.text)
            img_url = response.xpath("//div[@class='look_left']/a/img/@src")[0]
            book_real_url = response.xpath("//li[@class='y4_1']/a/@href")[0]
            return img_url,book_real_url
db = PostgreSql(settings.DATABASE)
b = BookSpiderNew(db)
b.start_parse()