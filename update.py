#!/usr/bin/python
import urllib
import json
import os
import requests


hc = "https://hc-ping.com/eb095278-f28d-448d-87fb-7b75c171a6aa"
plexapi = "plexapikeyhere"
host = "hostname_or_ip"
plexurl = "http://plex.local:8182/api/v2?apikey=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&cmd=get_pms_update"
tauturl = "http://plex.local:8182/api/v2?apikey=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&cmd=update_check"

try:
    requests.get(hc + "/start", timeout=10)
except requests.RequestException as e:
    # Log ping failure here...
    print("Ping failed: %s" % e)

url= urllib.urlopen(plexurl)

#data = json.loads(url.read().decode())
data = json.loads(url.read())
plexupdate = data['response']['data']['update_available']

print(plexupdate)

if plexupdate == True:
  print('plex needs updated')
  os.system('docker restart plex')

else:
  print('plex is good')

url=urllib.urlopen(tauturl)
data=json.loads(url.read())
tautupdate = data['response']['data']['update']
print(tautupdate)

if tautupdate == True:
  print('taut needs updated')
#  os.system('docker up -d tautulli')
  os.system('docker-compose -f ~/docker/plex/docker-compose.yml pull tautulli')
  os.system('docker-compose -f ~/docker/plex/docker-compose.yml up -d tautulli')
else:
  print('taut is good')

requests.get(hc)
