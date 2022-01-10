from faker import Faker
from faker.providers import internet, geo, user_agent
import fire
import random
import urllib.parse
import datetime as dt
import csv
import hashlib
import os

fake = Faker()
Faker.seed(0)
fake.add_provider(internet)
fake.add_provider(user_agent)
fake.add_provider(geo)

events = ["load", "search", "click"]

endusers = []
companies = []
locales = ["fr", "it", "en", "de", "es"]
countries = ["france", "italy", "spain", "USA", "china", "england", "germany", "russia"]
domains = ["lopez.com", "toto.fr", "charlie.fr", "company.com", "vodka.ru"]

def buildClientList(count=100):
    for _ in range(count):
        client = {
            "country" : random.choice(countries),
            "user_agent" : fake.user_agent(),
            "ip" : hashlib.md5(fake.ipv4().encode()).hexdigest()
        }
        
        endusers.append(client)
        
def buildCompanyList():
    for _ in range(100):
        companies.append(fake.company())

def getItem():
    event = random.choice(events)
    enduser = random.choice(endusers)
    company = random.choice(companies)
    locale = random.choice(locales)
    domain = random.choice(domains)
    
    url_params = {
        'load' : {},
        'search' : { "query" : company , "group" : fake.random_lowercase_letter(), "locale" : locale},
        'click' : { "query" : company , "group" : fake.random_lowercase_letter(), "locale" : locale, "domain" : domain}
    }[event]
    
    url_query_string = "/api/" + event + "?"
    url = url_query_string +  urllib.parse.urlencode(url_params)
    
    return {
        "client" : enduser,
        "event" : event,
        "timestamp" : fake.unix_time(dt.datetime(2022, 1, 30), dt.datetime(2022, 1, 1)),
        "url" : url
    }
    
def writeClientFile(filepath = ""):
    with open(filepath, 'w') as f:
        writer = csv.DictWriter(f, delimiter=";", quoting=csv.QUOTE_ALL, fieldnames=["ip", "user_agent", "country", "locale"])
        
        writer.writeheader()
        
        writer.writerows(endusers)
        
        f.close()
        
def writeAccessLog(events, filepath=""):
    with open(filepath, 'w') as f:
        
        for event in events:
            f.write("{} {} {}".format(event["client"]["ip"], event["url"], event["timestamp"]))
            f.write("\r\n")
        
        f.close()
        

def gen(count=10, output="."):
    buildClientList(1 + int(count/10))
    buildCompanyList()
    
    events = []
    
    for _ in range(count):
        events.append(getItem())
        
    os.mkdir(output)
        
    writeClientFile(filepath='{}/end_users.csv'.format(output))
    writeAccessLog(events, filepath="{}/access.log".format(output))

if __name__ == '__main__':
    fire.Fire(gen)
    