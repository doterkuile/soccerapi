import json
import requests

import pathlib
from pathlib import Path
import yaml

class LeagueDatabase():

    league: str
    league_id: int
    dataBaseFile: str
    dataBase: dict
    seasons: list
    dataHeaders: dict


    def __init__(self, yamlFile: str):
        self.config(yamlFile)

        self.loadDataBaseFile(self.dataBaseFile)


    def config(self, filename: str):
        configFile = self.loadFile(filename)


        self.league = configFile['league']
        self.league_id = configFile['league_id']
        self.dataBaseFile = "." + configFile['databaseFile']
        self.seasons = configFile['seasons']
        self.dataHeaders = {
            'x-rapidapi-host': configFile['api-host'],
            'x-rapidapi-key' : configFile['api-key']
        }


    def loadDataBaseFile(self, fileName: str):
        try:
            with open(fileName) as file:
                self.dataBase = json.load(file)
        except FileNotFoundError:
            print("Database does not exist yet")
            self.dataBase = {}
            pass

    def saveDataBaseFile(self):
        try:
            with open(self.dataBaseFile, 'w') as file:
                json.dump(self.dataBase, file)
        except FileNotFoundError:
            print("Database does not exist yet")
            pass



    def loadFile(self, fileName: str) -> dict:
        with open(fileName, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        return config

    def seasonsToRounds(self,seasonFixtures: list) -> dict:
        roundFixtures = {}
        for fixture in seasonFixtures:

            round = fixture['league']['round'].split('-')[-1]
            fixture.pop('league',None)
            if round not in roundFixtures:
                roundFixtures[round] = [fixture]
            else:
                roundFixtures[round].append(fixture)

        return roundFixtures

    def requestSeasons(self, seasons: list):
        for season in seasons:
            if str(season) not in self.dataBase:
                data = self.requestSeasonFixtures(season)
                self.dataBase[season] = {
                    'rounds': self.seasonsToRounds(data)
                }



    def requestSeasonFixtures(self, season: str):

        querySpecificStr = 'fixtures?season=' + str(season) + '&league=' + str(self.league_id)
        url = self.dataHeaders['x-rapidapi-host'] + querySpecificStr
        data = self.requestData(url)

        return data


    def requestData(self, url: str):

        response = requests.request('GET', url, headers=self.dataHeaders)
        return response.json()['response']

    def addFinalTable(self, seasons: list):

        for season in seasons:
            seasonKey = str(season)
            if seasonKey in self.dataBase:
                if 'teams' not in self.dataBase[seasonKey]:
                    teams = []
                    finalTable = {}
                    table = self.requestSeasonStanding(season)

                    for place in table:
                        team = {
                            'id': place['team']['id'],
                            'name': place['team']['name'],
                        }
                        teams.append(team)
                        finalTable[place['team']['id']] = place['rank']
                    self.dataBase[seasonKey]['teams'] = teams
                    self.dataBase[seasonKey]['finalTable'] = finalTable




    def requestSeasonStanding(self,season: str):
        querySpecificStr = '/standings?league=' + str(self.league_id) + '&season=' + str(season)
        url = self.dataHeaders['x-rapidapi-host'] + querySpecificStr
        data = self.requestData(url)[0]['league']['standings'][0]
        return data
