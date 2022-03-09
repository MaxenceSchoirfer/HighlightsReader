import re
import requests
from bs4 import BeautifulSoup

import os

from highlight import Highlight


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


file = 'data/Why We Sleep_ Unlocking the Power of Sleep and Dre - Notebook.html'
html = ""
with open(file, 'r', encoding="utf-8", errors='ignore') as f:
    for line in f:
        html = html + line

soup = BeautifulSoup(html, features="lxml")
data = soup.findAll(text=True)
result = filter(visible, data)
lines = []
for line in list(result):
    if line != "\n":
        lines.append(line.strip())

highlight = Highlight(lines[1], lines[2])
for i in range(len(lines)):
    if lines[i].__contains__("Location"):
        location = re.sub(r'^.*?L', 'L', lines[i])
        highlight.add_highlight(location, lines[i + 1])

print(highlight)
highlight.detect_language()

url = "https://api.notion.com/v1/pages"
headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json",
    "Authorization": ""
}

payloads = []

for location, items in highlight.highlights.items():
    for item in items:
        payload = {
            "parent": {"database_id": "fd5d35b9105740828b295425f4f4e1b2"},
            "properties": {
                "Summary": {"title": [{"text": {"content": "To Define"}}]},
                "Full Title": {"rich_text": [{"type": "text", "text": {"content": highlight.title}}]},
                "Author": {"select": {"name": highlight.author}},
                "Highlight": {"rich_text": [{"type": "text", "text": {"content": item}}]},
                "Location": {"rich_text": [{"type": "text", "text": {"content": location}}]},
                "Language": {"select": {"name": highlight.language}},
                "Source": {"select": {"name": "Book"}},
                "Status": {"select": {"name": "To-Do"}}
            }
        }
        payloads.append(payload)

for payload in payloads:
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)

