import csv
import pandas as pd
import comtrade_api
import difflib
 
class FoodLocationFinder:
    _comtrade = comtrade_api.ComtradeAPI()
    
    def __init__(self, dataset):
        data = pd.read_json(dataset)
        l = list(data['results'])
        self._df = pd.DataFrame(l)

    def get_code(self, food):
        regex = ' {} '.format(food)
        result = self._df[self._df['text'].str.contains(regex, case=False)]
        try:
            return list(result['id'])
        except IndexError:
            print("This product doesn't exist.")
            raise
            
    
    def get_biggest_producer(self, food, region):
        try:
            codes = self.get_code(food)
        except IndexError:
            return "Unknown"

        for c in codes:
            df = self._comtrade.get_data(commodity = c, region = region)

            if not df.empty:
                #We've found some data to work with
                df = df[['TradeValue', 'ptTitle', 'ptCode']]
                df = df.ix[df['ptTitle'] != 'World']
                
                result = df.loc[df['TradeValue'].idxmax()]
                return (result['ptCode'], result['ptTitle'])

        #If we get here then none of the codes worked
        return "Unknown"


if __name__ == "__main__":
    finder = FoodLocationFinder('ingredientsHS.json')

    print(finder.get_biggest_producer('apple', 826))
