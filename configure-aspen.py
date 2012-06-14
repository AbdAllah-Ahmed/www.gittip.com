import os

import gittip 
import gittip.wireup
import gittip.authentication


gittip.wireup.canonical()
gittip.wireup.db()
gittip.wireup.samurai()

website.github_client_id = os.environ['GITHUB_CLIENT_ID']
website.github_client_secret = os.environ['GITHUB_CLIENT_SECRET']
website.github_callback = os.environ['GITHUB_CALLBACK']

website.facebook_client_id = os.environ['FACEBOOK_CLIENT_ID']
website.facebook_client_secret = os.environ['FACEBOOK_CLIENT_SECRET']
website.facebook_callback = os.environ['FACEBOOK_CALLBACK']

website.hooks.inbound_early.register(gittip.canonize) 
website.hooks.inbound_early.register(gittip.authentication.inbound) 
website.hooks.outbound_late.register(gittip.authentication.outbound) 

def facebook_oauth_url(then=""):
    url = "https://www.facebook.com/dialog/oauth?client_id=%s"
    url %= website.facebook_client_id
    if url:
        url += "&redirect_uri=%s?then=%s" % (website.facebook_callback, then)
    return url

def github_oauth_url(then=""):
    url = "https://github.com/login/oauth/authorize?client_id=%s" 
    url %= website.github_client_id
    if url:
        url += "&redirect_uri=%s?then=%s" % (website.github_callback, then)
    return url

def add_stuff(request):
    request.context['__version__'] = gittip.__version__
    request.context['username'] = None 
    request.context['facebook_oauth_url'] = facebook_oauth_url
    request.context['github_oauth_url'] = github_oauth_url

website.hooks.inbound_early.register(add_stuff) 
