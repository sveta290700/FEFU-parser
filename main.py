import requests
import re

from bs4 import BeautifulSoup

url = 'https://www.dvfu.ru/schools/'

header = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': '_ga=GA1.2.616006793.1533973671; _ym_uid=1533973672627335240; BX_USER_ID=8911debcf6077dfcd21c7a250e740b96; _a_d3t6sf=duGJrQyVpaOXaX0BeQKXWtpU; _ym_d=1600145997; _univer_identity=de5912365017805caaa3b011b83b9edc78909de588a7f57a458e8ed625451ecba%3A2%3A%7Bi%3A0%3Bs%3A16%3A%22_univer_identity%22%3Bi%3A1%3Bs%3A49%3A%22%5B1118%2C%22ZyAbDFPZJnJfB_RQ-k62lvJmnUIeEc5n%22%2C2592000%5D%22%3B%7D; _jwts=2dd99d5c1e26d3262b11cf7d29e41124687c73ef123268e769cefd31b90cb83fa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_jwts%22%3Bi%3A1%3Bs%3A168%3A%22eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc0MDc3MzQsInVpZCI6MTExOCwidXNlcm5hbWUiOiJyZXZhLnNiIiwicm9sZSI6ImFkbWluIn0.rfZ0Ejeg1jueaquyxZ4yzgL-iR5mMctOLoyMz2Qnzos%22%3B%7D; _gid=GA1.2.613706071.1615248605; _univer_session=9cvlgclsjlple49ohs0s4pmj8j; LtpaToken2=iQ0g0MU0vw9m6i+BvK9K0/kkXwIMULKqrCPD4VJVG/nPhiZQ6MBbEc/H7wmXlxuoSP2Urp7vaqdhX7d4EVIoEAiFt08p89U8NWgdBRCPiJpygi9fiVsHpn808DuiHXpweLTx0sHaS0PotvV9Y1jg4ysJG591kMQJjNOmO0nVfHiDbEZWkLEPfZMPpIam5xi1ie0ly6EkVmtfcaMHxoa0UbTFcFCjdR0SFrJLbg62tpE4C+3T9sfcbtqVV38808SMyIHwXQQIWeqPPxA1vs3pMB+JN5iAPhFCwwmdTeTx8E9lc4EG/FoA70YT2o6DKRhvCnQiZSNAoLbWuKtmceIEkSEmiW3wlCsgYn0fZnzYAAIh+vjZpFeNc0FJZu1gC/zR; _ym_isad=1; _ym_visorc=w; PHPSESSID=eLVcWs4y082fG40aEsQnPw7moHMMOvO3; csrf-token-name=csrftoken; sputnik_session=1615503048823|19; session-cookie=166b6c8ddcfefbab0a05ff0abeb261f575df2e2a53d21e56d001284e881ed4978079b16829640bac0fc152bb0c73b5d3; csrf-token-value=166b6c8ddd0ee89ebb4350e1d71d6fb296ab76468d30c4496fb2fb4c0fdca96aa5f598e2ac8d7e3f',
'Host': 'www.dvfu.ru',
'Referer': 'https://www.dvfu.ru/about/rectorate/scheme/',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
}

session = requests.Session()
r = session.get(url, headers=header)

if r.status_code == 200:
  soup = BeautifulSoup(r.text, features="html.parser")
  tables = soup.find_all('div', {'class': 'schol-item'})
  school = tables[4]
  link = 'https://www.dvfu.ru' + school.find('a', {'target': 'blank'}).attrs['href'] + 'structure/departments/'
  name = school.find('div', {'class': 'name-schol'}).contents[0]
  r = session.get(link, headers=header)
  soup = BeautifulSoup(r.text, features="html.parser")
  tables = soup.find('div', {'class': 'content'})
  breadcrumbs = tables.find('div',{'class': 'breadcrumbs'})#.find_all('a')
  if breadcrumbs is not None:
    not_departments = breadcrumbs.find_all('a')
    #print(not_departments)
  else:
    not_departments = []
  departments = []
  counter = 0
  for d in tables.find_all('a'):
    real = True
    for nd in not_departments:
      if d == nd:
        real = False
        break
    if real:
      if counter % 2 == 1:
        departments.append(d)
      counter += 1
  #print(departments)
  #print()
  print(name)
  for d in departments:
    content = str(d.contents[0])
    if content[0] == '<':
      end = 0
      for i, c in enumerate(content):
        counter = 0
        if c == '"':
          counter += 1
        if counter == 2:
          end = i
          break
      content = content[11:end+1]
    elif len(content) > 2:
      print('    ' + content)

    link = 'https://www.dvfu.ru' + d.attrs['href'] + 'employees.php'
    r = session.get(link, headers=header)
    soup = BeautifulSoup(r.text, features="html.parser")
    tables = soup.find('tbody')
    td = tables.find_all('td')
    for td in tables.find_all('td'):
      b = td.find('b')
      if b is not None:
        if b.find('a') is not None:
          b = b.find('a')
        b = b.contents[0]
        res = re.search(r'\s*', str(b))
        b = b[res.end():]


        if td.find('div', {'itemprop':'Post'}) is not None:
          post = td.find('div', {'itemprop':'Post'})
          br = post.contents[0]
        else:
          br = ''
          pos = 0
          for cont in td.contents:
            pos += 1
            if str(cont).startswith('<b ') or str(cont).startswith('<b>') or str(cont).startswith('<a href'):
              break
          for i in range(pos, len(td.contents)):
            br += str(td.contents[i])
          #br = str(td.contents[len(td.contents) - 1])
          br = br.replace('<br>', '')
          br = br.replace('</br>', '')
          br = br.replace('<br/>', '')
          res = re.split(r'\s*\n\s+', br)
          res = list(filter(lambda x: len(x) > 0, res))
          br = ', '.join(res)
          l = re.findall(r'\S', br)

          test = td.find('br')
          if len(l) == 0 and td.find('br') is not None:
            br = td.find('br').contents[0]
            l.append(br)
        if len(l) > 0:
          print('        ' + b + ' - ' + br)
        else:
          print('        ' + b + " - Должность не указана")



