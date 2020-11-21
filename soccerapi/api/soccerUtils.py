import pandas as pd


# class soccerUtils():

def convertData(scrapedData: dict, matchKeyInfo: tuple) -> dict:
    (matchKeysList, dataKeys) = matchKeyInfo
    tmp_dict = {}
    for outerKey in matchKeysList:
        tmp_var = scrapedData

        for innerKey in dataKeys[outerKey]:
            try:
                tmp_var = tmp_var[innerKey]
            except (KeyError, IndexError) as e:
                print('key error, key or index not available')
                tmp_var = None
                break

        tmp_dict[outerKey] = tmp_var

    # match = pd.DataFrame(data=tmp_dict)
    return tmp_dict