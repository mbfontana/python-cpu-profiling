import requests
import re
import time
import asyncio
import aiohttp


def slow_endpoint_count_https():
    with open("websitesList.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f.readlines()]

    htmls = []
    for url in urls:
        htmls = htmls + [requests.get(url).text]

    count_https = 0
    count_http = 0
    for html in htmls:
        count_https += len(re.findall("https://", html))
        count_http += len(re.findall("http://", html))

    print("finished parsing")
    time.sleep(2.0)
    print(f"{count_https=}")
    print(f"{count_http=}")
    print(f"{count_https/count_http=}")


async def improved_endpoint_count_https():
    with open("websitesList.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f.readlines()]

    htmls = []

    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)

        for response in responses:
            htmls.append(await response.text())

    count_https = sum(len(re.findall("https://", html)) for html in htmls)
    count_http = sum(len(re.findall("http://", html)) for html in htmls)

    print("finished parsing")
    print(f"{count_https=}")
    print(f"{count_http=}")
    print(f"{count_https/count_http=}")


def main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        # slow_endpoint_count_https()
        asyncio.run(improved_endpoint_count_https())

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)

    with open("profiling_stats.txt", "w") as f:
        stats = pstats.Stats(pr, stream=f)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()

    stats.dump_stats(filename="profiling_improved_endpoint.prof")


if __name__ == "__main__":
    main()
