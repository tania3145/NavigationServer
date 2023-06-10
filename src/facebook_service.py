import facebook
import requests
import json


class FacebookFeed:
    FACEBOOK_USER = '100093079661512'
    FACEBOOK_CLIENT_ID = '965387987824255'
    FACEBOOK_CLIENT_SECRET = '84ca0118d6242f40c42b0e2850e5edc3'
    FACEBOOK_ACCESS_TOKEN = 'EAANuAZBgVrn8BAAvpeNOM5A4cJScyujAKZBqSxRvJOi93ZBZB1BfNfZB6nJjxZB5F3B1HfKEJaGs9C5IuDY3QY41fxj4XTiDTPtvxL7Fm31rXSW4Bf1vWZByC2L7CQusm4iJCMi21uRFoAfZBXc3ZBzLKv8DHpZBBLL4FgLyMnnlLCJyZCDTz46ZBG4kyffjRB0ZAeHMYsHTZBSZCGNRPMe042aMwwlxxlZB40aHazdBCbZBZARkxVfRukAZBEn9o7OZAHDTAOexJMIZD'

    token_url = 'https://graph.facebook.com/oauth/access_token'
    params = dict(client_id=FACEBOOK_CLIENT_ID, client_secret=FACEBOOK_CLIENT_SECRET,
                  grant_type='client_credentials')

    @classmethod
    def get_posts(cls, user=FACEBOOK_USER, access_token=FACEBOOK_ACCESS_TOKEN):
        try:
            if access_token is None:
                token_response = requests.get(url=cls.token_url, params=cls.params)
                json_response = json.loads(token_response.text)
                access_token = json_response['access_token']
            graph = facebook.GraphAPI(access_token)
            permissions = graph.get_permissions(user)
            if 'user_posts' not in permissions:
                raise 'user_posts permission not found!'
            posts = graph.get_connections('me', 'posts?fields=message,full_picture&&limit=10')['data']
            return posts
        except facebook.GraphAPIError:
            return None

    @classmethod
    def get_profile(cls, user=FACEBOOK_USER, access_token=FACEBOOK_ACCESS_TOKEN):
        try:
            if access_token is None:
                token_response = requests.get(url=cls.token_url, params=cls.params)
                json_response = json.loads(token_response.text)
                access_token = json_response['access_token']
            graph = facebook.GraphAPI(access_token)
            user = graph.get_object('{}?fields=picture,name'.format(user))
            user['picture'] = user['picture']['data']['url']
            return user
        except facebook.GraphAPIError:
            return None
