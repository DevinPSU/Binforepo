import requests
from bs4 import BeautifulSoup

url = "https://www.ossila.com/products/nickel-ii-oxide-powder"

try:
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        headings = soup.find_all('h1')
        synonyms = soup.find_all('td')
        references = soup.find_all('ol')
        
        print(f"--- Headings ---")
        for i, tag in enumerate(headings, 1):
            print(f"{i}. {tag.get_text().strip()}")

        print(f"\n--- Synonyms ---")
        for i, tag in enumerate(synonyms, 1):
            print(f"{i}. {tag.get_text().strip()}")

        print(f"\n--- References (Content between DOI and the first dot) ---")
        for i, tag in enumerate(references, 1):
            full_text = tag.get_text().strip()
            
            if "DOI" in full_text:
                # 1. Find the start of "DOI"
                start_index = full_text.find("DOI")
                content_start = start_index + 3 # Skip the letters 'D', 'O', 'I'
                
                # 2. Find the first "." AFTER the DOI start
                end_index = full_text.find(".", content_start)
                
                # 3. Slice the text
                if end_index != -1:
                    # Found a dot: slice from start to that dot
                    doi_snippet = full_text[content_start : end_index]
                else:
                    # No dot found: fallback to 20 chars so the script doesn't break
                    doi_snippet = full_text[content_start : content_start + 20]
                
                # .strip(" :") cleans up common separators like colons or spaces
                print(f"{i}. DOI content: {doi_snippet.strip(' :')}")

    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")