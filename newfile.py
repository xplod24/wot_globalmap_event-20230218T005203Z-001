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
sg.theme('Dark')
sys.path.append("/packages")
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
            print (a)
            if a == "Wojna Bogów":
                event_response = requests.get(url)
                b = event_response.content
                with open("events.json", "wb") as a:
                    a.write(b)
                gh = json.loads(b)
                front_id = gh["data"][0]["fronts"][0]["front_id"]
                event_id = gh["data"][0]["event_id"]
                sg.popup("Wyszukiwanie Eventu", "Event znaleziony!")
                reply = 0
            else:
                sg.popup("Wyszukiwanie Eventu - Błąd", "Brak aktywnego eventu!")
                run()
            break
        elif event == "Tankopedia":
            get_tanks_to_json()
        elif event == "BRAK AKTYWNYCH EVENTÓW":
            sg.popup("Wyszukiwanie Eventu - Błąd", "Brak aktywnego eventu!")
            run()
    window.close()

run()

def search_by_nick():
    global event_name, event_id, event_name, search_url, search_file, setnick_id, search, setnick_nick
    event_name = event_id+" Wyszukiwanie Nicku Gracza"
    second_layout = [[sg.Push(), sg.Text("Wpisz nick szukanego gracza"), sg.Push()],
                     [sg.Push(), sg.InputText(), sg.Push()],
                     [sg.Push(), sg.Submit(), sg.Push()]]
    window = sg.Window(layout=second_layout, title=event_name)
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        run()
    if event == 'Submit':
        search = values[0]
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
            clan_search_by_user_id()
            break
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
        url_by_nick = "https://api.worldoftanks.eu/wot/globalmap/eventaccountinfo/?application_id=9ec1b1d893318612477ebc6807902c3c&account_id="+str(v)+"&event_id="+str(event_id)+"&front_id="+str(front_id)
        response = requests.get(url_by_nick)
        filejson = response.content

        # if os.path.isfile(f"users/{v}_acc.json"):
        #     pass
        # else:
        with open(f"users/{v}_acc.json", "wb") as hh: 
            hh.write(filejson)
        accfile = json.loads(filejson)
        acc_coins = accfile["data"][str(v)]["events"][str(event_id)][0]["fame_points"]
        cl.append(v)
        cl.append(b)
        cl.append(acc_coins)
        clanner.append(cl)
    layout_clan_show = [[sg.Push(), sg.Table(clanner, ["Id", "Nickname", "PKT SŁAWY"], num_rows=10), sg.Push()],
                        [sg.Exit()]]
    window = sg.Window(layout=layout_clan_show, title="Clan members info")
    event, values = window.read()
    while True:
        if event == sg.WIN_CLOSED or event == 'Exit':
            sys.exit(0)
        else:
            break
    window.close()

    msg_clan = "Clan id: "+str(clan_id)
    sg.popup(msg_clan, title="Klan")


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
    ts = datetime.fromtimestamp(account[0]["updated_at"])
    a = ("Plik zmodyfikowany: "+str(time2))
    b = ("--------------------------")
    c = ("Statystyki konta ("+ setnick_nick +") w wydarzeniu")
    d = ("Czas aktualizacji: "+str(ts))
    e = ("PUNKTY SŁAWY: "+ str(account[0]["fame_points"]))
    f = ("Ranking: "+ str(account[0]["rank"]))
    g = ("Rozgrane bitwy: "+str(account[0]["battles"]))
    h = ("Punkty z ostatniej godziny: "+str(account[0]["fame_points_since_turn"]))
    j = ("Zmiana pozycji w rankingu: "+ str(account[0]["rank_delta"]))
    if account[0]["rank"] <= current_event_tank_place:
        i = ("CZOŁG IS SAFE")
    else:
        i = ("PEPEHANDS")
    acc_msg = a+"\n"+b+"\n"+c+"\n"+d+"\n"+e+"\n"+f+"\n"+g+"\n"+h+"\n"+j+"\n"+i
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