# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 21:10:42 2014

@author: kizzm
"""
import os, re

class episode(object):
    
    def __init__(self):
        self.__resetBuffer()
        self.__downloads = {'LibName':'Downloads','Path':''}
        self.__parseLib(self.__downloads)
        
    def __resetBuffer(self):
        try: 
            del self.__buffer
        except:
            pass
        self.__buffer = {'Series':'',
                         'Season':'', 
                         'Episode':'', 
                         'Path':'', 
                         'Parent':'', 
                         'FileName':'', 
                         'Ext':'',
                         'Status':'clear'}
        
    def __parseLib(self,libDict):
        self.__parseDirectory(libDict['Path'])
        for fPath in self.__filesBuffer:
            self.__parseFile(fPath) #fill buffer
            
            Episode = {'Episode':self.__buffer['Episode'],
                       'Path':self.__buffer['Path'],
                       'Parent':self.__buffer['Parent'],
                       'FileName':self.__buffer['FileName'],
                       'Ext':self.__buffer['Ext']}
            
            while not self.__buffer['Status'] == 'clear':
                if self.__buffer['Series'] in libDict.keys(): #check if Series exists
                    if self.__buffer['Season'] in libDict[self.__buffer['Series']].keys():#check if Season exists
                        libDict[self.__buffer['Series']][self.__buffer['Season']] = {self.__buffer['Episode']:Episode}# insert Episode
                        self.__resetBuffer()
                    else: #else create Seasoon and add to Series in lib
                        Season = {'Season':self.__buffer['Season']}
                        libDict[self.__buffer['Series']] = {self.__buffer['Season']:Season}
                
                else:    #else create Series and add to lib
                    Series = {'Series':self.__buffer['Series']}
                    libDict = {self.__buffer['Series']:Series}
           
           
           
           
           
#           if self.__buffer['Series'] in self.__downloads.keys():
#                
#                
#                self.seasonList[['Series']] = 
#                
#                self.__downloads[]
#            
#            else:
#                self.seasonList['Series'] = self.__buffer['Series']
#                self.seasonList[self.__buffer['Episode']] = self.__buffer
#                
#                self.__seriesBuffer['Series'] = self.seasonList['Series']
#                self.__seriesBuffer[self.seasonList['Episode']] = self.seasonList
#                
#        return  seriesList
            
            
    def __parseFile(self,path):
        self.__buffer['Path'] = path
        if os.path.isfile(self.__buffer['Path']):
            self.__splitPath() #Get Parent/FileName/Ext
            self.__parseEpisodeSeason() #Get SeasonNr/EpisodeNr
            self.__parseSerieName() #Get Series Name
            self.__buffer['Status'] = 'filled' #set bufferstatus
        else:
            raise NameError('__parseFile: File ist doch kein File!') 
    
    def __del__(self):
        pass
    
    def __splitPath(self):        
        head, self.__buffer['Ext'] = os.path.splitext(self.__buffer['Path'])
        self.__buffer['Parent'], self.__buffer['FileName'] = os.path.split(head)

            
    def __parseSerieName(self):
        namePattern = re.compile('.*[a-zA-Z0-9](?=[^a-zA-Z0-9]*[sS][0-9]+)')
        name = namePattern.findall(self.__buffer['FileName'])
        
        delimiters = '_', '.', '-', '%', ';', ':'
        regExpPattern = '|'.join(map(re.escape, delimiters))
        
        self.__buffer['Series'] = re.split(regExpPattern,name[0])
        
    def __parseEpisodeSeason(self):
        seasonPattern = re.compile('[sS][0-9]+')
        episodePattern = re.compile('[eE][0-9]+')
                
        self.__buffer['Season'] = seasonPattern.findall(self.__buffer['FileName'])[0][1:]
        self.__buffer['Episode'] = episodePattern.findall(self.__buffer['FileName'])[0][1:]
        
    def __parseDirectory(self,path):
        self.__filesBuffer = []
        self.__dirsBuffer = [path]
        for dirPath in self.__dirsBuffer:
            for el in os.listdir(dirPath):
                if os.path.isfile(dirPath+el):
                    self.__filesBuffer.append(dirPath+el)
                else:
                    self.__dirsBuffer.append(dirPath+el+'/')
    
    def getPath(self):
        return self.__buffer['Path']
        
    def getExt(self):
        return self.__buffer['Ext']
        
    def getFileName(self):
        return self.__buffer['FileName']
        
    def getParent(self):
        return self.__buffer['Parent']
        
    def getEpisodeNr(self):
        return self.__buffer['Episode']
        
    def getSeasonNr(self):
        return self.__buffer['Season']
        
    def getName(self):
        return self.__buffer['Series']
        
    def getDict(self):
        return self.__buffer