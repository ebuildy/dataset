from faker import Faker
from faker.providers import internet, geo, user_agent
from user_agents import parse

import fire
import random
import urllib.parse
import datetime as dt
import csv
import hashlib
import os
import collections

fake = Faker()
Faker.seed(0)
fake.add_provider(internet)
fake.add_provider(user_agent)
fake.add_provider(geo)

events = ["load", "search", "click"]
eventsRandomWeights = [0.1,0.6,0.3]

endusers = []
companies = []
locales = ["fr", "it", "en", "de", "es"]
localesWeight = [0.4, 0.1, 0.3, 0.1, 0.1]
countries = ["france", "italy", "spain", "USA", "china", "england", "germany", "russia"]
domains = ["lopez.com", "toto.fr", "charlie.fr", "company.com", "vodka.ru"]
requestDomains = ["www", "www2", "beta", "lite", "api"]
requestDomainsWeights = [0.3, 0.1, 0.1, 0.2, 0.3]

def buildClientList(count=100):
    for _ in range(count):
        ua_string = fake.user_agent()
        user_agent = parse(ua_string)
            
        client = {
            "country" : random.choice(countries),
            "user_agent" : ua_string,
            "ip" : hashlib.md5(fake.ipv4().encode()).hexdigest(),
            "ua" : {
                "os" : user_agent.os.family,
                "browser" : user_agent.browser.family,
                "browser_version" : user_agent.browser.version_string
            } 
        }
        
        endusers.append(client)
        
def buildCompanyList():
    for _ in range(100):
        companies.append(fake.company())

def getItem():
    event = random.choices(population=events, weights=eventsRandomWeights, k=1)[0]
    enduser = random.choice(endusers)
    company = random.choice(companies)
    locale = random.choices(population=locales, weights=localesWeight, k=1)[0]
    domain = random.choice(domains)
    requestDomain = random.choices(population=requestDomains, weights=requestDomainsWeights, k=1)[0]
    
    url_params = {
        'load' : {},
        'search' : { "query" : company , "group" : fake.random_lowercase_letter(), "locale" : locale},
        'click' : { "query" : company , "group" : fake.random_lowercase_letter(), "locale" : locale, "domain" : domain}
    }[event]
    
    url_query_string = "/api/" + event + "?"
    url = url_query_string +  urllib.parse.urlencode(url_params)
    
    event_client = flatten(enduser, 'client')
    event_query = flatten({
        #"url" : url,
        "data" : url_params,
        "host" : requestDomain
    }, "query")
    event_data = {
        "event" : event,
        "timestamp" : fake.unix_time(dt.datetime(2022, 1, 30), dt.datetime(2022, 1, 1)),
    }
    
    return {**event_client, **event_data, **event_query}
        
def writeFullDataset(events, filepath=""):
    with open(filepath, 'w') as f:
        bigEvent = {}
        
        for e in events:
            bigEvent = {**bigEvent, **e}
        
        writer = csv.DictWriter(f, delimiter=";", quoting=csv.QUOTE_ALL, fieldnames=bigEvent.keys())
        
        writer.writeheader()
        
        writer.writerows(events)
                    
        f.close()
        

def gen(count=10, output="."):
    buildClientList(1 + int(count/10))
    buildCompanyList()
    
    events = []
    
    for _ in range(count):
        events.append(getItem())
    
    if not os.path.exists(output):
        os.mkdir(output)
        
    writeFullDataset(events, filepath="{}/dataset.csv".format(output))
    
def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

if __name__ == '__main__':
    fire.Fire(gen)
    