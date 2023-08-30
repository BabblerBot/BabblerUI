import requests
import difflib
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


# code to get summary from summarize model
def get_summary(book_id):
    response = requests.get(os.getenv("SUMMARY_BACKEND") + f"get_summary/{book_id}")
    if response.status_code == 200:
        data = response.json()
        return data["summary"]
    return f"Error {response.status_code}"
