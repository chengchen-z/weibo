import csv

import pandas as pd
#import networkx as nx
import jieba
import jieba.analyse
import numpy as np
import re
from snownlp import SnowNLP

# 词云
import matplotlib as mpl
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.font_manager as fm

from collections import Counter

from PIL import Image
import numpy as np

'''
 读取文本函数
'''
def read_csv(path):
  # data = pd.read_csv("rmrb_text.csv")
  data = pd.read_csv(path,encoding='gbk')
  # 获取评论的指定列
  col = data["微博正文"]
  data1 = np.array(col)
  #print("以下为获取的文本内容：\n",data1)
  return data1

'''
数据预处理：不分词，保留句子的处理
'''
def pro_sentence(data1):
    data_bujb = []
    for text in data1:
        zh_puncts1 = "，；、。！？（）《》【】"
        URL_REGEX = re.compile(
            r'(?i)((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>' + zh_puncts1 + ']+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’' + zh_puncts1 + ']))',
            re.IGNORECASE)
        text = re.sub(URL_REGEX, "", text)

        EMAIL_REGEX = re.compile(r"[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}", re.IGNORECASE)
        text = re.sub(EMAIL_REGEX, "", text)
        text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)", " ", text)
        lb, rb = 1, 6
        text = re.sub(r"\[\S{" + str(lb) + r"," + str(rb) + r"}?\]", "", text)
        emoji_pattern = re.compile(
            "["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"u"\U0001F1E0-\U0001F1FF"u"\U00002702-\U000027B0" "]+",
            flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        text = re.sub(r"#\S+#", "", text)
        text = text.replace("\n", " ")

        text = re.sub(r"(\s)+", r"\1", text)
        stop_terms = ['展开', '全文', '展开全文', '一个', '网页', '链接', '?【', 'ue627', 'c【', '10', '一下', '一直', 'u3000', '24', '12',
                      '30', '?我', '15', '11', '17', '?\\', '显示地图', '原图']
        for x in stop_terms:
            text = text.replace(x, "")
        allpuncs = re.compile(
            r"[，↓\_《。》、？；：‘’＂“”【「】」·！@￥…（）—\,\<\.\>\/\?\;\:\'\"\[\]\{\}\~\`\!\@\#\$\%\^\&\*\(\)\-\=\+]")
        text = re.sub(allpuncs, "", text)
        # print(text)
        print(text, type(text))
        data_bujb += text
    # print(data_bujb)
    return data_bujb

'''
数据预处理，结巴分词
'''
def jieba_word(data1):
    data2 = []
    for text in data1:
        zh_puncts1 = "，；、。！？（）《》【】"
        URL_REGEX = re.compile(
            r'(?i)((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>' + zh_puncts1 + ']+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’' + zh_puncts1 + ']))',
            re.IGNORECASE)
        text = re.sub(URL_REGEX, "", text)

        EMAIL_REGEX = re.compile(r"[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}", re.IGNORECASE)
        text = re.sub(EMAIL_REGEX, "", text)
        text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)", " ", text)
        lb, rb = 1, 6
        text = re.sub(r"\[\S{" + str(lb) + r"," + str(rb) + r"}?\]", "", text)
        emoji_pattern = re.compile(
            "["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"u"\U0001F1E0-\U0001F1FF"u"\U00002702-\U000027B0" "]+",
            flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        text = re.sub(r"#\S+#", "", text)
        text = text.replace("\n", " ")

        text = re.sub(r"(\s)+", r"\1", text)
        stop_terms = ['展开', '全文', '展开全文', '一个', '网页', '链接', '?【', 'ue627', 'c【', '10', '一下', '一直', 'u3000', '24', '12',
                      '30', '?我', '15', '11', '17', '?\\', '显示地图', '原图']
        for x in stop_terms:
            text = text.replace(x, "")
        allpuncs = re.compile(
            r"[，↓\_《。》、？；：‘’＂“”【「】」·！@￥…（）—\,\<\.\>\/\?\;\:\'\"\[\]\{\}\~\`\!\@\#\$\%\^\&\*\(\)\-\=\+]")
        text = re.sub(allpuncs, "", text)
        # print(text)
        # 分词
        text = jieba.lcut(text)
        # print(text, type(text))
        data2 += text

    print(data2)
    return data2
