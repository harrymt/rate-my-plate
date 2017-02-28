import csv
import pandas as pd
import comtrade_api
from fuzzywuzzy import process 
import re
from nltk.stem.lancaster import LancasterStemmer
import sqlite3
import json

class FoodLocationFinder:
    _comtrade = comtrade_api.ComtradeAPI()
    _conn = sqlite3.connect('comtrade.db', check_same_thread=False)
    
    def __init__(self, dataset):
        with open(dataset, 'r') as infile:
            self._commodities = json.load(infile) 

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
        
        for item_id, words in self._commodities.items():
            #if re.search(stemmed, item['text'], re.IGNORECASE):
            r = process.extractOne(food, words)
            result.append((r[1], item_id))
            
        
        result.sort(key=lambda x: x[0], reverse=True) #Sort on 1st value
        print(result[:10])
        return [i[1] for i in result[:10]] #Provide 10 results
            
    
    def get_biggest_producer(self, food, region):
        try:
            codes = self.get_code(food)
        except IndexError:
            return "UU"
        
        #check in database

        for c in codes:
            cursor = self._conn.execute("SELECT ID, COMMODITY, REGION, COUNTRY_CODE FROM INGREDIENTS WHERE COMMODITY = ? AND REGION = ?", (c, region))
            for row in cursor:
                print("Getting result from DB")
                return row[3]
     
            try:
                df = self._comtrade.get_data(commodity = c, region = region)
            except Exception as e:
                print(e)
                continue

            if not df.empty:
                #print(df.columns.values)
                #We've found some data to work with
                df = df[['TradeValue', 'ptTitle', 'ptCode']]
                df = df.ix[df['ptTitle'] != 'World']
                
                result = df.loc[df['TradeValue'].idxmax()]
                code = self.find_country_code(result['ptCode'])
                self._conn.execute("INSERT INTO INGREDIENTS (commodity, region, country_code) \
                    VALUES (?, ?, ?)", (c, region, code))
                self._conn.commit()
                print("Inserted into DB")

                return code

        #If we get here then none of the codes worked
        return "UU"
    
    def get_producers_for_recipe(self, ingredients, region):
        result = []
        for i in ingredients:
            result.append(self.get_biggest_producer(i, region))
        return result


if __name__ == "__main__":
    finder = FoodLocationFinder('processed_ingredients.json')
    ingredients = ['carrot', 'peach', 'tomato', 'lamb', 'potato']

    print(finder.get_producers_for_recipe(ingredients, 826))
