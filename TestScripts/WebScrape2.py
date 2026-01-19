import requests
from bs4 import BeautifulSoup

url = input("Please paste the URL you want to scrape: ")
try:
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finding the data as per your structure
        headings = soup.find_all('h1')
        synonyms = soup.find_all('td')
        references = soup.find_all('ol' and 'ul')
        
        print(f"--- Headings ---")
        for i, tag in enumerate(headings, 1):
            print(f"{i}. {tag.get_text().strip()}")

        print(f"\n--- Synonyms ---")
        for i, tag in enumerate(synonyms, 1):
            print(f"{i}. {tag.get_text().strip()}")

        print(f"\n--- References (35 chars after DOI) ---")
        for i, tag in enumerate(references, 1):
            full_text = tag.get_text().strip()
            
            # Logic: Only print if "DOI" is found
            if "DOI" in full_text:
                # Find the position where "DOI" starts
                start_index = full_text.find("DOI")
                
                # Move the pointer to right after "DOI" (3 characters)
                content_start = start_index + 3
                
                # Slice the next 20 characters
                doi_snippet = full_text[content_start : content_start + 35]
                
                print(f"{i}. DOI content: {doi_snippet.strip()}")

    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")