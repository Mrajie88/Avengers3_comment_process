# -*-coding:utf-8-*-

###����txt�ļ��Ĵ���

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba

text = open("fulian3.txt", "rb").read()
# ��ͷִ�
wordlist = jieba.cut(text, cut_all=True)
wl = " ".join(wordlist)
# print(wl)#����ִ�֮���txt


# �ѷִʺ��txtд���ı��ļ�
# fenciTxt  = open("fenciHou.txt","w+")
# fenciTxt.writelines(wl)
# fenciTxt.close()


# ���ô���
wc = WordCloud(background_color="black",  # ���ñ�����ɫ
               # mask = "ͼƬ",  #���ñ���ͼƬ
               max_words=2000,  # ���������ʾ������
               # stopwords = "", #����ͣ�ô�
               font_path="fangsong_GB2312.ttf",
               # �����������壬ʹ�ô��ƿ�����ʾ������Ĭ�������ǡ�DroidSansMono.ttf����⡱����֧�����ģ�
               max_font_size=50,  # �����������ֵ
               random_state=30,  # �����ж������������״̬�����ж�������ɫ����
               )
myword = wc.generate(wl)  # ���ɴ���

# չʾ����ͼ
plt.imshow(myword)
plt.axis("off")
plt.show()