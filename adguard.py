from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
import requests
import json

# Import Scrape module
import scrape

# IP Address of AdGuard Home Instance
host = "http://192.168.1.1:8083"

# User Credentials
userName = "root"
password = "password"

# Block List URLs
block_url = "https://v.firebog.net/hosts/lists.php?type=tick"
block_urls = requests.get(block_url).text.splitlines()

# Whitelist URL and pattern
whitelist_url = "https://github.com/anudeepND/whitelist"
whitelist_url_pattern = r"^https:\/\/raw\.githubusercontent\.com\/([a-zA-Z0-9]+)\/whitelist\/master\/domains$"

# Scrape whitelist URLs
matching_links = scrape.scrape_links(whitelist_url, whitelist_url_pattern)

# Allow List URLs
allow_urls = list(matching_links)

# Adapter for TLSv1
class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

# Reuse session and adapter
s = requests.Session()
s.mount(host, MyAdapter())

# Login
login_payload = json.dumps({"name": userName, "password": password})
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
response = s.post(f"{host}/control/login", data=login_payload, headers=headers)
print(response.text)

# Combine filter objects for block and allow lists
filter_objects = []
for u in block_urls:
    filter_objects.append({'url': u, "name": u, "whitelist": False})
for u in allow_urls:
    filter_objects.append({'url': u, "name": u, "whitelist": True})

# Send bulk requests
bulk_payload = json.dumps(filter_objects)
response = s.post(f"{host}/control/filtering/add_urls", data=bulk_payload, headers=headers)
print(response.text)
