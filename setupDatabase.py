import requests
from pathlib import Path
import json

def seasonsToRounds(seasonFixtures: list) -> dict:
    roundFixtures = {}
    for fixture in seasonFixtures:
        round = fixture['league']['round'].split('-')[-1]
        if round not in roundFixtures:
            roundFixtures[round] = [fixture]
        else:
            roundFixtures[round].append(fixture)

    return roundFixtures


projectDir = Path('.')
saveFile: bool = True

league = ['eredivisie']
seasons = ['2018']
baseUrl = "https://v3.football.api-sports.io/"
querystring = {"timezone": "Europe/Amsterdam"}

headers = {
    'x-rapidapi-host': baseUrl,
    'x-rapidapi-key': "40e5783128da0bd975e0795e297b6341",

}

for season in seasons:
    querySpecificUrl = "fixtures?season=2018&league=88"
    url = baseUrl + querySpecificUrl

    response = requests.request("GET", url, headers=headers)

    roundData = response.json()
    roundData = seasonsToRounds(response.json()["response"])
    data = {
        'season': season,
        'fixtures': response.json()["response"],
    }


fileName = querySpecificUrl + ".json"
fileName = fileName.replace("/", "-").replace("&","-").replace("=","-").replace("?","-")
datafile = projectDir / 'dataFiles' / 'matchData' / fileName
with open(datafile, 'w') as fp:
    json.dump(data, fp)


