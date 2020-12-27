## Extraindo os links das noticias
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from pymongo import MongoClient

###### Ajustando o ambiente selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs",{"profile.default_content_setting_values.cookies": 2})
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("disable-dev-shm-usage")
chrome=webdriver.Chrome(executable_path="/home/alexandre/Documentos/CRC/chromedriver_linux64 (2)/chromedriver",options=chrome_options)

# Listas
Times = []
Portal = []
link = []

# Acessando as paginas do Globoesporte.com
actions = ActionChains(chrome)
clubes = ['athletico-pr','atletico-go','bahia','botafogo','bragantino','corinthians','coritiba','flamengo','fluminense','goias','gremio','internacional','palmeiras','ceara','fortaleza','sao-paulo','sport','vasco','atletico-mg']

for i in clubes:
    if i == 'athletico-pr':
        url = 'https://globoesporte.globo.com/pr/futebol/times/'+i
    else:
        url = 'https://globoesporte.globo.com/futebol/times/'+i


    chrome.get(url)
    print(url)
# Encontrando os links principais
    find = chrome.find_element_by_xpath("//*[@class= 'bstn-hls xlarge-22 xlarge-offset-1 theme model-3']")
    principal = chrome.find_elements_by_xpath("//*[@class= 'bstn-hl-wrapper']")
    j=0
    while j < 3:
        Times.append(i)
        Portal.append('Globo Esporte')
        link.append(principal[j].find_element_by_xpath("//*[@class='bstn-hl-link']").get_attribute('href'))
        j=j+1

    Corpo = chrome.find_elements_by_xpath("//*[@class ='bastian-page']")[0]
    corpus = Corpo.find_element_by_xpath("//*[@data-index='1']")
    corpus1 = corpus.find_element_by_xpath("//*[@class='_b']")
    corpus2 = corpus1.find_elements_by_xpath("//a[@class='feed-post-figure-link gui-image-hover']")
    for m in corpus2:
        corpus3=m.get_attribute('href')
        print(corpus3)
        link.append(corpus3)
        Times.append(i)
        Portal.append('Globo Esporte')

data =pd.DataFrame({'Url':link,'Clube':Times,'Portal':Portal})

client = MongoClient()
db = client["Jornais"]
Jornais = db["Noticias"]
Jornais.insert_many(data.to_dict("records"))
