import abc
from typing import Dict, List, Tuple
import pandas as pd
from soccerapi.api import soccerUtils
import requests
import numpy as np
from soccerapi.api import FootballMatch
import copy
import json
from pathlib import Path



class ApiBase(abc.ABC):
    """ The Abstract Base Class on which every Api[Boolmaker] is based on. """

    projectDir = Path('.')


    @abc.abstractmethod
    def _requests(self, competition: str, **kwargs) -> Tuple:
        """ Perform requests to site and get data_to_parse """
        pass

    @abc.abstractmethod
    def saveAsCsv(self, df: pd.DataFrame, fileName: str):
        """save matches to csv files"""
        pass


    @abc.abstractmethod
    def competition(self, url: str) -> str:
        """ Get the competition from url.
        First check it validity using regex,then exstract competition from it
        """
        pass
    @abc.abstractmethod
    def setupKeys(self) -> tuple:
        """setup keys for parsing data of matches"""
        pass

    @abc.abstractmethod
    def setupLiveKeys(self) -> tuple:
        """setup keys for parsing data of matches"""
        pass


    def odds(self, url: str) -> List:
        """ Get odds from country-league competition or from url """

        odds = []
        competition = self.competition(url)
        data_to_parse = self._requests(competition)


        for data, parser in zip(data_to_parse, self.parsers):
            try:
                odds.append(parser(data))
            except NoOddsError:
                # sometimes some odds categories aren't avaiable
                pass

        for category in odds[1:]:
            for i, event in enumerate(category):
                odds[0][i] = {**odds[0][i], **event}

        # If no odds are found the result from:
        # - Kambi based api is [[], [], []]
        # - bet365 is []
        if len(sum(odds, [])) > 0:
            return odds
        else:
            msg = f'No odds in {url} have been found.'
            raise NoOddsError(msg)

    def parseLiveData(self, countryCode: str) -> pd.DataFrame:
        """parse live data: Time, Home Draw Away, put in dataframe and then plot"""

        matchList = self.parseMatchData(countryCode)
        for i in range(1):

            match = soccerUtils.convertData(matchList[i],self.setupLiveKeys())

            outside = [match['ID'][0],match['ID'][0], match['ID'][0],match['ID'][0]]
            inside = 'Time HomeWin Draw AwayWin'.split()
            hier_index = list(zip(outside,inside))
            hier_index = pd.MultiIndex.from_tuples(hier_index)
            values = np.matrix([match['Time'], match['HomeWin'],match['Draw'],match['AwayWin']])
            df = pd.DataFrame(values, index=hier_index)

        return df

    def createDataFrame(self, country_code:str=None) -> pd.DataFrame:
        """ Return dataframe containing all matches"""
        matchData = pd.DataFrame()
        data = self.parseMatchData(country_code)

        for i in range(len(data)):
            match = pd.DataFrame(data=soccerUtils.convertData(data[i],self.setupKeys()))
            testmatch = FootballMatch.FootballMatch(soccerUtils.convertData(data[i],self.setupKeys()))
            print(testmatch.matchInfo)
            matchData = pd.concat([matchData, match])

        return matchData

    def parseMatches(self, country_code:str=None):
        """ Return dataframe containing all matches"""
        data = self.parseMatchData(country_code)
        self.matches = self.loadDataFile()
        for event in data:
            match = FootballMatch.FootballMatch(soccerUtils.convertData(event, self.setupKeys()))
            if str(match.matchId) not in self.matches:
                self.matches[str(match.matchId)] = copy.deepcopy(match.matchInfo)
            savedMatch = self.matches[str(match.matchId)]

            if match.isLive():
                print('match is live')
                liveData = soccerUtils.convertData(event, self.setupLiveKeys())
                match.addLiveData(liveData)
                if 'LiveInfo' not in savedMatch:
                    savedMatch['LiveInfo'] = {}
                    for key in match.liveInfo:
                        savedMatch['LiveInfo'][key] = []
                        savedMatch['LiveInfo'][key].append(match.liveInfo[key])
                else:
                    for key in savedMatch['LiveInfo']:
                        savedMatch['LiveInfo'][key].append(match.liveInfo[key])

        self.saveDataFile(self.matches)

    def loadDataFile(self) -> dict:
        datafile = self.projectDir / 'dataFiles' / 'matchData' / 'data.json'
        try:
            with open(datafile, 'r') as fp:
                data = json.load(fp)
        except FileNotFoundError:
            data = {}
        return data

    def saveDataFile(self, data: dict):
        datafile = self.projectDir / 'dataFiles' / 'matchData' / 'data.json'
        with open(datafile, 'w') as fp:
            json.dump(data, fp)


    def parseMatchData(self, country_code: str=None) -> List:

        data = []
        competition = ""

        try:
            competition = self.countryURLS[country_code]
        except KeyError:
            if not country_code == None:
                print('Not a valid country code, cannot return matches')
                return data
        try:
            data = self._requests(competition)[0]['events']
        except KeyError:
            print("KeyError: No events retrieved from the site")
            return data

        return data


    def getMatchIds(self, country_code:str=None) -> list:
        """Get the match id's of current matches"""
        # competition = self.competition(url)
        matches = []

        competition = ""
        # print(self.countryURLS[country_code])

        try:
            competition = self.countryURLS[country_code]
        except KeyError:
            if not country_code == None:
                print('Not a valid country code, cannot return matches')
                return matches

        data = self._requests(competition)[0]
        for event in data['events']:
            matches.append(
                {
                    'matchId': event['event']['id'],
                    'homeTeam': event['event']['homeName'],
                    'awayTeam': event['event']['awayName'],
                    'state': event['event']['state'],

                }
            )
        if len(matches) == 0:
            print("No matches found")

        return matches





