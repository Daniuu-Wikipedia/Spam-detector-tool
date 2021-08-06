# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 23:30:01 2021

@author: Daniuu

This file contains the main code for the interaction between the software and the wiki.
A file 'Keys.txt' containing the OAuth keys should be present in the current directory
"""

import requests
from requests_oauthlib import OAuth1
import datetime as dt #Import support for dates and times
import time

class Bot:
    "This function will implement the main functionalities for a bot"
    def __init__(self, api, m=1):
        'Constructs a bot, designed to interact with one Wikipedia'
        self.api = api
        self.ti = [] #A list to store the time stamps of the edits in
        self._token = None #This is a token that is handy
        self._auth = None #The OAuth ID (this is the token that will allow the auth - store this for every bot)
        self._max = m #this value is set, and can be changed if a bot bit would be granted
    
    def __str__(self):
        return self.api.copy()

