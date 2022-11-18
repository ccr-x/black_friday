from Scraper import Driver, Connection


global loop
loop = True


def black_friday():
    f = open("links.txt", "r")
    urls = []
    data = []

    for line in f.read():
        urls.append(line)

    while loop:
        try:
            
            # Obtain information from website
            for link in urls:

                # Create instance
                driver = Driver()

                # Create soup from site
                soup = driver.soup(url)

                # Create dir for the extracted data
                _dir = {}

                # Obtain Item name
                for header in soup.find_all('header'):
                    for h1 in header.find_all('h1'):
                        for a in h1.find_all('a'):
                            _dir['item-name'] = a.text
                
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
                                        _dir['shop-name'] = a.text
                                        _dir['shop-link'] = a.href

                            # Extract Item price
                            for td in tr.find_all('td', class_="shop-price"):
                                for p in td.find_all('p'):
                                    for a in p.find_all('a'):
                                        _dir['item-price'] = a.text

                            # Break loop
                            break
                
                # Add _row to data list
                data.append(_dir)

                # Quit the driver
                driver.quit()

            # Obtain information from database
            conn = Connection()
            
            for item in data:
                
                # Obtain specified row from database
                result = conn.get(table="black_friday", where=f"item-name = {item['item-name']}")

                # Check if the price has changed
                if result['item-price'] != item['item-price']:

                    # Update item price if it changed
                    conn.update(table="black_friday", setter={"item-price": item['item-price']}, where={"item-name": item['item-name']})

                # Alert if item price has dropped
                if result['item-price'] < item['item-price']:
                    
                    # Alert code
                    pass
        except:
            pass

def stop_black_friday():
    loop = False