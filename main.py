import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient

def run_program():
    for i in range(3):
        try:
            # Send an HTTP request to retrieve the HTML content of a web page
            response = requests.get("https://finance.yahoo.com/most-active")
            print("Status code:",response.status_code)
            response.raise_for_status()
            break
        except:
            if (i == 2):
                print("Connection is terminating after 3 retries")
            else:
                print("Error: Connection fails. Try again!")

    # Load the HTML content into BeautifulSoup
    page = BeautifulSoup(response.text, "html.parser")

    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    #Analyze pages and find the required data: python BeautifulSoup4 module
    stock_table = page.find(id="scr-res-table")
    tbody = stock_table.find("tbody")
    fields = ["Symbol", "Name", "Price (Intraday)", "Change", "Volume"]
    active_stocks = []
    idx = 1
    for tr in tbody:
        active_stock = {}
        active_stock['_id'] = idx
        idx += 1
        for td in tr:
            field = td.get('aria-label')
            if (field in fields):
                if field == "Volume":
                    # extract numbers only (22.122M)
                    active_stock[field] = float(td.text[0:-1])
                else:
                    active_stock[field] = float(td.text) if isfloat(td.text) else td.text
        active_stocks.append(active_stock)

    #Save data into a MongoDB database: python pymongo module
    client = MongoClient("mongodb://localhost:27017/")
    if 'nyse-db' in client.list_database_names():
        print("Database exists")
    mydb = client['nyse-db']
    #print(client.list_database_names())

    mycol = mydb['active-stocks']
    #If collection already have data, delete them and store new data
    if mycol.count_documents({}) == 0:
        print("Collection is empty")
        mycol.insert_many(active_stocks)
        print("Colelction created")
    else:
        res = mycol.delete_many({})
        if res.deleted_count > 0:
            print("Collection exists. Collection deleted")
            x = mycol.insert_many(active_stocks)
            print("Collection is updated")
            # for y in mycol.find():
            #     print(y)
    #print(mydb.list_collection_names())
    #mycol.drop()

round = 0
while round < 5:
    print("Round:",round)
    run_program()
    time.sleep(180) # Sleep 3 minutes
    round += 1
