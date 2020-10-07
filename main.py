import requests
import json
import os
import sys
import random
import string
from colorama import init,Fore
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from threading import Thread, Lock

init()
ua = UserAgent()

def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('ce', 'nt', 'dos'):
        os.system('cls')
    else:
        print("\n") * 120

def SetTitle(title_name:str):
    os.system("title {0}".format(title_name))

def ReadFile(filename,method):
    with open(filename,method) as f:
        content = [line.strip('\n') for line in f]
        return content

def PrintText(info_name,text,info_color:Fore,text_color:Fore):
    lock = Lock()
    lock.acquire()
    sys.stdout.flush()
    text = text.encode('ascii','replace').decode()
    sys.stdout.write(f'[{info_color+info_name+Fore.RESET}] '+text_color+f'{text}\n')
    lock.release()


SetTitle('One Man Builds Spotify Account Creator Tool')
clear()
birth_year_start = int(input('Enter the birth year start: '))
birth_year_end = int(input('Enter the birth year end: '))
method = int(input('[1] Valid credentails lookalike [2] Random strings (faster): '))


def AddRandomDomain(username):
    email_providers = ['gmail.com', 'yahoo.com', 'hotmail.com', 'hotmail.co.uk', 'hotmail.fr', 'outlook.com', 'icloud.com', 'mail.com', 'live.com', 'yahoo.it', 'yahoo.ca', 'yahoo.in', 'live.se', 'orange.fr', 'msn.com', 'mail.ru', 'mac.com']
    return username+'@'+random.choice(email_providers)

def GenUsername(gender):
    country_codes = ['ru','en','it','fr','uk','hu','pl','cz']

    country = random.choice(country_codes)

    URL = "https://fakenamegenerator.com/gen-{0}-{1}-{2}.php".format(gender,country,country)

    headers = {
        'User-Agent': ua.random
    }

    response = requests.get(URL,headers=headers).text
    soup = BeautifulSoup(response,"html.parser")
    fullname = soup.find('div',{'class':'address'}).h3.text
    uname_characters = string.ascii_letters + string.digits + '_'
    valid_username = fullname.lower().replace(' ','')
    characters = ''.join(random.choice(uname_characters) for i in range(random.randint(1,6)))
    return valid_username+characters


def GenCredentailsMethod1():
    credentails = {}
    credentails['gender'] = random.choice(['male', 'female'])
    credentails['birth_year'] = random.randint(birth_year_start,birth_year_end)
    credentails['birth_month'] = random.randint(1,12)
    credentails['birth_day'] = random.randint(1,28)
    password_characters = string.ascii_letters + string.digits
    password_characters = ''.join(random.choice(password_characters) for i in range(random.randint(8,15)))
    credentails['password'] = password_characters
    username = GenUsername(credentails['gender'])
    credentails['username'] = username
    email = AddRandomDomain(username)
    credentails['email'] = email
    return credentails

def GenCredentailsMethod2():
    credentails = {}
    credentails['gender'] = random.choice(['male', 'female'])
    credentails['birth_year'] = random.randint(birth_year_start,birth_year_end)
    credentails['birth_month'] = random.randint(1,12)
    credentails['birth_day'] = random.randint(1,28)
    password_characters = string.ascii_letters + string.digits
    password_characters = ''.join(random.choice(password_characters) for i in range(random.randint(8,15)))
    credentails['password'] = password_characters
    username = string.ascii_letters + string.digits
    username = ''.join(random.choice(username) for i in range(random.randint(7,11)))
    credentails['username'] = username
    email = AddRandomDomain(username)
    credentails['email'] = email
    return credentails




def SpotifyCreator(method):

    create_headers = {
        'User-agent': 'S4A/2.0.15 (com.spotify.s4a; build:201500080; iOS 13.4.0) Alamofire/4.9.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Accept': 'application/json, text/plain;q=0.2, */*;q=0.1',
        'App-Platform': 'IOS',
        'Spotify-App': 'S4A',
        'Accept-Language': 'en-TZ;q=1.0',
        'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
        'Spotify-App-Version': '2.0.15'
    }

    create_response = ''

    create_url = 'https://spclient.wg.spotify.com/signup/public/v1/account'
    
    credentails = ''

    if method == 1:
        credentails = GenCredentailsMethod1()
    else:
        credentails = GenCredentailsMethod2()
    
    payload = 'creation_point=lite_7e7cf598605d47caba394c628e2735a2&password_repeat={0}&platform=Android-ARM&iagree=true&password={1}&gender={2}&key=a2d4b979dc624757b4fb47de483f3505&birth_day={3}&birth_month={4}&email={5}&birth_year={6}'.format(credentails['password'],credentails['password'],credentails['gender'],credentails['birth_day'],credentails['birth_month'],credentails['email'],credentails['birth_year'])
    try:

        create_response = requests.post(create_url, data=payload, headers=create_headers)

        json_data = json.loads(create_response.text)

        if 'status' in json_data:
            if json_data['status'] == 1:
                username = json_data['username']
                if username != '':
                    PrintText('CREATED','{0}:{1} -> {2}:{3}/{4}/{5}/{6}'.format(credentails['email'],credentails['password'],credentails['username'],credentails['gender'],credentails['birth_year'],credentails['birth_month'],credentails['birth_day']),Fore.GREEN,Fore.WHITE)
                    with open('hits.txt','a') as f:
                        f.write('{0}:{1}\n'.format(credentails['email'],credentails['password']))
                    with open('detailed_hits.txt','a') as f:
                        f.write('{0}:{1} -> {2}:{3}/{4}/{5}/{6}\n'.format(credentails['email'],credentails['password'],credentails['username'],credentails['gender'],credentails['birth_year'],credentails['birth_month'],credentails['birth_day']))
                else:
                    SpotifyCreator(method)
            else:
                SpotifyCreator(method)
        else:
            SpotifyCreator(method)
    except:
        SpotifyCreator(method)



if __name__ == "__main__":
    print('')
    lock = Lock()
    while True:
        lock.acquire()
        Thread(target=SpotifyCreator(method)).start()
        lock.release()