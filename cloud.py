from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

#读取结果，得到单词项
f = open("result.txt",'r')
term_list = eval(f.read())
print(term_list)
texts_all = []
texts_list = []
count = 1
for term in term_list:
    term = re.findall(r'"\w+"', term[1])
    term = [w.replace("\"", "") for w in term]

    term_str = ' '.join(term)
    print(term_str)
    wordcloud = WordCloud().generate(term_str)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    img_path = "img/topic_"+str(count)+".png"
    count += 1
    plt.savefig(img_path)
    plt.axis("off")

    texts_list.append(term)
    texts_all.extend(term)
    # print(term)
texts_str = ' '.join(texts_all)
print(texts_str)

#画出所有的词云图片
wordcloud = WordCloud().generate(texts_str)
plt.figure()
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.savefig("img/topic_all.png")
plt.axis("off")
plt.show()

