# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 21:10:42 2014

@author: kizzm
"""
import os, re

class page(object):
    
    def __init__(self,path):
        self.__path = path
        if os.path.isfile(self.__path):
            self.__splitPath()
            self.__parseEpisodeSeason()
            self.__parseSerieName()
        else:
            self.__splitPath()
            #self.__parseEpisodeSeason()
            #self.__parseSerieName()
    
    def __del__(self):
        pass
    
    def __splitPath(self):        
        head, self.__ext = os.path.splitext(self.__path)
        self.__parent, self.__fileName = os.path.split(head)

    def __parseSerieName(self):
        namePattern = re.compile('.*[a-zA-Z0-9](?=[^a-zA-Z0-9]*[sS][0-9]+)')
        name = namePattern.findall(self.__fileName)
        
        delimiters = '_', '.', '-', '%', ';', ':'
        regExpPattern = '|'.join(map(re.escape, delimiters))
        
        self.__name = re.split(regExpPattern,name[0])
        
    def __parseEpisodeSeason(self):
        seasonPattern = re.compile('[sS][0-9]+')
        episodePattern = re.compile('[eE][0-9]+')
        
        self.__seasonNr = int( seasonPattern.findall(self.__fileName)[0][1:] )
        self.__episodeNr = int( episodePattern.findall(self.__fileName)[0][1:] )
        
    
    def getPath(self):
        return self.__path
        
    def getExt(self):
        return self.__ext
        
    def getFileName(self):
        return self.__fileName
        
    def getParent(self):
        return self.__parent
        
    def getEpisodeNr(self):
        return self.__episodeNr
        
    def getSeasonNr(self):
        return self.__seasonNr
        
    def getName(self):
        return self.__name
        

                
        