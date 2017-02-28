import csv
import pandas as pd
import comtrade_api
from fuzzywuzzy import process
import re
from nltk.stem.lancaster import LancasterStemmer

class FoodLocationFinder:
    _comtrade = comtrade_api.ComtradeAPI()
    
    def __init__(self, dataset):
        data = pd.read_json(dataset)
        self._commodities = list(data['results'])

    def find_country_code(self, num_code):
        #Would be preferable to keep file open
        with open("UNComtradeCountryList.csv", encoding = "ISO-8859-1") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == str(num_code):
                    return row[5] 


    def get_code(self, food):
        st = LancasterStemmer()
        stemmed = st.stem(food)
        result = [] 
        
        for item in self._commodities:
            #if re.search(stemmed, item['text'], re.IGNORECASE):
            x = process.extractOne(food, item['text'].split())
            result.append((x[1], item['id']))
            
        
        result.sort(key=lambda x: x[0], reverse=True) #Sort on 1st value
        print(result[:10])
        return [i[1] for i in result[:10]] #Provide 10 results
            
    
    def get_biggest_producer(self, food, region):
        try:
            codes = self.get_code(food)
        except IndexError:
            return ("UU", "Unknown")

        for c in codes:
            df = self._comtrade.get_data(commodity = c, region = region)

            if not df.empty:
                #print(df.columns.values)
                #We've found some data to work with
                df = df[['TradeValue', 'ptTitle', 'ptCode']]
                df = df.ix[df['ptTitle'] != 'World']
                
                result = df.loc[df['TradeValue'].idxmax()]
                code = self.find_country_code(result['ptCode'])
                return (code, result['ptTitle'])

        #If we get here then none of the codes worked
        return ("UU", "Unknown")
    
    def get_producers_for_recipe(self, ingredients, region):
        result = []
        for i in ingredients:
            result.append(self.get_biggest_producer(i, region))
        return result


if __name__ == "__main__":
    finder = FoodLocationFinder('ingredientsHS.json')
    ingredients = ['carrot']

    print(finder.get_producers_for_recipe(ingredients, 826))
