# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 22:38:27 2021

This code contains all the stuff required to process the various aspects of working with abuse filters.

@author: Daniuu
"""

from Interaction import Bot, NlBot, MetaHandler, MetaBot
import datetime as dt

class AllLockedError(Exception):
    "This error can be used to indicate that the bot could not find any new requests to handle"
    def __str__(self):
        return "All accounts that were found, are already listed at m:SRG or locked."

class Hit:
    "This class provides the code required to process a hit in the filter (or a log entry, what you prefer)"
    def __init__(self, hit):
        "Constructs hit from an abuselog entry"
        self.user = hit['user']
        self.title = hit['title']
        self.content = hit['details']['new_wikitext']
    
    def __str__(self):
        return self.user
    
    def __eq__(self, other):
        return self.user == other.user
    
    def __hash__(self):
        return self.user.__hash__()    
    
    def __repr__(self):
        return str(self)

class AbuseFilter:
    "This class provides the main functions for the Abuse filters (get hits and process them)"
    meta = MetaHandler()
    def __init__(self, bot, filterstring, number):
        assert isinstance(bot, Bot), "Please provide a valid bot object"
        self.bot = bot #Provide an instance of the Bot class
        assert isinstance(number, int), "Please provide an integer as the filter number"
        self.filter = number #The number of the filter that is being investigated
        self._continue, self.hits, self._string = None, None, filterstring
    
    def __str__(self):
        return self.bot.api + ' ' + str(self.filter)
    
    def prepare_query_for_hits(self):
        return {'action':'query',
               'list':'abuselog',
               'aflfilter':self.filter,
               'aflprop':'user|title|timestamp|details',
               'afllimit':50} #Separate function is only implemented for MultiFilter stuff
    
    def get_hits(self, cont=None, start=None):
        "Get the first 50 hits, starting from cont (for continuation of previous requests)"
        dic = self.prepare_query_for_hits()
        if cont is not None:
            dic['aflstart'] = self._continue
        data = AbuseFilter.meta.get(dic)
        try:
            self._continue = data['continue']['aflstart'] #Set the continuation parameter
        except KeyError:
            self._continue = None
        return dic

        #Generate a list of hits(but filter out the locked accounts)
        hits = data['query']['abuselog'] #The hits from the abuse log
        self.hits = set((Hit(i) for i in hits))
        return self.hits
    
    def filter_hits(self):
        if self.hits is None:
            self.get_hits()
        self.hits = [i for i in self.hits if AbuseFilter.meta(i)]
        if not self.hits:
            raise AllLockedError #All accounts were locked before
        return self.hits
    
    def __call__(self):
        "Iterator that can be used by the interface to get the matches one by one"
        if self.hits is None or isinstance(self.hits, set):
            self.filter_hits()
        return self.hits #Just store it
    
    def get_next_hits(self):
        "This will get the next bunch of hits (using the current self._continue value, obtained form the API)"
        self.get_hits(self._continue)
        return self()
    
    def check_next_hits(self):
        "Same function as get_next_hits, but in iterator form"
        self.get_next_hits(self._continue)
        for i in self():
            yield i
            
    def get_logs_from_time(self, date):
        if not isinstance(date, dt.datetime):
            raise TypeError('Please provide a valid date!')
        self.get_hits(None, date)
        return self()
    
    def request_locks(self):
        "This method will request locks for the accounts that are currently listed in the MetaHandler"
        AbuseFilter.meta.request_locks()

class MultiFilter(AbuseFilter):
    'This class can be used to store multiple abuse filters, and to patrol all of them'
    def __init__(self, bot, filterstring, filters):
        super().__init__(bot, filterstring, 0)
        self.filter = tuple(sorted(filters)) #Store a sorted tuple of the filters
    
    def prepare_query_for_hits(self):
        dic = super().prepare_query_for_hits()
        dic['aflfilter'] = '|'.join(self.filter)
        return dic #Return this and insert it into the other ones


class Hit:
    "This class provides the code required to process a hit in the filter (or a log entry, what you prefer)"
    def __init__(self, hit):
        "Constructs hit from an abuselog entry"
        self.user = hit['user']
        self.title = hit['title']
        self.content = hit['details']['new_wikitext']
    
    def __str__(self):
        return self.user
    
    def __eq__(self, other):
        return self.user == other.user
    
    def __hash__(self):
        return self.user.__hash__()
    
    def get_text(self):
        return self.content
    
    def get_user(self):
        return self.content
    
    def get_title(self):
        return self.title