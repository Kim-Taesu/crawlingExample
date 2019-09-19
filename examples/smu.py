# 필수 설치 plugin
# pandas, requests, beautifulSoup4, googletrans
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# 구글 번역 변수 생성
translator = Translator()

# 표 컬럼 목록
cols = ["Product Type", "Vendor", "Product", "Version", "Update", "Edition", "Language",
        "CVE ID", "CWE ID", "# of Exploits", "Vulnerability Type(s)", "Publish Date",
        "Update Date", "Score", "Gained Access Level", "Access", "Complexity",
        "Authentication", "Conf.", "Integ.", "Avail.", "Discription", "Discription(Korean)"]

# 정렬할 기준
standard = ['Product', 'Version']

# 저장 파일 및 위치
saveFile = '../data/result.csv'

# 검색할 year
year = 2019

# 조사할 product 목록
products = ['Apple-Iphone-Os', 'Google-Android']

# 조사할 product id 목록
productIds = {'Google-Android': 19997, 'Apple-Iphone-Os': 15556}

# 조사할 vendor id 목록
vendorIds = {'Google-Android': 1224, 'Apple-Iphone-Os': 49}

# 조사할 product hash key
shas = {'Google-Android': '&trc=103&sha=65688f66fb2607f9ebc84c1102561ceeaf53d8e3',
        'Apple-Iphone-Os': '&trc=156&sha=9268e05c272522ad7ffb4839270cfc837249a395'}

# 최종 데이터
res = []

for product in products:

    # 조사할 product id, vendor id, sha
    productId = str(productIds[product])
    vendorId = str(vendorIds[product])
    sha = shas[product]

    # url get (page 번호 얻기용)
    req = requests.get('https://www.cvedetails.com/vulnerability-list/vendor_id-' + str(vendorId)
                       + '/product_id-' + str(productId)
                       + '/year-' + str(year)
                       + '/' + product + '.html')

    # html parser
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # page 번호 get
    pageNum = len(soup.select('div.paging > a'))

    # 위에서 얻은 page 번호 만큼 반복
    for page in range(1, pageNum + 1):
        # url get (분석용)
        url = 'https://www.cvedetails.com/vulnerability-list.php?' \
              'vendor_id=' + vendorId + \
              '&product_id=' + productId + \
              '&version_id=&page=' + str(page) + \
              '&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=2019&month=0&cweid=0&order=1' \
              + sha
        print(url)

        # html parser
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        # 크롤링할 table get
        table = soup.find('table', attrs='searchresults sortable')

        # row 단위로 쪼갬
        table_rows = table.find_all('tr')

        # 첫번째 줄은 헤더이므로 pass 따라서 시작은 1부터 (코드 상단에 cols으로 헤더 정의)
        for tr in range(1, len(table_rows), 2):

            # 한개의 row를 각각의 열로 쪼갬
            td = table_rows[tr].find_all('td')

            # 결과 데이터에 들어갈 row(list)
            row = []

            # table 크롤링 결과를 row에 저장
            for i in range(1, len(td)):
                row.append(td[i].text.strip().replace('\t', ''))

            # discription get
            discription = table_rows[tr + 1].text.strip()

            # discription row에 저장
            row.append(discription)

            # 해석된 discription row에 저장
            row.append(translator.translate(discription, src='en', dest='ko').text)

            # 상세정보 url get
            cveUrl = 'https://www.cvedetails.com/cve/' + row[0] + '/'

            # 상세정보 url parser
            req2 = requests.get(cveUrl)
            html2 = req2.text
            soup2 = BeautifulSoup(html2, 'html.parser')

            # 상세정보 url에서 table get
            table2 = soup2.find('table', attrs='listtable')

            # get한 테이블을 row로 쪼갬
            table_rows2 = table2.find_all('tr')

            # 각 row만큼 반복 (첫 번째는 헤더이므로 시작은 1부터)
            for tr2 in range(1, len(table_rows2)):
                # 상세정보 url 정보를 저장할 row 생성
                row2 = []

                # 각 row를 컬럼으로 쪼갬
                td2 = table_rows2[tr2].find_all('td')

                # 각 row의 컬럼 데이터 row2에 저장
                for i in range(1, len(td2) - 1):
                    row2.append(td2[i].text.strip().replace('\t', ''))

                # 상세정보 url row2 데이터와 상위 url row 데이터가 존재하면 최종데이터(res)에 저장
                if row2 and row: res.append(row2 + row)

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
