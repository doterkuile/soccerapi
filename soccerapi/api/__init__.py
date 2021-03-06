import importlib

package = 'soccerapi.api'

Api888Sport = importlib.import_module('.888sport', package).Api888Sport
ApiBet365 = importlib.import_module('.bet365', package).ApiBet365
ApiUnibet = importlib.import_module('.unibet', package).ApiUnibet
soccerUtils = importlib.import_module('.soccerUtils', package)
FootballMatch = importlib.import_module('.FootballMatch', package).FootballMatch
LeagueDatabase = importlib.import_module('.LeagueDatabase', package).LeagueDatabase