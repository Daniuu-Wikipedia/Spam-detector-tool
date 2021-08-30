# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 18:25:58 2021

@author: Daniuu
"""

#Implement a graphical interface when one finds the time to do so
import AbuseFilter as af
import Interaction as inter 
import tkinter as tk

class Window:
    "This class contains the code for a nice window"
    def __init__(self, filters):
        self.root = tk.Tk() #Create the main loop
        self.buttons = [] #A list containing the necessary buttons (to perform the different actions)
        self.filter = filters #This is the AbuseFilter object that should be passed
        assert isinstance(self.filter, af.AbuseFilter), "Please provide a valid AbuseFilter to the query"
        self._title = tk.StringVar(self.root) #The value for the title (string)
        self._content = tk.StringVar(self.root) #The string for the content
        self._user = tk.StringVar(self.root)
    
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