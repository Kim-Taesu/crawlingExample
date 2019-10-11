# 필수 설치 plugin
# pandas, requests, beautifulSoup4, googletrans
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# 구글 번역 변수 생성
translator = Translator()

# 표 컬럼 목록
cols = ["구분", "Vendor", "제품 이름", "Vuln ID", "CVSS Serverity", "Published", "Summary", "Summary_kr"]

# 정렬할 기준
standard = ['구분', 'Vendor','제품 이름']

# 저장 파일 및 위치
saveFile = '../data/result_smu_nvd_vuln_search.csv'

# 기본 url
basicUrl = 'https://nvd.nist.gov/vuln/search/results?form_type=Advanced&results_type=overview&search_type=all'

# 조사할 product 목록
products = [
    'embedded linux|Linux|제품총합',
    'embedded linux|Linux|Audit',
    'embedded linux|Linux|Direct Connect',
    'embedded linux|Linux|Ipsec Tools Racoon Daemon',
    'embedded linux|Linux|Kernel',
    'embedded linux|Linux|Systemd',
    'embedded linux|Linux|Util-linux',
    'AI 스피커|Amazon|echo',
    'AI 스피커|Apple|siri',
    '기타|Microsoft|cortana'
]

# 조사할 vendor id 목록
querys = {
    'embedded linux|Linux|제품총합': '&query=linux',
    'embedded linux|Linux|Audit': '&query=audit',
    'embedded linux|Linux|Direct Connect': '&query=Direct+Connect',
    'embedded linux|Linux|Ipsec Tools Racoon Daemon': '&query=Ipsec+Tools+Racoon+Daemon',
    'embedded linux|Linux|Kernel': '&query=Kernel',
    'embedded linux|Linux|Systemd': '&query=Systemd',
    'embedded linux|Linux|Util-linux': '&query=Util-linux',
    'AI 스피커|Amazon|echo': '&query=echo',
    'AI 스피커|Apple|siri': '&query=siri',
    '기타|Microsoft|cortana': '&query=cortana'
}

cpe_vendors = {
    'embedded linux|Linux|제품총합': '&cpe_vendor=cpe%3A%2F%3Alinux',
    'embedded linux|Linux|Audit': '&cpe_vendor=cpe%3A%2F%3Alinux',
    'embedded linux|Linux|Direct Connect': '&cpe_vendor=cpe%3A%2F%3Alinux',
    'embedded linux|Linux|Ipsec Tools Racoon Daemon': '&cpe_vendor=cpe%3A%2F%3Alinux',
    'embedded linux|Linux|Kernel': '&cpe_vendor=cpe%3A%2F%3Alinux',
    'embedded linux|Linux|Systemd': '&cpe_vendor=cpe%3A%2F%3Alinux',
    'embedded linux|Linux|Util-linux': '&cpe_vendor=cpe%3A%2F%3Alinux',
    'AI 스피커|Amazon|echo': '&cpe_vendor=cpe%3A%2F%3Aamazon',
    'AI 스피커|Apple|siri': '&cpe_vendor=cpe%3A%2F%3Aapple',
    '기타|Microsoft|cortana': '&cpe_vendor=cpe%3A%2F%3Amicrosoft'
}

# 최종 데이터
res = []
row=[]
for product in products:
    # 조사할 product id, vendor id, sha, year, trc
    query = querys[product]
    cpe_vendor = cpe_vendors[product]

    productTmp = product.split('|')

    division = productTmp[0]
    vendor = productTmp[1]
    productName = productTmp[2]

    urlTmp = basicUrl + query + cpe_vendor

    # url get (page 번호 얻기용)
    req = requests.get(urlTmp)

    # html parser
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # page index get
    try:
        pageIndexes = int(soup.select(".pagination > li > a")[-1].attrs['href'].split('&')[-1].split('=')[-1]) // 20
    except IndexError:
        pageIndexes = 1

    # 위에서 얻은 page 번호 만큼 반복
    for pageIndex in range(pageIndexes):
        url = urlTmp + '&startIndex=' + str(pageIndex * 20)
        print(url)

        # html parser
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        # 크롤링할 table get
        table = soup.find('tbody')

        # row 단위로 쪼갬
        table_rows = table.find_all('tr')

        yearInRange = False

        # table의 열 크롤링
        for tr in range(len(table_rows)):

            vulnId = table_rows[tr].find('a').text

            yearCheck = int(vulnId.split('-')[1])

            if yearCheck >= 2018:
                yearInRange = True
            else:
                continue

            # 한개의 row를 각각의 열로 쪼갬
            td = table_rows[tr].find_all('td')

            summary = td[0].find('p').text
            published = td[0].find('span').text

            cvssSeverity = []
            cvssSeverityTmp = td[1].find_all('span')

            for c in cvssSeverityTmp:
                try:
                    cVersion = c.find('em').text.strip()
                    cContent = c.find('a').text.strip()
                    cvssSeverity.append(cVersion + ' ' + cContent)
                except AttributeError:
                    cvssSeverity.append('(not available)')

            # 결과 데이터에 들어갈 row(list)
            row = [division, vendor, productName, vulnId, cvssSeverity, published, summary]

            # 해석된 discription row에 저장
            try:
                row.append(translator.translate(summary, src='en', dest='ko').text)
            except:
                row.append('translator err')

            res.append(row)

        if not yearInRange:
            print('page %d is break' % pageIndex)
            break

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
