import pandas as pd
recipes = pd.read_csv('recipes.csv')
def findIngredients(recipe):
    matches = recipes[recipes['title'].str.contains(recipe)]
    for values in matches.iloc[0]:
        

def main():
    recipes.fillna(True)
    findIngredients('Tomato-Onion Topping')




if __name__ == "__main__":
    main()
