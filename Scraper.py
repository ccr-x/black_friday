import signal
from dotenv import load_dotenv
from pathlib import Path
import os
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
import mariadb

OPERATING_SYSTEM = "windows"

# --- Stray Functions --- #
def screenshot(link: str, item_name: str, tag: str, sharepoint=True, typeof: str = None, name: str = None):
    """
    Screenshot the current page based on the given parameters.

    :param link: link of the page that you want to screenshot
    :param sharepoint: Boolean that determines if the picture will be taken an uploaded to sharepoint
    :param tag: the tag: div, span, p, head, body...
    :param typeof: tag parameter: class, name, id ...
    :param name: Name of the class, name or id
    :param item_name: Name of the item that is to be screenshotted
    """

    driver = Driver()

    if typeof is None or name is None:
        # Go to link
        driver.get(link)

        # Get the right tag and class
        element = driver.find_element(By.TAG_NAME, tag)

        if sharepoint:
            # Make a screenshot
            url = driver.save_to_sharepoint({item_name: element.screenshot_as_png})

            driver.quit()

            return url

    else:
        # Go to link
        driver.get(link)

        # Get the right tag and class
        element = driver.find_element(By.CSS_SELECTOR, f"{tag}[{typeof}='{name}']")

        if sharepoint:
            # Make a screenshot
            url = driver.save_to_sharepoint({item_name: element.screenshot_as_png})

            driver.quit()

            return url


def multiReplace(string):
    """Changes certain characters with other characters"""

    string = str(string).replace("'", '')
    string = string.replace('\r', '')
    string = string.replace('\n', ' ')
    string = string.replace('\xa0', ' ')
    string = string.replace('/', ' ')
    string = string.replace(':', '.')

    return string


def create_dict(columns, values):
    """
    Creates multiple dicts with the given parameters

    :param columns: Must be a tuple that has the same length as the tuples inside the values tuple
    :param values: Must be tuples in tuples
    """

    # Check for length of given data
    if isinstance(values[0], tuple) or isinstance(values[0], list):
        # Create variables
        _list = []

        # Create multiple dicts and add them to a list
        for x in values:
            _dict = {}
            for y, z in enumerate(x):
                _dict[columns[y]] = z
            _list.append(_dict)

        return _list

    else:
        # Create a single dict
        _dict = {}
        for x, y in enumerate(columns):
            _dict[y] = values[x]
        return _dict

# --- End of Stray Functions --- #


