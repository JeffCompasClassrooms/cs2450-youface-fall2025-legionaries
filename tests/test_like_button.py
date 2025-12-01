import os
from selenium import webdriver
import time
import tinydb
import unittest

from db import posts

class TestLikeButton(unittest.TestCase):

    def setUp(self):
        self.filename = '/tmp/youfacetestdb'+str(time.time())
        self.db = tinydb.TinyDB(self.filename)

        self.username = "username"

        # create user
        users = self.db.table('users')
        user_record = {
                'username': self.username,
                'password': self.username,
                'friends': []
                }
        users.insert(user_record)

        # create post
        posts_table = self.db.table('posts')
        self.post = {"user": self.username, "text": "asdf", "time": time.time(), "likers": []}
        self.post_id = posts_table.insert(self.post)

        # 'user': user['username'],
        # 'text': text,
        # 'time': time.time()
        # 'likers': []


    @unittest.skip("Not concerned about this right now")
    def test_database_function(self):
        # when called on a post, # of likes on that post should be increased by 1
        posts_table = self.db.table('posts')
        original_count = len(posts_table.get(doc_id=self.post_id)['likers'])
        posts.like_post(self.db, self.post_id, self.username)
        new_count = len(posts_table.get(doc_id=self.post_id)['likers'])

        self.assertNotEqual(original_count, new_count, "Hey man, do better! "
                "The like_post function didn't actually increment the count "
                "of likes.")
        self.assertEqual(original_count+1, new_count)


        # when called on a post by a user who has already liked this post, post
        # count should remain the same

    def test_like_button(self):
        driver = webdriver.Chrome(executable_path="./tests/chromedriver")
        # TODO: don't forget proto
        driver.add_cookie({"name": "username", "value": self.username})
        driver.add_cookie({"name": "password", "value": self.username})
        driver.get("http://localhost:5000")
        self.assertEqual("YouFace 2.0", driver.title, "Make sure the title is correct")
        login_btn = driver.find_element_by_class_name("btn-primary")
        self.assertEqual(login_btn.get_attribute("value"), "Login")
        # 1. find username box
        # 2. enter username into the box (e.g., text_field.send_keys(self.username))
        # 3. do same for password
        login_btn.click()
        alerts = driver.find_element_by_class_name("alert")
        self.assertEqual(len(alerts), 1)
        driver.close()

    def tearDown(self):
        self.db.close()
        os.remove(self.filename)
