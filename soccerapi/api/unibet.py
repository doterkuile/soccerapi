import re
import pandas as pd

from .base import ApiKambi


class ApiUnibet(ApiKambi):
    """ The ApiBase implementation for unibet.com """

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
        self.liveParsers = [
            self._live_result_
            # self._time_
        ]

        self.countryURLS = {
                'NL' : 'netherlands',
                'UK' : 'england/premier_league',
                'SP' : 'spain/la_liga',
                'IT' : 'italy/serie_a',
                'GE' : 'germany/bundesliga',
                'FR' : 'france/ligue_1',
                'CL' : 'champions_league',
                'EL' : 'europa_league'
            }

        self.liveMatch = pd.DataFrame([],columns='Home Draw Away Time'.split( ))
        print(self.liveMatch)

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
