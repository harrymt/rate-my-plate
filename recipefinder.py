import pandas as pd
import difflib
from collections import OrderedDict


def preProcessData(file_name):
    recipes = pd.read_csv(file_name)
    recipes = recipes.dropna()
    return recipes


def findIngredients(recipe, recipes, similar=False):
    try:
        recipe = difflib.get_close_matches(recipe, recipes['title'], cutoff=0.5)[0]
    except:
        return False

    if similar:
        matches = recipes[recipes['title'].str.contains(recipe)]
    else:
        matches = recipes[recipes['title'] == recipe]

    # print(matches)
    return matches


def normalizeData(data, columns_to_normalize):
    for col in columns_to_normalize:
        data[col] = data[col].apply(lambda x: abs(x))
        data[col] = data[col].apply(lambda x: x/data[col].median())


def findSimilarIngredients(recipe_id, recipes, columns=["calories", "protein", "fat", "sodium"], critical=[], n=1):
    relevant_dataset = recipes.copy()[columns]
    normalizeData(relevant_dataset, columns)
    relevant_recipe = relevant_dataset.loc[recipe_id].copy()
    relevant_dataset["means"] = relevant_dataset.mean(axis=1)
    print(relevant_recipe)
    print(relevant_dataset)
    scores = relevant_dataset.mean(axis=1) - relevant_recipe.mean(axis=1)
    #print(scores)


def main():
    recipes = preProcessData('recipes.csv')

    match_recipe = findIngredients('beef burger', recipes, True)  # test
    print(match_recipe)
    findSimilarIngredients(match_recipe.index, recipes)


if __name__ == "__main__":
    main()
