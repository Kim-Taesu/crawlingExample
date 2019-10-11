# 필수 설치 plugin
# pandas, requests, beautifulSoup4, googletrans
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# 구글 번역 변수 생성
translator = Translator()

# 표 컬럼 목록
cols = ["구분", "Vendor", "제품 이름", "CVE", "ID","Summary", "Summary_kr", "CVSS", "CWE", "Published", "Last modified", ]

# 정렬할 기준
standard = ["구분", "Vendor", "제품 이름"]

# 저장 파일 및 위치
saveFile = '../data/result_smu_cve.csv'

# 기본 url
basicUrl = 'http://cve.circl.lu/cve/'

# 조사할 product 목록
products = [
    'AI 스피커|Google|Google Home'
]

cves={
'AI 스피커|Google|Google Home' : 'CVE-2018-12716'
}

# 최종 데이터
res = []

for product in products:

    productTmp = product.split('|')

    division = productTmp[0]
    vendor = productTmp[1]
    productName = productTmp[2]
    cve = cves[product]

    print(cve)
    # 조사할 product id, vendor id, sha, year, trc

    urlTmp = basicUrl + cve

    # url get (page 번호 얻기용)
    req = requests.get(urlTmp)

    # html parser
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # 크롤링할 table get
    table = soup.select('#cveInfo > tbody')[0]

    # row 단위로 쪼갬
    table_rows = table.find_all('tr')

    row = [division,vendor,productName,cve]
    # table의 열 크롤링
    for tr in table_rows:

        # 한개의 row를 각각의 열로 쪼갬
        td = tr.find_all('td')

        title = td[0].text.strip()
        content = td[1].text.strip()


        if title in cols:
            if title == 'Summary':
                # 해석된 discription row에 저장
                try:
                    row.append(translator.translate(content, src='en', dest='ko').text)
                except:
                    row.append('translator err')

            if title == 'CVSS':
                contents = content.split('\n')
                contentTmp=[]
                for c in contents:
                    contentTmp.append(''.join(c.replace(' ','')))
                content=contentTmp

            row.append(content)
        else:
            continue
    res.append(row)

print(res)


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
