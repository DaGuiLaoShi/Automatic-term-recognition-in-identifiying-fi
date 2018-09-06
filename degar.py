
import urllib.request
from bs4 import BeautifulSoup as bs




#得到网页源代码
#参数：网址
#返回：网页源代码
def GetHtmlCode(url):
    # 解析网页
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print("error2: 网络连接超时",e)
        return None
    if response.getcode() != 200:
        print("error1: 打开网页失败，请检查您的网络！")
        return None

    content_html = response.read()
    # print(content_html.decode('utf8'))  # 解码
    return content_html

def Get10KUrl(url):
    content_html = GetHtmlCode(url)
    soup = bs(content_html, 'html.parser', from_encoding='utf-8')
    tables=soup.find("table",class_="tableFile")
    trs=tables.find_all("tr")
    url = trs[1].find("a")["href"]
    return url
    #print(url)


#第二种通过目录找Risk开头
def GetRiskTextTwo(url,name):
    #print(url)
    content_html = GetHtmlCode(url)
    soup = bs(content_html, 'html.parser', from_encoding='utf-8')
    divs = soup.find_all("div")
    flag = 0
    endStr = "-1"
    for div in divs:
        n = len(div.get_text())
        temp_s = div.get_text()

        if flag == 1 and endStr=="-1":
            if n<5:
                continue
            a = div.find("a")
            if a is not None:
                endStr = temp_s
                #print(endStr)
                continue
        if flag == 2 :
           # print(endStr)
            if endStr =="-1":
                return
            temp_s = temp_s.replace(' ', ' ')
            temp_s = temp_s.replace('   ', ' ')
            temp_s = temp_s.replace('•', ' ')
            # print(temp_s)

            if n < 100 and n > 3:
                if endStr.lower() in temp_s.lower():
                    global count
                    count += 1
                    print(count)
                    return True
            # xieruwenjian
            # Table of Contents
            if (temp_s.startswith("Table") or n < 3):
                continue

            f = open(name, 'a',encoding="utf-8")
            # print(name)
            f.write(temp_s)
            f.write("\n")
            continue

        if n < 100 and n > 8:
            if  "risk" in temp_s.lower() and "factors" in temp_s.lower():
                # print(temp_s)
                flag += 1
    return False

#第一种方法通过Itam 1A找
def GetRiskText(url,name):
    print(url)
    content_html = GetHtmlCode(url)

    soup = bs(content_html, 'html.parser', from_encoding='utf-8')
    divs = soup.find_all("div")
    flag = 0
    for div in divs:
        n = len(div.get_text())
        temp_s = div.get_text()
        if flag == 2:
            temp_s = temp_s.replace(' ', ' ')
            temp_s = temp_s.replace('   ', ' ')
            temp_s = temp_s.replace('•', ' ')
            #print(temp_s)

            if n < 100 and n > 3:
                if "item" in temp_s.lower():
                    global count
                    count +=1
                    print(count)
                    return True
            # xieruwenjian
            #Table of Contents
            if(temp_s.startswith("Table") or n<3):
                continue

            f= open(name, 'a',encoding="utf-8")
            #print(name)
            f.write(temp_s)
            f.write("\n")
            continue

        if n < 100 and n>8:
            if  "risk" in temp_s.lower() and "factors" in temp_s.lower():
                #print(temp_s)
                flag += 1
    return False
import csv
import time
if __name__ == '__main__':

    filePath = "I:\risk factor\test.csv"
    name=""
    headurl = "https://www.sec.gov"
    count=0
    with open(filePath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for enme,line in enumerate(reader):
            if enme<300:
                continue
            try:
                time.sleep(1)
                name=line[2]+"_"+line[0]+"_"+line[3]+".txt"
                name.replace("/","-")
                url=line[4]
                url=headurl+Get10KUrl(url)
                #url = "https://www.sec.gov/Archives/edgar/data/4904/000101540205001007/aep10k04.htm"
                if GetRiskText(url,name) == False:
                    GetRiskTextTwo(url,name)

            except Exception as e:
                print("error:",e)