'''
使用停词集
'''
def use_stopwords(data2):
  with open('cn_stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = [w.strip() for w in f.readlines()]
  data3 = [w for w in data2 if w not in stopwords]
  print(len(data2))
  print(len(data3))
  print(data3)
  return data3
'''计算词个数'''
def count_wf(data3):
  word_count = dict(sorted(Counter(data3).items(), key=lambda x: x[1], reverse=True))
  print(word_count)
  return word_count
'''输出普通词云结果'''
def vs_wordcloud(data3):
  word_count = count_wf(data3)
  #zhfont = fm.FontProperties(fname='/usr/share/fonts/truetype/liberation/simhei.ttf')
  plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
  wc = WordCloud(background_color='white',
                 #font_path='/usr/share/fonts/truetype/liberation/simhei.ttf',
                 font_path='simhei.ttf',
                 # 电脑中用系统的路径：font_path='/System/Library/Fonts/STHeiti Medium.ttc',
                 random_state=10,
                 max_font_size=None,
                 stopwords=['包括']  ## stopwords not work when wc.genreate_from_frequencies
                 )
  wc.generate_from_frequencies(frequencies=word_count)
  #wc.generate(word_count)
  plt.figure(figsize=(15, 15))
  plt.imshow(wc)
  plt.axis("off")
  plt.savefig('static/assets/img/cloudImg/wc_BJO.png')
  plt.show()


'''漂亮的词云'''
def vs_wordcloud_bf(data3):
  word_count = count_wf(data3)
  # image_mask = np.array(Image.open('usa.png'))
  image_mask = np.array(Image.open('static/assets/img/tree.jpg'))
  zhfont = fm.FontProperties(fname='/usr/share/fonts/truetype/liberation/simhei.ttf')
  plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
  wc = WordCloud(background_color='white',
                 font_path='/usr/share/fonts/truetype/liberation/simhei.ttf',
                 # 电脑中用系统的路径：font_path='/System/Library/Fonts/STHeiti Medium.ttc',
                 random_state=10,
                 max_font_size=None,
                 stopwords=['包括'],  ## stopwords not work when wc.genreate_from_frequencies
                 mask=image_mask
                 )
  wc.generate_from_frequencies(frequencies=word_count)
  plt.figure(figsize=(15, 15))
  plt.imshow(wc)
  plt.axis("off")
  plt.savefig('static/assets/img/cloudImg/wc_bf_BJO.png')
  plt.show()

def hot_wordcloud():
    # path = input('请输入文件名：')
    path = 'data_initial/beijingO.csv'
    # 读取文本
    data1 = read_csv(path)
    # 不分词的简单处理句子
    data_bujb = pro_sentence(data1)
    # jieba 分词结果
    data2 = jieba_word(data1)

    # 使用停词集
    data3 = use_stopwords(data2)
    # 制作词云（内含 调用统计词频的函数）
    # data_test = "什么叫格局，这个就是格局，这个词云再不正确输出，我就要骂人了"
    vs_wordcloud(data3)
    vs_wordcloud_bf(data3)

'''
对于每条微博文本的情感分析计算
'''
def pro_one(data_one):
  text = data_one
  zh_puncts1 = "，；、。！？（）《》【】"
  URL_REGEX = re.compile(
      r'(?i)((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>' + zh_puncts1 + ']+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’' + zh_puncts1 + ']))',
      re.IGNORECASE)
  text = re.sub(URL_REGEX, "", text)

  EMAIL_REGEX = re.compile(r"[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}", re.IGNORECASE)
  text = re.sub(EMAIL_REGEX, "", text)
  text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)", " ", text)
  lb, rb = 1, 6
  text = re.sub(r"\[\S{" + str(lb) + r"," + str(rb) + r"}?\]", "", text)
  emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"u"\U0001F1E0-\U0001F1FF"u"\U00002702-\U000027B0" "]+", flags=re.UNICODE)
  text = emoji_pattern.sub(r'', text)
  text = re.sub(r"#\S+#", "", text)
  text = text.replace("\n", " ")

  text = re.sub(r"(\s)+", r"\1", text)
  stop_terms = ['展开', '全文', '展开全文', '一个', '网页', '链接', '?【', 'ue627', 'c【', '10', '一下', '一直', 'u3000', '24', '12', '30', '?我', '15', '11', '17', '?\\', '显示地图', '原图']
  for x in stop_terms:
      text = text.replace(x, "")
  allpuncs = re.compile(
      r"[，↓\_《。》、？；：‘’＂“”【「】」·！@￥…（）—\,\<\.\>\/\?\;\:\'\"\[\]\{\}\~\`\!\@\#\$\%\^\&\*\(\)\-\=\+]")
  text = re.sub(allpuncs, "", text)
  text = re.sub(r" ", "",text)
  #print(text)
  #print(text,type(text))
  data_bujb = ''.join(text)
  #print(data_bujb)
  #print(type(data_bujb))
  return data_bujb
def getOneEmotion(data1):
    sense = []
    for i in range(0, 19):
        # print(data1[i])
        data_bujb = pro_one(data1[i])
        # print(data_bujb)
        s = SnowNLP(str(data_bujb))
        sense.append(s.sentiments)
        # print(data1[i],"——这句话的情感分析结果为——",sense[i])
        print(sense[i])
        print(i)
    return sense
'''list 写入到csv '''
def listTcsv(sense):
    # with open('emotion_BJO.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     for row in sense:
    #         writer.writerow(row)
    final = pd.DataFrame(sense)
    final.to_csv('emotion_BJO.csv', index=False)

def hot_emotion():
    # path = input('请输入文件名：')
    path = 'data_initial/beijingO.csv'
    # 读取文本
    data1 = read_csv(path)
    sense = getOneEmotion(data1)
    listTcsv(sense)




if __name__ == '__main__':
    ''' 输出每一个热点的可视化图形'''
    # hot_wordcloud()
    ''' 输出每个话题的情感分析结果'''
    hot_emotion()