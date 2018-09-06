import nltk
import nltk.data
import csv
import os

def splitSentence(paragraph):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(paragraph)
    return sentences

def AlterLine(result):
    for i,res in enumerate(result):
        result[i] = result[i].replace("\n"," ")
        result[i] = result[i].replace("  ", " ")
    return result
if __name__ == '__main__':
    open_folder_path = "D:\Python\SplitSentence\dataset"
    list = os.listdir(open_folder_path)
    with open("./result.csv", "a",newline='', encoding='gb2312', errors='ignore') as fw:
        writer = csv.writer(fw)
        for i in range(0, len(list)):
            single_file_path = os.path.join(open_folder_path, list[i])
            file_object = open(single_file_path,encoding='gb2312', errors='ignore')
            try:
                file_context = file_object.read()
                result = splitSentence(file_context)
                result = AlterLine(result)
                title = list[i].split('_')
                result.insert(0,list[i])
                result.insert(1,title[0])
                result.insert(2,title[2].split('.')[0])
                result.insert(3,title[1])
                result.insert(4,'FINANCE SERVICES [6199]')
                writer.writerow(result)
                print(result)
            finally:
                file_object.close()
    #nltk.download()