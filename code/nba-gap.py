# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 12:27:05 2017

@author: Ignacio Bengoechea
"""
from urllib.request import urlopen
from urllib.error import HTTPError
from lxml import html
import numpy as np
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def getNBADataPlayers(url):
 try:
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.get(url)
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "row")))
    content = driver.page_source
    tree = html.fromstring(content)
    driver.close()
 except HTTPError as e:
     return
 try:
    players = tree.xpath('//tbody/tr/td[@class="player"]/a/text()')
    stats=[]
    row=[]
    for i in range(0, 50):
        rowStats = tree.xpath('//tbody/tr[@index="' + str(i) + '"]/td/text()|//tbody/tr[@index="' + str(i) + '"]/td/a/text()')
        row.append(players[i])
        row.append(rowStats[2]) #games
        row.append(rowStats[3]) #minutes
        row.append(rowStats[4]) #points
        row.append(rowStats[16]) #rebounds
        row.append(rowStats[17]) #assists
        row.append(rowStats[18]) #steals
        row.append(rowStats[19]) #blocks
        stats.append(row)
        row=[]
 except Exception as e:
     print('Error gLDP on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
     return stats
 return stats

def getRWNBADataPlayers(url):
 try:
    page = requests.get(url)
    tree = html.fromstring(page.content)
 except HTTPError as e:
     return
 try:
    tempPlayers = tree.xpath('//tbody/tr/td/a/text()')
    stats=[]
    row=[]
    players={}
    rowStats = tree.xpath('//table/tbody/tr/td/text()')
    
    for i in range(0, len(tempPlayers)):
        players[tempPlayers[i]]=i
        row.append(tempPlayers[i])
        games=int(rowStats[i*21+2])
        row.append(games) #games
        row.append(int(float(rowStats[i*21+3])*games)) #minutes
        row.append(int(float(rowStats[i*21+4])*games)) #points
        row.append(int(float(rowStats[i*21+5])*games)) #rebounds
        row.append(int(float(rowStats[i*21+6])*games)) #assists
        row.append(int(float(rowStats[i*21+7])*games)) #steals
        row.append(int(float(rowStats[i*21+8])*games)) #blocks
        row.append(0) #sallary
        row.append(0.0) #sallary/points
        row.append(0.0) #sallary/rebounds
        row.append(0.0) #sallary/assists
        row.append(0.0) #sallary/steals
        row.append(0.0) #sallary/blocks
        
        stats.append(row)
        row=[]
 except Exception as e:
     print('Error gLDP on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
     return stats, players
 return stats, players

def showHeaderStats(stats,gender):
    print(' ',end='\n') 
    print("=====================================", end='\n')
    if gender==0:
        print("Dataset of basic stats of NBA Players", end='\n')
    if gender==1:
        print("Dataset of basic stats of WNBA Players", end='\n')
    print("=====================================", end='\n')
    print(' ',end='\n') 
    header=["player", "games", "minutes", "points", "rebds.", 
             "assists", "steals", "blocks","salary",
             "salary/points","salary/rebounds","salary/assists",
             "salary/steals","salary/blocks"]
    for i in range(0,len(header)):
        print(header[i],end='\t')
        if i==0:
            print('',end='\t')
    print(' ',end='\n') 
    for i in range(0,len(stats)):
        for j in range(0,linelen):
                print(stats[i][j],end='\t')
        print(' ',end='\n')  
        
def getSalaryNBADataPlayers(url,stats, players):
 try:
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.get(url)
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "tablesorter-headerRow")))
     
    content = driver.page_source
    tree = html.fromstring(content) 
 except HTTPError as e:
     return
 try:
    names=tree.xpath('//td[@class="rank-name player noborderright"]/h3/a/text()')
    print(len(names))
    salaries = tree.xpath('//tbody/tr/td/span[@class="info"]/text()')
 except Exception as e:
    print('Error gLDP on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
 
 for i in range(0,len(salaries)):
     try:
         salary=int(salaries[i].replace(",","").replace("$",""))
         player=players[names[i]]
         stats[player][8]=salary
         stats[player][9]=round(salary/stats[player][3],1)
         stats[player][10]=round(salary/stats[player][4],1)
         stats[player][11]=round(salary/stats[player][5],1)
         stats[player][12]=round(salary/stats[player][6],1)
         stats[player][13]=round(salary/stats[player][7],1)
     except Exception as e:
         print('Error gLDP on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

 return stats

def exportCSV(stats, gender):
 try:
     print("Exporting dataset.", end='\n')
     header=["player", "games", "minutes", "points", "rebds.", 
             "assists", "steals", "blocks","salary",
             "salary/points","salary/rebounds","salary/assists",
             "salary/steals","salary/blocks"]
     if gender==0:
         csvfile = "../data/nba-stats_out.csv"
     if gender==1:
         csvfile = "../data/wnba-stats_out.csv"
     with open(csvfile, "w") as output:
         writer = csv.writer(output, lineterminator='\n')
         writer.writerow(header)
         for stat in stats:
             writer.writerow(stat)
     print("Dataset exported to {}.".format(csvfile))
 except Exception as e:
     print('Error eCSV on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
     return 
 return

linelen=14
urlWNBA="https://www.rotowire.com/wnba/player-stats-byseason.php"
urlNBA="https://www.rotowire.com/basketball/player-stats.php"
urlSalaryNBA="http://www.spotrac.com/nba/rankings/"

#urlNBA="https://stats.nba.com/leaders/?Season=2016-17&SeasonType=Regular%20Season&PerMode=Totals"
stats,players=getRWNBADataPlayers(urlNBA)
stats=getSalaryNBADataPlayers(urlSalaryNBA,stats, players)
showHeaderStats(stats,0)
exportCSV(stats, 0)
#stats=getRWNBADataPlayers(urlWNBA)
#showHeaderStats(stats,1)

#exportCSV(stats, 1)