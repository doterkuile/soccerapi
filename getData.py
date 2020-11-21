from soccerapi.api import ApiUnibet
import pandas as pd
import numpy as np
import time

api = ApiUnibet()
countryCode = 'NL'
try:
    while True:
        api.parseMatches('NL')
        time.sleep(60)


except KeyboardInterrupt:
    print('interrupted!')

