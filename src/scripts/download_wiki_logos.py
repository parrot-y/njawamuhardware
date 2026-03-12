import json
import os
import time
import urllib.request
import urllib.parse
from html.parser import HTMLParser

class WikiImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.image_url = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            has_internal = False
            href = ""
            for attr in attrs:
                if attr[0] == "class" and "internal" in attr[1]:
                    has_internal = True
                if attr[0] == "href":
                    href = attr[1]
            if has_internal and href and (href.endswith('.svg') or href.endswith('.png')):
                if href.startswith('//'):
                    self.image_url = "https:" + href
                else:
                    self.image_url = href

brands = [
    ("Toyota", "https://commons.wikimedia.org/wiki/File:Toyota.svg", "toyota.svg"),
    ("Nissan", "https://commons.wikimedia.org/wiki/File:Nissan_logo.png", "nissan.png"),
    ("Honda", "https://commons.wikimedia.org/wiki/File:Honda_Logo.svg", "honda.svg"),
    ("Mazda", "https://commons.wikimedia.org/wiki/File:Mazda_Logo.png", "mazda.png"),
    ("BMW", "https://commons.wikimedia.org/wiki/File:BMW.svg", "bmw.svg"),
    ("Subaru", "https://commons.wikimedia.org/wiki/File:Subaru_logo.svg", "subaru.svg")
]

base_dir = "/home/kali/Documents/graceful-motion-autospares/src/assets/images/brands"

def get_actual_url_from_wiki(wiki_url):
    req = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            parser = WikiImageParser()
            parser.feed(html)
            return parser.image_url
    except Exception as e:
        print(f"Failed to fetch {wiki_url}: {e}")
    return None

def download_file(url, filepath):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Failed direct DL: {e}")
        return False

for name, url, filename in brands:
    print(f"Processing {name}...")
    actual_url = get_actual_url_from_wiki(url)
    if actual_url:
        print(f"Found direct URL: {actual_url}")
        target = os.path.join(base_dir, filename)
        if download_file(actual_url, target):
            print(f"Successfully downloaded to {target}")
    time.sleep(1)
