import unittest
import os
import json
import final_project as project
from final_project import *

class TestDatabase(unittest.TestCase):
    def test_db(self):
        #first delete the existing database
        DBNAME = 'pizza_info.db'
        if os.path.isfile(DBNAME):
            os.remove(DBNAME)
        self.assertFalse(os.path.isfile(DBNAME))
        create_database()
        self.assertTrue(os.path.isfile(DBNAME))

    def test_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        self.assertTrue(isvalidcity('Los Angeles'))

# class TestTweets(unittest.TestCase):
#     restaurant1 =

unittest.main()
