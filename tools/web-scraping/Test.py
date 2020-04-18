import requests
import bs4
res = requests.get('https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-current-cases-details')
soup = bs4.BeautifulSoup(res.text, 'html.parser')
for link in soup.find_all('a', href = True):
    x = link['href']
    if x[:7] == '/system':
        data = 'https://www.health.govt.nz' + str(link['href'])
        print(data)
    else:
        pass
