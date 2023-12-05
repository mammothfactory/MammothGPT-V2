import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# if a base url of a certain website is given, we can extract all the sub urls of the base url using the following code
def get_all_sub_urls(base_url):
    # Send a GET request to the base URL
    response = requests.get(base_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all anchor tags (links) from the page
        all_links = soup.find_all('a')

        # Get the base URL's netloc (hostname) to resolve relative URLs
        base_netloc = urlparse(base_url).netloc

        sub_urls = set()

        # Iterate through all found links
        for link in all_links:
            href = link.get('href')

            # Resolve relative URLs to absolute URLs
            if href and not href.startswith('#'):  # Ignore anchor links
                url = urljoin(base_url, href)

                # Check if the URL belongs to the same domain (netloc) as the base URL
                parsed_url = urlparse(url)
                if parsed_url.netloc == base_netloc:
                    sub_urls.add(url)

        return list(sub_urls)
    else:
        print(f"Failed to fetch {base_url}. Status code: {response.status_code}")
        return []

# Replace 'your_website_url_here' with the URL you want to scrape
base_url = 'https://www.example.com'  # Replace this with the URL you want to scrape
sub_urls = get_all_sub_urls(base_url)

if sub_urls:
    print(f"All sub-URLs from {base_url}:")
    for url in sub_urls:
        print(url)
else:
    print("No sub-URLs found.")
