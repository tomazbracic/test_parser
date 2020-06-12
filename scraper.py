from bs4 import BeautifulSoup
import requests
import csv

url = "http://192.168.88.188:8050/run" # local Splash instance

headers = {
    'Content-Type': 'application/json'
}

lua_script = """
splash:go(args.url)
splash:set_viewport_full()
local element = splash:select('.more-link')
element:mouse_click()
splash:wait(3)
return splash:html()
"""

# calling main page and clicking on "more customer link"
response = requests.post(url, json={
    'lua_source': lua_script,
    'url': 'https://www.chorus.ai/customers'
})

data = response.content
soup = BeautifulSoup(data, 'html.parser')
tags = soup.select('.card-post__inner > a')

all_customers = []

# getting links of ALL listed customers - after expaning the list with "click from Splash"
for tag in tags:
    # opening PER CUSTOMER web page
    customer_response = requests.get(tag.get('href'))
    customer_data = customer_response.content
    soup = BeautifulSoup(customer_data, 'html.parser')

    # Customer NAME
    customer_name = soup.select('.breadcrumb__link')[1].text

    # Customer DOMAIN
    customer_domain = soup.select('.alt-btn__text')[0].text

    # Customer LOGO
    customer_logo = soup.select('.about-company__logo > img')[0].get('src')

    c = (customer_name, customer_domain, customer_logo)
    all_customers.append(c)

with open('customers.csv','w') as out:
    csv_out=csv.writer(out, delimiter=';')
    csv_out.writerow(['Customer_Name','Customer_Domain','Customer_Logo'])
    for row in all_customers:
        csv_out.writerow(row)