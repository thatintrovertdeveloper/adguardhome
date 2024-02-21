from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
import requests
import json

# IP Address of AdGuard Home Instance
host = "http://192.168.1.1:8083" # "http(s)://<adguardHomeIp:<port>"

# User Credentials
userName = "root" # Username
password = "password" # Password

# Block List URLs
url = "https://v.firebog.net/hosts/lists.php?type=tick"
block_urls = (requests.get(url, allow_redirects=True).text).splitlines()

# Allow List URLs
allow_urls = [
  "https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt",
  "https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/referral-sites.txt",
  "https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/optional-list.txt",
]

# Open TLSv1 Adapter
class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0', 'Content-Type': 'application/json'}     

s = requests.Session()
s.mount(host, MyAdapter())
x = s.post(host + "/control/login", json.dumps({"name": userName, "password" : password}), headers=headers)
print(x.text)

# Cycle through block lists
for u in block_urls:
	filterObj = json.dumps({'url':u, "name":u,"whitelist":False})
	print(filterObj)
	x = s.post(host + "/control/filtering/add_url", data = filterObj, headers=headers)
	print(x.text)

# Cycle through allow lists
for u in allow_urls:
	filterObj = json.dumps({'url':u, "name":u,"whitelist":True})
	print(filterObj)
	x = s.post(host + "/control/filtering/add_url", data = filterObj, headers=headers)
	print(x.text)