To succesfully run the code one must first:

    - Have python 3.9 or higher installed
    - Created a virtual environment using ```python -m venv venv```
    - Activated the virtual environment using either ```.\venv\scripts\activate``` (for Windows) or ```source venv/bin/activate``` (for Linux)
    - Installed the necessary requirements using ```pip install -r requirements.txt```

    - Have a configured (postgresql) database with a "black_friday" table
        - (table_name) black_friday
        - (columns) id(int, PRIMARY KEY), NOT NULL
                    item-name(varchar(255), NOT NULL
                    item-price(varchar(8)), NOT NULL
                    shop-link(varchar(255)), NOT NULL
                    date-changed(date), NOT NULL
        - CREATE TABLE black_friday 
        (
            id INT NOT NULL PRIMARY KEY, 
            `item-name` VARCHAR(255) NOT NULL, 
            `item-price` VARCHAR(8) NOT NULL, 
            `shop-link` VARCHAR(255) NOT NULL, 
            `date-changed` DATE NOT NULL
        )

    - Have successfully filled in the .env file with a:
        - HOST
        - USERNAME
        - PASSWORD
        - PORT
        - DATABASE