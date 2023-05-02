import requests
from bs4 import BeautifulSoup

def check_links(urls):
    broken_links_found = False
    
    for url in urls:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Use BeautifulSoup to parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links on the page
        links = soup.find_all('a')
        
        # Check each link to see if it's broken
        for link in links:
            href = link.get('href')
            if href is not None:
                # If the link starts with "http" or "https", assume it's an external link and skip it
                if href.startswith('http') or href.startswith('https'):
                    continue
                # Otherwise, append the link to the base URL and send a HEAD request to check if it's valid
                else:
                    full_url = url + href
                    try:
                        response = requests.head(full_url)
                        response.raise_for_status()
                    except requests.exceptions.HTTPError:
                        print(f"Broken link found: {full_url}")
                        broken_links_found = True
    
    if not broken_links_found:
        print("No broken links found.")

# Example usage
urls = ['https://www.example.com/', 'https://www.example.com/about', 'https://www.example.com/contact']
check_links(urls)
