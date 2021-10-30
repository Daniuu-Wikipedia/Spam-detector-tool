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
        #self.root.option.add('*Font', Window.font)
        self.reqbut, self.lockbut, self.igbut = None, None, None #Generate the three buttons
        self.filter = filters #This is the AbuseFilter object that should be passed
        assert isinstance(self.filter, af.AbuseFilter), "Please provide a valid AbuseFilter to the query"
        self._title = tk.StringVar(self.root, value="Title placeholder") #The value for the title (string)
        self._content = tk.StringVar(self.root) #The string for the content
        self._user = tk.StringVar(self.root)
        self._titlefield, self._contentfield, self._userfield = None, None, None #should be set later
        self._queue = [] #Load an empty list to store the processed accounts
        self.prepare_fields()
        self.prepare_buttons()
    
    #Properties that make it easier to set the main interface values
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
    
    #Prepare the main aspects of the interface
    def prepare_fields(self):
        "This method prepares the three fields with the main parameters"
        #Initialize the labels
        self._titlefield = tk.Label(self.root, font=Window.font, textvariable=self._title, fg='brown')
        self._contentfield = tk.Label(self.root, font=Window.font, textvariable=self._content)
        self._userfield = tk.Label(self.root, font=Window.font, textvariable=self._user, fg='navy')
        self._titlefield.config(font=(Window.font, 20)) #Configure the font size
        self._contentfield.config(font=(Window.font, 12), wraplength=50, justify='left')
        self._userfield.config(font=(Window.font, 20)) #Configure font size
        
    def prepare_buttons(self):
        self.make_lock_button()
        self.ignore_button()
        self.ask_lock_button()
        
    def make_button(self, text, action, color):
        "This method will make a general button with the requested settings"
        return tk.Button(self.root, fg=color, font=(Window.font, 20), text=text, command=action)

    def ignore_button(self):
        "This method prepares a button that ignores the currently listed user."
        self.igbut = self.make_button('Ignore (I)', self.ignore, 'Green')
    
    def make_lock_button(self):
        "This method returns a button that can be used to request locks for the stored accounts."
        self.reqbut = self.make_button("Request locks (R)", self.proceed, "blue")
        
    def ask_lock_button(self):
        "A method that produces a button to ask for a lock of the current account"
        self.lockbut = self.make_button("Lock account (L)", self.ask_lock, 'Red')
            
    #Functional: decisions to be made per account    
    def request_locks(self, event=None): #Additional event argument required for TKinter issue
        "This method is the callback for the request locks button"
        return self.filters.request_locks()
    
    def ignore(self, event=None):#Additional event argument required for TKinter issue
        "Ignore the current user and continue to the next one"
        self.load_next_account() #Load the next account, do nothing with the currect user
    
    def ask_lock(self, event=None):#Additional event argument required for TKinter issue
        "A method that will add the account to the list of users to be locked"
        self.filter.ask_lock_for_account(self.user)
        self.load_next_account() #Load the next account, as a lock has already been requested
        
    def bind_keys(self):
        'Method binds keys to a series of actions'
        self.root.bind('l', self.ask_lock)
        self.root.bind('r', self.request_locks)
        self.root.bind('i', self.ignore)
    
    #Some functional stuff
    def load_next_account(self):
        "This method loads the next account into the program"
        if not self._queue:
            self.get_next_hits()
        self.title = self._queue[0].title
        self.user = self._queue[0].user 
        self.content = self._queue[0].content #Set these, is always handy to use StringVars     
        self._queue = self._queue[1:]
    
    def get_next_hits(self):
        "Gets a new bunch of hits from the spam filter. Also filters out locked accounts or reported accounts"
        self._queue += self.filters() #Use the method from the filter itself to store the next bundh of locks
    
    def proceed(self):
        "Gets the next set of hits and requests locks for the accounts listed."
        threading.Thread(target=self.request_locks).start() #Request the locks in parallel
        self.get_next_hits()
        return self.load_next_account() #Load the next account into the list
    
    def stop_run(self):
        "Stops the current run and tells the user to abort the run."
        
        


#Code used for testing - do not modify or use for some sort of operation
bot = inter.NlBot()
fil = af.AbuseFilter(bot, 'nlwiki abusefilter 107', 107)
test = Window(fil)