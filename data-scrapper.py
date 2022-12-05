import requests
from bs4 import BeautifulSoup
import pymongo

import ScamProfileAnalyzer
from GoFundScrapper import MyWebScraper
from GoFundScrapper import scrap_profile_data
from PROPERTIES import FIREBASE_DB_URL,FIREBASE_CERTIFICATE, DB_PASSWORD
import firebase_admin
from firebase_admin import db


DB_URL = 'mongodb+srv://medscamscapper:' + DB_PASSWORD + '@med-scrap-data.mjhhsle.mongodb.net/?retryWrites=true&w=majority'

cred_obj = firebase_admin.credentials.Certificate(FIREBASE_CERTIFICATE)
app = firebase_admin.initialize_app(cred_obj);



def dumpScarpData(data, collection):
    client = pymongo.MongoClient(DB_URL)
    db = client.db[f'{collection}']
    try:
        db.insert_many(data)
        print(f'inserted {len(data)} ')
    except Exception as e:
        print(f'an error occurred {collection} were not stored to db', e)


def getScarpData(collection, limitValue=-1):
    client = pymongo.MongoClient(DB_URL)
    db = client.db[f'{collection}']
    foundData = []
    try:

        if limitValue == -1:
            foundData = db.find()
        else:
            foundData = db.find().limit(limitValue)

    except Exception as e:
        print(f'an error occurred {collection} were not stored to db', e)

    return foundData


# Press the green button in the gutter to run the script.

def process_fund_url():
    # medical url only
    searchResultLink = MyWebScraper('https://www.gofundme.com/s?q=&c=11')
    fundRaiserLinks = []

    for data in searchResultLink.fundraisers_links:
        fundRaiserLinks.append({'link': data, 'profile_scrapped': 'false'})

    dumpScarpData(fundRaiserLinks, 'fundraiser-link')


def process_fund_profile():
    urls = getScarpData('fundraiser-link')

    links = []
    for url in urls:
        links.append('https://www.gofundme.com' + url['link'])

    for url in links:
        dumpScarpData([scrap_profile_data(url)], 'fundraiser-profile')


def process_analyzed_data():

    for data in getScarpData('fundraiser-profile', 5):
        scamLinkData = ScamProfileAnalyzer.analyze_profile(data)

    # push_link_firebase(scamLinkData)

def push_link_firebase(linkData):
    print('firebase: pushing data links')
    ref = db.reference("/")
    link_data_ref = ref.child('scam-url')

    new_link_data_ref = link_data_ref.push()
    new_link_data_ref.set({
        'url': 'example.com',
    })

    for link in linkData:
        new_link_data_ref.push().set({
            'url': link
        })
    print('firebase: data pushed successfully')


# if __name__ == '__main__':
#     inputSelection = int(input('Enter Selection:\n 1. FETCH FUND URL\n 2. FETCH FUND PROFILE\n 3. Analyze FUND DATA\n'))
#
#     if inputSelection == 1:
#         process_fund_url()
#     elif inputSelection == 2:
#         process_fund_profile()
#     elif inputSelection == 3:
#         process_analyzed_data()


push_link_firebase('example2.com')
