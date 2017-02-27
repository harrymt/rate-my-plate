from flask import Flask, send_from_directory, send_file, request
import recipefinder
# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username


# EB looks for an 'application' callable by default.
application = Flask(__name__)

#ratemyplate.com/meals?recipe=spghetti

@application.route('/meals')
def get_recipe_breakdown():
    recipe_name = request.args.get('recipe');
    ingredients = recipefinder.findIngredients(recipe_name,True)
    return "getting your recipe ;)"

@application.route('/icons/<path:path>')
def send_icon(path):
    return send_from_directory('icons', path)

@application.route('/<path:path>')
def send_meal_breakdown(path):
    return send_from_directory('static', path)
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()