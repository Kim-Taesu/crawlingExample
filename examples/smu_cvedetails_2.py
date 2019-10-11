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
saveFile = '../data/result_smu_cvedetails_2.csv'

# 조사할 product 목록
products = [
    # 'Apple-Iphone-Os',
    # 'Google-Android',
    # 'Zephyrproject-Zephyr',
    # 'Apple-Watch-Os',
    # 'Microsoft-Windows-10',
    # 'Windriver-Vxworks',
    'Linux',
    'Linux-Audit',
    'Linux-Direct-Connect',
    'Linux-Ipsec-Tools-Racoon-Daemon',
    'Linux-Kernel1',
    'Linux-Kernel2',
    # 'Linux-Linux-Kernel',
    # 'Linux-Linux-Kernel-I40e-i40evf',
    # 'Linux-Linux-Kernel-Ixgbe',
    # 'Linux-Linux-Kernel-rt',
    # 'Linux-Systemd',
    # 'Linux-Util-linux'
]

# 조사할 vendor id 목록
vendorIds = {
    # 'Google-Android': 1224,
    # 'Apple-Iphone-Os': 49,
    # 'Zephyrproject-Zephyr': 19255,
    # 'Apple-Watch-Os': 49,
    # 'Microsoft-Windows-10': 26,
    # 'Windriver-Vxworks': 95,
    'Linux': 33,
    'Linux-Audit': 33,
    'Linux-Direct-Connect': 33,
    'Linux-Ipsec-Tools-Racoon-Daemon': 33,
    'Linux-Kernel1': 33,
    'Linux-Kernel2': 33,
    # 'Linux-Linux-Kernel': 33,
    # 'Linux-Linux-Kernel-I40e-i40evf': 33,
    # 'Linux-Linux-Kernel-Ixgbe': 33,
    # 'Linux-Linux-Kernel-rt': 33,
    # 'Linux-Systemd': 33,
    # 'Linux-Util-linux': 33
}

# 조사할 product id 목록
productIds = {
    # 'Google-Android': 19997,
    # 'Apple-Iphone-Os': 15556,
    # 'Zephyrproject-Zephyr': 50119,
    # 'Apple-Watch-Os': 32530,
    # 'Microsoft-Windows-10': 32238,
    # 'Windriver-Vxworks': 15063,
    'Linux': 0,
    'Linux-Audit': 13730,
    'Linux-Direct-Connect': 14392,
    'Linux-Ipsec-Tools-Racoon-Daemon': 14771,
    'Linux-Kernel1': 6861,
    'Linux-Kernel2': 17489,
    # 'Linux-Linux-Kernel': 47,
    # 'Linux-Linux-Kernel-I40e-i40evf': 43288,
    # 'Linux-Linux-Kernel-Ixgbe': 43287,
    # 'Linux-Linux-Kernel-rt': 34136,
    # 'Linux-Systemd': 22614,
    # 'Linux-Util-linux': 13878
}

# 검색할 year
years = {
    # 'Google-Android': 2019,
    # 'Apple-Iphone-Os': 2019,
    # 'Zephyrproject-Zephyr': 0,
    # 'Apple-Watch-Os': 0,
    # 'Microsoft-Windows-10': 0,
    # 'Windriver-Vxworks': 0,
    'Linux': 0,
    'Linux-Audit': 0,
    'Linux-Direct-Connect': 0,
    'Linux-Ipsec-Tools-Racoon-Daemon': 0,
    'Linux-Kernel1': 0,
    'Linux-Kernel2': 0,
    # 'Linux-Linux-Kernel': 0,
    # 'Linux-Linux-Kernel-I40e-i40evf': 0,
    # 'Linux-Linux-Kernel-Ixgbe': 0,
    # 'Linux-Linux-Kernel-rt': 0,
    # 'Linux-Systemd': 0,
    # 'Linux-Util-linux': 0
}

