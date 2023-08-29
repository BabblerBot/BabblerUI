import requests
import urllib.parse

GUTENDEX_URL = "https://gutendex.com/"


def search_book(query):
    parsed_query = urllib.parse.quote(query)
    response = requests.get(GUTENDEX_URL + "books/?search=" + parsed_query)
    if response.status_code != 200:
        return "Error: %s" % response.text, None
    data = response.json()
    if data["count"] == 0:
        return "Book not found", None
    book = data["results"][0]
    return None, book
