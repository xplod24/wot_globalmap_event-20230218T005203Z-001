#!/usr/bin/env python3
import requests
import json
import os
import os.path
import sys
from time import sleep
from datetime import datetime
from easygui import *
from alive_progress import alive_bar
import PySimpleGUI as sg

url_tanks_by_name = "https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=9ec1b1d893318612477ebc6807902c3c&fields=name&page_no=1"

def get_tanks_to_json():
    global gh, count, page_total, total, limit, page
    event_response = requests.get(url_tanks_by_name)
    b = event_response.content
    with open("tanks_by_name.json", "wb") as a:
        a.write(b)
    gh = json.loads(b)
    metadata = gh["meta"]
    count = 0
    page_total = 0
    total = 0
    limit = 0
    page = 0
    for i in metadata:
        if i == "count":
            count = str(metadata[i])
        if i == "page_total":
            page_total = str(metadata[i])
        if i == "total":
            total = str(metadata[i])
        if i == "limit":
            limit = str(metadata[i])
        if i == "page":
            page = str(metadata[i])
    msg = f"Pojazdów na stronę: {count}\nLiczba stron: {page_total}\nLiczba pojazdów: {total}\nLimit wyświetlania na stronę (max:100): {limit}\nStrona wyświetlana: {page}"

    sg.popup(msg,title="Wynik wyszukiwania")
        




