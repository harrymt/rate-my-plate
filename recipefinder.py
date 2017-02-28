import pandas as pd
import difflib
from collections import OrderedDict
import requests
import json


def preProcessData(file_name):
    recipes = pd.read_csv(file_name)
    recipes = recipes.dropna()
    return recipes

bbcFood = preProcessData("bbc_food.csv")


def findIngredients(recipe, recipes, similar=False):
    try:
        recipe = difflib.get_close_matches(recipe, recipes['title'], cutoff=0.5)[0]
    except:
        return False

    if similar:
        matches = recipes[recipes['title'].str.contains(recipe)]
    else:
        matches = recipes[recipes['title'] == recipe]

    ingredients = []
    print(matches.shape)
    for i, value in enumerate(matches.iloc[0]): 
        if(value == 1.0): 
            ingredients.append(recipes.columns[i]) 
 
    return ingredients 


def getRecipeFromApi(recipe):
    r = requests.get("https://api.edamam.com/search?q=" + recipe + "&app_id=90bb0a66&app_key=2c44ec80d7269b7c30d7e4215bfb83d1&to=40")
    jsonContent = json.loads(r.text)
    recipes = jsonContent['hits']
    best_guess_foods = []
    best_guess_weights = []
    for recipe in recipes:
        ingredients = recipe['recipe']['ingredients']
        foods = []
        weights = []
        for ingredient in ingredients:
            success = True
            if len(ingredient['text']) < 30 and 'weight' in ingredient:
                foods.append(ingredient['text'])
                weights.append(ingredient['weight'])
            else:
                 success = False
        if success and len(foods) > len(best_guess_foods):
            best_guess_foods = foods
            best_guess_weights = weights
    return best_guess_foods, best_guess_weights


def normalizeData(data, columns_to_normalize):
    for col in columns_to_normalize:
        data[col] = data[col].apply(lambda x: abs(x))
        data[col] = data[col].apply(lambda x: x/data[col].median())


def findSimilar(recipe_id, recipes, columns=["calories", "protein", "fat", "sodium"], critical=[], n=10):
    relevant_dataset = recipes.copy()[columns]
    normalizeData(relevant_dataset, columns)
    relevant_recipe = relevant_dataset.loc[recipe_id].copy()

    recipes["means"] = relevant_dataset.mean(axis=1)
    recipes["scores"] = recipes["means"] - float(relevant_recipe.mean(axis=1))
    recipes["scores"] = recipes["scores"].apply(lambda x: abs(x))
    return recipes.sort(["scores"])[1:(1+n)]


def main(search="beef burger"):
    recipes = preProcessData('recipes.csv')

    match_recipe = findIngredients(search, recipes, True)

    print(findSimilar(match_recipe.index, recipes))


if __name__ == "__main__":
    recipes = preProcessData('recipes.csv')
    print(getRecipeFromApi("soup"))
