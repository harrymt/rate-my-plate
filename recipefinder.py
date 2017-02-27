import pandas as pd
import math
recipes = pd.read_csv('recipes.csv')
def findIngredients(recipe):
    matches = recipes[recipes['title'].str.contains(recipe)]
    ingredients = []
    matches.fillna(True)
    for i, value in enumerate(matches.iloc[0]):
        if(value == 1.0 and i > 13):
            ingredients.append(recipes.columns[i])

    return ingredients

def main():
    recipes.fillna(True)
    ingredients = findIngredients('Tomato-Onion Topping')




if __name__ == "__main__":
    main()
