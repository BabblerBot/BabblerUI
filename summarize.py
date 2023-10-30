import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()


async def get_summary(book_id):
    async with aiohttp.ClientSession(
        headers={
            "ngrok-skip-browser-warning": "true",
        }
    ) as session:
        async with session.get(
            os.getenv("SUMMARY_BACKEND") + f"get_summary/{book_id}"
        ) as response:
            if response.status == 200:
                data = await response.json()
                # print(data)
                return data["summary"]
            # print(response)
            return f"Error {response.status}"
