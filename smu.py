import pandas as pd
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

translator = Translator()
cols = ["Product Type", "Vendor", "Product", "Version", "Update", "Edition", "Language",
        "CVE ID", "CWE ID", "# of Exploits", "Vulnerability Type(s)", "Publish Date",
        "Update Date", "Score", "Gained Access Level", "Access", "Complexity",
        "Authentication", "Conf.", "Integ.", "Avail.", "Discription", "Discription(Korean)"]
standard = ['Product', 'Version']
saveFile = 'result.csv'
year = 2019
products = ['Apple-Iphone-Os', 'Google-Android']
productIds = {'Google-Android': 19997, 'Apple-Iphone-Os': 15556}
vendorIds = {'Google-Android': 1224, 'Apple-Iphone-Os': 49}
shas = {'Google-Android': '&trc=103&sha=65688f66fb2607f9ebc84c1102561ceeaf53d8e3',
        'Apple-Iphone-Os': '&trc=156&sha=9268e05c272522ad7ffb4839270cfc837249a395'}
res = []

for product in products:
    productId = str(productIds[product])
    vendorId = str(vendorIds[product])
    sha = shas[product]
    req = requests.get('https://www.cvedetails.com/vulnerability-list/vendor_id-' + str(vendorId)
                       + '/product_id-' + str(productId)
                       + '/year-' + str(year)
                       + '/' + product + '.html')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    pageNum = len(soup.select('div.paging > a'))

    for page in range(1, pageNum + 1):
        url = 'https://www.cvedetails.com/vulnerability-list.php?' \
              'vendor_id=' + vendorId + \
              '&product_id=' + productId + \
              '&version_id=&page=' + str(page) + \
              '&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=2019&month=0&cweid=0&order=1' \
              + sha
        print(url)
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table', attrs='searchresults sortable')
        table_rows = table.find_all('tr')

        for tr in range(1, len(table_rows), 2):
            td = table_rows[tr].find_all('td')
            row = []
            for i in range(1, len(td)):
                row.append(td[i].text.strip().replace('\t', ''))
            discription = table_rows[tr + 1].text.strip()
            row.append(discription)
            row.append(translator.translate(discription, src='en', dest='ko').text)

            cveUrl = 'https://www.cvedetails.com/cve/' + row[0] + '/'
            req2 = requests.get(cveUrl)
            html2 = req2.text
            soup2 = BeautifulSoup(html2, 'html.parser')

            table2 = soup2.find('table', attrs='listtable')
            table_rows2 = table2.find_all('tr')

            for tr2 in range(1, len(table_rows2)):
                row2 = []
                td2 = table_rows2[tr2].find_all('td')
                for i in range(1, len(td2) - 1):
                    row2.append(td2[i].text.strip().replace('\t', ''))
                if row2 and row: res.append(row2 + row)

df = pd.DataFrame(res, columns=cols).sort_values(by=standard).reset_index(drop=True)
print(df)
df.to_csv(saveFile, mode='w')
print('finish')
