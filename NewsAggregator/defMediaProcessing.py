import textwrap
from grab import Grab
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getArticleDate(source_name, article):
    if source_name == 'dvnovosti.ru':
        time1 = article.find('pubDate')
        print(time1)
        ArticleDate = datetime.strptime(time1.text[:16], '%a, %d %b %Y').strftime('%Y-%m-%d')
        return ArticleDate


def getMedia(source = list()):
    url = source['url']
    prefix = source['prefix']
    articles = []
    errorFile = open(str(datetime.today().strftime('%Y-%m-%d')) + ' Error events.txt', mode='a', encoding='utf-8')
    errorNumber = 1

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome()
    #browser.implicitly_wait(15)

    """ Сбор ссылок на  сообщения СМИ (новости и статьи) """
    for path in source['paths']:
        if len(source['paths']) > 0: mainUrl = url + path
        else: mainUrl = url
        """ Формирование списка обработанных сообщений СМИ за текущий день """
        try:
            processedMediaLinksFile = open(prefix + '/' + str(datetime.today().strftime('%Y-%m-%d')) + ' Processed Articles Links.txt', mode='r', encoding='utf-8')
            processedLinks = processedMediaLinksFile.read().split()
            processedMediaLinksFile.close()
        except Exception:
            processedLinks = []
        """ Загрузка страницы сайта с сообщениями СМИ """
        g = Grab()
        g.setup(connect_timeout=50, timeout=50)
        try:
            soup = bs(g.go(mainUrl).body, source['parser'])
        except Exception as e:
            errorFile.write(str(datetime.today().strftime('%Y-%m-%d %H:%M')) + ' #' + str(errorNumber) + ' Source: ' + mainUrl + ', ' + 'Error: ' + str(e) + '\n')
            errorNumber += 1
            continue
        """ Поиск ссылок на сообщения СМИ за текущий день с учетом обработанных """
        try:
            articlesBox = soup.select(source['articlesBox']['articleSelector'])
        except Exception as e:
            errorFile.write(str(datetime.today().strftime('%Y-%m-%d %H:%M')) + ' #' + str(errorNumber) + ' Source: ' + mainUrl + ', ' + 'Error: ' + str(e) + '\n')
            continue

        for article in articlesBox:
            """ Обработка сообщений из новостной ленты сайта """
            href = article.find('guid').text.strip()
            if 'http' != href[:4]: href = url + href
            if href not in processedLinks:
                #if getArticleDate(prefix, article) == datetime.today().strftime('%Y-%m-%d'):
                if getArticleDate(prefix, article) == (datetime.today()-timedelta(days=0)).strftime('%Y-%m-%d'):
                    """ Получение содержания сообщения СМИ """
                    try:
                        browser.get(href)
                        sleep(10)
                        generated_html = browser.page_source
                        articleSoup = bs(generated_html, 'lxml')
                    except Exception as e:
                        print(Exception)
                        errorFile.write(str(datetime.today().strftime('%Y-%m-%d %H:%M')) + ' #' + str(errorNumber) + ' Source: ' + href + ', ' + 'Error: ' + str(e) + '\n')
                        errorNumber += 1
                        continue
                    articleParams = '/СМИ\n'
                    articleParams += '1/' + source['id'] + '\n'
                    articleParams += '2/' + str((datetime.today()-timedelta(days=0)).strftime('%Y-%m-%d')) + '\n'
                    articleParams += '3/\n'
                    title = articleSoup.select_one('title')
                    articleParams += '4/' + title.text.strip() + '\n'
                    f = articleSoup.select('p')
                    ThisText=''
                    for abz in f:
                        ThisText+= abz.text.strip()+'\n'
                    articleParams += '5/' + ThisText
                    while '  ' in articleParams: articleParams=articleParams.replace('  ',' ')
                    articleParams = articleParams.replace('Ё', 'Е').replace('ё', 'е')
                    """ Запись обработанного сообщения СМИ в список """
                    articles.append(articleParams)
                    """ Запись ссылки сообщения СМИ в список и файл обработанных """
                    processedLinks.append(href)
                    processedMediaLinksFile = open(prefix + '/' + str(datetime.today().strftime('%Y-%m-%d')) + ' Processed Articles Links.txt',  mode='a', encoding='utf-8')
                    processedMediaLinksFile.write(href + ' ')
                    processedMediaLinksFile.close()
    """ Выгрузка всех обработанных сообщений СМИ из функции"""
    browser.quit()
    errorFile.close()
    return articles