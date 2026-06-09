# def hello():
#     print("Hello")

# async def helloasync():
#     print("hello")

# hello()
# helloasync()

import asyncio
import aiohttp

async def hello():
    print("Hello")

    await asyncio.sleep(3)

    print("End")

# asyncio.run(hello())


async def fetch():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://timesindian.com") as response:
            print(response.status)

# asyncio.run(fetch())


# Real URL Scanner

urls = [
    "https://example.com",
    "https://google.com",
    "https://github.com"
]

async def check(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(url,response.status)
    except Exception:
        print(f"Failed : {url}")


async def main():
    tasks = []
    for  url in urls:
        tasks.append(check(url))

    await asyncio.gather(*tasks)


asyncio.run(main())
