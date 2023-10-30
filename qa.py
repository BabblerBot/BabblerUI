import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()


async def prepare_qa(book_id, book_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            os.getenv("QA_BACKEND") + f"book",
            params={"book_id": book_id, "book_name": book_name},
        ) as response:
            if response.status == 200:
                data = await response.json()
                if data["status"] == "success":
                    return True
            return False
