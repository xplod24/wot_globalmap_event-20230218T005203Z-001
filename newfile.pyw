#!/usr/bin/env python3

import requests
import json
import os
import os.path
import sys
from time import *
from datetime import *
from alive_progress import *
import PySimpleGUI as sg
from tankopedia import *
import operator
import tabulate
import logging

logging.basicConfig(filename='operations.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#Let us Create an object 
logger=logging.getLogger() 
#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)

def sort_table(table, cols):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table

sg.theme('Dark')
sys.path.append("packages/")
def files_delete():
    if os.path.isfile("filejson.json"):
        os.remove("filejson.json")
    if os.path.isfile("events.json"):
        os.remove("events.json")
    if os.path.isfile("nickjson.json"):
        os.remove("nickjson.json")
    if os.path.isfile("clan.json"):
        os.remove("clan.json")
    if os.path.isfile("tanks_by_name.json"):
        os.remove("tanks_by_name.json")

reply = 0
event_name = ""
current_event_tank_place = 10000
front_id = ""
event_id = ""
setnick_id = ""
setnick_nick = ""
clan_id = ""
account = ""
search = ""
url = "https://api.worldoftanks.eu/wot/globalmap/events/?application_id=9ec1b1d893318612477ebc6807902c3c"
search_url = "https://api.worldoftanks.eu/wot/account/list/?application_id=9ec1b1d893318612477ebc6807902c3c&search="+str(search)
msg = "Wybierz EVENT do sprawdzenia"
choices = []
def run():
    global reply, front_id, event_id, url, msg, gh, asd
    event_response = requests.get(url)
    b = event_response.content
    with open("events.json", "wb") as a:
        a.write(b)
    gh = json.loads(b)
    if gh["status"] == "error":
        pass
    elif gh["status"] == "ok":
        asd = gh["data"]
    mm = 0
    for i in asd:
        if i["status"] == "ACTIVE":
            if i["event_id"] == "we_2023":
                i["event_name"] = "Wojna Bogów"
                a = i["event_name"]
                mm += 1
                if a not in choices:
                    choices.append(a)
                else:
                    pass
            else:
                pass
        elif i["status"] == "FINISHED":
            if i["event_id"] == "we_2023":
                i["event_name"] = "Wojna Bogów"
                a = i["event_name"]
                mm += 1
                if a not in choices:
                    choices.append(a)
                else:
                    pass
            else:
                a = i["event_name"]
                if a not in choices:
                    choices.append(a)
                else:
                    pass
        else:
            a = "Brak aktywnego eventu"
            choices.append(a)
    layout = [[sg.Push(), sg.Text(msg), sg.Push()],
              [sg.Push(), sg.Listbox(values=choices, size=(50,5), key="-BOX-"), sg.Push()],
              [sg.Push(), sg.Submit(), sg.Push()]
              ]
    exitbutton = [sg.Push(),sg.Button("Tankopedia"), sg.Exit(), sg.Push()]
    layout.append(exitbutton)

    window = sg.Window("WOT Global Map Event Chcecker", layout)
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            sys.exit(0)
        elif event == 'Submit':
            a = values["-BOX-"][0]
            ind = choices.index(a)
            print(ind)
            print(a)
            if a == "Wojna Bogów":
                front_id = gh["data"][ind]["fronts"]
                event_id = gh["data"][ind]["event_id"]
                if front_id:
                    front_id = gh["data"][ind]["fronts"][0]["front_id"]
                    sg.popup("Wyszukiwanie Eventu", f"Event id: {event_id}-{front_id} znaleziony!")
                    reply = 0
                else:
                    window.close()
                    sg.popup("Wyszukiwanie Eventu", f"Front z eventu {event_id} nie został odnaleziony. Aleja sław nie jest już dostępna.")
                    run()
            else:
                front_id = gh["data"][ind]["fronts"]
                event_id = gh["data"][ind]["event_id"]
                if front_id:
                    sg.popup("Wyszukiwanie Eventu", f"Event id: {event_id}-{front_id} znaleziony!")
                    reply = 0
                else:
                    window.close()
                    sg.popup("Wyszukiwanie Eventu", f"Front z eventu {event_id} nie został odnaleziony. Aleja sław nie jest już dostępna.")
                    run()
            break
        elif event == "Tankopedia":
            get_tanks_to_json()
        elif event == "BRAK AKTYWNYCH EVENTÓW":
            window.close()
            sg.popup("Wyszukiwanie Eventu - Błąd", "Brak aktywnego eventu!")
            run()
    window.close()

run()

def search_by_nick():
    global event_name, event_id, event_name, search_url, search_file, setnick_id, search, setnick_nick
    file = open("last_search.txt", "r")
    read = file.read()

    event_name = event_id+" Wyszukiwanie Nicku Gracza"
    second_layout = [[sg.Push(), sg.Text("Wpisz nick szukanego gracza"), sg.Push()],
                     [sg.Push(), sg.InputText(), sg.Push()],
                     [sg.Push(), sg.Text("Ostatnie wyszukiwanie"), sg.Push()],
                     [sg.Push(), sg.StatusBar(text=read, key="-Search_History-"), sg.Push()],
                     [sg.Push(), sg.Submit(), sg.Push()]]
    
    window = sg.Window(layout=second_layout, title=event_name)
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        sys.exit(0)
    if event == 'Submit':
        if values[0]:
            search = values[0]
            file = open("last_search.txt", "w")
            file.write(str(search))
            window["-Search_History-"].update(search)
        print(event, values)
        sg.popup("Trwa wyszukiwanie... ", no_titlebar=True, auto_close=True, auto_close_duration=2, grab_anywhere=True, modal=True, non_blocking=True)
        window.close()
    if search:
        pass
    elif search =='':
        sg.popup("Wpisz poprawny nick", "Błąd")
        window.close()
        search_by_nick()
    else:
        sg.popup("Wpisz poprawny nick", "Błąd")
        window.close()
        search_by_nick()

    print(search)
    print(search_url)
    a = str(search_url)+str(search)
    print(a)

    nick_response = requests.get(a)
    searchjson = nick_response.content
    with open("nickjson.json", "wb") as a:
        a.write(searchjson)
    search_file = json.loads(searchjson)
    nick_print = search_file["data"]
    nick_choices = []
    msg_choices = "Wybierz nick z listy"
    index = 0

    third_layout = [[sg.Push(), sg.Text("Wybierz jeden ze znalezionych nicków:"), sg.Push()]
                ]
    for i in nick_print:
        a = (str(index)+". nick: "+i["nickname"]+" id: ")
        b = i["account_id"]
        index += 1
        nick_choices.append(a+str(b))

    if not nick_choices:
        sg.popup("Nie znaleziono nicku - ponów wyszukiwanie.", "Błąd")
        window.close()
        search_by_nick()

    nicks = [sg.Push(), sg.Listbox(values=nick_choices, size=(50,15), key="-LISTBOX-"), sg.Push()]
    confirm = [sg.Push(), sg.Submit(), sg.Push()]
    third_layout.append(nicks)
    third_layout.append(confirm)
    window = sg.Window(layout=third_layout, title=msg_choices)
    event, values = window.read()
    while True:
        if event == sg.WIN_CLOSED or event == 'Exit':
            sys.exit(0)
        elif event == "Submit":
            break
    window.close()
    print(event, values)
    print("Konto: "+values["-LISTBOX-"][0])
    set_nick=values["-LISTBOX-"][0]

    if set_nick is not None:
        a = nick_choices.index(set_nick)
        set_nick = a
        print("")
    else:
        sys.exit(0)

    setnick_id = search_file["data"][set_nick]["account_id"]
    setnick_nick = search_file["data"][set_nick]["nickname"]
    chosen_acc = "Wybrane konto: id: "+str(setnick_id)+", nick: "+setnick_nick
    sg.popup(chosen_acc, title="Wybrano konto")

    layout_fifth = [[sg.Push(), sg.Text("Szukać klanowo?"), sg.Push()],
                    [sg.Push(), sg.Button("Tak"), sg.Button("Nie"), sg.Push()]]
    window = sg.Window(layout=layout_fifth, title=msg_choices)
    event, values = window.read()
    while True:
        if event == sg.WIN_CLOSED or event == 'Exit':
            sys.exit(0)
        elif event == "Nie":
            break
        elif event == "Tak":
            window.close()
            clan_search_by_user_id()
    window.close()

def clan_search_by_user_id():
    global setnick_id, clan_id, current_event_tank_place, event_id, front_id
    url1 = "https://api.worldoftanks.eu/wot/account/info/?application_id=9ec1b1d893318612477ebc6807902c3c&account_id="+str(setnick_id)
    
    response = requests.get(url1)
    filejson = response.content
    with open("account.json", "wb") as f:
        f.write(filejson)
    json_file = json.loads(filejson)
    clan_id = json_file["data"][str(setnick_id)]["clan_id"]
    url2 = "https://api.worldoftanks.eu/wot/clans/info/?application_id=9ec1b1d893318612477ebc6807902c3c&clan_id="+str(clan_id)
    print(url2)
    response2 = requests.get(url2)
    filejson2 = response2.content
    with open("clan.json", "wb") as a:
        a.write(filejson2)
    json2_file = json.loads(filejson2)
    clan_members = json2_file["data"][str(clan_id)]["members"]
    clanner = []

    for member in clan_members:
        cl = []
        v = member["account_id"]
        b = member["account_name"]

        if os.path.isfile(f"users/{v}_acc.json"):
            jsonloader = open(f"users/{v}_acc.json", "rb")
            jsonloader2 = jsonloader.read()
            accfile = json.loads(jsonloader2)
            if accfile["status"] == "error":
                pass
            elif accfile["status"] == "ok":
                acc_coins = accfile["data"][str(v)]["events"][str(event_id)][0]["fame_points"]
            if accfile["status"] == "error":
                pass
            elif accfile["status"] == "ok":
                cl.append(v)
                cl.append(b)
                cl.append(acc_coins)
                clanner.append(cl)
        else:
            cl = []
            v = member["account_id"]
            b = member["account_name"]
            if os.path.isfile(f"users/{v}_acc.json"):
                os.path.remove(f"users/{v}.json")
            url_by_nick = "https://api.worldoftanks.eu/wot/globalmap/eventaccountinfo/?application_id=9ec1b1d893318612477ebc6807902c3c&account_id="+str(v)+"&event_id="+str(event_id)+"&front_id="+str(front_id)
            response = requests.get(url_by_nick)
            filejson = response.content
            with open(f"users/{v}_acc.json", "wb") as hh: 
                hh.write(filejson)
                accfile = json.loads(filejson)
            if accfile["status"] == "error":
                pass
            elif accfile["status"] == "ok":
                acc_coins = accfile["data"][str(v)]["events"][str(event_id)][0]["fame_points"]
            if accfile["status"] == "error":
                pass
            elif accfile["status"] == "ok":
                cl.append(v)
                cl.append(b)
                cl.append(acc_coins)
                clanner.append(cl)

    layout_clan_show = [[sg.Push(), sg.Table(values=clanner ,num_rows=10, key="-TABLE-", enable_click_events=True, headings=['Id', 'Nick', 'PKT SłAWY']), sg.Push()],
                        [sg.Exit(),sg.Button('Odśwież dane')]]
    
    window = sg.Window(layout=layout_clan_show, title="Clan members info")
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            sys.exit(0)

        elif event == 'Odśwież dane':
            for member in clan_members:
                cl = []
                v = member["account_id"]
                b = member["account_name"]
                if os.path.isfile(f"users/{v}_acc.json"):
                    os.remove(f"users/{v}_acc.json")
                url_by_nick = "https://api.worldoftanks.eu/wot/globalmap/eventaccountinfo/?application_id=9ec1b1d893318612477ebc6807902c3c&account_id="+str(v)+"&event_id="+str(event_id)+"&front_id="+str(front_id)
                response = requests.get(url_by_nick)
                filejson = response.content
                with open(f"users/{v}_acc.json", "wb") as hh: 
                    hh.write(filejson)
                    accfile = json.loads(filejson)
                if accfile["status"] == "error":
                    pass
                elif accfile["status"] == "ok":
                    acc_coins = accfile["data"][str(v)]["events"][str(event_id)][0]["fame_points"]
                cl.append(v)
                cl.append(b)
                cl.append(acc_coins)
                clanner.append(cl)
                window.close()
                clan_search_by_user_id()

        if isinstance(event, tuple):
        # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
            if event[0] == '-TABLE-':
                if event[2][0] == -1 and event[2][1] != -1:           # Header was clicked and wasn't the "row" column
                    col_num_clicked = event[2][1]
                    new_table = sort_table(clanner[1:][:],(col_num_clicked, 0))
                    window['-TABLE-'].update(new_table)
                    clanner = [clanner[0]] + new_table
        elif event == 'Exit':
            break
    window.close()


def acc_print():
    global setnick_id, setnick_nick, current_event_tank_place, event_id, front_id
    url_by_nick = "https://api.worldoftanks.eu/wot/globalmap/eventaccountinfo/?application_id=9ec1b1d893318612477ebc6807902c3c&account_id="+str(setnick_id)+"&event_id="+str(event_id)+"&front_id="+str(front_id)
    response = requests.get(url_by_nick)
    filejson = response.content
    with open("filejson.json", "wb") as f:
        f.write(filejson)
    json_file = json.loads(filejson)
    account = json_file["data"][str(setnick_id)]["events"][str(event_id)]
    time = os.path.getmtime('filejson.json')
    time2 = datetime.fromtimestamp(time)
    a = ("Plik zmodyfikowany: "+str(time2))
    b = ("--------------------------")
    c = ("Statystyki konta ("+ setnick_nick +") w wydarzeniu")
    e = ("PUNKTY SŁAWY: "+ str(account[0]["fame_points"]))
    f = ("Ranking: "+ str(account[0]["rank"]))
    g = ("Rozgrane bitwy: "+str(account[0]["battles"]))
    h = ("Punkty z ostatniej godziny: "+str(account[0]["fame_points_since_turn"]))
    j = ("Zmiana pozycji w rankingu: "+ str(account[0]["rank_delta"]))
    if account[0]["rank"] is not None:
        if account[0]["rank"] <= current_event_tank_place:
            i = ("CZOŁG IS SAFE")
        else:
            i = ("PEPEHANDS")
    else:
        i = ("NAWET NIE GRAŁEŚ, PEPEANGRY")
    acc_msg = a+"\n"+b+"\n"+c+"\n"+e+"\n"+f+"\n"+g+"\n"+h+"\n"+j+"\n"+i
    layout = [[sg.Push(),sg.Text(acc_msg),sg.Push()],
              [sg.Push(),sg.Button("Cykliczne sprawdzanie"),sg.Exit(),sg.Push()]]
    window = sg.Window(title="Informacje o koncie", layout=layout, auto_close=True, auto_close_duration=10)
    event, values = window.read()
    while True:
        if event == sg.WIN_CLOSED or event == 'Exit':
            sys.exit(0)
        elif event == "Cykliczne sprawdzanie":
            break
        else:
            break
    window.close()

def time_printer(time):
    sleep(time)
    acc_print()
    time_printer(time)

def cycles():
    layout = [[sg.Push(), sg.Text("Wpisz co ile sekund program ma odświeżać statystyki"), sg.Push()],
                    [sg.Push(), sg.InputText(), sg.Push()],
                    [sg.Push(), sg.Submit(), sg.Push()]]
    window = sg.Window(layout=layout, title="Cykliczne odświeżanie")
    event, values = window.read()
    print(event, values)
    window.close()
    time = values[0]
    time = int(time)
    time_printer(time)

search_by_nick()
acc_print()
csc = gh["data"][reply]["status"]
if csc == "ACTIVE":
    cycle_layout = [[sg.Push(), sg.Text("Czy chcesz uruchomić cykliczne sprawdzanie?"), sg.Push()],
                    [sg.Push(),sg.Button("Tak"), sg.Button("Nie"), sg.Push()]]
    window = sg.Window(layout=cycle_layout, title="Cykliczne sprawdzanie")
    event, values = window.read()
    while True:
        if event == sg.WIN_CLOSED or event == 'Nie':
            acc_print()
            sys.exit(0)
        elif event == "Tak":
            break
    window.close()
    print(event, values)
else:
    sg.popup("Cykliczne sprawdzanie jest wyłączone dla nieaktywnych eventów. Program zostanie wyłączony.", title="Błąd")
    sys.exit(0)
cycles()