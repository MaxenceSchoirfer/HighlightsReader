from collections import defaultdict

from langdetect import detect


class Highlight:

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.highlights = {}
        self.language = ""

    def __str__(self):
        string = "Title : " + self.title + "\n"
        string += "Author : " + self.author + "\n"
        for key, item in self.highlights.items():
            for i in item:
                string += key + " : " + i + "\n"
        return string

    def add_highlight(self, location, content):
        if location not in self.highlights:
            self.highlights[location] = []
        self.highlights[location].append(content)
        self.language = content

    def detect_language(self):
        lang = detect(self.language)
        if lang == "en":
            self.language = "English"
        elif lang == "fr":
            self.language = "French"
        else:
            self.language = "Unknown"
