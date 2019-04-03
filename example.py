## parser.py
import requests
from bs4 import BeautifulSoup

i = 1
maxpage = 0

data=[]
for q in range(1, 11):
    ## HTTP GET Request
    req = requests.get('http://campusmon.jobkorea.co.kr/Contest/List?_Page=' + str(q))
    ## HTML 소스 가져오기
    html = req.text
    ## BeautifulSoup으로 html소스를 python객체로 변환하기
    ## 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
    ## 이 글에서는 Python 내장 html.parser를 이용했다.
    soup = BeautifulSoup(html, 'html.parser')

    ## CSS Selector를 통해 html요소들을 찾아낸다.
    my_titles = soup.select('p.ti > a')
    my_status = soup.select('td.day > span')
    my_tag = soup.select('td.tl > p.tag ')

    # for link in my_titles:
    #     print(link.get('href'))

    if len(my_titles) == 0:
        maxpage = i
        print("page end")
        break

    for i in range(0, len(my_titles)):
        result = []
        tag = []
        for j in my_tag[i]:
            if (j == "\n"):
                continue
            tag.append(j.text)
        if (my_status[i].text == "마감"):
            continue

        result.append(my_titles[i].text)
        result.append(my_status[i].text)
        result.append('http://campusmon.jobkorea.co.kr'+my_titles[i].get('href'))
        result.append(tag)
        data.append(result)

for i in data:
    print(i)