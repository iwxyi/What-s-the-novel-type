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


# 提取创世每一个类型的书名数组 http://chuangshi.qq.com/bang/fav/xh-zong.html
def add_chuangshi_novel_type(type_page, type_id, type_name):
    global full_lines
    html = get_html("http://chuangshi.qq.com/bang/fav/" + type_page + ".html")
    if html.find('无法访问') > 0:
        html = get_html("http://chuangshi.qq.com/bang/fav/" + type_page + ".html")
        if html.find('无法访问') > 0:
            html = get_html("http://chuangshi.qq.com/bang/fav/" + type_page + ".html")
            if html.find('无法访问') > 0:
                html = get_html("http://chuangshi.qq.com/bang/fav/" + type_page + ".html")

    names = re.findall(
        "<a target='_blank' href='http://chuangshi.qq.com/bk/" + type_id + "/\\d+.html'>(.+?)</a>"
        , html)
    # print("http://chuangshi.qq.com/bang/fav/" + type_id + "-zong.html")
    # print(html)
    print(type_name, " : ", len(full_lines), " : ", names)
    for name in names:
        full_lines += ["__label__" + type_name + " " + " ".join(jieba.cut(name))]


# 提取晋江每一个类型的书名数组 http://chuangshi.qq.com/bang/fav/xh-zong.html
def add_jinjiang_novel_type(type_name):
    global full_lines
    html = open("data/jinjiang_source.txt", "r", encoding='utf-8').read()
    names = re.findall(
        '<td height="23">&nbsp;<a href="oneauthor.php\\?authorid=\\d+">(.+)</a></td>'
        , html)
    print(type_name, " : ", len(full_lines), " : ", names)
    for name in names:
        full_lines += ["__label__" + type_name + " " + " ".join(jieba.cut(name))]


# 提取笔趣阁每一个类型的书名数组
def add_biquge_novel_type(type_id, last_page, type_name):
    global full_lines
    for page in range(1, last_page + 1):  # 遍历每一页
        html = get_html("http://www.xbiquge.la/fenlei/" + str(type_id) + "_" + str(page) + ".html")
        names = re.findall(
            '<li><span class="s2">《<a href="http://www.xbiquge.la/\\d+/\\d+/" target="_blank">(.+)</a>》'
            , html)
        print(type_name, "(", str(page), "/", str(last_page), ") : ", len(full_lines), " : ", names)
        # save_text_file("data/biquge_source"+str(page)+".txt", html)
        for name in names:
            full_lines += ["__label__" + type_name + " " + " ".join(jieba.cut(name))]


# =========================================================================
# 起点 https://www.qidian.com/rank/collect?chn=4&page=3

add_qidian_novel_type("21", "玄幻")
add_qidian_novel_type("1", "玄幻")  # 奇幻
add_qidian_novel_type("2", "武侠")
add_qidian_novel_type("22", "修真")  # 仙侠
add_qidian_novel_type("4", "都市")  # 言情？
add_qidian_novel_type("15", "现实")
add_qidian_novel_type("6", "军事")
add_qidian_novel_type("5", "历史")
add_qidian_novel_type("7", "游戏")
add_qidian_novel_type("8", "体育")
add_qidian_novel_type("9", "科幻")
add_qidian_novel_type("10", "灵异")
add_qidian_novel_type("12", "二次元")

random.shuffle(full_lines)  # 随机打乱顺序
fulltext = "\n".join(full_lines)  # 组成字符串
save_text_file('data/qidian_names.txt', fulltext)  # 保存到文件

# =====================================================================
# 创世 http://chuangshi.qq.com/bang/fav/xh-zong.html

full_lines = []

add_chuangshi_novel_type("xh-zong", "xh", "玄幻")
add_chuangshi_novel_type("qh-zong", "qh", "玄幻")  # 奇幻
add_chuangshi_novel_type("wx-zong", "wx", "武侠")
add_chuangshi_novel_type("xx-zong", "xx", "修真")  # 仙侠
add_chuangshi_novel_type("ds-zong", "ds", "都市")
add_chuangshi_novel_type("yq-zong", "qc", "现实")  # 言情？
add_chuangshi_novel_type("js-zong", "js", "军事")
add_chuangshi_novel_type("ls-zong", "ls", "历史")
add_chuangshi_novel_type("wy-zong", "yx", "游戏")
add_chuangshi_novel_type("ty-zong", "ty", "体育")
add_chuangshi_novel_type("kh-zong", "kh", "科幻")
add_chuangshi_novel_type("ly-zong", "ly", "灵异")
add_chuangshi_novel_type("2cy-zong", "2cy", "二次元")

random.shuffle(full_lines)  # 随机打乱顺序
fulltext = "\n".join(full_lines)  # 组成字符串
save_text_file('data/chuangshi_names.txt', fulltext)  # 保存到文件

# =======================================================================
# 晋江

full_lines = []

add_jinjiang_novel_type("言情")

random.shuffle(full_lines)  # 随机打乱顺序
fulltext = "\n".join(full_lines)  # 组成字符串
save_text_file('data/jinjiang_names.txt', fulltext)  # 保存到文件

# ========================================================================
# 笔趣阁 http://www.xbiquge.la/fenlei/1_2.html

full_lines = []

add_biquge_novel_type(1, 331, "玄幻")
add_biquge_novel_type(2, 101, "修真")
add_biquge_novel_type(3, 305, "都市")
add_biquge_novel_type(4, 86, "穿越")
add_biquge_novel_type(5, 74, "游戏")
add_biquge_novel_type(6, 132, "科幻")

random.shuffle(full_lines)  # 随机打乱顺序
fulltext = "\n".join(full_lines)  # 组成字符串
save_text_file('data/biquge_names.txt', fulltext)  # 保存到文件
