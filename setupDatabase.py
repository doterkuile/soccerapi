from pathlib import Path
from soccerapi.api import LeagueDatabase
import json

def main():
    projectDir = Path('.')
    configFile = projectDir / "config" / "eredivisie.yaml"
    database = LeagueDatabase(configFile)

    # saveFile = True
    seasons = [2011]

    # Setup seasons
    database.requestSeasons(database.seasons)

    # Setup final table for each season
    database.addFinalTable(database.seasons)

    # Save file
    if saveFile:
        database.saveDataBaseFile()

def requestTeamStanding():
    projectDir = Path('.')
    configFile = projectDir / "config" / "eredivisie.yaml"
    database = LeagueDatabase(configFile)
    querySpecificStr = '/standings?league=88&season=2018'
    url = database.dataHeaders['x-rapidapi-host'] + querySpecificStr
    data = database.requestData(url)
    return data

def teamstandings(data):



    table = data[0]['league']['standings'][0]
    teams = []
    finalTable = {}
    for place in table:
        team = {
            'id': place['team']['id'],
            'name': place['team']['name'],
        }
        teams.append(team)
        finalTable[place['team']['id']] = place['rank']

    print("finaTable and Rank")

def loadFile(fileName:str):
    data = []
    try:
        with open(fileName) as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Database does not exist yet")
        data = []
        pass
    return data

def saveFile(fileName:str, data):
    with open(fileName, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()
    # datafile = './dataFiles/matchData/eredivisie.json'
    # data = loadFile(datafile)
    # print("hoi")




