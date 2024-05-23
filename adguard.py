import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import json
import scrape

# Prompt user for input
host = input("Enter the IP address of the AdGuard Home instance (e.g., http://192.168.1.1:8083): ")
userName = input("Enter the username: ")
password = input("Enter the password: ")

# Block List URLs
block_url = "https://v.firebog.net/hosts/lists.php?type=tick"
block_urls = requests.get(block_url).text.splitlines()

# Whitelist URL and pattern
whitelist_url = "https://github.com/anudeepND/whitelist"
whitelist_url_pattern = r"^https:\/\/raw\.githubusercontent\.com\/([a-zA-Z0-9]+)\/whitelist\/master\/domains$"

# Scrape whitelist URLs
allow_urls = list(scrape.scrape_links(whitelist_url, whitelist_url_pattern))

# Open TLSv1 Adapter
class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_version=ssl.PROTOCOL_TLSv1)

# Function to create session and login
def create_session_and_login(host, userName, password):
    s = requests.Session()
    s.mount(host, MyAdapter())
    login_payload = json.dumps({"name": userName, "password": password})
    headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
    response = s.post(f"{host}/control/login", data=login_payload, headers=headers)
    
    if response.status_code == 200:
        print("Login successful.")
        return s
    else:
        print(f"Login failed. Status code: {response.status_code}")
        return None

# Function to add URLs
def add_urls(session, host, urls, whitelist):
    headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
    for url in urls:
        filter_obj = json.dumps({'url': url, 'name': url, 'whitelist': whitelist})
        response = session.post(f"{host}/control/filtering/add_url", data=filter_obj, headers=headers)
        print(response.text)

# Create session and login
session = create_session_and_login(host, userName, password)

if session:
    # Add blocklist URLs
    add_urls(session, host, block_urls, whitelist=False)
    
    # Add allowlist URLs
    add_urls(session, host, allow_urls, whitelist=True)
else:
    print("Exiting due to login failure.")
