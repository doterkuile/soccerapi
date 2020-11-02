# from soccerapi.api import Api888Sport
from soccerapi.api import ApiUnibet
import pandas as pd
import time
import matplotlib.pyplot as plt
# %matplotlib inline
from IPython.display import display, clear_output

# from soccerapi.api import ApiBet365

api = ApiUnibet()
# url = 'https://www.unibet.com/betting/sports/filter/football/netherlands/eredivisie/matches'
# url = 'https://www.unibet.com/betting/sports/filter/football/netherlands/knvb_beker/matches'
# matchId = 1006925420
url = 'https://www.unibet.com/betting/sports/filter/football/netherlands/eerste_divisie/matches'

# url = 'https://www.unibet.com/betting/sports/filter/football/italy/tim_cup/matches'
# odds = api.parseLiveData(url, matchId)
# print(odds)
# df = pd.DataFrame.from_dict(odds,orient='index')

homeTeam = []
awayTeam = []
draw     = []
matchTime = []
matchId = 1006651618
odds = api.parseLiveData(url, matchId)
df = pd.DataFrame.from_dict(odds,orient='index')


fig = plt.figure()
axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# axes.clear()
plt.style.use('seaborn-dark')

odds['1'] = 2
# homePlot = axes.plot(matchTime, homeTeam)
for i in range(30):
    try:
        homeTeam.append(odds['1'])
        matchTime.append(i)
    except KeyError:
        continue

    # axes.cla()
    axes.plot(matchTime, homeTeam,'r')
    display(fig)
    clear_output(wait = True)
    time.sleep(0.2)
    plt.show()


#     time.sleep(60)




# odds = api.odds(url)
# try:
#     api.liveMatch['Home'].append(odds[0]['full_time_result']['1'])
# except NoKeyError:
#     api.liveMatch['Home'].append(0)
# api.liveMatch['Home'].append(odds[0][0]['full_time_result']['1'])

      # ['Home'].append())