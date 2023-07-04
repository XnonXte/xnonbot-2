import os
import requests
import json
from pexels_api import API


class Requests:
    def get_quote():
        quote = requests.get("https://zenquotes.io/api/random")
        load_quote = json.loads(quote.text)
        return load_quote[0]["a"], load_quote[0]["q"]

    def get_dog_pic():
        dog = requests.get("https://dog.ceo/api/breeds/image/random")
        load_dog = json.loads(dog.text)
        return load_dog["message"]

    def get_cat_pic():
        cat = requests.get("https://api.thecatapi.com/v1/images/search")
        load_cat = json.loads(cat.text)
        return load_cat[0]["url"]

    def get_waifu_pic(category):
        waifu = requests.get(f"https://api.waifu.pics/sfw/{category}")
        load_waifu = json.loads(waifu.text)
        return load_waifu["url"]

    def get_pexels_photos(results, query):
        pexels_client_api = API(os.requests("PEXELSAPI"))
        pexels_client_api.search(query, page=1, results_per_page=results)
        images = pexels_client_api.get_entries()
        for image in images:
            return image.original, image.photographer, image.description

    def get_dad_joke():
        dad_joke = requests.get("https://icanhazdadjoke.com/slack")
        load_dad_joke = json.loads(dad_joke.text)
        return load_dad_joke["attachments"][0]["text"]

    def get_would_you_rather():
        wyr = requests.get("https://would-you-rather-api.abaanshanid.repl.co/")
        load_wyr = json.loads(wyr.text)
        return load_wyr["data"]
