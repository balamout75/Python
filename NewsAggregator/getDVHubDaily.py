from os import mkdir, getcwd, path, rename, replace
from datetime import datetime, timedelta
import defMediaProcessing as dmp
import json, time
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

start_time = time.time()

"""with open('sources.json', 'r', encoding='utf-8') as fh:
    sources = json.load(fh)"""
sources = [
    {'id': '1',
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

try :
    if len(sys.argv) > 1:
        deepstr=sys.argv[1]
        if (deepstr.isdigit()): deep = int(deepstr)
        else: deep=0
except Exception:
    print('нет аргументов' + Exception)

todayMediaStat = open(str(datetime.today().strftime('%Y-%m-%d')) + ' Media statistics.txt', mode='a', encoding='utf-8')
if path.isfile('hb' + str((datetime.today() - timedelta(days=1)).strftime('%d%m%y')) + '_dvnovosti.smi'):
    rename('hb' + str((datetime.today() - timedelta(days=1)).strftime('%d%m%y')) + '_dvnovosti.smi', 'hb' + str(datetime.today().strftime('%d%m%y')) + '_dvnovosti.smi')
todayMediaFile = open('hb' + str(datetime.today().strftime('%d%m%y_%H_%M')) + '_dvnovosti.smi', mode='a', encoding='cp866')


totalHourMedia = 0

for source in sources:
    start_time_source = time.time()
    sourceMediaCount = 0
    if path.isdir(getcwd()+ '/' + source['prefix']) == False:
        mkdir(getcwd() + '/' + source['prefix'])
    for article in dmp.getMedia(source, deep):
        todayMediaFile.write(str(article.encode('cp866', 'ignore').decode('cp866')) + '\n')
        sourceMediaCount += 1
`    if sourceMediaCount > 0:
        todayMediaStat.write(str(datetime.today().strftime('%Y-%m-%d %H:%M')) + ' С сайта ' + source['prefix'] + ' загружено сообщений: ' + str(sourceMediaCount) + ' (затрачено: {:.2f} сек.)'.format(time.time() - start_time_source) + '\n')
    totalHourMedia += sourceMediaCount

todayMediaStat.write(str(datetime.today().strftime('%Y-%m-%d %H:%M')) + ' Со всех обрабатываемых источников загружено: <' + str(totalHourMedia) + '>\n')

todayMediaStat.close()
filename = todayMediaFile.name
todayMediaFile.close()

try:
    sender_email = 'sender@mail.ru'
    receiver_email = 'recipient@mail.ru'
    msg = MIMEMultipart()
    msg.attach(MIMEText('С Уважением!'))
    myfile=open(filename, mode='r', encoding='cp866')
    MMT=MIMEText(myfile.read())
    MMT.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(MMT)
    msg['Subject'] = 'DV_News'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    smtp = smtplib.SMTP('smtp.mail.ru',25)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(sender_email, '')
    smtp.sendmail(sender_email,receiver_email, msg.as_string())
    smtp.quit()
    myfile.close()
    #replace(filename,'send/'+filename)
except Exception:
    print('ОШИБКА ОТПРАВКИ ПОЧТЫ 1'+Exception)
try:
    sender_email = 'sender@mail.ru'
    receiver_email = 'recipient@mail.ru'
    msg = MIMEMultipart()
    msg.attach(MIMEText('С Уважением!'))
    myfile=open(filename, mode='r', encoding='cp866')
    MMT=MIMEText(myfile.read())
    MMT.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(MMT)
    msg['Subject'] = 'DV_News'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    smtp = smtplib.SMTP('smtp.mail.ru',25)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(sender_email, '')
    smtp.sendmail(sender_email,receiver_email, msg.as_string())
    smtp.quit()
    myfile.close()
    #replace(filename,'send/'+filename)
except Exception:
    print('ОШИБКА ОТПРАВКИ ПОЧТЫ 2'+Exception)
try:
    sender_email = 'sender@mail.ru'
    receiver_email = 'recipient@mail.ru'
    msg = MIMEMultipart()
    msg.attach(MIMEText('С Уважением!'))
    myfile=open(filename, mode='r', encoding='cp866')
    MMT=MIMEText(myfile.read())
    MMT.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(MMT)
    msg['Subject'] = 'DV_News'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    smtp = smtplib.SMTP('smtp.mail.ru',25)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(sender_email, '')
    smtp.sendmail(sender_email,receiver_email, msg.as_string())
    smtp.quit()
    myfile.close()
    replace(filename,'send/'+filename)
except Exception:
    print('ОШИБКА ОТПРАВКИ ПОЧТЫ 3'+Exception)



print('Длительность работы скрипта: {:.2f} сек.'.format(time.time() - start_time))
