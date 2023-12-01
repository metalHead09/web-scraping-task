#This script should extract hotel rooms related data from the given link and store in json format.


from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import json
import csv

if __name__ == '__main__':

    url = 'https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2023-12-13&checkOut=2023-12-14&children=0&infants=0&location=London%2C%20England%2C%20United%20Kingdom&page=1&payWith=cash&searchType=list&sortBy=popularity'
    ##new_page = requests.get(url)
    ##new_soup = BeautifulSoup(new_page.text, 'html.parser')

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    html = driver.page_source

    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    room_names_class = 'css-vknzmc-Heading-Heading-Text e13es6xl3'

    rate_list = []

    roomDiv_class = 'css-1e13e1k-Box-Flex e1yh5p90'
    room_divs = soup.find_all('div', class_=roomDiv_class)

    for rooms in room_divs:                     #rooms contains the repeating divs html one by one
        room_name = rooms.find('h3', class_=room_names_class).text.strip() #name of the room in current div
        room_rates = [i.text.strip() for i in rooms.find_all('div', {'data-testid': 'total-to-pay'})]
        currency = [i.text.strip()[0:3] for i in rooms.find_all('div', class_='css-1dvtiwl-Box e1m6xhuh0')]

        guests = [int(i.text.strip()[0]) for i in rooms.find_all('span', {'data-testid': 'offer-guest-text'})]
        refund_policy = [i.text.strip() for i in rooms.find_all('div', class_='css-70zr7a-Box-Flex e1pfwvfi0')]

        deals = [i.text.strip() for i in rooms.find_all('span', class_='css-1jr3e3z-Text-BadgeText e34cw120')]

        #create json object
        rate = {"room_name": room_name, "rate_name": room_rates, "currency": currency, "no_of_guests": guests,
         "cancellation_policy": refund_policy, "deal": deals}

        rate_list.append(rate)

    json_data = json.dumps(rate_list, indent=2)

    #print(json_data)

    #json file output
    with open("output.json", "w") as json_file:
        json_file.write(json_data)

    # converting dicts directly to csv
    csv_file_path = "output.csv"
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=rate_list[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(rate_list)
