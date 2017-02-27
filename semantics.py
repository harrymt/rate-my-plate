from nltk.corpus import wordnet as wn

dairy = ["egg", "milk", "cheese", "dairy"]
meat = ["meat", "fish", "pork", "beef", "poultry", "lamb", "seafood"]
fruit = ["berry", "fruit"]
other = ["grain", "nut", "wheat", "bakery"]
vegetable = ["bean", "vegetable"]
categories = dairy + meat + fruit + other + vegetable
searches = ["pineapple", "chicken", "Gouda", "hazelnut", "strawberry", "Salmon", "cod", "Ham"]
synset_categories = []

for search in searches:
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
    print("classified as", best_guess)