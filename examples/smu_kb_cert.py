# 필수 설치 plugin
# pandas, requests, beautifulSoup4, googletrans
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# 구글 번역 변수 생성
translator = Translator()

# 표 컬럼 목록
cols = ['Product','Scope', 'Impact', 'Likelihood', 'Description', 'CWE Description', 'CWE Extended Description']

# 정렬할 기준
standard = ['Product','Scope', 'Impact']

# 저장 파일 및 위치
saveFile = '../data/result_smu_kb_cert.csv'

# 조사할 product 목록
products = [
    'Tizen', 'windows 10'
]

# 조사할 product hash key
vulsIds = {
    'Tizen': '240311',
    'windows 10': '576688'
}

basicUrl = 'https://kb.cert.org/vuls/id/'

# 최종 데이터
res = []

for product in products:
    vulsId = vulsIds[product]
    urlTmp = basicUrl + vulsId
    print(urlTmp)

    # url get (page 번호 얻기용)
    req = requests.get(urlTmp)

    # html parser
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    description = soup.select('table.wrapper-table >tr > td >p')[0].text
    print(description)

    links = soup.select('table.wrapper-table > tr > td > p > a')

    for link in links:
        link = link['href']
        if 'cwe' in link:
            # url get (page 번호 얻기용)
            print(link)
            req = requests.get(link)

            # html parser
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            cweDescription = soup.select('#Description > div.expandblock > div.detail >div.indent')[0].text
            try:
                cweExtendedDescription = \
                soup.select('#Extended_Description > div.expandblock > div.detail >div.indent')[0].text
            except IndexError:
                cweExtendedDescription = ''

            print(cweDescription)
            print(cweExtendedDescription)

            table = soup.select('#Common_Consequences > div.expandblock > div.tabledetail > div.indent > #Detail')[0]

            table_rows = table.find_all('tr')

            for tr in range(1, len(table_rows)):
                tds = table_rows[tr].find_all('td')

                scope = tds[0].text.strip()

                impactTmp = tds[1].select('div')

                impactTech = impactTmp[0].text.strip()
                impactContent = impactTmp[1].text.strip()

                likelihood = tds[2].text.strip()

                row = [product,scope, impactTech + '\n' + impactContent, likelihood, cweDescription, cweExtendedDescription,
                       description]
                print(row)
                res.append(row)


# 최종데이터를 dataframe으로 변경하고 위에서 선언한 standard 기준으로 정렬하고 index 재설정
df = pd.DataFrame(res, columns=cols).sort_values(by=standard).reset_index(drop=True)
# 위 dataframe 변환 작업 후 출력
print(df)

# 변환한 dataframe을 코드 상단에서 선언한 saveFile 경로로 저장
df.to_csv(saveFile, mode='w')

# 저장된 csv가 엑셀로 실행하면 한글이 깨짐현상이 발생됩니다.
# 메모장으로 실행시킨뒤 다른 이름으로 저장으로 해서 인코딩을 'ANSI'로 해주시고 저장 후 엑셀로 실행하면 한글이 잘 나옵니다!

# end
print('finish')
