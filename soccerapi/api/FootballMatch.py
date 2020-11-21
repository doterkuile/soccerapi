


class FootballMatch():

    matchInfo = {}
    liveInfo = {}
    matchInfoKeys = 'Date Competition HomeTeam AwayTeam HomeWin Draw AwayWin State'.split()
    matchLiveKeys = 'Time HomeWin Draw AwayWin'.split()
    matchId: int
    def __init__(self, matchData: dict):
        try:
            self.addMatchId(matchData['ID'])
        except KeyError:
            print('No matchID found')

        for key in self.matchInfoKeys:
            try:
                self.matchInfo[key] = matchData[key]
            except KeyError:
                print("KeyError: {} does not exist in the given matchData, data might be incomplete")




    def addMatchData(self, data: dict):
        pass

    def addLiveData(self, liveData:dict):
        del liveData['ID']
        self.liveInfo = liveData

    def isLive(self) -> bool:

        if self.matchInfo['State'] == 'STARTED':
            return True

        return False

    def addMatchId(self, matchId: int):
        self.matchId = matchId


