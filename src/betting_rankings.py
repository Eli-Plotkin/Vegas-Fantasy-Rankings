from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import openpyxl
import time
from bs4 import BeautifulSoup


class bettingFantasyRankings():
    def __init__(self):
        self.driver = None
        try:
            self.options = webdriver.ChromeOptions()
            self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.options.add_experimental_option("useAutomationExtension", False)
        except:
            print("Error setting up options")
        
        try:
            self.driver = webdriver.Chrome(options=self.options)
        except Exception as e: 
            print("Error creating webdriver instance")
        
    def getPlayerData(self, playerName = str, playerType = str):
        firstName, lastName = playerName.split(" ", 1)

        url = f"https://www.bettingpros.com/nfl/odds/player-futures/{firstName}-{lastName}/"
        self.driver.get(url)

        time.sleep(2)
        

        self.driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(1)


        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        oddSections = soup.find_all('div', class_ = "flex odds-offer")

        self.recOver = "Not found"
        self.recUnder = "Not found"
        self.recYardsOver = "Not found"
        self.recYardsUnder = "Not found"
        self.rushYardsOver = "Not found"
        self.rushYardsUnder = "Not found"
        self.recTDOver = "Not found"
        self.recTDUnder = "Not found"
        self.rushTDOver = "Not found"
        self.rushTDUnder = "Not found"


        for section in oddSections:
            title = section.find('div').find('div').find('span').text 

            if title == "Total Receptions":
                odds = section.find_all('span', class_ = "typography odds-cell__line")
                self.recOver = odds[0].text
                self.recUnder = odds[1].text

            if title == "Total Receiving Yards":
                odds = section.find_all('span', class_ = "typography odds-cell__line")
                self.recYardsOver = odds[0].text
                self.recYardsUnder = odds[1].text


            if title == "Total Receiving Touchdowns":
                odds = section.find_all('span', class_ = "typography odds-cell__line")
                self.recTDOver = odds[0].text
                self.recTDUnder = odds[1].text
            
            if title == "Total Rushing Yards":
                odds = section.find_all('span', class_ = "typography odds-cell__line")
                self.rushYardsOver = odds[0].text
                self.rushYardsUnder = odds[1].text

            if title == "Total Rushing Touchdowns":
                odds = section.find_all('span', class_ = "typography odds-cell__line")
                self.rushTDOver = odds[0].text
                self.rushTDUnder = odds[1].text


        return {
                "playerName": playerName,
                "receptions": (self.recOver, self.recUnder),
                "receivingYards": (self.recYardsOver, self.recYardsUnder),
                "receivingTouchdowns": (self.recTDOver, self.recTDUnder),
                "rushingYards": (self.rushYardsOver, self.rushYardsUnder), 
                "rushingTouchdowns": (self.rushTDOver, self.rushTDUnder)
            }
            

    def getAllPlayerData(self, fileName):
        file = open(fileName, 'r')

        allPlayerData = []
        for name in file.readlines():
            data = self.getPlayerData(name)
            allPlayerData.append(data)

        return allPlayerData
    
    def calcFantasyPoints(self, player = tuple):
        rec = player["receptions"][0]
        recYards = player["receivingYards"][0]
        recTDs = player["receivingTouchdowns"][0]
        rushYards = player["rushingYards"][0]
        rushTDs = player["rushingTouchdowns"][0]

        if rec == "Not found":
            rec = 0
        else:
            list = rec.split()
            if list[0] == "O" or list[0] == "U":
                rec = list[1]
        if recYards == "Not found":
            recYards = 0
        else:
            list = recYards.split()
            if list[0] == "O" or list[0] == "U":
                recYards = list[1]
        if recTDs == "Not found":
            recTDs = 0
        else:
            list = recTDs.split()
            if list[0] == "O" or list[0] == "U":
                recTDs = list[1]
        if rushYards == "Not found":
            rushYards = 0
        else:
            list = rushYards.split()
            if list[0] == "O" or list[0] == "U":
                rushYards = list[1]
        if rushTDs == "Not found":
            rushTDs = 0
        else:
            list = rushTDs.split()
            if list[0] == "O" or list[0] == "U":
                rushTDs = list[1]

        
        return 0.5*float(rec) + 0.1*(float(recYards) + float(rushYards)) + 6*(float(rushTDs) + float(recTDs))
    

    def outputAllData(self, inputFile):
        data = self.getAllPlayerData(inputFile)
        outputFile = open('output.txt', 'w')
        for player in data:
            outputFile.write(player["playerName"] + " stats:\n")
            outputFile.write("Receptions: " + player["receptions"][0] + ", " + player["receptions"][0] + "\n")
            outputFile.write("Receiving Yards: " + player["receivingYards"][0] + ", " + player["receivingYards"][1] + "\n")
            outputFile.write("Receiving Touchdowns: " + player["receivingTouchdowns"][0] + ", " 
                             + player["receivingTouchdowns"][1] + "\n")
            outputFile.write("Rushing Yards: " + player["rushingYards"][0] + ", " 
                             + player["rushingYards"][1] + "\n")
            outputFile.write("Rushing Touchdowns: " + player["rushingTouchdowns"][0] + ", " 
                             + player["rushingTouchdowns"][1] +"\n")
            fPts = str(self.calcFantasyPoints(player))
            outputFile.write("Fantasy Points: " + fPts + "\n")
            outputFile.write("\n")
        
        outputFile.close()




        



