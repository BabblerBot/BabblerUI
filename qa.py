import requests
import os
from dotenv import load_dotenv

load_dotenv()


async def prepare_qa(book_id):
    response = requests.get(
        os.getenv("QA_BACKEND") + f"book", params={"book_id": book_id}
    )
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            return True
    return False