class Driver(object):
    """ Creates an object that will let the user scrape data from webpages """

    def __init__(self):

        self.options = webdriver.FirefoxOptions()

        # Set headless mode to True (Does not open a physical browser)
        self.options.headless = True

        # Fools the browser by letting it know that it is not a bot
        self.options.add_argument('--disable-blink-features=AutomationControlled')

        # Set driver to firefox
        self.driver = webdriver.Firefox(options=self.options)

    def get(self, url):
        """ Opens a new instance of firefox and goes the provided link

            :param url: URL of page that the driver will navigate to

        """
        self.driver.get(url)

    def close(self):
        """ Closes currently open tab in firefox instance """
        self.driver.close()

    def quit(self):
        """ Closes the whole firefox instance """

        self.driver.quit()

        if OPERATING_SYSTEM == "linux":
            try:
                pid = True
                while pid:
                    pid = os.waitpid(-1, os.WNOHANG)

                    # Wonka's Solution to avoid infinite loop cause pid value -> (0, 0)
                    try:
                        if pid[0] == 0:
                            pid = False
                    except:
                        pass
                    # ---- ----

            except ChildProcessError:
                pass

    def kill(self):
        """ Extreme way of ending an open driver session. This will kill the whole process.

            Note: Only use this if driver.quit() or driver.close() do not work properly
        """
        try:
            pid = self.driver.service.process.pid
            os.kill(int(pid), signal.SIGTERM)

        except Exception as err:
            pass  # print(f"{bcolors.FAIL}[WARNING]: {bcolors.ENDC + type(err).__name__}: {err}")

    def implicitly_wait(self, timeout):
        """ Makes the webdriver wait for specified amount of time to let the page load

            :param timeout: Amount (in seconds) that the webdriver will wait
        """
        self.driver.implicitly_wait(timeout)

    def impatiently_wait(self, timeout):
        """ Makes the whole script wait for specified amount of time

            :param timeout: Amount (in seconds) that the webdriver will wait
        """
        sleep(timeout)

    def save_to_sharepoint(self, data: dict):
        """ Saves screenshot to sharepoint

            :param data: screenshot (in byte format) + name

            :Usage:
            ::

                url = driver.save_to_sharepoint({"foo": "bar"})
        """
        try:
            item_name = ''
            item = ''

            for name, byte in data.items():
                item_name = name
                item = byte

            # Create a link to the uploaded screenshot
            url = f"https://cttwente.sharepoint.com/sites/sales2/Gedeelde%20%20documenten/General/Nieuwsberichten/" \
                  f"{item_name}"

            # Upload the screenshot
            y = Sharepoint()
            y.new_sp_upload(item_name, item)

            return url

        except Exception as err:
            print(f"{bcolors.FAIL}[WARNING]: {bcolors.ENDC + type(err).__name__}: {err}")

    def find_element(self, by=By.ID, value: str = None) -> WebElement:
        """ Find element given a By strategy and locator

            :Usage:
            ::

                element = driver.find_element(By.ID, 'foo')

            :rtype: WebElement
        """
        try:
            return self.driver.find_element(by, value)

        except Exception as err:
            print(f"{bcolors.FAIL}[WARNING]: {bcolors.ENDC + type(err).__name__}: {err}")

    def soup(self, url=None, timeout=0, extra=None):
        """ Creates soup using the driver navigated webpage. \n
            It is recommended to use one of the built-in wait functions to help the webpage load in completely.

            :Usage:
            ::

                soup = driver.soup(url)
        """

        try:
            if url is None:
                return BeautifulSoup(self.driver.page_source, 'html.parser')
            else:
                self.get(url)

                if timeout > 0:
                    if extra == "sleep":
                        self.impatiently_wait(timeout)
                    else:
                        self.implicitly_wait(timeout)

                return BeautifulSoup(self.driver.page_source, 'html.parser')

        except Exception as err:
            print(f"{bcolors.FAIL}[WARNING]: {bcolors.ENDC + type(err).__name__}: {err}")

    def execute_script(self, script: str):
        """ Executes given javascript script

            :param script: Script that is to be executed

            :Usage:
            ::

                driver.execute_script("console.log('foo bar');")
         """
        return self.driver.execute_script(script=script)

    @property
    def page_source(self) -> str:
        """
        Gets the source of the current page.

        :Usage:
            ::

                driver.page_source
        """
        return self.driver.page_source


