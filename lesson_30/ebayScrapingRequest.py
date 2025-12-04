import requests


url = "https://www.ebay.com/sch/i.html?_nkw=laptop"

response = requests.get(url)

if response.status_code == 200:
   print(response.text)

else:
   print(f"failed to retrieve content from {url}")