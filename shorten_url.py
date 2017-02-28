from pyshorteners import Shortener

url = 'http://www.google.com'
shortener = Shortener('Tinyurl')
print("My short url is {}".format(shortener.short(url)))