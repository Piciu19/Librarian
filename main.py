import json
import datetime
import prettytable
import msvcrt
import os
from dotenv import load_dotenv, find_dotenv
import pymongo
import keyboard

activeHiresFile = 'active.json'
historyFile = 'history.json'
dateFormat = "%d.%m.%Y"


load_dotenv(find_dotenv())
user = os.environ.get("MONGODB_USER")
password = os.environ.get("MONGODB_PASSWORD")
connectionString = f"mongodb+srv://{user}:{password}@librarian.3akhsbc.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connectionString)
db = client.Prymus
activeCollection = db.activeRents
historyCollection = db.historyRents

isJson = bool
if os.environ.get('JSON') == 'True':
    isJson = True
else:
    isJson = False

def addHire():
    """Zapisywane dane to: imię, nazwisko, klasa, tytuł książki, data wypożyczenia, kaucja"""
    sure = 0
    hireData = {}

    # imię
    print("Wpisz imię: ", end='', flush=True)  # use print instead of input to avoid blocking
    name = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                print()
                break  # exit loop
            elif key == 8:  # backspace key
                if len(name) > 0:
                    name = name[:-1]
                    print(f"\rWpisz imię: {name} {''}\b", end='', flush=True)
            else:
                name += chr(key)
                print(chr(key), end='', flush=True)

    hireData["name"] = name

    # nazwisko
    print("Wpisz nazwisko: ", end='', flush=True)  # use print instead of input to avoid blocking
    lastName = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                print()
                break  # exit loop
            elif key == 8:  # backspace key
                if len(lastName) > 0:
                    lastName = lastName[:-1]
                    print(f"\rWpisz nazwisko: {lastName} {''}\b", end='', flush=True)
            else:
                lastName += chr(key)
                print(chr(key), end='', flush=True)

    hireData["lastName"] = lastName

    print("Podaj klasę czytelnika (np. 2a): ", end='', flush=True)  # use print instead of input to avoid blocking
    klasa = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                print()
                break  # exit loop
            elif key == 8:  # backspace key
                if len(klasa) > 0:
                    klasa = klasa[:-1]
                    print(f"\rPodaj klasę czytelnika (np. 2a): {klasa} {''}\b", end='', flush=True)
            else:
                klasa += chr(key)
                print(chr(key), end='', flush=True)

    hireData["klasa"] = klasa

    # tytuł książki
    print("Wpisz tytuł wypożyczonej książki: ", end='', flush=True)  # use print instead of input to avoid blocking
    bookTitle = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                print()
                break  # exit loop
            elif key == 8:  # backspace key
                if len(bookTitle) > 0:
                    bookTitle = bookTitle[:-1]
                    print(f"\rWpisz tytuł wypożyczonej książki: {bookTitle} {''}\b", end='', flush=True)
            else:
                bookTitle += chr(key)
                print(chr(key), end='', flush=True)

    hireData["bookTitle"] = bookTitle

    print("Wpisz wartość kaucji (jeśli nie wpłacił kaucji kliknij ENTER): ", end='', flush=True)  # use print instead of input to avoid blocking
    deposit = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                if deposit == '' or deposit.isdigit() == True:
                    print()
                    break  # exit loop
            elif key == 8:  # backspace key
                if len(deposit) > 0:
                    deposit = deposit[:-1]
                    print(f"\rWpisz wartość kaucji (jeśli nie wpłacił kaucji kliknij ENTER): {deposit} {''}\b", end='', flush=True)
            else:
                deposit += chr(key)
                print(chr(key), end='', flush=True)

    isDeposit = bool
    if deposit == '':
        hireData["deposit"] = 'Brak'
        isDeposit = False
    else:
        hireData["deposit"] = str(deposit) + "zl"
        isDeposit = True

    # ustawienie daty wypożyczenia
    rentalDate = datetime.date.today()
    maxReturnDate = rentalDate + datetime.timedelta(weeks=2)
    hireData["rentalDate"] = str(f"{rentalDate.strftime(dateFormat)}")
    if isDeposit:
        hireData["maxDate"] = str(f"{maxReturnDate.strftime(dateFormat)}")
    else:
        hireData["maxDate"] = '14:10'

    summary = prettytable.PrettyTable(['Imię', 'Nazwisko', 'Klasa', 'Tytuł książki', 'Data wypożyczenia', 'Zwrot do', 'Kaucja'])
    summary.add_row([hireData["name"], hireData["lastName"], hireData["klasa"], hireData["bookTitle"], hireData["rentalDate"], hireData["maxDate"], hireData["deposit"]])
    print(summary)

    while True:
        try:
            print("[1] - tak")
            print("[0] - nie")

            sure = int(input("Na pewno chcesz dodać nowego czytelnika? "))
            if sure != 1 and sure != 0:
                raise Exception
            break
        except Exception:
            print("Wprowadzone dane są niepoprawne. Spróbuj ponownie")
            continue

    if isJson:
        if sure == 1:
            try:
                with open(activeHiresFile, "r") as f:
                    temp = json.load(f)
                    temp.append(hireData)
                with open(activeHiresFile, "w") as f:
                    json.dump(temp, f, indent=4)
                print("Wypożyczenie dodane")
            except Exception as error:
                print(error)
        elif sure == 0:
            print("Anulowano dodanie wypożyczenia")
    else:
        if sure == 1:
            activeCollection.insert_one(hireData)
        elif sure == 0:
            print("Anulowano dodanie wypożyczenia")

