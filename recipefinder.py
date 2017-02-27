import pandas as pd
import difflib


recipes = pd.read_csv('recipes.csv')


def findIngredients(recipe, similar=False):
    try:
        recipe = difflib.get_close_matches(recipe, recipes['title'], cutoff=0.5)[0]
    except:
        return False

    if similar:
        matches = recipes[recipes['title'].str.contains(recipe)]
    else:
        matches = recipes[recipes['title'] == recipe]

    print(matches)
    return matches


def main():
    recipes.replace('nan', 0)
    findIngredients('Fried Chicken', True)  # test


if __name__ == "__main__":
    main()
