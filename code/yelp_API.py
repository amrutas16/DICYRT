from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io,json
write_bytes=False

# read API keys
with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

    params = {
    'term': 'food',
    'lang': 'fr'
    }

    #response=client.search('San Francisco', **params)
    businessName="garland-raleigh-2"
    response=client.get_business(businessName)
    #print (json.dumps(response.business))
    print ( response.business)
    print (response.business.name)
    #print (','.join([i for i in response.businesses]))