def endHire():
    if isJson:
        with open(activeHiresFile, "r") as f:
            viewActiveHires()
            temp = json.load(f)
            data_length = len(temp)
    else:
        documentIDs = viewActiveHires()
        data_length = activeCollection.count_documents({})

    if data_length <= 0:
        return

    print(f"Wybierz ID 1-{data_length}: ", end='', flush=True)  # use print instead of input to avoid blocking
    documentChoice = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                delOptRange = range(1, int(data_length + 1))
                if int(documentChoice) in delOptRange:
                    print()
                    print("Wypożyczenie zakończone")
                    break# exit loop
                else:
                    continue
            elif key == 8:  # backspace key
                if len(documentChoice) > 0:
                    documentChoice = documentChoice[:-1]
                    print(f"\rWybierz ID 1-{data_length}: {documentChoice} {''}\b", end='', flush=True)
            else:
                documentChoice += chr(key)
                print(chr(key), end='', flush=True)

    if isJson:
        new_data = []
        i = 1
        for entry in temp:
            if i == int(documentChoice):
                returnDate = datetime.datetime.now()
                entry["returnDate"] = str(f"{returnDate.day}.{returnDate.month}.{returnDate.year}")
                with open(historyFile, "r") as f:
                    temp = json.load(f)
                    temp.append(entry)
                with open(historyFile, "w") as f:
                    json.dump(temp, f, indent=4)
                i = i + 1
            else:
                new_data.append(entry)
                i = i + 1
            with open(activeHiresFile, "w") as f:
                json.dump(new_data, f, indent=4)
    else:
        chosenDocument = activeCollection.find_one({'_id': documentIDs[int(documentChoice) - 1]["_id"]})
        returnDate = datetime.datetime.now()
        chosenDocument["returnDate"] = str(f"{returnDate.day}.{returnDate.month}.{returnDate.year}")
        historyCollection.insert_one(chosenDocument)
        activeCollection.delete_one({'_id': chosenDocument['_id']})