class ApiKambi(ApiBase):
    """888sport, unibet and other use the same CDN (eu-offering.kambicdn)
    so the requetsting and parsing process is exaclty the same.
    The only thing that chage is the base_url and the competition method"""

    @staticmethod
    def _full_time_result(data: Dict) -> List:
        """ Parse the raw json requests for full_time_result """

        odds = []



        for event in data['events']:
            if event['event']['state'] == 'STARTED':

                continue
            try:
                full_time_result = {
                    '1': event['betOffers'][0]['outcomes'][0].get('odds'),
                    'X': event['betOffers'][0]['outcomes'][1].get('odds'),
                    '2': event['betOffers'][0]['outcomes'][2].get('odds'),
                }
            except IndexError:
                full_time_result = None

            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'full_time_resut': full_time_result,
                }
            )
        return odds

    @staticmethod
    def _both_teams_to_score(data: Dict) -> List:
        """ Parse the raw json requests for both_teams_to_score """

        odds = []
        for event in data['events']:
            if event['event']['state'] == 'STARTED':

                continue
            try:
                both_teams_to_score = {
                    'yes': event['betOffers'][0]['outcomes'][0].get('odds'),
                    'no': event['betOffers'][0]['outcomes'][1].get('odds'),
                }
            except IndexError:
                both_teams_to_score = None
            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'both_teams_to_score': both_teams_to_score,
                }
            )
        return odds

    @staticmethod
    def _double_chance(data: Dict) -> List:
        """ Parse the raw json requests for double chance """

        odds = []
        for event in data['events']:
            if event['event']['state'] == 'STARTED':
                continue
            try:
                double_chance = {
                    '1X': event['betOffers'][0]['outcomes'][0].get('odds'),
                    '12': event['betOffers'][0]['outcomes'][1].get('odds'),
                    '2X': event['betOffers'][0]['outcomes'][2].get('odds'),
                }
            except IndexError:
                double_chance = None
            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'double_chance': double_chance,
                }
            )
        return odds

    def _requests(self, competition: str, market: str = 'IT') -> Tuple[Dict]:
        """Build URL starting from country and league and request data for
        - full_time_result
        - both_teams_to_score
        - double_chance
        """
        s = requests.Session()
        base_params = {'lang': 'en_US', 'market': market}
        url = '/'.join([self.base_url, competition]) + '.json'

        return (
            # full_time_result      12579
            s.get(url, params={**base_params, 'category': 12579}).json(),
            # both_teams_to_score   11942
            s.get(url, params={**base_params, 'category': 11942}).json(),
            # double_chance         12220
            s.get(url, params={**base_params, 'category': 12220}).json(),
        )


class NoOddsError(Exception):
    """ No odds are found. """
