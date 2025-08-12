import asyncio
from crawl4ai import (
    AsyncWebCrawler, 
    CrawlerRunConfig,
    LXMLWebScrapingStrategy,
)

async def main():
    async with AsyncWebCrawler() as crawler:
        # Scrap internal links (among other things)
        results = await crawler.arun(
            url="https://www.uoregon.edu",
            config=CrawlerRunConfig(
                scraping_strategy=LXMLWebScrapingStrategy(),
                verbose=True
            ),
        )
        if not results.success:
            print("Crawl failed:", result.error_message)
            return None

        # Write the internal links to file in the same way as `beautiful_soup.py`
        links = set()
        for link in results.links["internal"]:
            links.add(link['href'])
        with open('c4a.out', 'w') as f:
            for link in sorted(links):
                f.write(f'{link}\n')


if __name__ == "__main__":
    asyncio.run(main())