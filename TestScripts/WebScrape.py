import requests
from bs4 import BeautifulSoup

# The URL you want to scrape
url = "https://www.ossila.com/products/nickel-ii-oxide-powder"

try:
    # 1. Send a GET request to the page
    response = requests.get(url)
    
    # 2. Check if the request was successful (Status Code 200)
    if response.status_code == 200:
        # 3. Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 4. Find specific data (e.g., all <h1> tags)
        headings = soup.find_all('h1')
        synonyms = soup.find_all('td')
        references = soup.find_all('ol')
        
        print(f"Found {len(headings)} headings:")
        print(f"Found {len(synonyms)} synonyms:")
        print(f"Found {len(references)} references:")
        for i, tag in enumerate(headings, 1):
            print(f"{i}. {tag.get_text().strip()}")
        for i, tag in enumerate(synonyms, 1):
            print(f"{i}. {tag.get_text().strip()}")
        for i, tag in enumerate(references, 1):
            print(f"{i}. {tag.get_text().strip()}")
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")