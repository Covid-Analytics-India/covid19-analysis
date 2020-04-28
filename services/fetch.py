import requests
def get(url):
    try:
        response = requests.get(url)
        # print( f"Request returned {response.status_code} : '{response.reason}'" )
    except requests.HTTPError:
        # print(response.status_code, response.reason)
        raise
    return response