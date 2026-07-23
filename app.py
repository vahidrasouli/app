import asyncio
from rubpy import Client
# import requests

async def main():
    async with Client("time_sessions") as app:
        me = await app.get_me()
        print("===================== API RESPONSE =================")
        print(me)
        print("====================================================")

if __name__ == "__main__":
    asyncio.run(main())