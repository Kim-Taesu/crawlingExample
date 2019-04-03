## parser.py
import requests
from bs4 import BeautifulSoup
import json

i = 1
maxpage = 0

data={}
for q in range(1, 50):
    req = requests.get('https://www.thinkcontest.com/Contest/CateField.html?page=' + str(q))
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')


    titles = soup.select('div.contest-title > a')
    tags = soup.select('td.txt-left > div.contest-cate')
    status = soup.findAll("span", {"class": "labeling"})
    page = soup.select('td.txt-left > div > a')

    newStatus=[]
    for i in status:
        if(i.text=="코칭가이드"):continue
        newStatus.append(i.text)

    for i in range(0, len(titles)):
        result = []
        tag = []

        if newStatus[i]=="마감":
            continue

        for j in tags[i]:
            if (j == "\n"): continue
            tag.append(j.text)



        result.append(titles[i].text)
        result.append(newStatus[i])
        result.append("https://www.thinkcontest.com" + titles[i].get('href'))
        result.append(tag)

        for t in tag:
            if t in data:
                tmp=data.get(t)
                tmp.append(result)
                data[t]=tmp
            else:
                tmp=[]
                tmp.append(result)
                data[t]=tmp


for i in data.keys():
    print(i,"\t",len(data.get(i)),"\t",data.get(i))


with open('data/j.json', 'w', encoding='UTF-8-sig') as file:
    file.write(json.dumps(data, ensure_ascii=False))