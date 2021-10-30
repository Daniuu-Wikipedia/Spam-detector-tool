# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 23:30:01 2021

@author: Daniuu

This file contains the main code for the interaction between the software and the wiki.
The processing of abuse filters and other stuff is done in other files.
A file 'Keys.txt' containing the OAuth keys should be present in the current directory
"""

import requests
from requests_oauthlib import OAuth1
import datetime as dt #Import support for dates and times
import time
import re #Regex should be used

class Bot:
    "This function will implement the main functionalities for a bot"  
    def __init__(self, api=r"https://meta.wikimedia.org/w/api.php", m=1):
        'Constructs a bot, designed to interact with one Wikipedia. Here, metawiki should be used as main wiki'
        self.api = api
        self.ti = [] #A list to store the time stamps of the edits in
        self._token = None #This is a token that is handy
        self._auth = None #The OAuth ID (this is the token that will allow the auth - store this for every bot)
        self._max = m #this value is set, and can be changed if a bot bit would be granted
    
    def __str__(self):
        return self.api.copy()

    def verify_OAuth(self, file="OAuth Spam detector.txt"):
        'This function will verify whether the OAuth-auth has been configured. If not, it will do the configuration.'
        if self._auth is None:
            with open(file, 'r') as secret:
                self._auth = OAuth1(*[i.strip() for i in secret][1::2]) #This is the reason why those keys should never be published
    
    def verify_token(self):
        if self._token is None:
            self.get_token()
        elif float(time.time()) - self._token[1] > 8:
            self.get_token() #Tokens expire after approximately 8 seconds, so generate a new one
        return self._token[0]
    
    def get(self, payload):
        "This function will provide functionality that does all the get requests"
        self.verify_OAuth()
        payload['format'] = 'json' #Set the output format to json
        return requests.get(self.api, params=payload, auth=self._auth).json()

    def get_token(self, t='csrf', n=0, store=True):
        'This function will get a token'
        assert isinstance(t, str), 'Please provide a string as a token!'
        pay = {'action':'query',
               'meta':'tokens',
               'type':t}
        z = self.get(pay), float(time.time())
        try:
            if store is True:
                self._token = z[0]['query']['tokens'][f'{t}token'], z[1]
                return self._token[0]
            else:
                return self._token[0] #Just return the token
        except KeyError:
            assert n <= 1, 'Cannot generate the requested token'
            return self.get_token(t, n + 1)

    def post(self, params):
        assert 'action' in params, 'Please provide an action'
        t = float(time.time())
        self.ti = [i for i in self.ti if i >= t - 60] #Clean this mess
        if len(self.ti) >= self._max: #Check this again, after doing the cleaning
            print('Going to sleep for a while')
            time.sleep(20) #Fuck, we need to stop
            return self.post(params) #run the function again - but: with a delay of some 60 seconds
        if 'token' not in params: #Place this generation of the key here, to avoid having to request too many tokens
            params['token'] = self.verify_token() #Generate a new token
        params['format'] = 'json'
        params['maxlag'] = 5 #Using the standard that's implemented in PyWikiBot
        self.ti.append(float(time.time()))
        k = requests.post(self.api, data=params, auth=self._auth).json()
        if 'error' in k:
            print('An error occured somewhere') #We found an error
            if 'code' in k['error'] and 'maxlag' in k['error']['code']:
                print('Maxlag occured, please try to file the request at a later point in space and time.')
        return k

class MetaBot(Bot):
    def __init__(self):
        super().__init__('https://meta.wikimedia.org/w/api.php')

class NlBot(Bot):
    def __init__(self):
        super().__init__('https://nl.wikipedia.org/w/api.php')
        
class MetaHandler(MetaBot):
    "This is a class that will do some elementary stuff at metawiki (like getting a list of requested locks)"
    def __init__(self):
        super().__init__()
        self.requested = set() #A set in which all accounts currently listed on m:SRG can be put into
        self.new = set() #A set to be used to store any new accounts to be locked in
        self.update_edit_conflict() #UTC time at this point, override later
        self._srg = "Steward requests/Global"
    
    def __iadd__(self, account):
        self.new_lock_request(account)
        return self
    
    def check_locked(self, account):
        "Checks whether the account passed is currently locked"
        check = {'action':'query', 'meta':'globaluserinfo', 'guiuser':account, 'format':'json'}
        try:
            data = self.get(check)['query']['globaluserinfo']
            return 'locked' in data
        except:
            return False
    
    def filter_new_locks(self):
        "This function will filter out all accounts for which a lock has already been requested"
        if not self.requested:
            self.existing_lock_requests() #Get the existing lock requests the first time this is requested
        self.new -= self.requested
        locked = set()
        for i in self.new:
            if self.check_locked(i) is True:
                locked.add(i)
        self.new -= locked #Remove all accounts that were already locked for the ease of calculation
        return self.new
    
    def update_edit_conflict(self):
        "This code indicates that we made a new query"
        self._editconflict = dt.datetime.utcnow().isoformat()
    
    def existing_lock_requests(self):
        "This function will identify the lock requests placed"
        sp, mp = r'\{\{Lock[hH]ide\|[^\}]+\}\}', r'\{\{Multi[lL]ock\|[^\}]+\}\}' #Define the regex patterns to be used
        payload = {'action': 'parse',
                   'page':self._srg,
                   'disabletoc':True,
                   'prop':'wikitext'}
        content = self.get(payload)['parse']['wikitext']['*']
        for i in re.findall(sp, content) + re.findall(mp, content): #Browse through all the found templates (MultiLocks and LockHide)
            k = i.split('|')
            k[-1] = k[-1].replace('}', '')
            self.requested |= set((z for z in k if '{' not in z and '=' not in z))
        del content #Remove this heavy bunch of text from the memory
        return self.requested        
    
    def new_lock_request(self, account):
        "This method is used to request a lock for a new account"
        if isinstance(account, set):
            self.new |= {i.strip() for i in account}
        elif isinstance(account, str):
            self.new |= {account.strip()}
        elif hasattr(account, 'user'):
            self.new |= {account.user}
        else:
            self.new |= set((i.strip() for i in account)) #If a list would have been passed
    
    def check_requested(self, account):
        if not self.requested:
            self.existing_lock_requests()
        return account.strip() in self.requested
    
    def __call__(self, account):
        return not(self.check_requested(account.account()) or self.check_locked(account.account()))
    
    def get_lock_requests(self):
        return tuple(sorted(self.new))
            
    def get_SRG_section(self):
        "This function gets the current sections at m:SRG. This method is called by request_locks. The method returns the section index that should be used"
        dic = {'action':'parse',
               'page':self._srg,
               'prop':'sections'}
        fish = self.get(dic)['parse']['sections']
        self.update_edit_conflict()
        return int(next((i for i in fish if i['line'] == 'See also'))['index']) - 1 #This is the section number where text has to be appended
    
    def request_locks(self, filterstring):
        "This function will request locks for all the accounts listed in self.new"
        self.filter_new_locks()
        assert self.new, 'There is nothing to lock!'
        lines = ['\n',
                 f'=== Global lock for {next(iter(self.new))} and {len(self.new) - 1} other spam accounts ===',
                 '{{Status}}'] #List to store the lines containing the block message
        #The accounts to be locked are the ones in self.new - prepare the template and the request
        if len(self.new) == 1:
            lines.append('*{{LockHide|%s}}'%(''.join(self.new)))
            lines[1] = f'=== Global lock for {next(iter(self.new))} ==='
        elif len(self.new) >= 10:
            #This is a special case, it is not desired to list all of the accounts
            lines += ['{{Collapse top|User list}}',
                      '*{{MultiLock|%s}}'%('|'.join(self.new)),
                      '{{Collapse bottom}}']
        else:
            lines.append('*{{MultiLock|%s}}'%('|'.join(self.new)))
        
        if filterstring.endswith('.'):
            filterstring = filterstring[:-1] #Remove the final dot, it's already placed in the summary
            
        lines.append(f'Spam account(s), caught in {filterstring}. --~~~~') #Filterstring indicates the wiki and the number of the filter
        #Make the request to the Meta API
        d2 = {'action':'edit',
              'title':self._srg,
              'summary':f'Reporting {len(self.new)} account(s)',
              'section':self.get_SRG_section(),
              'nocreate':True,
              'appendtext':'\n'.join(lines)}
        return self.post(d2)