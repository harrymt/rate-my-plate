"""
Comtrade API Extract
Nathan Goldschlag
December 17, 2014
Version 1.0
Written in Python 2.7

This python program extracts trade data from the Comtrade API. 

"""
## IMPORT LIBRARIES
import pickle
import requests
import datetime
import os 
from os import listdir
from os.path import isfile, join
import pandas as pd


class ComtradeAPI:
    _url = 'http://comtrade.un.org/api/get?'
    _calls_in_hour = 0
    _first_call = None
    _max_calls = 95
    
    _init = False
    
    def get_data(self, commodity = 'AG2', region = '826'):
        
        if self._first_call is None:
            self._first_call = datetime.datetime.now()
        
        s = self._url + 'max=5000&'
        s += 'type=C&'
        s += 'freq=A&'
        s += 'px=HS&'
        s += 'ps=2015,2014&'
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
    com.getBiggestProducer(commodity='0101')

'''
# read in JSON file of country codes as a list
cids = pd.read_csv('UN Comtrade Country List.csv', keep_default_na=False, encoding="ISO-8859-1")
#print(cids['ctyCode'])
#f = open('reporterAreas.json','r')
#areas = json.load(f)
countryIDs = []
for i in cids['ctyCode']:
    countryIDs.append(str(i))
countryIDs.remove('0')
print(countryIDs)

# define the rg parameter, trade flow (default = all): The most common area 1 (imports) and 2 (exports)
#time.sleep(3600)
# track the number of calls made
t0 = time.time()
callsThisHour = 1

baseurl = 'http://comtrade.un.org/api/get?max=50000&type=C&freq=A&px=HS&ps=2015,2014&r={0}&p=all&rg=1&cc=AG2&fmt=csv'
for c in countryIDs:
    print('country:', c, '\n', 'time this hour:', time.time()-t0, '\n','calls this hour:',callsThisHour)
    # create the URL and submit url
    url= baseurl.format(c)
    apiResponse = requests.get(url)
    # parse return output
    csv = apiResponse.content.decode('utf-8')
    print(csv)

    # store output
    lines = csv.split('\r\n')
    f = open('comtrade_'+c+'.csv','w')
    for line in lines:
        f.write(line+'\n')
    f.close()

    # track the number of calls this hour
    callsThisHour+=1
    time.sleep(3)
    timePassed = time.time() - t0
    
    # if hour limit reached, sleep for the remainer of the hour
    if timePassed<3600 and callsThisHour>98:
        print('sleeping...')
        time.sleep(3700-timePassed)
        print('awake')
        # reset hour and number of calls
        t0=time.time()
        callsThisHour=0


'''
