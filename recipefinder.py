import pandas as pd
recipes = pd.read_json('full_format_recipes.json')

def findIngredients(recipe):
    print(recipes.title)


def main():
    print(recipes.shape)
    findIngredients("Sweet Buttermilk Spoon Breads")




if __name__ == "__main__":
    main()
