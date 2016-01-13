# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 21:10:42 2014

@author: kizzm
"""
import os, re

class fileLib(object):
    
    def __init__(self,libName,libPath):
        self.__resetBuffer()
        self.lib = {'LibName':libName,'Path':libPath}
        self.__parseLib(self.lib)

    def __del__(self):
        pass
            
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
                         
    def __checkBuffer(self):
        if not self.__buffer['Status'] in ['filled']:
            if not self.__buffer['Status'] in ['clear']:
                if not self.__buffer['Status'] in ['cancel']:
                    pass
                else:
                    print('cancel')
                    self.__resetBuffer()
            else:
                print('clear')
        else:
            print('filled')
                      
    def __parseFile(self,path):
        self.__buffer['Path'] = path
        if os.path.isfile(self.__buffer['Path']):
            self.__buffer['Status'] = 'filled' #set bufferstatus
            if self.__splitPath(): #Get Parent/FileName/Ext
                if self.__parseEpisodeSeason(): #Get SeasonNr/EpisodeNr
                    if self.__parseSerieName(): #Get Series Name
                        pass
        else:
            raise NameError('__parseFile: File ist doch kein File!') 

    def __splitPath(self):        
        head, self.__buffer['Ext'] = os.path.splitext(self.__buffer['Path'])
        self.__buffer['Parent'], self.__buffer['FileName'] = os.path.split(head)
        if not self.__buffer['Ext'] in ['part']:
            return 1
        else:
            self.__buffer['Status'] = 'cancel'
            return 0

            
    def __parseSerieName(self):
        namePattern = re.compile('.*[a-zA-Z0-9](?=[^a-zA-Z0-9]*[sS][0-9]+)')
        name = namePattern.findall(self.__buffer['FileName'])
        
        delimiters = '_', '.', '-', '%', ';', ':'
        regExpPattern = '|'.join(map(re.escape, delimiters))
        
        try:
            self.__buffer['Series'] = re.split(regExpPattern,name[0])
            self.__buffer['Series'] = ' '.join(self.__buffer['Series'])
        except:
            self.__buffer['Status'] = 'cancel'
            return 0
        return 1
        
    def __parseEpisodeSeason(self):
        seasonPattern = re.compile('[sS][0-9]+')
        episodePattern = re.compile('[eE][0-9]+')
        
        try:        
            self.__buffer['Season'] = seasonPattern.findall(self.__buffer['FileName'])[0][1:]
            self.__buffer['Episode'] = episodePattern.findall(self.__buffer['FileName'])[0][1:]
        except IndexError:
            self.__buffer['Status'] = 'cancel'
            return 0
        return 1
        
    def __parseDirectory(self,path):
        self.__filesBuffer = []
        self.__dirsBuffer = [path]
        for dirPath in self.__dirsBuffer:
            for el in os.listdir(dirPath):
                if os.path.isfile(dirPath+el):
                    self.__filesBuffer.append(dirPath+el)
                else:
                    self.__dirsBuffer.append(dirPath+el+'/')
                    
        
    def __parseLib(self,libDict):
        self.__parseDirectory(libDict['Path'])
        for fPath in self.__filesBuffer:
            self.__parseFile(fPath) #fill buffer
            
            if not self.__buffer['Status'] == 'cancleL':
                Episode = {'Episode':self.__buffer['Episode'],
                           'Path':self.__buffer['Path'],
                           'Parent':self.__buffer['Parent'],
                           'FileName':self.__buffer['FileName'],
                           'Ext':self.__buffer['Ext']}
                
                while not self.__buffer['Status'] == 'clear':
#                    print(self.__buffer['Series'])
#                    print(libDict.keys())
                    if self.__buffer['Series'] in libDict.keys(): #check if Series exists
                        if self.__buffer['Season'] in libDict[self.__buffer['Series']].keys():#check if Season exists
                            libDict[self.__buffer['Series']][self.__buffer['Season']][self.__buffer['Episode']] = Episode# insert Episode
#                            print(self.getName(), ' ', self.getSeasonNr(), ' ', self.getEpisodeNr())
                            self.__resetBuffer()
                        else: #else create Seasoon and add to Series in lib
                            Season = {'Season':self.__buffer['Season']}
                            libDict[self.__buffer['Series']][self.__buffer['Season']] = Season
                    
                    else:    #else create Series and add to lib
                        Series = {'Series':self.__buffer['Series']}
                        libDict[self.__buffer['Series']] = Series
            else:
                self.__resetBuffer()
    
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
 
    def getSeries(self):
        return self.lib.keys()
         
    def getSeasons(self,SeriesName):
        return self.lib[SeriesName].keys()
         
    def getEpisodes(self,SeriesName,Season):
        return self.lib[SeriesName][Season].keys()
       
#==============================================================================
#     def mergeSeries(self,libName,Alternatives):
#         lib = self.__Index[libName]
#         mergedSeries = {'Series':Alternatives[0]}
#         for SeriesName in Alternatives:
#             for Season in self.getSeasons(libName,SeriesName):
#                 if not Season in mergedSeries.keys():
#                     mergedSeries[Season]
#                 
#==============================================================================
        
        