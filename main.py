import requests
import json
from os import name,system
from sys import stdout
from random import choice,randint
from string import ascii_letters,digits
from colorama import init,Style,Fore
from bs4 import BeautifulSoup
from threading import Thread,Lock,active_count
from time import sleep

class Main:

    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        system("title {0}".format(title_name))

    def ReadFile(self,filename,method):
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('useragents.txt','r')
        return choice(useragents)

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        proxies = {}
        if self.proxy_type == 1:
            proxies = {
                "http":"http://{0}".format(choice(proxies_file)),
                "https":"https://{0}".format(choice(proxies_file))
            }
        elif self.proxy_type == 2:
            proxies = {
                "http":"socks4://{0}".format(choice(proxies_file)),
                "https":"socks4://{0}".format(choice(proxies_file))
            }
        else:
            proxies = {
                "http":"socks5://{0}".format(choice(proxies_file)),
                "https":"socks5://{0}".format(choice(proxies_file))
            }
        return proxies

    def __init__(self):
        init(convert=True)
        self.createds = 0
        self.retries = 0
        self.SetTitle('One Man Builds Spotify Account Creator Tool')
        self.clear()
        self.title = Style.BRIGHT+Fore.RED+"""
                                   ╔════════════════════════════════════════════════╗ 
                                       ╔═╗╔═╗╔═╗╔╦╗╦╔═╗╦ ╦  ╔═╗╔═╗╔═╗╔═╗╦ ╦╔╗╔╔╦╗
                                       ╚═╗╠═╝║ ║ ║ ║╠╣ ╚╦╝  ╠═╣║  ║  ║ ║║ ║║║║ ║ 
                                       ╚═╝╩  ╚═╝ ╩ ╩╚   ╩   ╩ ╩╚═╝╚═╝╚═╝╚═╝╝╚╝ ╩ 
                                                 ╔═╗╦═╗╔═╗╔═╗╔╦╗╔═╗╦═╗                     
                                                 ║  ╠╦╝║╣ ╠═╣ ║ ║ ║╠╦╝                     
                                                 ╚═╝╩╚═╚═╝╩ ╩ ╩ ╚═╝╩╚═
                                   ╚════════════════════════════════════════════════╝                                                    
                                                                                                                
                                
        """
        print(self.title)
        self.method = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Valid Credentails Lookalike (slower) ['+Fore.RED+'0'+Fore.CYAN+']Random Strings (faster): '))
        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Proxy ['+Fore.RED+'0'+Fore.CYAN+']Proxyless: '))

        if self.use_proxy == 1:
            self.proxy_type = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Https ['+Fore.RED+'2'+Fore.CYAN+']Socks4 ['+Fore.RED+'3'+Fore.CYAN+']Socks5: '))
        
        self.threads = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Threads: '))
        self.birth_year_start = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Birth year start: '))
        self.birth_year_end = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Birth year end: '))
        self.lock = Lock()
        print('')

    def AddRandomDomain(self,username):
        email_providers = ['gmail.com', 'yahoo.com', 'hotmail.com', 'hotmail.co.uk', 'hotmail.fr', 'outlook.com', 'icloud.com', 'mail.com', 'live.com', 'yahoo.it', 'yahoo.ca', 'yahoo.in', 'live.se', 'orange.fr', 'msn.com', 'mail.ru', 'mac.com']
        return username+'@'+choice(email_providers)

    def GenUsername(self,gender):
        country_codes = ['ru','en','it','fr','uk','hu','pl','cz']

        country = choice(country_codes)

        URL = f"https://fakenamegenerator.com/gen-{gender}-{country}-{country}.php"

        headers = {
            'User-Agent': self.GetRandomUserAgent()
        }

        response = requests.get(URL,headers=headers).text
        soup = BeautifulSoup(response,"html.parser")
        fullname = soup.find('div',{'class':'address'}).h3.text
        uname_characters = ascii_letters + digits + '_'
        valid_username = fullname.lower().replace(' ','')
        characters = ''.join(choice(uname_characters) for i in range(randint(1,6)))
        return valid_username+characters


    def GenCredentailsMethod1(self):
        credentails = {}
        credentails['gender'] = choice(['male', 'female'])
        credentails['birth_year'] = randint(self.birth_year_start,self.birth_year_end)
        credentails['birth_month'] = randint(1,12)
        credentails['birth_day'] = randint(1,28)
        password_characters = ascii_letters + digits
        password_characters = ''.join(choice(password_characters) for i in range(randint(8,15)))
        credentails['password'] = password_characters
        username = self.GenUsername(credentails['gender'])
        credentails['username'] = username
        email = self.AddRandomDomain(username)
        credentails['email'] = email
        return credentails

    def GenCredentailsMethod2(self):
        credentails = {}
        credentails['gender'] = choice(['male', 'female'])
        credentails['birth_year'] = randint(self.birth_year_start,self.birth_year_end)
        credentails['birth_month'] = randint(1,12)
        credentails['birth_day'] = randint(1,28)
        password_characters = ascii_letters + digits
        password_characters = ''.join(choice(password_characters) for i in range(randint(8,15)))
        credentails['password'] = password_characters
        username = ascii_letters + digits
        username = ''.join(choice(username) for i in range(randint(7,11)))
        credentails['username'] = username
        email = self.AddRandomDomain(username)
        credentails['email'] = email
        return credentails

    def TitleUpdate(self):
        while True:
            self.SetTitle(f'One Man Builds Spotify Account Creator ^| CREATED: {self.createds} ^| RETRIES: {self.retries} ^| THREADS: {active_count()-1}')
            sleep(0.1)

    def SpotifyCreator(self):
        try:
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

            if self.method == 1:
                credentails = self.GenCredentailsMethod1()
            else:
                credentails = self.GenCredentailsMethod2()
            
            payload = 'creation_point=lite_7e7cf598605d47caba394c628e2735a2&password_repeat={0}&platform=Android-ARM&iagree=true&password={1}&gender={2}&key=a2d4b979dc624757b4fb47de483f3505&birth_day={3}&birth_month={4}&email={5}&birth_year={6}'.format(credentails['password'],credentails['password'],credentails['gender'],credentails['birth_day'],credentails['birth_month'],credentails['email'],credentails['birth_year'])
            
            create_response = ''

            if self.use_proxy == 1:
                create_response = requests.post(create_url, data=payload, headers=create_headers,proxies=self.GetRandomProxy(),timeout=5)
            else:
                create_response = requests.post(create_url, data=payload, headers=create_headers)

            json_data = json.loads(create_response.text)

            if 'status' in json_data:
                if json_data['status'] == 1:
                    username = json_data['username']
                    if username != '':
                        self.PrintText(Fore.CYAN,Fore.RED,'CREATED','{0}:{1} | {2} | {3} | {4}/{5}/{6}'.format(credentails['email'],credentails['password'],credentails['username'],credentails['gender'],credentails['birth_year'],credentails['birth_month'],credentails['birth_day']))
                        self.createds += 1
                        with open('hits.txt','a') as f:
                            f.write('{0}:{1}\n'.format(credentails['email'],credentails['password']))
                        with open('detailed_hits.txt','a') as f:
                            f.write('{0}:{1} | {2} | {3} | {4}/{5}/{6}\n'.format(credentails['email'],credentails['password'],credentails['username'],credentails['gender'],credentails['birth_year'],credentails['birth_month'],credentails['birth_day']))
                    else:
                        self.retries += 1
                        self.SpotifyCreator()
                else:
                    self.retries += 1
                    self.SpotifyCreator()
            else:
                self.retries += 1
                self.SpotifyCreator()
        except:
            self.retries += 1
            self.SpotifyCreator()

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        while True:
            if active_count()<=self.threads:
                Thread(target=self.SpotifyCreator).start()


if __name__ == "__main__":
    main = Main()
    main.Start()
    