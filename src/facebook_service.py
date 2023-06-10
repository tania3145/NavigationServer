import facebook
import requests
import json


class FacebookFeed:
    FACEBOOK_USER = '100093079661512'
    FACEBOOK_CLIENT_ID = '965387987824255'
    FACEBOOK_CLIENT_SECRET = '84ca0118d6242f40c42b0e2850e5edc3'
    FACEBOOK_ACCESS_TOKEN = 'EAANuAZBgVrn8BABKMnjaYF5v60ZCZBVMtbhOzrBrB75kns6eFhI2gzFPPJOHP2ASmIoBVVKnqSCsjFmSG8aaSUb6by6Ja1fgdZBZBpCRi6ZCXGq06ZCInlKaraaALAN0lVCIyNmkxZBse0QoZCgZCZCpZCTfeBc0OeFFqPpG58Uvhgsk1QsxXa3IJK1saKNRsld5JX6gW6e9q0n2HNEIzp3NZBQZC1HmqicTcQrK8krIVZBJxzzLZA7hV1Qhm4kKFXSELesO9cwZD'

    token_url = 'https://graph.facebook.com/oauth/access_token'
    params = dict(client_id=FACEBOOK_CLIENT_ID, client_secret=FACEBOOK_CLIENT_SECRET,
                  grant_type='client_credentials')

    @classmethod
    def get_posts(cls, user=FACEBOOK_USER, access_token=FACEBOOK_ACCESS_TOKEN):
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

    @classmethod
    def get_profile(cls, user=FACEBOOK_USER, access_token=FACEBOOK_ACCESS_TOKEN):
        if access_token is None:
            token_response = requests.get(url=cls.token_url, params=cls.params)
            json_response = json.loads(token_response.text)
            access_token = json_response['access_token']
        graph = facebook.GraphAPI(access_token)
        user = graph.get_object('{}?fields=picture,name'.format(user))
        user['picture'] = user['picture']['data']['url']
        return user
