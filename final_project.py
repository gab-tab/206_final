#final project
#Gaby Tabachnik
import secrets
import sqlite3
import csv
import json
import requests
from bs4 import BeautifulSoup
import json
from requests_oauthlib import OAuth1
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#auth = OAuth1(secrets.twitter_api_key, secrets.twitter_api_secret, secrets.twitter_access_token, secrets.twitter_access_token_secret)

CACHE_FNAME = 'final_project_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def params_unique_combination(url, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return url + "_".join(res)

def save_cache():
    full_text = json.dumps(CACHE_DICTION)
    cache_file_ref = open(CACHE_FNAME, 'w')
    cache_file_ref.write(full_text)
    cache_file_ref.close()

def load_cache():
    global CACHE_DICTION
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}

def make_request_using_cache(url, headers, params, verify=False):
    unique_ident = params_unique_combination(url, params)
    if unique_ident in CACHE_DICTION:
        print('Getting cached data...')
        return CACHE_DICTION[unique_ident]
    else:
        print('Making request for new data...')
        resp = requests.get('GET', url, headers=headers, params=params)
        CACHE_DICTION[unique_ident] = resp.text
        save_cache()
        return CACHE_DICTION[unique_ident]

DBNAME = 'pizza_info.db'
PIZZACSV = 'pizza.csv'

conn = sqlite3.connect(DBNAME)
cur = conn.cursor()
statement_drop_pizza = 'DROP TABLE IF EXISTS "Pizza"'
cur.execute(statement_drop_pizza)
conn.commit()

statement_drop_city = "DROP TABLE IF EXISTS 'City'"
cur.execute(statement_drop_city)
conn.commit()

create_pizza = '''
CREATE TABLE IF NOT EXISTS 'Pizza' (
'id' TEXT,
'address' TEXT,
'categories' TEXT,
'city' INTEGER,
'country' TEXT,
'keys' TEXT,
'latitude' INTEGER,
'longitude' INTEGER,
'menuPageURL' INTEGER,
'menus_amountMax' INTEGER,
'menus_amountMin' INTEGER,
'menus_dateSeen' TEXT,
'menus_name' TEXT,
'name' TEXT,
'postalCode' INTEGER,
'priceRangeCurrency' TEXT,
'priceRangeMin' INTEGER,
'priceRangeMax' INTEGER,
'province' TEXT);
'''
cur.execute(create_pizza)

create_city = '''
CREATE TABLE IF NOT EXISTS 'City' (
'id' TEXT,
'name' TEXT);
'''
cur.execute(create_city)
conn.commit()



city_count = 0
city_ids = {}

pizza_file = open("pizza.csv", "r")
data = csv.DictReader(pizza_file)
cache = open("cache_data.txt", "w")
for info in data:
    id = info["id"]
    address = info["address"]
    categories = info["categories"]
    city = info["city"]
    if not city in city_ids:
        city_count += 1
        city_ids[city] = city_count
        insert_to_table = (city_ids[city],city)
        statement = '''
        INSERT INTO 'City'
        VALUES (?,?)
        '''
        cur.execute(statement, insert_to_table)
    country = info["country"]
    keys = info["keys"]
    latitude = info["latitude"]
    longitude = info["longitude"]
    menuPageURL = info["menuPageURL"]
    menus_amountMax = info["menus.amountMax"]
    menus_amountMin = info["menus.amountMin"]
    menus_dateSeen = info["menus.dateSeen"]
    menus_name = info["menus.name"]
    name = info["name"]
    postalCode = info["postalCode"]
    priceRangeCurrency = info["priceRangeCurrency"]
    priceRangeMin = info["priceRangeMin"]
    priceRangeMax = info["priceRangeMax"]
    province = info["province"]

    # INSERT INTO pizza(id, address) VALUES (?, ?);
    insert_to_table = (id,address,categories,city_ids[city],country,keys,latitude,longitude,menuPageURL,menus_amountMax,menus_amountMin,menus_dateSeen,menus_name,name,postalCode,priceRangeCurrency,priceRangeMin,priceRangeMax,province)
    statement = '''
    INSERT INTO 'Pizza'
    Values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    '''
    cur.execute(statement, insert_to_table)
conn.commit()

def get_data_from_yelp(term, location, limit=50):
    url = 'https://api.yelp.com/v3/businesses/search'
    API_KEY = secrets.YELP_API_KEY
    headers = {
    'Authorization': 'Bearer {}'.format(API_KEY)
        }
    params = {'term': term, 'location': location, 'limit':50}
    uniq = params_unique_combination(url, params)
    if uniq in CACHE_DICTION:
        text = CACHE_DICTION[uniq]
        return text
    else:
        response = requests.get(url, headers=headers, params=params, verify=False)
        yelpinfo = json.loads(response.text)
        CACHE_DICTION[uniq] = yelpinfo
        save_cache()
        return yelpinfo
load_cache()

get_data_from_yelp('Pizza', 'Chicago')
