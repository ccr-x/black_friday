from Scraper import Driver
import requests
from bs4 import BeautifulSoup


def scrape_bf():
    urls = open("links.txt", "r").readlines()
    data = []

    try:

        # Obtain information from website
        for link in urls:

            # Create instance
            driver = Driver()
            #url = requests.get(link)

            # Create soup from site
            soup = driver.soup(link)
            #soup = BeautifulSoup(url.content, features="html.parser")

            # Create dir for the extracted data
            _dir = {
                "`item-name`": "None",
                "`item-price`": "None",
                "`shop-name`": "None",
                "`shop-link`": "None"
            }

            # Obtain Item name
            for header in soup.find_all('header'):
                for h1 in header.find_all('h1'):
                    for a in h1.find_all('a'):
                        _dir['`item-name`'] = a.text
                        print(f"Found: {_dir['`item-name`']}")

            # Obtain cheapest price
            # Get table
            for table in soup.find_all('table', class_='shop-listing'):

                # Get table body
                for tbody in table.find_all('tbody'):

                    # Get individual row
                    for tr in tbody.find_all('tr'):

                        # Extract specific data from row

                        # Extract Shop name and Shop link
                        for td in tr.find_all('td', class_="shop-name"):
                            for p in td.find_all('p'):
                                for a in p.find_all('a'):
                                    _dir['`shop-name`'] = str(a.text).replace("\n", "")
                                    _dir['`shop-link`'] = link

                        # Extract Item price
                        for td in tr.find_all('td', class_="shop-price"):
                            for p in td.find_all('p'):
                                for a in p.find_all('a'):
                                    _dir['`item-price`'] = str(a.text).replace('\xa0', '').replace('\n', '')

                        # Break loop
                        break

            # Add _row to data list
            data.append(_dir)

            # Quit the driver
            driver.quit()
            
    except Exception as err:
        print(err)

    return data
