# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 22:38:27 2021

This code contains all the stuff required to process the various aspects of working with abuse filters.

@author: Daniuu
"""

from Interaction import Bot, NlBot, MetaHandler

class AllFoundError(Exception):
    "This error can be used to indicate that the bot could not find any new requests to handle"
    

class AbuseFilter:
    "This class provides the main functions for the Abuse filters (get hits and process them)"
    
    meta = MetaHandler()
    
    def __init__(self, bot, number):
        assert isinstance(bot, Bot), "Please provide a valid bot object"
        self.bot = bot #Provide an instance of the Bot class
        assert isinstance(number, int), "Please provide an integer as the filter number"
        self.filter = number #The number of the filter that is being investigated
    
    def __str__(self):
        return self.bot.api + ' ' + str(self.filter)
    
    def get_hits(self, cont=None, start=None):
        "Get the first 50 hits, starting from cont (for continuation of previous requests)"
        dic = {'action':'query',
               'list':'abuselog',
               'aflfilter':self.filter,
               'aflprop':'user|title|timestamp|details'}
        
    
    
    

class Hit:
    "This class provides the code required to process a hit in the filter (or a log entry, what you prefer)"
    pass