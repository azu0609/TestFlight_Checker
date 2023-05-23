import requests
from bs4 import BeautifulSoup
import sys


class Checker():
    def __init__(self, url: str):
        self.site_recipe = [
            {
                "name": "osu!",
                "target_url": "https://osu.ppy.sh/home/testflight",
                "class_name": "osu-page osu-page--generic",
                "body_tag": "a"
            },
        ]
        for recipe in self.site_recipe:
            print("RECIPE: Finding recipe")
            if recipe["name"] in url:
                print(f"{recipe['name']}: Found recipe. Following recipe...")
                print(f"{recipe['name']}: Sending request to: {recipe['target_url']}")
                self.response = requests.get(recipe["target_url"], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'})
                print(f"{recipe['name']}: Fetching testflight link from: {recipe['target_url']}")
                url = self.fetch_html(recipe["class_name"], recipe["body_tag"])
                print(f"{recipe['name']}: Done.")

        # Send a GET request to the website
        self.response = requests.get(url)
        if self.response.status_code == 200:
            status = self.fetch_html("beta-status", "span")
            if status.strip() == "This beta is full.":
                print("WARN: This beta is full. Try again after few days.")
            elif status.strip() == "This beta isn't accepting any new testers right now.":
                print("WARN: This beta isn't accepting any new testers right now. Try again with different link.")
            else:
                print(f"INFO: This beta is accepting new tester! what a great day! Click this link to claim: {url}")
        elif self.response.status_code == 404:
            print("ERROR: Provided link is invalid. Try again with different link.")
        elif self.response.status_code == 403:
            print("ERROR: Rate limited by Apple. Try again later")
        else:
            raise Exception(self.response.status_code + ": " + self.response.text)
    
    def fetch_html(self, class_name, element_type):
        soup = BeautifulSoup(self.response.content, 'html.parser', from_encoding="utf-8") # Create BeautifulSoup object
        div_element = soup.find('div', class_=class_name) # Find the <div> element with class 'beta-status'
        text_element = div_element.find(element_type) # Find the text element within the <div> element
        text = text_element.get_text() # Extract the text from the text element

        return text
    

if len(sys.argv) > 1:
    url = sys.argv[1:][0]
    Checker(url)
else:
    raise Exception("No arguments found.")