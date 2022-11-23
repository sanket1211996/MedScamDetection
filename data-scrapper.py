import requests
from bs4 import BeautifulSoup
import pymongo
from GoFundScrapper import MyWebScraper

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
    client = pymongo.MongoClient("mongodb+srv://medscamscapper:<password>@med-scrap-data.mjhhsle.mongodb.net/?retryWrites=true&w=majority")
    db = client.db[f'{collection}']
    try:
        db.insert_many(data)
        print(f'inserted {len(data)} ')
    except Exception as e:
        print(f'an error occurred {collection} were not stored to db', e)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # medical url only
    searchResultLink = MyWebScraper('https://www.gofundme.com/s?q=&c=11')
    fundRaiserLinks = []

    for data in searchResultLink.fundraisers_links:
        fundRaiserLinks.append({'link': data, 'profile_scrapped': 'false'})

    dumpScarpData(fundRaiserLinks, 'fundraiser-link')
