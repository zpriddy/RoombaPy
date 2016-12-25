# -*- coding: utf-8 -*-
# @Author: Zachary Priddy
# @Date:   2016-11-12 22:32:35
# @Last Modified by:   Zachary Priddy
# @Last Modified time: 2016-11-12 22:38:00
import ConfigParser

class Roomba(object):
  def __init__(self, username=None, password=None, host=None, config=None, local=True):

    if config:
      c = ConfigParser.ConfigParser()
      c.read(config)
      username = c.get('roomba', 'user')
      password = c.get('roomba', 'pass')
      host = c.get('roomba', 'host')

    self._local = local
    self._pass = password
    self._user = username
    self._host = host

    