from os import mkdir, getcwd, path, rename
from datetime import datetime, timedelta
import defMediaProcessing as dmp
import json, time

start_time = time.time()

"""with open('sources.json', 'r', encoding='utf-8') as fh:
    sources = json.load(fh)"""
sources = [
    {'id': '107.0.1001.2821',
     'url': 'https://www.dvnovosti.ru',
     'prefix': 'dvnovosti.ru',
     'parser': 'xml',
     'paths': ['/rss/'],
     'articlesBox': {'articleSelector': 'item',
                     'anotherArticleSelector': ''},
     'articleContent': {'tag': 'div',
                        'attr': 'class',
                        'name': 'journal-content-article',
                        'titleTag': 'title'},
     'selectConditions': {'location': ''}
     }
 ]

#with open('sources123.json', 'w', encoding='utf-8') as fh:
#    json.dump(sources, fh)

todayMediaStat = open(str(datetime.today().strftime('%Y-%m-%d')) + ' Media statistics.txt', mode='a', encoding='utf-8')
if path.isfile('hb' + str((datetime.today() - timedelta(days=1)).strftime('%d%m%y')) + '_dvnovosti.smi'):    rename('hb' + str((datetime.today() - timedelta(days=1)).strftime('%d%m%y')) + '_dvnovosti.smi', 'hb' + str(datetime.today().strftime('%d%m%y')) + '_dvnovosti.smi')
todayMediaFile = open('hb' + str(datetime.today().strftime('%d%m%y')) + '_dvnovosti.smi', mode='a', encoding='cp866')


totalHourMedia = 0

for source in sources:
    start_time_source = time.time()
    sourceMediaCount = 0
    if path.isdir(getcwd()+ '/' + source['prefix']) == False:
        mkdir(getcwd() + '/' + source['prefix'])
    for article in dmp.getMedia(source):
        todayMediaFile.write(str(article.encode('cp866', 'ignore').decode('cp866')) + '\n')
        sourceMediaCount += 1
    if sourceMediaCount > 0:
        todayMediaStat.write(str(datetime.today().strftime('%Y-%m-%d %H:%M')) + ' С сайта ' + source['prefix'] + ' загружено сообщений: ' + str(sourceMediaCount) + ' (затрачено: {:.2f} сек.)'.format(time.time() - start_time_source) + '\n')
    totalHourMedia += sourceMediaCount

todayMediaStat.write(str(datetime.today().strftime('%Y-%m-%d %H:%M')) + ' Со всех обрабатываемых источников загружено: <' + str(totalHourMedia) + '>\n')

todayMediaStat.close()
todayMediaFile.close()

print('Длительность работы скрипта: {:.2f} сек.'.format(time.time() - start_time))
