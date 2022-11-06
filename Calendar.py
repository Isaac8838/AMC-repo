from __future__ import print_function
import requests as req
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

########

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
CAL = build('calendar', 'v3', http=creds.authorize(Http()))

########

url = 'https://www.xn--fiqv34aqphd4v.com/tutor/Login.aspx'

header = {
    'User-Agent' : 'User-Agent',
}

# login payload
data = {
    '__VIEWSTATE' : 'payload data',
    '__VIEWSTATEGENERATOR' : 'payload data',
    'ctl00$ContentPlaceHolder1$Login1$UserName' : 'email',
    'ctl00$ContentPlaceHolder1$Login1$Password' : 'password',
    'ctl00$ContentPlaceHolder1$Login1$btnLogin' : '登　入',
}

session = req.Session()
r = session.post(url, headers = header, data = data)
re = session.get('https://www.xn--fiqv34aqphd4v.com/tutor/member/lesson.aspx?tid=plan#plan', headers = header)
soup = BeautifulSoup(re.text, "lxml")

# time
i = 0
date = []
while (True) :
    t = soup.find("span", id = "ctl00_ContentPlaceHolder1_gvGrid_cell" + str(i) + "_0_labClassDateTime")
    if t is None:
        break
    date.append(t.text)
    i += 1

# course name
i = 0
name = []
while (True):
    n = soup.find("a", id = "ctl00_ContentPlaceHolder1_gvGrid_cell" + str(i) + "_0_gvGrid_CourseMeterial_cell0_0_hlDownload")
    if n is None:
        break
    name.append(n.text)
    i += 1

# time deal
list = []
for i in date:
    list.append(i.split(' '))

ymd = []
sTime = []
eTime = []
for i in list:
    ymd.append(i[0])
    temp = i[1].split('-')
    sTime.append(temp[0])
    eTime.append(temp[1])
    
GMT_OFF = '+08:00'
for i in range(len(date)):
    EVENT = {
        'summary' : name[i],
        'start' : {'dateTime': ymd[i] + 'T' + sTime[i] + ':00' + '%s' % GMT_OFF},
        'end' : {'dateTime': ymd[i] + 'T' + eTime[i] + ':00' + '%s' % GMT_OFF},

    }
    e = CAL.events().insert(calendarId = 'primary',
            sendNotifications=True, body=EVENT).execute()

print('''=== %r event added:
    Start: %s
    End:   %s''' % (e['summary'].encode('utf-8'),
    e['start']['dateTime'], e['end']['dateTime']))
