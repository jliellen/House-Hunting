from bs4 import BeautifulSoup 
import requests 
import csv 
import time
import lxml

# The target webpage
url = "https://www.kijiji.ca/b-for-rent/city-of-toronto/c30349001l1700273"

# initialize page number
page = 0
# create or open rent.csv file
csv_file = open("rent.csv","w",encoding="utf-8")
# define write to object
csv_writer = csv.writer(csv_file, delimiter=',')
# loop all pages
while True:
    page += 1
    print("fetch: ", url.format(page=page)) 
    time.sleep(1)
    # get the target page
    response = requests.get(url.format(page=page))
    # set encoding format
    response.encoding = 'utf-8'
    # generate BeautifulSoup object to get the page content
    html = BeautifulSoup(response.text,features="lxml")
    # Select housing info block
    house_list = html.select(".info-container")

    
    # loop stops when there's no page to read
    if not house_list:
        break
       # loop each house 
    for i, house in enumerate(house_list):
        # get title
        house_title = house.select(".title")[1].string.replace("\n", "").strip()
        # get price
        house_money = house.select(".price")[0].string
        if house_money:
            house_money.replace("\n", "").strip()
        #get location
        house_location = house.select(".location > span")[0].string.replace("\n", "").strip()
        # get url
        house_url = "http://www.kijiji.ca" + house.select("a")[0]["href"]

        # write to csv file
        csv_writer.writerow([house_title, house_money, house_location, house_url]) 
# close csv file 
csv_file.close()