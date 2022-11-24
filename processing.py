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
  #data = pd.read_csv("IrC1TqAxz.csv")
  data = pd.read_csv(path)
  # 获取评论的指定列
  col = data["评论内容"]
  data1 = np.array(col)
  print("以下为获取的评论内容：\n",data1)
  return data1
##########################################################
##########################################################
'''
数据预处理：不分词，保留句子的处理
'''
def pro_sentence(data1):
# 删除回复到冒号之间的中文
  zh_puncts1 = "[，；、。！？（）《》【】]"
  data_bujb=[]
  for x in data1:
    x = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)", "", x)
    # x = re.sub(r"？+","",x)
    # x = re.sub(r"，+","",x)
    # x = re.sub(r"。+","",x)
    data_bujb += x
    print(x)
    x = re.sub(zh_puncts1,"",x)
    #data_bujb += x
    #print(x)
  print(data_bujb)
  return data_bujb

'''
数据预处理，结巴分词
'''
def jieba_word(data1):
  # 一些中文字符
  zh_puncts1 = "[，；、。！？（）《》【】]"
  data2 = []
  for x in data1:
    x = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)", "", x)
    x = re.sub(zh_puncts1,"",x)
    x = re.sub(" ","",x)
    x = jieba.lcut(x)
    print(x)
    data2 += x
  print("以下为jieba分词结果：\n",data2)
  return data2

def use_stopwords(data2):
  with open('cn_stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = [w.strip() for w in f.readlines()]
  data3 = [w for w in data2 if w not in stopwords]
  print(len(data2))
  print(len(data3))
  print(data3)
  return data3


'''
一些有效可视化输出：
0. 统计词频
1. 词云
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# import matplotlib.font_manager as fm
'''
def count_wf(data3):
  word_count = dict(sorted(Counter(data3).items(), key=lambda x: x[1], reverse=True))
  print(word_count)
  return word_count

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
  plt.show()

## 漂亮的pycharm
def vs_wordcloud_bf(data3):
  word_count = count_wf(data3)
  # image_mask = np.array(Image.open('usa.png'))
  image_mask = np.array(Image.open('img/daishu.png'))
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
  plt.show()

#################################################################
#################################################################
'''
情感分析 
'''
def emotion_analyse(data1):
  from snownlp import SnowNLP

  # 情感分析 小句子试错
  text1 = '这是我遇见的最棒的一家店，种类多，价格低，更喜欢的是服务质量很好'
  text2 = '这是我遇到的最差的一家店，种类少，价格贵，更气人的是服务质量很差'
  s1 = SnowNLP(text1)
  s2 = SnowNLP(text2)
  # 越接近1.情感上越积极
  print(s1.sentiments)
  print(s2.sentiments)

  # 对data1
  for x in data1:
    s = SnowNLP(x)
    print(x, "------这一句的情感分析结果为-----", s.sentiments)

###################################################################
##################################################################
'''
主函数，统揽全局
'''
if __name__ == '__main__':
   #path =  input('请输入文件：')
   path = 'data_initial/IrC1TqAxz.csv'
   # 读取文本
   data1 = read_csv(path)
   # jieba 分词结果
   data2 = jieba_word(data1)
   # 不分词的简单处理句子
   data_bujb = pro_sentence(data1)
   # 使用停词集
   data3 = use_stopwords(data2)
   #制作词云（内含 调用统计词频的函数）
   #data_test = "什么叫格局，这个就是格局，这个词云再不正确输出，我就要骂人了"
   vs_wordcloud(data3)
   vs_wordcloud_bf(data3)

   # 情感分析 词性标注
   emotion_analyse(data1)