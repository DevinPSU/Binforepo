
import random
import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    """
    Scrapes the title and body of a web article.

    Args:
        url (str): The URL of the article to scrape.

    Returns:
        tuple: A tuple containing the article title (str) and body (str),
               or (None, None) if scraping fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the article title (often in <h1>)
        title = soup.find('h1')
        title_text = title.get_text(strip=True) if title else "No Title Found"

        # Find all paragraph tags for the article body
        paragraphs = soup.find_all('p')
        body_text = ' '.join([p.get_text(strip=True) for p in paragraphs])

        return title_text, body_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None, None
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None, None

def replace_random_word(text, replacement_dict):
    """
    Randomly selects and replaces a word in the text based on a dictionary.

    Args:
        text (str): The text to modify.
        replacement_dict (dict): A dictionary where keys are words to find
                                 and values are their replacements.

    Returns:
        str: The text with one word randomly replaced, or the original text
             if no replaceable words are found.
    """
    words = text.split()
    
    # Find all words in the text that are in our replacement dictionary
    replaceable_words = [word for word in words if word.lower().strip('.,!?;:') in replacement_dict]

    if not replaceable_words:
        print("No words from the replacement dictionary were found in the article.")
        return text

    # Randomly select one of the replaceable words
    word_to_replace = random.choice(replaceable_words)
    clean_word = word_to_replace.lower().strip('.,!?;:')
    
    # Get the replacement from the dictionary
    replacement = replacement_dict[clean_word]

    # To maintain case, we can check if the original word was capitalized
    if word_to_replace.istitle():
        replacement = replacement.capitalize()
    
    # Replace only the first occurrence of the randomly chosen word instance
    # This is a simple approach. For more complex scenarios, regex might be better.
    # We use a trick with a list to replace only the first match
    for i, word in enumerate(words):
        if word == word_to_replace:
            words[i] = replacement
            break
            
    return ' '.join(words)

if __name__ == "__main__":
    # --- Configuration ---
    # URL of the article to scrape
    ARTICLE_URL = "https://www.tofugu.com/japanese/da-vs-desu-in-real-life/?series=common-japanese-beginner-questions"

    # Dictionary of words to replace {word_to_find: replacement}
    # Words to find should be lowercase
    REPLACEMENT_DICT = {
        "python": "anaconda",
        "language": "dialect",
        "code": "script",
        "programming": "scripting",
        "interpreted": "translated",
        "developer": "creator"
    }
    # -------------------

    print(f"Scraping article from: {ARTICLE_URL}")
    article_title, article_body = scrape_article(ARTICLE_URL)

    if article_body:
        print("\n--- Original Article Title ---")
        print(article_title)
        
        print("\n--- Original Article Body (first 500 chars) ---")
        print(article_body[:500] + "...")

        # Combine title and body for replacement
        full_text = article_title + " " + article_body
        
        # Perform the random word replacement
        modified_text = replace_random_word(full_text, REPLACEMENT_DICT)

        print("\n\n--- Article After Random Word Replacement (first 500 chars) ---")
        print(modified_text[:500] + "...")
        
        # You can also save the full modified text to a file if you wish
        # with open("modified_article.txt", "w") as f:
        #     f.write(modified_text)
        # print("\nFull modified article saved to modified_article.txt")
