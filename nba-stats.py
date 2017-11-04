# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 12:27:05 2017

@author: Ignacio Bengoechea
"""
from urllib.request import urlopen
from urllib.error import HTTPError
from lxml import html
import numpy as np
import requests
import sys

def getLxmlListPlayers(url):
 try:
    page = requests.get(url)
    tree = html.fromstring(page.content)
 except HTTPError as e:
     return
 try:
     players = tree.xpath('//td[@data-append-csv]//@href')
 except AttributeError as e:
     print('Error gLLP on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
     return None
 return players

def getLxmlDataPlayer(url):
 try:
    page = requests.get(url)
    tree = html.fromstring(page.content)
 except HTTPError as e:
     return
 try:
     stats=[]
     for i in range(0,len(inverseSeasons)):
         stats.append([inverseSeasons[i],0,0,0.0,0.0,0.0,0.0,0.0,0.0])
     season = tree.xpath('//tbody/tr/td[not(contains(@a,"TOT"))]/../th[@data-stat="season"]/a/text()|//tbody/tr/th[not(contains(@a,"TOT"))]/../th[@data-stat="season"]/a/strong/text()')
     g = tree.xpath('//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="g"]/text()|//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="g"]/strong/text()')
     mpg = tree.xpath('//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="mp_per_g"]/text()|//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="mp_per_g"]/strong/text()')
     ptspg = tree.xpath('//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="pts_per_g"]/text()|//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="pts_per_g"]/strong/text()')
     trbpg = tree.xpath('//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="trb_per_g"]/text()|//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="trb_per_g"]/strong/text()')
     astpg = tree.xpath('//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="ast_per_g"]/text()|//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="ast_per_g"]/strong/text()')
     stlpg = tree.xpath('//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="stl_per_g"]/text()|//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="stl_per_g"]/strong/text()')
     blkpg = tree.xpath('//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="blk_per_g"]/text()|//tbody/tr/td[not(contains(@a,"TOT"))]/../td[@data-stat="blk_per_g"]/strong/text()')
     tempStats=np.column_stack((season,g[:len(season)],mpg[:len(season)],ptspg[:len(season)],trbpg[:len(season)],astpg[:len(season)],
                                     stlpg[:len(season)],blkpg[:len(season)]))
     for i in range(0,len(season)):
         j=seasons[tempStats[i][0]]
         for k in range(1,linelen-1):
             if (k==1):
                 stats[j][k]=1
                 stats[j][k+1]=int(tempStats[i][k])+stats[j][k+1]
             else:
                 stats[j][k+1]=round(float(tempStats[i][k])+stats[j][k+1],1)
 except Exception as e:
     print('Error gLDP on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
     return stats
 return stats
   

def showHeaderStats(stats):
    print("Dataset of stats of all spanish NBA players per season, adjusted to 240 minutes", end='\n')
    print(' ',end='\n') 
    header=["season", "players", "games", "minutes", "points", "rebds.", 
             "assists", "steals", "blocks"]
    for name in header:
        print(name,end='\t')
    print(' ',end='\n') 
    for i in range(0,len(seasons)):
        if (stats[i][1]!=0):
            for j in range(0,linelen):
                print(stats[i][j],end='\t')    
            print(' ',end='\n')  
        
def createTeamStats():
    teamStats=[]
    for i in range(0,len(inverseSeasons)):
         teamStats.append([inverseSeasons[i],0,0,0.0,0.0,0.0,0.0,0.0,0.0])
    return teamStats

def addTeamStats(stats, teamStats):
 try:
     for i in range(0,len(seasons)):
         for k in range(1,linelen):
             if (k==1):
                 teamStats[i][k]=stats[i][k]+teamStats[i][k]
             else:
                 teamStats[i][k]=round(stats[i][k]+teamStats[i][k],1)
 except Exception as e:
     print('Error aTS on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
     return teamStats
 return teamStats
        
def addHeader(stats):
     header=["season", "games", "minutes", "points", "total rebounds", 
             "assists", "steals", "blocks"]
     stats= np.insert(stats,0,header)
     return stats
     
def listSeasons():
    seasons = {}
    inverseSeasons = {}
    año1=1984
    año2=85
    total=2017-año1
    for i in range(0,total):
        seasons[str(año1+i+1)+'-'+str((año2+i+1)%100).zfill(2)] = i
        inverseSeasons[i]=str(año1+i+1)+'-'+str((año2+i+1)%100).zfill(2)
    return seasons, inverseSeasons

def changePlayers(players):
    players.remove('/players/b/bryanwa01.html')
    players.remove('/players/s/szczewa02.html')
    players.append('/players/m/mirotni01.html')
    players.append('/players/i/ibakase01.html')
    return players

def adjustStats(teamStats):
 try:
     minutes=48*5
     for i in range(0,len(seasons)):
         ratio=0.0
         for k in range(3,linelen):
            if (k==3 and teamStats[i][k]!=0.0):
                 ratio=(minutes/teamStats[i][k])
                 teamStats[i][k]=round(teamStats[i][k]*ratio,1)
            else:
                 teamStats[i][k]=round(teamStats[i][k]*ratio,1) 
                 
 except Exception as e:
     print('Error aS on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
     return teamStats
 return teamStats

print("Loading data. Please wait.")        
linelen=9
seasons, inverseSeasons=listSeasons()
urlBase="https://www.basketball-reference.com/friv/birthplaces.fcgi?country=ES&state="
print("Loading list of players of Spain:")
players= getLxmlListPlayers(urlBase)
players=changePlayers(players)
urlBase="https://www.basketball-reference.com"
teamStats=createTeamStats()
i=0
for player in players:
    print("Loading player:{}".format(i+1))
    stats=getLxmlDataPlayer(urlBase + player)
    teamStats=addTeamStats(stats, teamStats)
    i+=1
teamStats=adjustStats(teamStats)
showHeaderStats(teamStats)



 


