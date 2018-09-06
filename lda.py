from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from nltk import pos_tag
from gensim import corpora, models
import gensim
import os
#分词
tokenizer = RegexpTokenizer(r'\w+')
#设置停用词
en_stop = get_stop_words('en')
#设置特定停用词
stop_words = open("stop_words.txt")
stop_words = stop_words.read().split('\n')
print(stop_words)
#词干提取


#读入文档，预处理后存为一个列表
dir_path = "risk factor/"
files = os.listdir(dir_path)
file_lists = []
count = 1
for f in files:
    print("第 ",count," 个——")
    count += 1
    f = dir_path+f
    file = open(f,'r',encoding="utf8")
    file_content = file.read()
    file_content = file_content.lower()
    #得到单词列表
    word_list = tokenizer.tokenize(file_content)
    #停用词
    stop_word_list = [i for i in word_list if not i in en_stop]
    #词干提取
   
    #只保留名词
    tags = pos_tag(word_list)
    result_list = []
    for tag in tags:
            if tag[0] in stop_words:
                continue
            result_list.append(tag[0])
    # print(result_list)
    file_lists.append(result_list)
print(len(file_lists))
#统计词频
dictionary = corpora.Dictionary(file_lists)
corpus = [dictionary.doc2bow(text) for text in file_lists]
print(corpus[0])
#LDA模型
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=30,id2word = dictionary)
result = ldamodel.print_topics(num_topics=30,num_words=25) #num_words=10
print(result)
#保存结果到文件
f = open("result.txt","w")
f.write(str(result))
f.close()
