from nltk.corpus import wordnet as wn

def get_food_group(search):
    dairy = ["egg", "milk", "cheese", "dairy"]
    meat = ["meat", "fish", "pork", "beef", "poultry", "lamb", "seafood"]
    fruit = ["berry", "fruit"]
    other = ["grain", "nut", "wheat", "bakery"]
    vegetable = ["bean", "vegetable"]
    categories = dairy + meat + fruit + other + vegetable

    print("Searching for", search)
    scores = dict()
    search_synset = wn.synset(search + ".n.01")
    for cat in categories:
        scores[cat] = wn.synset(cat + ".n.01").path_similarity(search_synset)
    #print(scores)
    best_guess = max(scores, key=scores.get)
    if best_guess in dairy:
        best_guess = "dairy"
    if best_guess in meat:
        best_guess = "meat/fish"
    if best_guess in fruit:
        best_guess = "fruit"
    if best_guess in other:
        best_guess = "nut/grain"
    if best_guess in vegetable:
        best_guess = "vegetable"

    return best_guess


def get_co2_equivalent_of_item(search, amount=1, food_group=None):
    """
        Give amount in grams
    """
    co2_equivalent = {"dairy": 4,
                      "meat/fish": 10,
                      "nut/grain": 3,
                      "fruit": 1.6,
                      "vegetable": 2}
    if not food_group:
        food_group = get_food_group(search)
    estimate = co2_equivalent[food_group] * amount
    return estimate, food_group


def process_ingredients_impact(ingredient_list):
    processed_impact = dict()
    processed_quantities = dict()
    for ingredient in ingredient_list:
        impact, food_group = get_co2_equivalent_of_item(ingredient[0], ingredient[1])
        if food_group in processed_impact:
            processed_impact[food_group] += impact * 1000
            processed_quantities[food_group] += ingredient[1] * 1000
        else:
            processed_impact[food_group] = impact * 1000
            processed_quantities[food_group] = ingredient[1] * 1000

    return processed_impact, processed_quantities