def viewActiveHires():
    results = prettytable.PrettyTable(['Imię', 'Nazwisko', 'Klasa', 'Tytuł książki', 'Data wypożyczenia', 'Zwrot do', 'Kaucja', 'Status'])
    results.title = 'Trwające wypożyczenia'
    if isJson:
        with open(activeHiresFile, 'r') as f:
            jsonFile = json.load(f)
        for item in jsonFile:
            name = item["name"]
            lastName = item["lastName"]
            rentClass = item["klasa"]
            bookTitle = item["bookTitle"]
            rentalDateSTR = item["rentalDate"]
            maxDateSTR = item["maxDate"]
            deposit = item["deposit"]

            overdue = ''
            maxDate = None

            #overdue
            today = None
            if maxDateSTR != '14:10':
                #jeśli kaucja jest wpłacona
                today = datetime.datetime.today().date()
                maxDate = datetime.datetime.strptime(maxDateSTR, dateFormat).date()
                if maxDate < today:
                    difference = today - maxDate
                    overdue = f'Przetrzymanie (Kara: {difference .days}zł)'
                else:
                    overdue = 'Wypożyczona'
            else:
                # jeśli kaucja nie została wpłacona
                rentalDate = datetime.datetime.strptime(rentalDateSTR, dateFormat).date()
                today = datetime.datetime.today().date()
                if rentalDate < today:
                    difference  = today - rentalDate
                    overdue = f'Przetrzymanie (Kara: {difference .days}zł)'
                else:
                    overdue = 'Wypożyczona'

            results.add_row([name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])
    else:
        documentIDs = []
        entries = activeCollection.find()
        for item in entries:
            documentIDs.append(item) # pamiatac o numeracji od 0 w tablicy IDkow a od 1 w tabeli co się wyswietla !!!!
            name = item["name"]
            lastName = item["lastName"]
            rentClass = item["klasa"]
            bookTitle = item["bookTitle"]
            rentalDateSTR = item["rentalDate"]
            maxDateSTR = item["maxDate"]
            deposit = item["deposit"]

            # overdue
            overdue = ''
            maxDate = None
            today = None
            if maxDateSTR != '14:10':
                # jeśli kaucja jest wpłacona
                today = datetime.datetime.today().date()
                maxDate = datetime.datetime.strptime(maxDateSTR, dateFormat).date()
                if maxDate < today:
                    difference = today - maxDate
                    overdue = f'Przetrzymanie (Kara: {difference.days}zł)'
                else:
                    overdue = 'Wypożyczona'
            else:
                # jeśli kaucja nie została wpłacona
                today = datetime.datetime.today().date()
                rentalDate = datetime.datetime.strptime(rentalDateSTR, dateFormat).date()
                if rentalDate < today:
                    difference = today - rentalDate
                    overdue = f'Przetrzymanie (Kara: {difference.days}zł)'
                else:
                    overdue = 'Wypożyczona'

            results.add_row([name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])

    results.add_autoindex('ID')
    if len(results.rows) == 0:
        print()
        print('Lista jest pusta')
    else:
        print(results)

    if not isJson:
       return documentIDs

def viewHistoryHires():
    results = prettytable.PrettyTable(
        ['Imię', 'Nazwisko', 'Klasa', 'Tytuł książki', 'Data wypożyczenia', 'Zwrot do', 'Data zwrotu', 'Kaucja'])
    results.title = 'Historia wypożyczeń'
    if isJson:
        with open(historyFile, 'r') as f:
            jsonFile = json.load(f)
        for item in jsonFile:
            name = item["name"]
            lastName = item["lastName"]
            rentClass = item["klasa"]
            bookTitle = item["bookTitle"]
            rentalDate = item["rentalDate"]
            maxDate = item["maxDate"]
            returnDate = item["returnDate"]
            deposit = item["deposit"]
            results.add_row([name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDate),str(returnDate), deposit])
    else:
        entries = historyCollection.find()
        for item in entries:
            name = item["name"]
            lastName = item["lastName"]
            rentClass = item["klasa"]
            bookTitle = item["bookTitle"]
            rentalDate = item["rentalDate"]
            maxDate = item["maxDate"]
            returnDate = item["returnDate"]
            deposit = item["deposit"]
            results.add_row([name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDate),str(returnDate), deposit])

    results.add_autoindex('ID')
    if len(results.rows) == 0:
        print()
        print('Lista jest pusta')
    else:
        print(results)