# 검색할 trcs
trcs = {
    # 'Google-Android': 103,
    # 'Apple-Iphone-Os': 156,
    # 'Zephyrproject-Zephyr': 4,
    # 'Apple-Watch-Os': 2,
    # 'Microsoft-Windows-10': 1080,
    # 'Windriver-Vxworks': 25,
    'Linux': 2368,
    'Linux-Audit': 1,
    'Linux-Direct-Connect': 2,
    'Linux-Ipsec-Tools-Racoon-Daemon': 1,
    'Linux-Kernel1': 1,
    'Linux-Kernel2': 14,
    # 'Linux-Linux-Kernel': 2355,
    # 'Linux-Linux-Kernel-I40e-i40evf': 1,
    # 'Linux-Linux-Kernel-Ixgbe': 1,
    # 'Linux-Linux-Kernel-rt': 2,
    # 'Linux-Systemd': 1,
    # 'Linux-Util-linux': 4
}

# 조사할 product hash key
shas = {
    # 'Google-Android': '&sha=65688f66fb2607f9ebc84c1102561ceeaf53d8e3',
    # 'Apple-Iphone-Os': '&sha=9268e05c272522ad7ffb4839270cfc837249a395',
    # 'Zephyrproject-Zephyr': '&sha=87ba9c30c0a32b596cdb67110cc51b643c7458d6',
    # 'Apple-Watch-Os': '&sha=b40b19fa2def1a46a655790fbba12f99e96c921f',
    # 'Microsoft-Windows-10': '&sha=41e451b72c2e412c0a1cb8cb1dcfee3d16d51c44',
    # 'Windriver-Vxworks': '&sha=362cecfc66d6e06c3491afe8f86ee9a435ddd697',
    'Linux': '&sha=2f79d8daa05f3cbce8cd668c2f5513fece73c35b',
    'Linux-Audit': '&sha=a4fdcd43b7d8e1e4ca89419cd110dbb3eb264f37',
    'Linux-Direct-Connect': '&sha=51b26927c5609010a8d5dd59b2d5f04f13609284',
    'Linux-Ipsec-Tools-Racoon-Daemon': '&sha=6257621264310525b91bda41c8a517d3b6bf5973',
    'Linux-Kernel1': '&sha=b775008fb26b4cc121d16dc1c4637deb2d9e6ea9',
    'Linux-Kernel2': '&sha=8c5cb41806770918dce520ff5abdfb5c349c0964',
    # 'Linux-Linux-Kernel': '&sha=544260ec3a86a7e17f8b02b39d6342815d8d4bd5',
    # 'Linux-Linux-Kernel-I40e-i40evf': '&sha=e747b8ae84cb5bfc2eaca621ad69c1d426bd79ee',
    # 'Linux-Linux-Kernel-Ixgbe': '&sha=c707f305c9dc4106710d8057e7f99c63dad56d83',
    # 'Linux-Linux-Kernel-rt': '&sha=0f1ae2f0090e43ebb9338c833b424db5996e74ac',
    # 'Linux-Systemd': '&sha=89ad2da99dcc01842da0b6892b3bfd0bb6ae3d0a',
    # 'Linux-Util-linux': '&sha=2c6de89433948b23942a8760161a66b205684e2a'
}

# 최종 데이터
res = []

for product in products:

    # 조사할 product id, vendor id, sha, year, trc
    productId = str(productIds[product])
    vendorId = str(vendorIds[product])
    sha = shas[product]
    year = years[product]
    trc = trcs[product]

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
    for page in range(1,  pageNum + 1):
        # url get (분석용)
        url = 'https://www.cvedetails.com/vulnerability-list.php?' \
              'vendor_id=' + vendorId + \
              '&product_id=' + productId + \
              '&version_id=&page=' + str(page) + \
              '&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0' \
              '&year=' + str(year) + \
              '&month=0&cweid=0&order=1' \
              '&trc=' + str(trc) + sha
        print('url',url)

        # html parser
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        # 크롤링할 table get
        table = soup.select('#vulnslisttable')[0]

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
            try:
                row.append(translator.translate(discription, src='en', dest='ko').text)
            except:
                row.append('translator err')

            # 상세정보 url get
            cveUrl = 'https://www.cvedetails.com/cve/' + row[0] + '/'

            # 상세정보 url parser
            req2 = requests.get(cveUrl)
            html2 = req2.text
            soup2 = BeautifulSoup(html2, 'html.parser')

            # 상세정보 url에서 table get
            table2 = soup2.select('#vulnprodstable')[0]

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
                if row2 and row:
                    res.append(row2 + row)

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
