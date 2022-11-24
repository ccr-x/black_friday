from Scraper import Driver
import requests
from bs4 import BeautifulSoup


def scrape_bf():
    urls = [
        "https://tweakers.net/pricewatch/1618228/amd-ryzen-5-5600x-boxed.html",
        "https://tweakers.net/processors/amd/ryzen-5-7600x_p1416760/vergelijken/",
        "https://tweakers.net/pricewatch/1618234/amd-ryzen-7-5800x-boxed.html",
        "https://tweakers.net/pricewatch/1856830/amd-ryzen-7-7700x-boxed.html",
        "https://tweakers.net/pricewatch/1740286/msi-mag-x570s-tomahawk-max-wifi.html",
        "https://tweakers.net/pricewatch/1684892/nzxt-n7-b550-zwart.html",
        "https://tweakers.net/pricewatch/1684890/nzxt-n7-b550-wit.html",
        "https://tweakers.net/pricewatch/1707712/msi-geforce-rtx-3070-ti-ventus-3x-8g-oc.html",
        "https://tweakers.net/pricewatch/1721302/asus-tuf-gaming-geforce-rtx-3080-v2-oc-edition-met-lhr.html",
        "https://tweakers.net/pricewatch/1818742/msi-radeon-rx-6750-xt-gaming-x-trio.html",
        "https://tweakers.net/pricewatch/1634706/asus-tuf-gaming-rx-6800-xt-oc.html",
        "https://tweakers.net/pricewatch/1707512/asrock-radeon-rx-6900-xt-oc-formula.html",
        "https://tweakers.net/pricewatch/1803252/gigabyte-aorus-aorus-geforce-rtx-3090-ti-xtreme-waterforce-24g.html",
        "https://tweakers.net/pricewatch/1458912/sharkoon-pure-steel-rgb-wit.html",
        "https://tweakers.net/pricewatch/1420152/thermaltake-h200-tg-snow-rgb.html",
        "https://tweakers.net/pricewatch/1721930/corsair-rm850-2021-zwart.html",
        "https://tweakers.net/pricewatch/1411298/corsair-vengeance-lpx-cmk16gx4m2d3600c18.html",
        "https://tweakers.net/pricewatch/1422518/corsair-vengeance-rgb-pro-cmw16gx4m2z3600c18.html",
        "https://tweakers.net/pricewatch/1558654/corsair-vengeance-rgb-pro-cmw16gx4m2d3600c18w.html",
        "https://tweakers.net/pricewatch/1736122/corsair-vengeance-rgb-rt-cmn16gx4m2z3600c18w.html",
    ]
    urls = open("links.txt", "r").readlines()
    data = []

    try:

        # Obtain information from website
        for link in urls:

            # Create instance
            #driver = Driver()
            url = requests.get(link)

            # Create soup from site
            #soup = driver.soup(link)
            soup = BeautifulSoup(url.content, features="html.parser")

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
            #driver.quit()
            
    except Exception as err:
        print(err)

    return data
