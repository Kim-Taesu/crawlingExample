import pandas as pd
import requests
from bs4 import BeautifulSoup

all = ['논문/리포트', '기획/아이디어', '네이밍/슬로건', '디자인', '광고/마케팅', '사진', 'UCC/영상', '예체능',
       '문학/수기', '캐릭터/만화', '과학/공학', '게임/소프트웨어', '건축/건설', '체험/참여', '취업/창업', '경품/이벤트',
       '전시/페스티발', '장학(금)재단', '봉사활동', '해외']
cols = ['공모명', '분류', '주최', '진행사항', '디데이', '시작','종료', '조회수', '라벨']
topics = {}
for i in range(len(all)):
    topics[i + 1] = all[i]

res = []
maxPage = 5

for topic in range(1, len(all) + 1):
    print(topics[topic], end=' ')
    for page in range(1, maxPage + 1):
        url = 'https://www.thinkcontest.com/Contest/CateField.html?page=' + str(page) + '&c=' + str(topic)
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table', attrs='type-2 mg-t-5 contest-table')
        table_rows = table.find_all('tr')

        for tr in range(1, len(table_rows)):
            td = table_rows[tr].find_all('td')
            row = []
            labeling = '-'
            flag = False
            for i in range(len(td)):
                if i == 0:
                    divs = td[i].find_all('div')
                    row.append(divs[0].find('a').text)
                    labelingTmp = divs[0].find('span')
                    if labelingTmp: labeling = labelingTmp.text
                    fieldListTmp = divs[1].find_all('span', attrs='cate-name')
                    field = []
                    for tmp in fieldListTmp:
                        field.append(tmp.text)
                    row.append(field)
                elif i == 2:
                    tmp = td[i].text.strip().replace('\t', '').replace('\n', '')
                    if tmp == '마감':
                        flag = True
                        break
                    else:
                        row.append(tmp.split('D')[0])
                        row.append('D' + tmp.split('D')[1])
                elif i==3:
                    tmp = td[i].text.strip().replace('\t', '').split('~')
                    row.append(tmp[0])
                    row.append(tmp[1])
                else:
                    row.append(td[i].text.strip().replace('\t', ''))
            if flag: continue
            row.append(labeling)
            res.append(row)
    print('finish')

df = pd.DataFrame(res, columns=cols)
df.to_csv('data/crawlingResult.csv', mode='w', encoding='UTF-8')
