# -*- coding: utf-8 -*-
# @Author: Zachary Priddy
# @Date:   2016-11-12 20:00:23
# @Last Modified by:   Zachary Priddy
# @Last Modified time: 2016-11-12 22:01:18

import base64
import json
import logging
import requests
import sys

logging.captureWarnings(True)

SETUP_MESSAGE = '''
Make sure your robot is on the Home Base and powered on (green   lights on).
Then press and hold the HOME button on your robot until it   plays a series of tones (about 2 seconds).
Release the button and your   robot will flash WIFI light. Then wait and look here...
'''

SUCCESS_MESSAGE = '''
\nGood Job!

Password: %(pass)s
Username/blid: %(blid)s
Use this credentials in the config file or arguments for RoombaPy.
please note that these credentials may chnage if you chnage your wifi network on the roomba.

This is what your config file should look like:

[roomba]
host: %(host)s
blid: %(blid)s
pass: %(pass)s
'''


def getRequestOptions(host):
  options = {
    'headers': {
      'Content-Type': 'application/json',
      'Connection': 'close',
      'User-Agent': 'aspen%20production/2618 CFNetwork/758.3.15 Darwin/15.4.0',
      'Content-Encoding': 'identity',
      'Accept': '*/*',
      'Accept-Language': 'en-us',
      'Host': host
    },
    'url': 'https://' + host + ':443/umi'
  }

  return options


def getPassword(host, rid):
  requestOptions = getRequestOptions(host)
  requestOptions['json'] = {
    'do': 'get',
    'args': ['passwd'],
    'id': rid
  }

  sys.stdout.write('\nTrying to contact roomba.')
  sys.stdout.flush()

  while rid <= 120:
    sys.stdout.write('.')
    sys.stdout.flush()

    r = requests.post(requestOptions['url'],
                      headers=requestOptions['headers'],
                      json=requestOptions['json'],
                      verify=False,
                      timeout=100)

    if r.status_code == 200:
      break

  try:
    password = json.loads(r.text)['ok']['passwd']
    return password
  except:
    print 'Error: Error getting password'
    exit()


def getBlid(host, rid, password):
  requestOptions = getRequestOptions(host)
  requestOptions['json'] = {
    'do': 'get',
    'args': ['sys'],
    'id': rid
  }

  requestOptions['headers']['Authorization'] = 'Basic ' + str(
      base64.b64encode('user:' + password))

  r = requests.post(requestOptions['url'],
                    headers=requestOptions['headers'],
                    json=requestOptions['json'],
                    verify=False)

  try:
    rawBlid = json.loads(r.text)['ok']['blid']
    blid = ""
    for b in rawBlid:
      blid += hex(b + 0x1000)[-2:].upper()
    return blid
  except:
    print 'Error: Error getting blid'
    exit()


def main(args):
  if len(args) < 2:
    print '\nPlease use this with the IP of the roomba. i.e:\n\
$ ./getPassword 192.168.1.12 <--- Replace with the IP of the roomba\n\
    '
    exit()
  host = args[1]
  print 'Using ' + str(host) + ' as the IP of the roomba'
  print SETUP_MESSAGE

  rid = 1
  password = getPassword(host, rid)
  rid += 1
  blid = getBlid(host, rid, password)

  print SUCCESS_MESSAGE % {'host': host, 'blid': blid, 'pass': password}


if __name__ == "__main__":
  try:
    main(sys.argv)
  except KeyboardInterrupt:
    print '\n\nBye'
    exit()
