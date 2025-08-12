import requests
from bs4 import BeautifulSoup
from urllib.parse import (
    urljoin, 
    urlparse, 
    urlunparse
)

#####################################################################################
# CREDIT crawl4ai (https://github.com/unclecode/crawl4ai/blob/main/crawl4ai/utils.py)
#####################################################################################

# source: (https://github.com/unclecode/crawl4ai/blob/main/crawl4ai/utils.py)
def normalize_url(href, base_url):
    """Normalize URLs to ensure consistent format"""
    from urllib.parse import urljoin, urlparse, urlunparse #< Joseph's Edit: Add urlunparse

    # Parse base URL to get components
    parsed_base = urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL format: {base_url}")
    
    if  parsed_base.scheme.lower() not in ["http", "https"]:
        # Handle special protocols
        raise ValueError(f"Invalid base URL format: {base_url}")
   
    # Original Version
    # cleaned_href = href.strip()

    # Joseph's EDIT: changed cleaned_href to strip query and fragment paramenters
    parsed_href = urlparse(href)._replace(query="", fragment="")
    cleaned_href = urlunparse(parsed_href).strip()

    # Use urljoin to handle all cases
    return urljoin(base_url, cleaned_href)


# source: (https://github.com/unclecode/crawl4ai/blob/main/crawl4ai/utils.py)
def is_external_url(url: str, base_domain: str) -> bool:
    """
    Extract the base domain from a given URL, handling common edge cases.

    How it works:
    1. Parses the URL to extract the domain.
    2. Removes the port number and 'www' prefix.
    3. Handles special domains (e.g., 'co.uk') to extract the correct base.

    Args:
        url (str): The URL to extract the base domain from.

    Returns:
        str: The extracted base domain or an empty string if parsing fails.
    """
    special = {"mailto:", "tel:", "ftp:", "file:", "data:", "javascript:"}
    if any(url.lower().startswith(p) for p in special):
        return True

    try:
        parsed = urlparse(url)
        if not parsed.netloc:  # Relative URL
            return False

        # Strip 'www.' from both domains for comparison
        url_domain = parsed.netloc.lower().replace("www.", "")
        base = base_domain.lower().replace("www.", "")

        # Check if URL domain ends with base domain
        return not url_domain.endswith(base)
    except Exception:
        return False


#########################################
#               Main Code               #
#########################################


def main():
    base_url = "https://www.uoregon.edu"
    base_domain = urlparse(base_url).netloc

    # send HTTP GET request to the url and process the raw HTML.
    response = requests.get(base_url)
    response.raise_for_status()  # Throw an error if request failed
    soup = BeautifulSoup(response.text, "html.parser")


    # Collect all internal links in a set.
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        normalized_href = normalize_url(href, base_url)
        is_external = is_external_url(normalized_href, base_domain)
        if not is_external:
            links.add(normalized_href)

    # Output the internal links to a file.
    with open('bs4.out', 'w') as f:
        for link in sorted(links):
            f.write(f'{link}\n')


if __name__ == "__main__":
    main()