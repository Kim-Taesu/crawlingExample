# 필수 설치 plugin
# pandas, requests, beautifulSoup4, googletrans
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# 구글 번역 변수 생성
translator = Translator()

# 표 컬럼 목록
cols = ["구분", "Vendor", "제품 이름", "CVE", "Base Score", "Access Vector (AV)", "Access Complexity (AC)",
        "Authentication (AU)", "Confidentiality (C)", "Integrity (I)", "Availability (A)", "Description",
        "Description (kr)"]

# 정렬할 기준
standard = ["구분", "Vendor", ]

# 저장 파일 및 위치
saveFile = '../data/result_smu_nvd_vuln_detail.csv'

# 기본 url
basicUrl = 'https://nvd.nist.gov/vuln/detail/'

# 조사할 product 목록
products = [
    '기타|Amazon|Alexa',
    'AI 스피커|Google|Google Home',
    'AI 스피커|Lenovo|Lenovo Smart Assistant',
    '기타|Google|Google Assistant'
]

# 조사할 vendor id 목록
cves = {
    '기타|Amazon|Alexa': 'CVE-2018-11567',
    'AI 스피커|Google|Google Home': 'CVE-2018-12716',
    'AI 스피커|Lenovo|Lenovo Smart Assistant': 'CVE-2018-9070#vulnCurrentDescriptionTitle',
    '기타|Google|Google Assistant': 'CVE-2019-2103'
}

# 최종 데이터
res = []
row = []
for product in products:
    # 조사할 product id, vendor id, sha, year, trc
    cve = cves[product]
    productTmp = product.split('|')
    division = productTmp[0]
    vendor = productTmp[1]
    productName = productTmp[2]

    url = basicUrl + cve
    print(url)

    # html parser
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # 크롤링할 table get
    baseScore = soup.find('span', attrs={"data-testid": "vuln-cvssv3-base-score"}).text.strip()
    accessVector = soup.find('span', attrs={"data-testid": "vuln-cvssv2-av"}).text.strip()
    accessComplexity = soup.find('span', attrs={"data-testid": "vuln-cvssv2-ac"}).text.strip()
    authentication = soup.find('span', attrs={"data-testid": "vuln-cvssv2-au"}).text.strip()
    availability = soup.find('span', attrs={"data-testid": "vuln-cvssv2-a"}).text.strip()
    integrity = soup.find('span', attrs={"data-testid": "vuln-cvssv2-i"}).text.strip()
    confidentiality = soup.find('span', attrs={"data-testid": "vuln-cvssv3-c"}).text.strip()
    discription = soup.find('span', attrs={"data-testid": "vuln-cvssv2-additional"}).text.strip()
    # 결과 데이터에 들어갈 row(list)
    row = [division, vendor, productName, cve, baseScore, accessVector, accessComplexity, authentication,
           confidentiality, integrity, availability, discription]
    print(row)
    # 해석된 discription row에 저장
    try:
        row.append(translator.translate(discription, src='en', dest='ko').text)
    except:
        row.append('translator err')

    [x.encode('ANSI') for x in row]

    res.append(row)

# 최종데이터를 dataframe으로 변경하고 위에서 선언한 standard 기준으로 정렬하고 index 재설정
df = pd.DataFrame(res, columns=cols).sort_values(by=standard).reset_index(drop=True)
# 위 dataframe 변환 작업 후 출력
print(df.head())

# 변환한 dataframe을 코드 상단에서 선언한 saveFile 경로로 저장
df.to_csv(saveFile, mode='w')

# 저장된 csv가 엑셀로 실행하면 한글이 깨짐현상이 발생됩니다.
# 메모장으로 실행시킨뒤 다른 이름으로 저장으로 해서 인코딩을 'ANSI'로 해주시고 저장 후 엑셀로 실행하면 한글이 잘 나옵니다!

# end
print('finish')
