# `bs4` vs `c4a`

## Purpose
This prototype aims to compare two methods of extracting internal links from the 'uoregon.edu' domain: 1) HTTP GET requests combined with `bs4` (BeautifulSoup), and 2) `c4a` (crawl4ai).

## Methodology
requests and `bs4` are used to send an HTTP GET request to 'www.uoregon.edu' and extract all anchor tags with an href attribute from the raw HTML. Utility functions from `c4a`, namely `normalize_href` and `is_external`, were used to process and distinguish internal hrefs. The function `normalize_href` in `beautiful_soup.py` was modified to remove query and fragment parameters from the input href to better match the output data from the `c4a` method. The `c4a` method launches an instance of `AsyncWebCrawler` using the recommended `LXMLWebScrapingStrategy` to extract all internal links from 'www.uoregon.edu'. In both methods, the collected links are written to a file in sorted order using Python's sorted function.

## Findings
* HTTP GET requests + `bs4` is much faster than `c4a` when extracting links from a single webpage.
* HTTP GET requests extract more links than `c4a` from 'www.uoregon.edu'.

## Discussion
HTTP GET requests + `bs4` is quicker but intrinsically prone to error. The raw HTML retrieved by the HTTP GET request is usually not the same as the HTML displayed to the user. Since `c4a` uses `puppeteer` to launch a headless browser, the retrieved HTML exactly matches what the user would see. However, waiting for the final HTML is slower than simply using the raw HTML. Therefore, a headless browser approach like `c4a` is more accurate, while an HTTP request approach using `bs4` is faster.