import fastText
import jieba


# 判断小说类型的调用语句
def judge(novel):
    print(novel, " : ", classifier.predict(" ".join(jieba.cut(novel))))


# 保存到文本文件
def save_text_file(file_name, contents):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(contents)


# 判断哪些素材要进行训练
sources = ['biquge', 'qidian', 'chuangshi', 'jinjiang']
fulltext = ""
for source in sources:
    fulltext += open("data/"+source+"_names.txt", encoding='utf-8').read() + "\n"
save_text_file("data/novel_names.txt", fulltext)


classifier = fastText.train_supervised("data/novel_names.txt", lr=0.1, wordNgrams=1, loss="hs")
model = classifier.save_model("data/novel_names.model")
# classifier = fastText.load_model("data/novel_names.model")


judge("机械囚宠：元帅亲点爱")
judge("指掌浩瀚")
judge("医世倾城")
judge("夏蝉冬雪")
