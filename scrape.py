import re
import requests
from bs4 import BeautifulSoup

def scrape_links(url, regex_pattern):
    # Create a session for improved performance
    with requests.Session() as session:
        # Send a GET request to the URL
        response = session.get(url)
        
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Compile the regular expression pattern
            pattern = re.compile(regex_pattern)
            
            # Find all <a> tags in the HTML content and yield matching links
            for link in soup.find_all('a'):
                if link.has_attr('href') and pattern.match(link['href']):
                    yield link['href']
        else:
            # Print an error message if the request was unsuccessful
            print("Error: Unable to retrieve webpage.")
            
