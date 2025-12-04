import requests
url = "https://www.wikipedia.org"

try:
    response = requests.get(url)
    response.raise_for_status()
    print(response.text)

except requests.exceptions.HTTPError as http_err:
    print(f"http error:{http_err}")
except requests.exceptions.ConnectionError as con_err:
    print(f"connection error:{con_err}")
except requests.exceptions.Timeout as time_err:
    print(f"timeout error:{time_err}")
except requests.exceptions.RequestException as req_err:
    print(f"error:{req_err}")