def activeSearch():
    print('[1] - imię')
    print('[2] - nazwisko')
    print('[3] - klasa')
    print('[4] - tytuł książki')

    print("Po czym chcesz szukać: ", end='', flush=True)  # use print instead of input to avoid blocking
    choice = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                if int(choice) in range(1,5):
                    print()
                    break  # exit loop
                else:
                    continue
            elif key == 8:  # backspace key
                if len(choice) > 0:
                    choice = choice[:-1]
                    print(f"\rPo czym chcesz szukać: {choice} {''}\b", end='', flush=True)
            else:
                choice += chr(key)
                print(chr(key), end='', flush=True)

    print("Wprowadź szukaną frazę: ", end='', flush=True)  # use print instead of input to avoid blocking
    phrase = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                print()
                phrase = phrase
                break  # exit loop
            elif key == 8:  # backspace key
                if len(phrase) > 0:
                    phrase = phrase[:-1]
                    print(f"\rWprowadź szukaną frazę: {phrase} {''}\b", end='', flush=True)
            else:
                phrase += chr(key)
                print(chr(key), end='', flush=True)
    results = prettytable.PrettyTable(['Imię', 'Nazwisko', 'Klasa', 'Tytuł książki', 'Data wypożyczenia', 'Zwrot do', 'Kaucja', 'Status'])
    results.title = f'Szukana fraza: {phrase}'
    with open(activeHiresFile, 'r') as f:
        jsonFile = json.load(f)

    if isJson:
        for item in jsonFile:

            name = item["name"]
            lastName = item["lastName"]
            rentClass = item["klasa"]
            bookTitle = item["bookTitle"]
            rentalDateSTR = item["rentalDate"]
            maxDateSTR = item["maxDate"]
            deposit = item["deposit"]

            overdue = ''
            maxDate = None
            today = None
            if maxDateSTR != '14:10':
                today = datetime.datetime.today().date()
                maxDate = datetime.datetime.strptime(maxDateSTR, dateFormat).date()
                if maxDate < today:
                    difference = today - maxDate
                    overdue = f'Przetrzymanie (Kara: {difference.days}zł)'
                else:
                    overdue = 'Wypożyczona'
            else:
                rentalDate = datetime.datetime.strptime(rentalDateSTR, dateFormat).date()
                today = datetime.datetime.today().date()
                if rentalDate < today:
                    difference = today - rentalDate
                    overdue = f'Przetrzymanie (Kara: {difference.days}zł)'
                else:
                    overdue = 'Wypożyczona'

            if choice == str("1"):
                if str(phrase) in name:
                    results.add_row([name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])
            if choice == str("2"):
                if str(phrase) in lastName:
                    results.add_row([name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])
            if choice == str("3"):
                if str(phrase) in rentClass:
                    results.add_row([name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])
            if choice == str("4"):
                if str(phrase) in bookTitle:
                    results.add_row([name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])
    else:
        entries = activeCollection.find()
        for item in entries:

            name = item["name"]
            lastName = item["lastName"]
            rentClass = item["klasa"]
            bookTitle = item["bookTitle"]
            rentalDateSTR = item["rentalDate"]
            maxDateSTR = item["maxDate"]
            deposit = item["deposit"]

            overdue = ''
            maxDate = None
            today = None
            if maxDateSTR != '14:10':
                today = datetime.datetime.today().date()
                maxDate = datetime.datetime.strptime(maxDateSTR, dateFormat).date()
                if maxDate < today:
                    difference = today - maxDate
                    overdue = f'Przetrzymanie (Kara: {difference.days}zł)'
                else:
                    overdue = 'Wypożyczona'
            else:
                rentalDate = datetime.datetime.strptime(rentalDateSTR, dateFormat).date()
                today = datetime.datetime.today().date()
                if rentalDate < today:
                    difference = today - rentalDate
                    overdue = f'Przetrzymanie (Kara: {difference.days}zł)'
                else:
                    overdue = 'Wypożyczona'

            if choice == str("1"):
                if str(phrase) in name:
                    results.add_row(
                        [name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])
            if choice == str("2"):
                if str(phrase) in lastName:
                    results.add_row(
                        [name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])
            if choice == str("3"):
                if str(phrase) in rentClass:
                    results.add_row(
                        [name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])
            if choice == str("4"):
                if str(phrase) in bookTitle:
                    results.add_row(
                        [name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])

    if len(results.rows) <= 0:
        print()
        print('Lista jest pusta')
    else:
        print(results)

