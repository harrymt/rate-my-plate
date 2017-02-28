from flask import Flask, send_from_directory, send_file, request, render_template
from werkzeug.contrib.cache import SimpleCache
import pandas as pd
import recipefinder
import sys
import food_loc_finder
import json
import numpy as np
import tensorflow as tf

modelFullPath = './neuro/output_graph.pb'
labelsFullPath = './neuro/output_labels.txt'

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username


# EB looks for an 'application' callable by default.
application = Flask(__name__)
cache = SimpleCache()
recipes = recipefinder.preProcessData('recipes.csv')
country_locations = pd.read_csv('countries.csv')
icon_list = pd.read_csv('icons/iconlist.csv').ix[:,0].tolist()
finder = food_loc_finder.FoodLocationFinder('ingredientsHS.json')
#ratemyplate.com/meals?recipe=spghetti

@application.route('/meals')
def get_recipe_breakdown():
    recipe_name = request.args.get('recipe');  
    image_file = request.args.get('image');
    if image_file:
        print("got image")
    rv = cache.get(recipe_name)
    if rv is None:
        print(recipe_name, file=sys.stderr)
        ingredients, weights = recipefinder.getRecipeFromApi(recipe_name)
        countries = finder.get_producers_for_recipe(ingredients, 826)
        locations = get_locations(countries)
        icons = []
        for ingredient in ingredients:
            icons.append(get_icon(ingredient))
        template = render_template("index.html", recipe=json.dumps(recipe_name), ingredients=json.dumps(ingredients), producers=json.dumps(countries), locations=json.dumps(locations), weights=json.dumps(weights), icons=json.dumps(icons))
        cache.set(template, rv, timeout=10*60)
        return template
    else:
        return rv



@application.route('/icons/<path:path>')
def send_icon(path):
    return send_from_directory('icons', path)

@application.route('/<path:path>')
def send_meal_breakdown(path):
    return send_from_directory('static', path)


def get_icon(ingredient):
    words = ingredient.split()
    for word in words:
        file = word + ".png"
        if file in icon_list:
            return "localhost:5000/icons/" + file
    return None

def get_locations(producers):
    locations = []
    for producer in producers:
        match = country_locations.loc[country_locations['country'] == producer]
        try:
            locations.append((match['latitude'].item(), match['longitude'].item()))
        except:
            locations.append((0,0))
    return locations

def create_graph():
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(imagePath):
    answer = None

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return answer

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    # Creates graph from saved GraphDef.
    create_graph()

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-5:][::-1]  # Getting top 5 predictions
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))

        answer = labels[top_k[0]]
        return answer



# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
    #print(run_inference_on_image('./neuro/ed.jpg'))