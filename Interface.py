# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 18:25:58 2021

@author: Daniuu
"""

#Implement a graphical interface when one finds the time to do so
import AbuseFilter as af
import Interaction as inter 
import tkinter as tk
import threading #Import threading to run things in parallel
import time

class Window:
    "This class contains the code for a nice window"
    font = 'Courier'
    
    def __init__(self, filters):
        self.root = tk.Tk() #Create the main loop
        self.root.option.add('*Font', Window.font)
        self.buttons = [] #A list containing the necessary buttons (to perform the different actions)
        self.filter = filters #This is the AbuseFilter object that should be passed
        assert isinstance(self.filter, af.AbuseFilter), "Please provide a valid AbuseFilter to the query"
        self._title = tk.StringVar(self.root, value="Title placeholder") #The value for the title (string)
        self._content = tk.StringVar(self.root) #The string for the content
        self._user = tk.StringVar(self.root)
        self._titlefield, self._contentfield, self._userfield = None, None, None #should be set later
        self.prepare_fields()
    
    @property #Define a couple of properties for the most commoon operations
    def title(self):
        return self._title.get() #Gets the current value of the title
    
    @title.setter
    def title(self, value):
        if isinstance(value, str):
            self._title.set(value)
    
    @property
    def content(self):
        return self._content.get()
    
    @content.setter
    def content(self, value):
        if isinstance(value, str):
            self._content.set(value)
    
    @property
    def user(self):
        return self._user.get()
    
    @user.setter 
    def user(self, value):
        return self._user.set(value)
    
    def prepare_fields(self):
        "This method prepares the three fields with the main parameters"
        #Initialize the labels
        self._titlefield = tk.Label(self.root, font=Window.font, textvariable=self._title, fg='brown')
        self._contentfield = tk.Label(self.root, font=Window.font, textvariable=self._content)
        self._userfield = tk.Label(self.root, font=Window.font, textvariable=self._user, fg='navy')
        self._titlefield.config(font=(Window.font, 20)) #Configure the font size
        self._contentfield.config(font=(Window.font, 12))
        self._userfield.config(font=(Window.font, 20)) #Configure font size
        
    def make_button(self, text, action, color, col, row=3):
        "This method will make a general button with the requested settings"
        new = tk.Button(self.root)
        return new
    
    def make_lock_button(self):
        "This method returns a button that can be used to request locks for the stored accounts."
        pass
        
    def request_locks(self):
        "This method is the callback for the request locks button"
        return self.filters.request_locks()
    
    def ignore_button(self):
        "This method prepares a button that ignores the currently listed user."
        pass
    
    def ignore(self):
        "Ignore the current user and continue to the next one"
        pass
    
    def ask_lock(self):
        "A method that will add the account to the list of users to be locked"
        pass
    
    def ask_lock_button(self):
        "A method that produces a button to ask for a lock of the current account"
        pass
    
    def load_next_account(self):
        "This method loads the next account into the program"
        pass
    
    def get_next_hits(self):
        "Gets a new bunch of hits from the spam filter. Also filters out locked accounts or reported accounts"
        pass
    
    def proceed(self):
        "Gets the next set of hits and requests locks for the accounts listed."
        pass
        


#Code used for testing - do not modify or use for some sort of operation
bot = inter.NlBot()
fil = af.AbuseFilter(bot, 'nlwiki abusefilter 107', 107)
test = Window(fil)