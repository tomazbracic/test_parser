from bs4 import BeautifulSoup
import requests

url = "http://192.168.88.188:8050/run" # local Splash instance

headers = {
    'Content-Type': 'application/json'
}

# 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'

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

# print(response.content)

data = response.content
# print(data)

soup = BeautifulSoup(data, 'html.parser')

tags = soup.select('.card-post__inner > a')

# getting links of ALL listed customers - after expaning the list with "click from Splash"
for tag in tags:
    # opening PER CUSTOMER web page
    customer_response = requests.get(tag.get('href'))
    customer_data = customer_response.content
    soup = BeautifulSoup(customer_data, 'html.parser')

    # Customer NAME
    customer_name = soup.select('.breadcrumb__link')[1].text
    print(customer_name)

    # Customer DOMAIN
    customer_domain = soup.select('.alt-btn__text')[0].text
    print(customer_domain)

    # Customer LOGO
    customer_logo = soup.select('.about-company__logo > img')[0].get('src')
    print(customer_logo)

    






# print(customer_links)