# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:03:30 2020
Written by Maria Gonzalez Bocanegra
@author: User
"""
############################## Section 1 ################################### 
## GET every team link in the nba official website 
import requests
import pandas as pd
from bs4 import BeautifulSoup

baseurl = 'https://www.nba.com/teams'

header = {
    'User-Agent': 'https://developers.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes'    
    } # allows to webscrape

r = requests.get('https://www.nba.com/teams')   # page I am requesting data from
soup = BeautifulSoup(r.content, 'lxml') #lxml is the parser

team_profile = soup.find_all('div', class_= 'flex text-sm') #finds the teams' links in the website
team_list =[] #name in line 39 will append here


teamProfile_links = [] #store teams' links

for item in team_profile: # for each team in the list find all links
    for link in item.find_all('a', href=True, text='Profile'): # href is the link to the team #THIS
        teamProfile_links.append('https://www.nba.com' + link['href']) #append the links found to nba.com to go to team website

############################## Section 2 ###################################        
## Get information from the team's nba website (iterate over team links)
PlayerProfile_Links_Main = []
NBA_PlayerList = []
NBA_Team_List = []

for link2 in teamProfile_links:

    #testLink= 'https://www.nba.com/team/1610612738'
        
    r= requests.get(link2, headers=header) #link2
        
    soup= BeautifulSoup(r.content, 'lxml')
    ## Name of team and headcoach
    name = soup.find('div', class_='TeamHeader_name__1i3fv').text.strip() #get the team's name
    headcoach = soup.find('ul', class_='TeamCoaches_list__3EDq-').text.strip()
    
    ## Information on the team (founded, city, arena) (find_next_sibling METHOD)
    d_founded = soup.find('dd') #dummy to find next sibling
    d_city = d_founded.find_next_sibling('dd') #dummy to find next sibling
    d_arena = d_city.find_next_sibling('dd') #dummy to find next sibling
    
    founded = d_founded.text
    city = d_city.text
    arena = d_arena.text
    
    ## Team Statistics (findALL METHOD)
    stats = soup.findAll("div", {"class" : "TeamHeader_rankValue__1pj3i"})
    team_PPG = stats[0].text
    team_RPG = stats[1].text
    team_APG = stats[2].text
    
    ## Number of Championships
    # World Championships Won (Nested Classes)
    world_champ = soup.find(class_='TeamAwards_group__jkS1e').find(class_='TeamAwards_list__1UhSV')
    champs = [] #array to save the championship years
    for trophies in world_champ:
        champs.append(trophies.text)
    
    championships = len(champs) # number of championships won
    
    ## Get Player Roster 
    PlayerProfile_Links=[] #dummy that resets on every team
    roster = soup.findAll("td", {"class" : "primary text"}) # get players name class
    players = []
    for player in roster:
       players.append(player.text) #append the links found to nba.com to go to player website
    
        
    for playerLink in roster: # for each player in the list find all links
        for link3 in playerLink.find_all('a', href=True): # href is the link to the team #THIS
            PlayerProfile_Links.append('https://www.nba.com' + link3['href'])
            PlayerProfile_Links_Main.append('https://www.nba.com' + link3['href'])
            
        
    ############################## Section 2.2 ###################################             
        # Get Player info (iterate over every player in the current team)
    for link4 in PlayerProfile_Links:
            #testLink2 = 'https://www.nba.com/player/1628369/jayson-tatum/'
         
        r= requests.get(link4, headers=header) #link4 in testlink 
        soup= BeautifulSoup(r.content, 'lxml')
        #Player Name
        
        Player_name = soup.findAll('p', class_='PlayerSummary_playerNameText__K7ZXO') #get the team's name
        #print(Player_name)
        FirstName = Player_name[0].text.strip()
        LastName = Player_name[1].text.strip()
        FullName = FirstName +' '+ LastName
            
        ## Player Statistics (findALL METHOD)
        pstats = soup.findAll("p", {"class" : "PlayerSummary_playerStatValue__3hvQY"})
        player_PPG = pstats[0].text
        player_RPG = pstats[1].text
        player_APG = pstats[2].text
    
        ## Player Info
        pinfo = soup.findAll("p", {"class" : "PlayerSummary_playerInfoValue__mSfou"})
        height = pinfo[0].text
        weight = pinfo[1].text
        age = pinfo[4].text
        ## Save Player Info    
        NBA_Player = {
        'Link': link4,
        'Full Name': FullName,
        'Age': age,
        'Height': height,
        'Weight': weight,
        'Player Points Per Game': player_PPG,
        'Player Rebounds Per Game': player_RPG,
        'Player Assists Per Game': player_APG,
        'Player Team': name
        }
        NBA_PlayerList.append(NBA_Player)
        print('Saving: ', NBA_Player['Full Name'])
        
    ############################## Section 2.3 ###################################  
    ## Save NBA Team Information        
    NBA_Team = {
        'Link': link2,
        'Name': name,
        'Date Founded': founded,
        'City': city,
        'Arena': arena,
        'Headcoach': headcoach,
        'Number of Championship': championships,
        'Points Per Game': team_PPG,
        'Rebounds Per Game': team_RPG,
        'Assists Per Game': team_APG,
        'Roster': players
        }

    NBA_Team_List.append(NBA_Team)
    print('Saving: ', NBA_Team['Name'])
    

df = pd.DataFrame(NBA_Team_List)
# print(df)
df.to_excel('NBA_Teams.xlsx',)
df2 = pd.DataFrame(NBA_PlayerList)
df2.to_excel('NBA_Players.xlsx')

df.to_csv('NBA_Teams.csv')
df2.to_csv('NBA_Players.csv')
