# coding: utf-8
import random
import sys
import urllib.request
import re

import chardet
import jieba

full_lines = []  # 结果的每一行
full_text = ""

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


def get_douluo_chapters(begin_page, end_page):
    global full_text
    for page in range(begin_page, end_page+1):
        html = get_html("http://www.tangsanshu.com/douluodalu/"+str(page)+".html")
        names = re.findall(
            '<div id="content" class="showtxt">((?:.|\n)+?)</div>'
            , html)
        # print(names)
        print("斗罗大陆", "(", str(page), ") : ", len(full_lines), " : ", len(names))
        if len(names) != 0:
            full_text += names[0]
    save_text_file("data/douluo_chapters.txt", full_text)


# =========================================================================
# 斗罗大陆 http://www.tangsanshu.com/douluodalu/2253.html

get_douluo_chapters(2253, 2253)
# get_douluo_chapters(2253, 2858)
