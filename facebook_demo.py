from src.facebook_service import FacebookFeed

if __name__ == '__main__':
    print(FacebookFeed.get_posts())
    # api = pyfacebook.GraphAPI(access_token='EAANuAZBgVrn8BADqXhxMgqF7Nd19pbt8KUqKeHDwS8JbqGIrPfwA4QZB927rjTslUiuQsG5ZARHScxIEpZBdmOg0BNtGdlMx6V8RufIRGKjORkhcUfDPbK4eC4OCfwR4WOFBT7zI45iBoeQLFrzITfa5qqbScvN2IcGYBIXElSYf6tPNWWoNxKG7nfOoEtE1YL3zwXEP3xozt1cdbdav0hDgvnBFgl1L2oPfOVkFcyXcyUBE6MeOubPcZANZCLDrIZD')
    # api = pyfacebook.GraphAPI(app_id='965387987824255', app_secret='84ca0118d6242f40c42b0e2850e5edc3',
    #                           application_only_auth=True)
    # print(api.get_authorization_url())
