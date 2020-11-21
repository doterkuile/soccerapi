import re
import pandas as pd
from pathlib import Path
from .base import ApiKambi


class ApiUnibet(ApiKambi):
    """ The ApiBase implementation for unibet.com """
    matchKeyList = 'ID Date Competition HomeTeam AwayTeam HomeWin Draw AwayWin State'.split()
    liveKeyList = 'ID Time HomeWin Draw AwayWin '.split()  # HomeWin Draw AwayWin State
    # HomeWin Draw AwayWin State
    projectDir = Path('.')

    def __init__(self):
        self.name = 'unibet'
        self.base_url = (
            'https://eu-offering.kambicdn.org/'
            'offering/v2018/ub/listView/football'
        )
        self.parsers = [
            self._full_time_result,
            self._both_teams_to_score,
            self._double_chance,
        ]

        self.countryURLS = {
            'NL': 'netherlands',
            'UK': 'england/premier_league',
            'SP': 'spain/la_liga',
            'IT': 'italy/serie_a',
            'GE': 'germany/bundesliga',
            'FR': 'france/ligue_1',
            'CL': 'champions_league',
            'EL': 'europa_league'
        }
        self.matchKeys = self.setupKeys()
        self.liveKeys = self.setupLiveKeys()


    def setupKeys(self) -> tuple:

        matchInfo = {self.matchKeyList[0]: 'event id'.split(),  # MatchID
                     self.matchKeyList[1]: 'event start'.split(),  # Date
                     self.matchKeyList[2]: 'event group'.split(),  # Competition
                     self.matchKeyList[3]: 'event homeName'.split(),  # HomeTeam
                     self.matchKeyList[4]: 'event awayName'.split(),  # AwayTeam
                     self.matchKeyList[5]: ['betOffers', 0, 'outcomes', 0, 'odds'],  # HomeWin
                     self.matchKeyList[6]: ['betOffers', 0, 'outcomes', 1, 'odds'],  # Draw
                     self.matchKeyList[7]: ['betOffers', 0, 'outcomes', 2, 'odds'],  # AwayWin
                     self.matchKeyList[8]: 'event state'.split(),  # AwayTeam
                     }
        return (self.matchKeyList, matchInfo)

    def setupLiveKeys(self) -> tuple:
        liveInfo = {self.liveKeyList[0]: 'event id'.split(),
                    self.liveKeyList[1]: 'liveData matchClock minute'.split(), #Time
                    self.liveKeyList[2]: ['betOffers', 0, 'outcomes', 0, 'odds'],  # HomeWin
                    self.liveKeyList[3]: ['betOffers', 0, 'outcomes', 1, 'odds'],  # Draw
                    self.liveKeyList[4]: ['betOffers', 0, 'outcomes', 2, 'odds'],  # AwayWin
                    }
        return(self.liveKeyList, liveInfo)

    def competition(self, url: str) -> str:
        re_unibet = re.compile(
            r'https?://www\.unibet\.\w{2,3}/'
            'betting/sports/filter/[0-9a-zA-Z/]+/(?:matches)?/?'
        )
        if re_unibet.match(url):
            return '/'.join(url.split('/')[7:9])
        else:
            msg = f'Cannot parse {url}'
            raise ValueError(msg)


    def saveAsCsv(self, df: pd.DataFrame, fileName: str):
        """Save as csv file"""
        matchFile = fileName + '.csv'
        liveFile = fileName + '_Live.csv'
        matchFilePath = self.projectDir / 'dataFiles' / 'matchData' / matchFile
        liveFilePath = self.projectDir / 'dataFiles' / 'liveData' / liveFile
        df.to_csv(matchFilePath, index =False)

