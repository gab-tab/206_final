import unittest
import json
import final_project as project
from final_project import *

class TestDatabase(unittest.TestCase):
    def test_city(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        self.assertTrue(isvalidcity('Los Angeles'))

    def test_restaurant(self):
        sql = "SELECT DISTINCT name FROM Pizza"
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('The Brentwood',), result_list)

    def test_num_rests(self):
        sql = "SELECT DISTINCT name FROM Pizza"
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 933)

    def test_city_table(self):
        sql = "SELECT name FROM City"
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 673)

class TestYelp(unittest.TestCase):
    def test_yelp(self):
        restaurant = "Patsy's Pizzeria"
        user_city = "New York"
        z_json = get_data_from_yelp(restaurant, user_city)
        load_cache()
        z_json = z_json['businesses'][0]['rating']
        self.assertEqual(z_json, 4.5)


class TestTweets(unittest.TestCase):
    def test_tweets(self):
        rest1 = 'Mangia Mangia Café'
        rest2 = 'Crown Fried Chicken'

        tweets1 = get_tweets_for_rest(rest1)
        self.assertTrue(len(tweets1) > 0 and len(tweets1) < 10)

        tweets2 = get_tweets_for_rest(rest2)
        self.assertEqual(len(tweets2), 10) # there have to be at least 10 for Yellowstone!

        self.assertFalse(tweets2[2].is_retweet)
        self.assertTrue(tweets2[0].popularity_score >= tweets2[1].popularity_score)
        self.assertTrue(tweets2[3].popularity_score >= tweets2[7].popularity_score)

        tweet_string = str(tweets2[0]) # will call Tweet.__str__()
        self.assertTrue('@' in tweet_string)
        self.assertTrue('retweeted' in tweet_string)
        self.assertTrue('favorited' in tweet_string)









# class TestTweets(unittest.TestCase):
#     restaurant1 =

unittest.main()
