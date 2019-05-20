# coding: utf-8
import random
import sys
import urllib.request
import re

import chardet
import jieba

full_lines = []  # 结果的每一行


# 获取网页源码
def get_html(url):
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(req)
    return html.read().decode('utf-8', 'ignore')


# 保存到文本文件
def save_text_file(file_name, contents):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(contents)


# 提取起点每一个类型的书名数组
def add_qidian_novel_type(type_id, type_name):
    global full_lines
    for page in range(1, 25):  # 遍历每一页
        html = get_html("https://www.qidian.com/rank/collect?chn=" + type_id + "&page=" + str(page))
        names = re.findall(
            '<h4><a href="//book.qidian.com/info/\\d+" target="_blank" data-eid="qd_C40" data-bid="\\d+">(.+?)</a></h4>'
            , html)
        print(type_name, "(", str(page), ") : ", len(full_lines), " : ", names)
        for name in names:
            full_lines += ["__label__" + type_name + " " + " ".join(jieba.cut(name))]


def get_douluo_chapters(begin_page, end_page):
    for page in range(begin_page, end_page+1):
        html = get_html("http://www.tangsanshu.com/douluodalu/"+str(page)+".html")


# =========================================================================
# 斗罗大陆 http://www.tangsanshu.com/douluodalu/2253.html

get_douluo_chapters(2253, 2858)

random.shuffle(full_lines)  # 随机打乱顺序
fulltext = "\n".join(full_lines)  # 组成字符串
save_text_file('data/biquge_names.txt', fulltext)  # 保存到文件