def historySearch():
    print('[1] - imię')
    print('[2] - nazwisko')
    print('[3] - klasa')
    print('[4] - tytuł książki')

    print("Po czym chcesz szukać: ", end='', flush=True)  # use print instead of input to avoid blocking
    choice = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                if int(choice) in range(1, 5):
                    print()
                    break  # exit loop
                else:
                    continue
            elif key == 8:  # backspace key
                if len(choice) > 0:
                    choice = choice[:-1]
                    print(f"\rPo czym chcesz szukać: {choice} {''}\b", end='', flush=True)
            else:
                choice += chr(key)
                print(chr(key), end='', flush=True)

    print("Wprowadź szukaną frazę: ", end='', flush=True)  # use print instead of input to avoid blocking
    phrase = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                print()
                phrase = phrase
                break  # exit loop
            elif key == 8:  # backspace key
                if len(phrase) > 0:
                    phrase = phrase[:-1]
                    print(f"\rWprowadź szukaną frazę: {phrase} {''}\b", end='', flush=True)
            else:
                phrase += chr(key)
                print(chr(key), end='', flush=True)
    results = prettytable.PrettyTable(['Imię', 'Nazwisko', 'Klasa', 'Tytuł książki', 'Data wypożyczenia', 'Zwrot do', 'Data zwrotu', 'Kaucja'])
    results.title = f'Szukana fraza: {phrase}'
    with open(historyFile, 'r') as f:
        jsonFile = json.load(f)

    if isJson:
        for item in jsonFile:

            name = item["name"]
            lastName = item["lastName"]
            rentClass = item["klasa"]
            bookTitle = item["bookTitle"]
            rentalDate = item["rentalDate"]
            maxDate = item["maxDate"]
            returnDate = item['returnDate']
            deposit = item["deposit"]

            if choice == str("1"):
                if str(phrase) in name:
                    results.add_row([name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDate),str(returnDate), deposit])
            if choice == str("2"):
                if str(phrase) in lastName:
                    results.add_row([name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDate),str(returnDate), deposit])
            if choice == str("3"):
                if str(phrase) in rentClass:
                    results.add_row([name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDate),str(returnDate), deposit])
            if choice == str("4"):
                if str(phrase) in bookTitle:
                    results.add_row([name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDate),str(returnDate), deposit])
    else:
        entries = historyCollection.find()
        for item in entries:

            name = item["name"]
            lastName = item["lastName"]
            rentClass = item["klasa"]
            bookTitle = item["bookTitle"]
            rentalDate = item["rentalDate"]
            maxDate = item["maxDate"]
            returnDate = item['returnDate']
            deposit = item["deposit"]

            if choice == str("1"):
                if str(phrase) in name:
                    results.add_row(
                        [name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDate), str(returnDate), deposit])
            if choice == str("2"):
                if str(phrase) in lastName:
                    results.add_row(
                        [name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDate), str(returnDate), deposit])
            if choice == str("3"):
                if str(phrase) in rentClass:
                    results.add_row(
                        [name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDate), str(returnDate), deposit])
            if choice == str("4"):
                if str(phrase) in bookTitle:
                    results.add_row(
                        [name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDate), str(returnDate), deposit])

    if len(results.rows) == 0:
        print()
        print('Lista jest pusta')
    else:
        print(results)

def addDeposit():
    if isJson:
        with open(activeHiresFile, "r") as f:
            viewActiveHires()
            temp = json.load(f)
            data_length = len(temp)
    else:
        documentIDs = viewActiveHires()
        data_length = activeCollection.count_documents({})

    if data_length <= 0:
        return

    print("Wpisz ID wypożyczenia w którym chcesz dodać kaucję: ", end='',
          flush=True)  # use print instead of input to avoid blocking
    documentChoice = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                idRange = range(1, int(data_length + 1))
                if int(documentChoice) in idRange:
                    print()
                    break  # exit loop
            elif key == 8:  # backspace key
                if len(documentChoice) > 0:
                    documentChoice = documentChoice[:-1]
                    print(f"\rWpisz ID wypożyczenia w którym chcesz dodać kaucję: {documentChoice} {''}\b", end='',
                          flush=True)
            else:
                documentChoice += chr(key)
                print(chr(key), end='', flush=True)

    print("Wpisz wartość kaucji (jeśli nie wpłacił kaucji kliknij ENTER): ", end='',flush=True)  # use print instead of input to avoid blocking
    deposit = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                if deposit == '' or deposit.isdigit() == True:
                    print()
                    break  # exit loop
            elif key == 8:  # backspace key
                if len(deposit) > 0:
                    deposit = deposit[:-1]
                    print(f"\rWpisz wartość kaucji (jeśli nie wpłacił kaucji kliknij ENTER): {deposit} {''}\b", end='',flush=True)
            else:
                deposit += chr(key)
                print(chr(key), end='', flush=True)

    if deposit == '':
        deposit = "Brak"
        isDeposit = False
    else:
        deposit = str(deposit) + "zl"
        isDeposit = True

    if isJson:
        newData = []
        i = 1
        for entry in temp:
            if i == int(documentChoice):
                entry["deposit"] = deposit
                if isDeposit:
                    rentalDateSTR = entry["rentalDate"]
                    rentalDate = datetime.datetime.strptime(rentalDateSTR, dateFormat)
                    maxReturnDate = rentalDate + datetime.timedelta(weeks=2)
                    entry["maxDate"] = str(f"{maxReturnDate.strftime(dateFormat)}")
                else:
                    entry["maxDate"] = '14:10'
                newData.append(entry)
                i = i + 1
            else:
                newData.append(entry)
                i = i + 1

        with open(activeHiresFile, 'w') as f:
            json.dump(newData,f, indent=4)
    else:
        chosenDocument = activeCollection.find_one({'_id': documentIDs[int(documentChoice) - 1]["_id"]})
        if isDeposit:
            rentalDateSTR = chosenDocument["rentalDate"]
            rentalDate = datetime.datetime.strptime(rentalDateSTR, dateFormat)
            maxReturnDate = rentalDate + datetime.timedelta(weeks=2)
            maxDate = str(f"{maxReturnDate.strftime(dateFormat)}")
        else:
            maxDate = '14:10'
        updates = {
            "$set": {"deposit": deposit, "maxDate": maxDate}
        }
        activeCollection.update_one({"_id": chosenDocument["_id"]}, update=updates)
    print('Zmieniono kaucję')

