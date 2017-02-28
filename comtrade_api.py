
## IMPORT LIBRARIES
import requests
import datetime
import pandas as pd


class ComtradeAPI:
    _url = 'http://comtrade.un.org/api/get?'
    _calls_in_hour = 0
    _first_call = None
    _max_calls = 95
    
    _init = False
    
    def get_data(self, commodity = 'AG2', region = '826'): #UK by default

        if self._first_call is None:
            self._first_call = datetime.datetime.now()
        
        s = self._url + 'max=5000&'
        s += 'type=C&'
        s += 'freq=A&'
        s += 'px=HS&'
        s += 'ps=2015&'
        s += 'r={}&'.format(region)
        s += 'p=all&'
        s += 'rg=1&'
        s += 'cc={}&'.format(commodity)
        s += 'fmt=json'
    
        if (self._first_call < datetime.datetime.now() + datetime.timedelta(hours=-1)):
            #We've waited long enough
            self._first_call = datetime.datetime.now()
            self._calls_in_hour = 0
        else:
            #We're within the time
            if (self._calls_in_hour >= self._max_calls):
                #Had too many
                raise Exception("You have made too many API calls")
            else:
                #OK to use API
                apiResponse = requests.get(s)
                data = apiResponse.json()
                data = data['dataset']
                self._calls_in_hour += 1

                df = pd.DataFrame(data)
                return df
        

if __name__ == '__main__':
    com = ComtradeAPI()
    print(com.get_data(commodity='0806'))

