import json
import string
from nltk.corpus import stopwords

with open('ingredientsHS.json', 'r') as infile:
    x = json.load(infile)

x = x['results']
translator_punc = str.maketrans('', '', string.punctuation)
translator_num = str.maketrans('', '', '0123456789')

result = {}
for record in x:
    data = record['text']
    data = data.lower()
    data = data.translate(translator_punc) #Remove punctuation
    data = data.translate(translator_num) #Remove punctuation
    result[record['id']] = [word for word in data.split() if word not in stopwords.words('english')]
     
with open('processed_ingredients.json', 'w') as outfile:
    json.dump(result, outfile)