def viewTodayReturns():
    results = prettytable.PrettyTable(['Imię', 'Nazwisko', 'Klasa', 'Tytuł książki', 'Data wypożyczenia', 'Zwrot do', 'Kaucja'])
    results.title = 'Książki z dzisiejszym terminem'
    with open(activeHiresFile, 'r') as f:
        jsonFile = json.load(f)

    if isJson:
        for entry in jsonFile:
            maxReturnDate = ''
            name = entry["name"]
            lastName = entry["lastName"]
            rentClass = entry["klasa"]
            bookTitle = entry["bookTitle"]
            rentalDate = entry["rentalDate"]
            maxDateSTR = entry["maxDate"]
            deposit = entry["deposit"]

            today = datetime.date.today().strftime(dateFormat)
            if maxDateSTR != '14:10':
                maxReturnDate = datetime.datetime.strptime(maxDateSTR, dateFormat).strftime(dateFormat)

            if maxReturnDate == today or maxDateSTR == '14:10':
                results.add_row([name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDateSTR), deposit])
    else:
        entries = activeCollection.find()
        for entry in entries:
            maxReturnDate = ''
            name = entry["name"]
            lastName = entry["lastName"]
            rentClass = entry["klasa"]
            bookTitle = entry["bookTitle"]
            rentalDate = entry["rentalDate"]
            maxDateSTR = entry["maxDate"]
            deposit = entry["deposit"]

            today = datetime.date.today().strftime(dateFormat)
            if maxDateSTR != '14:10':
                maxReturnDate = datetime.datetime.strptime(maxDateSTR, dateFormat).strftime(dateFormat)

            if maxReturnDate == today or maxDateSTR == '14:10':
                results.add_row([name, lastName, rentClass, bookTitle, str(rentalDate), str(maxDateSTR), deposit])

    if len(results.rows) == 0:
        print()
        print('Lista jest pusta')
    else:
        print(results)

