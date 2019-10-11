# 필수 설치 plugin
# pandas, requests, beautifulSoup4, googletrans
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# 구글 번역 변수 생성
translator = Translator()

# 표 컬럼 목록
cols = ["Product", "Vuln ID", "CVSS Serverity", "Published", "Summary", "Summary_kr"]

# 정렬할 기준
standard = ["Product", 'Vuln ID']

# 저장 파일 및 위치
saveFile = '../data/result_smu_nvd_products_search.csv'

# 기본 url
basicUrl = 'https://nvd.nist.gov/products/cpe/search/results?status=FINAL&orderBy=CPEURI&namingFormat=2.3'

products = [
    'Zephyr', 'Watch OS', 'Vxworks'
]

# 조사할 vendor id 목록
keywords = {
    'Zephyr': '&keyword=Zephyr',
    'Watch OS': '&keyword=watch+os',
    'Vxworks': '&keyword=vxworks'
}

# 최종 데이터
res = []
row=[]
for product in products:
    keyword = keywords[product]

    urlTmp = basicUrl + keyword
    print(urlTmp)

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

        urlTrs = soup.select('div.searchResults > table > tbody > tr')
        for urlTr in urlTrs:
            urlCve = "https://nvd.nist.gov" + urlTr.select('td>div>div>a')[0]['href']
            print(urlCve)
            # html parser
            req = requests.get(urlCve)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            # page index get
            try:
                cvePageIndexes = int(
                    soup.select(".pagination > li > a")[-1].attrs['href'].split('&')[-1].split('=')[-1]) // 20
            except IndexError:
                cvePageIndexes = 1

            for cvePageIndexe in range(cvePageIndexes):
                cveUrl = urlCve + '&startIndex=' + str(cvePageIndexe * 20)
                print(cveUrl)

                req = requests.get(urlCve)
                html = req.text
                soup = BeautifulSoup(html, 'html.parser')

                # 크롤링할 table get
                table = soup.find('tbody')

                # row 단위로 쪼갬
                try:
                    table_rows = table.find_all('tr')
                except AttributeError:
                    continue

                yearInRange = False

                # table의 열 크롤링
                for tr in range(len(table_rows)):

                    vulnId = table_rows[tr].find('a').text

                    yearCheck = int(vulnId.split('-')[1])

                    if yearCheck >= 2015:
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
                    row = [product, vulnId, cvssSeverity, published, summary]

                    # 해석된 discription row에 저장
                    try:
                        row.append(translator.translate(summary, src='en', dest='ko').text)
                    except:
                        row.append('translator err')
                    if row not in res:
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
