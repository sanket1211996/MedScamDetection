import requests
from bs4 import BeautifulSoup
import pymongo
from GoFundScrapper import MyWebScraper
from GoFundScrapper import scrap_profile_data

DB_URL = 'mongodb+srv://medscamscapper:OtyCeNbpSt3ZuCSd@med-scrap-data.mjhhsle.mongodb.net/?retryWrites=true&w=majority'


def scrape_quotes():
    more_links = True
    page = 1
    quotes = []
    while (more_links):
        markup = requests.get(f'http://quotes.toscrape.com/page/{page}').text
        soup = BeautifulSoup(markup, 'html.parser')
        for item in soup.select('.quote'):
            quote = {}
            quote['text'] = item.select_one('.text').get_text()
            quote['author'] = item.select_one('.author').get_text()
            tags = item.select_one('.tags')
            quote['tags'] = [tag.get_text() for tag in tags.select('.tag')]
            quotes.append(quote)

        next_link = soup.select_one('.next > a')

        # print which page was scraped
        print(f'scraped page {page}')

        # check if the next link element exists
        if (next_link):
            page += 1
        else:
            more_links = False
    return quotes

def dumpScarpData(data, collection):
    client = pymongo.MongoClient(DB_URL)
    db = client.db[f'{collection}']
    try:
        db.insert_many(data)
        print(f'inserted {len(data)} ')
    except Exception as e:
        print(f'an error occurred {collection} were not stored to db', e)

def getScarpData(collection):
    client = pymongo.MongoClient(DB_URL)
    db = client.db[f'{collection}']
    foundData = []
    try:
        foundData = db.find()
    except Exception as e:
        print(f'an error occurred {collection} were not stored to db', e)

    return foundData
# Press the green button in the gutter to run the script.

def get_fund_url():
    # medical url only
    searchResultLink = MyWebScraper('https://www.gofundme.com/s?q=&c=11')
    fundRaiserLinks = []

    for data in searchResultLink.fundraisers_links:
        fundRaiserLinks.append({'link': data, 'profile_scrapped': 'false'})

    dumpScarpData(fundRaiserLinks, 'fundraiser-link')

def get_fund_profile():

    urls = getScarpData('fundraiser-link')

    links = []
    for url in urls:
        links.append('https://www.gofundme.com'+url['link'])
    # print(links)
    # links = ['https://www.gofundme.com/f/matt-summers?qid=43ccfcca04466864bbdc550e384c205c']

    for url in links:
        dumpScarpData([scrap_profile_data(url)], 'fundraiser-profile')

if __name__ == '__main__':
    # get_fund_url()
    get_fund_profile()