def extension():
    newData = []
    with open(activeHiresFile, 'r') as f:
        temp = json.load(f)
        dataLengthList = []
        if isJson:
            for item in temp:
                if item["maxDate"] != '14:10':
                    dataLengthList.append(item)
            dataLength = len(dataLengthList)
        else:
            dataLength = activeCollection.count_documents({"maxDate":{"$not":"14:10"}})
            entries = activeCollection.find({"maxDate": {"$not": "14:10"}})

    # View
    view = prettytable.PrettyTable(['Imię', 'Nazwisko', 'Klasa', 'Tytuł książki', 'Data wypożyczenia', 'Zwrot do', 'Kaucja', 'Status'])
    view.title = 'Trwające wypożyczenia'
    if isJson:
        for item in temp:
            name = item["name"]
            lastName = item["lastName"]
            rentClass = item["klasa"]
            bookTitle = item["bookTitle"]
            rentalDateSTR = item["rentalDate"]
            maxDateSTR = item["maxDate"]
            deposit = item["deposit"]
            overdue = ''
            maxDate = None

            # overdue
            today = None
            if maxDateSTR != '14:10':
                # jeśli kaucja jest wpłacona
                today = datetime.datetime.today().date()
                maxDate = datetime.datetime.strptime(maxDateSTR, dateFormat).date()
                if maxDate < today:
                    difference = today - maxDate
                    overdue = f'Przetrzymanie (Kara: {difference.days}zł)'
                else:
                    overdue = 'Wypożyczona'
                view.add_row([name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])
    else:
        for item in entries:
            name = item["name"]
            lastName = item["lastName"]
            rentClass = item["klasa"]
            bookTitle = item["bookTitle"]
            rentalDateSTR = item["rentalDate"]
            maxDateSTR = item["maxDate"]
            deposit = item["deposit"]
            overdue = ''
            maxDate = None

            # overdue
            today = None
            # jeśli kaucja jest wpłacona
            today = datetime.datetime.today().date()
            maxDate = datetime.datetime.strptime(maxDateSTR, dateFormat).date()
            if maxDate < today:
                difference = today - maxDate
                overdue = f'Przetrzymanie (Kara: {difference.days}zł)'
            else:
                overdue = 'Wypożyczona'
            view.add_row(
                [name, lastName, rentClass, bookTitle, str(rentalDateSTR), str(maxDateSTR), deposit, overdue])

    view.add_autoindex('ID')
    if len(view.rows) <= 0:
        print()
        print('Lista jest pusta')
        return
    else:
        print(view)
    # End of view

    print("Wpisz ID wypożyczenia które chcesz przedłużyć: ", end='',
          flush=True)  # use print instead of input to avoid blocking
    objectChange = ""
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # escape key
                print()
                os.system('cls')
                return  # exit function
            elif key == 13:  # enter key
                idRange = range(1, int(dataLength + 1))
                if int(objectChange) in idRange:
                    print()
                    break  # exit loop
                else:
                    continue
            elif key == 8:  # backspace key
                if len(objectChange) > 0:
                    objectChange = objectChange[:-1]
                    print(f"\rWpisz ID wypożyczenia które chcesz przedłużyć: {objectChange} {''}\b", end='', flush=True)
            else:
                objectChange += chr(key)
                print(chr(key), end='', flush=True)

    i = 1
    if isJson:
        for entry in temp:
            if entry["maxDate"] != '14:10':
                if i == int(objectChange):
                    maxDate = datetime.datetime.strptime(entry["maxDate"], dateFormat)
                    maxDate = maxDate + datetime.timedelta(weeks=2)
                    entry["maxDate"] = maxDate.strftime(dateFormat)
                    newData.append(entry)
                    i = i + 1
                else:
                    newData.append(entry)
                    i = i + 1
            else:
                newData.append(entry)

        with open(activeHiresFile, 'w') as f:
            json.dump(newData, f, indent=4)
    else:
        for entry in entries:
            if i == int(objectChange):
                maxDate = datetime.datetime.strptime(entry["maxDate"], dateFormat)
                maxDate = maxDate + datetime.timedelta(weeks=2)
                entry["maxDate"] = maxDate.strftime(dateFormat)
                newData.append(entry)
                i = i + 1
            else:
                continue

    print('Przedłużono wypożyczenie')

while True:
    choice = 0
    print("----------------------------------------------------------------------------")
    print("[1] - Dodaj wypożyczenie")
    print("[2] - Zakończ wypożyczenie")
    print("[3] - Wypożyczone książki")
    print("[4] - Zarządzaj wypożyczeniami")
    print("[5] - Wyświetl książki z dzisiejszą datą zwrotu")

    choice = input("Wybierz z listy: ")
    print()
    if choice == '1':
        addHire()
    elif choice == '2':
        endHire()
    elif choice == '3':
        print('[1] - Wyświetl trwające wypożyczenia')
        print('[2] - Wyświetl historię wypożyczeń')
        print('[3] - Przeszukaj trwające wypożyczenia')
        print('[4] - Przeszukaj historię wypożyczeń')
        choice = input("Wybierz z listy: ")
        print()
        if choice == '1':
            viewActiveHires()
        elif choice == '2':
            viewHistoryHires()
        elif choice == '3':
            activeSearch()
        elif choice == '4':
            historySearch()
        else:
            print("Wprowadzone dane są niepoprawne. Spróbuj ponownie")
    elif choice == "4":
        print('[1] - Zmień lub dodaj kaucję')
        print('[2] - Przedłuż wypożyczenie')
        choice = input("Wybierz z listy: ")
        print()
        if choice == '1':
            addDeposit()
        elif choice == '2':
            extension()
        else:
            print("Wprowadzone dane są niepoprawne. Spróbuj ponownie")
    elif choice == '5':
        viewTodayReturns()
    elif choice == 'cls':
        os.system('cls')
    else:
        print("Wprowadzone dane są niepoprawne. Spróbuj ponownie")