class Connection(object):
    """ Creates an object that will let the user access the PostGreSQL database """

    def __init__(self):
        # Get variables from .env file
        load_dotenv(dotenv_path=Path('.env'))

        host = os.getenv('HOST')
        username = os.getenv('USER')
        password = os.getenv('PWDS')
        port = os.getenv('PORT')
        database = os.getenv('DB')

        # Make connection with the Postgresql database
        try:
            self.connection = mariadb.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database
            )

        except Exception as err:
            print(f"{bcolors.FAIL}[WARNING]: {bcolors.ENDC + type(err).__name__}: {err}")

    def close(self):
        """ Closes currently active connection """

        try:
            self.connection.close()

        except Exception as err:
            print(f"[WARNING]: {type(err)}: {err}")

    def get(self, table: str, selector: str = '*', where: str or dict = None, custom=None):
        """ Performs select query on user specified table

            :param table: Table that the query is performed on
            :param selector: Returns only selected columns
            :param where: Where clause for querying specific data
            :param custom: Functions like args, just extra keywords

            :Usage:
            ::

                data = connection.get('myTable', 'foo, bar', 'id=0')
        """
        try:
            cursor = self.connection.cursor()

            if isinstance(where, dict):
                _str = ''
                for x, y in where.items():
                    _str += f"{x}='{y}' AND "

                where = _str[:-5]

            cursor.execute(f"SELECT {selector} FROM {table} {'WHERE' + ' ' + where if where is not None else ''}")

            data = cursor.fetchall()

            if custom == 'cursor':
                return cursor

            # Close cursor
            cursor.close()

            return data
        except Exception as err:
            print(f"{bcolors.FAIL}[WARNING]: {bcolors.ENDC + type(err).__name__}: {err}")

    def create(self, table: str, data: dict):
        """ Performs create query on user specified table

            :param table: Table that the query is performed on
            :param data: The values that are to be inserted into the table

            :Usage:
            ::

                connection.create('myTable', {"foo": "bar"})
        """

        try:
            columns = ''
            values = ''

            # Extract the columns and values from data dict
            for col, val in data.items():
                columns += f"{col}, "
                values += f"'{val}', "

            cursor = self.connection.cursor()

            cursor.execute(f"INSERT INTO {table} ({columns[:-2]}) VALUES ({values[:-2]})")
            self.connection.commit()

            # Close cursor
            cursor.close()

        except Exception as err:
            print(f"{bcolors.FAIL}[WARNING]: {bcolors.ENDC + type(err).__name__}: {err}")

    def update(self, table: str, setter: str or dict, where: str or dict):
        """ Performs update query on user specified table

            :param table: Table that the query is performed on
            :param where: Where clause for updating
            :param setter: All the data that is going to be changed

            :Usage:
            ::

                connection.update('myTable', 'foo=bar AND ...', id=0)

                or

                connection.update('myTable', {"foo": "bar",}, {"id": 0,})
        """
        try:
            cursor = self.connection.cursor()

            if isinstance(setter, dict):
                _str = ''
                for x, y in setter.items():
                    _str += f"{x}='{y}' AND "

                setter = _str[:-5]

            if isinstance(where, dict):
                _str = ''
                for x, y in where.items():
                    _str += f"{x}='{y}' AND "

                where = _str[:-5]

            cursor.execute(f"UPDATE {table} SET {setter} WHERE {where}")
            self.connection.commit()

            # Close cursor
            cursor.close()

        except Exception as err:
            print(f"{bcolors.FAIL}[WARNING]: {bcolors.ENDC + type(err).__name__}: {err}")

    def delete(self, table: str, where: str or dict):
        """ Performs delete query on user specified table

            :param table: Table that the query is performed on
            :param where: Where clause for deletion

            :Usage:
            ::

                connection.delete('myTable', 'foo=bar AND ...')
                connection.delete('myTable', {"foo": "bar",})
         """
        try:
            cursor = self.connection.cursor()

            if isinstance(where, dict):
                _str = ''
                for x, y in where.items():
                    _str += f"{x}='{y}' AND "

                where = _str[:-5]

            cursor.execute(f"DELETE FROM {table} WHERE {where}")
            self.connection.commit()

            # Close cursor
            cursor.close()

        except Exception as err:
            print(f"{bcolors.FAIL}[WARNING]: {bcolors.ENDC + type(err).__name__}: {err}")

    def insert_to_table(self, table: str, data: dict, screenshot_arr: list or tuple, sharepoint: bool = False):
        """ Inserts data into specified table if it's not a duplicate item

            :param table: The table that is used for insertion and checking
            :param data: The data that are inserted into the table
            :param screenshot_arr: 3 arguments that are required to screenshot (TAG, TYPE, NAME)
            :param sharepoint: Bool value that will determine the sharepoint screenshot upload

            :Usage:
            ::

                connection.insert_to_table("myTable", {"foo": "bar"}, ["div", "class", "container"], True)
        """
        try:

            # Create new dict with specific data
            _dict = {
                'link': data['link'],
                'datePublished': data['datePublished'],
                'content': data['content'],
                'source': data['source']
            }

            # Query for existing data
            cursor = self.get(table=table, where=_dict, custom='cursor')

            if cursor.rowcount >= 1:
                return

            cursor.close()

            self.create(table=table, data=data)

            if sharepoint:
                _list = self.get(table=table, selector='datePublished, uuid', where=_dict)

                item_name = f"{datetime.strftime(_list[0][0], '%Y-%m-%d')}-{_list[0][1]}.png"

                # Create a screenshot
                link = screenshot(link=data['link'], item_name=item_name, tag=screenshot_arr[0], typeof=screenshot_arr[1],
                                  name=screenshot_arr[2])

                # Update entry in database and add the sharepoint link to it
                self.update(table=table, setter=f"sharepointlink = '{link}'", where=_dict)

        except Exception as err:
            if err == KeyError:
                print(f"[WARNING]: Missing key: {err}")
            else:
                print(f"{bcolors.FAIL}[WARNING]: {bcolors.ENDC + type(err).__name__}: {err}")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

