import pandas as pd
import requests
from bs4 import BeautifulSoup

all = ['논문/리포트', '기획/아이디어', '네이밍/슬로건', '디자인', '광고/마케팅', '사진', 'UCC/영상', '예체능',
       '문학/수기', '캐릭터/만화', '과학/공학', '게임/소프트웨어', '건축/건설', '체험/참여', '취업/창업', '경품/이벤트',
       '전시/페스티발', '장학(금)재단', '봉사활동', '해외']
head = ['공모명', '주최', '진행사항', '디데이', '진행기간', '조회수', '분류']

topics = {}
for i in range(len(all)):
    topics[i + 1] = all[i]
print(topics)

topic = input('분야 번호를 입력하세요')
maxPage = 10

result = {}
flag = False

for i in head:
    result[i] = []

for page in range(1, maxPage + 1):
    if flag: break
    req = requests.get('https://www.thinkcontest.com/Contest/CateField.html?page=' + str(page) + '&c=' + topic)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    total = soup.select('div.all-contest > table > tbody > tr')

    for column in total:
        line = column.text.strip().split('\n')
        line = [x for x in line if x]
        if '마감' in line:
            flag = True
            break
        title = line.pop(0)
        if (line[0] not in all):
            title = title + '(' + line.pop(0) + ')'

        result[head[0]].append(title)
        headerIndex = 1
        tags = []
        for i in line:

            if i in all:
                tags.append(i)
            else:
                tmp = result[head[headerIndex]]
                tmp.append(i)
                headerIndex += 1
        result['분류'].append(tags)
    df = pd.DataFrame(result)

print(df)
print(len(df))
