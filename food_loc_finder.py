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
        result = self._df[self._df['text'].str.contains(food, case=False)]
        try:
            return result.iloc[0]['id']
        except IndexError:
            print("This product doesn't exist.")
            raise
            
    
    def get_biggest_producer(self, food, region):
        try:
            code = self.get_code(food)
        except IndexError:
            return "Unknown"
        df = self._comtrade.get_data(commodity = code, region = region)
        
        df = df[['TradeValue', 'ptTitle']]
        df = df.ix[df['ptTitle'] != 'World']
        
        result = df.loc[df['TradeValue'].idxmax()]
        return result['ptTitle']


if __name__ == "__main__":
    finder = FoodLocationFinder('ingredientsHS.json')

    print(finder.get_biggest_producer('Plaiceadsfasd', 826))
