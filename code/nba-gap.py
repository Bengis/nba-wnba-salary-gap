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
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getLxmlDataPlayers(url):
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
url1="http://www.wnba.com/stats/player-stats/#?Season=2016&SeasonType=Regular%20Season&PerMode=Totals"
url2="https://stats.nba.com/leaders/?Season=2016-17&SeasonType=Regular%20Season&PerMode=Totals"
stats=getLxmlDataPlayers(url1)
print(stats)

 


