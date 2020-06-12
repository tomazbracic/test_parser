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

response = requests.post(url, json={
    'lua_source': lua_script,
    'url': 'https://www.chorus.ai/customers'
})

# print(response.content)

data = response.content
# print(data)

soup = BeautifulSoup(data, 'html.parser')

tags = soup.select('.card-post__inner > a')

for tag in tags:
    print(tag.get('href'))