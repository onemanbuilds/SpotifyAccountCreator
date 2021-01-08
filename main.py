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
from datetime import datetime

class Main:

    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title:str):
        if name == 'posix':
            stdout.write(f"\x1b]2;{title}\x07")
        elif name in ('ce', 'nt', 'dos'):
            system(f'title {title}')
        else:
            stdout.write(f"\x1b]2;{title}\x07")

    def ReadFile(self,filename,method):
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def ReadJson(self,filename,method):
        with open(filename,method) as f:
            return json.load(f)

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('[Data]/useragents.txt','r')
        return choice(useragents)

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('[Data]/proxies.txt','r')
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
        self.SetTitle('[One Man Builds Spotify Account Creator Tool]')
        self.clear()
        self.title = Style.BRIGHT+Fore.GREEN+"""
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

        config = self.ReadJson('[Data]/configs.json','r')

        self.method = config['method']
        self.use_proxy = config['use_proxy']
        self.proxy_type = config['proxy_type']
        self.threads = config['threads']
        self.birth_year_start = config['birth_year_start']
        self.birth_year_end = config['birth_year_end']
        self.webhook_enable = config['webhook_enable']
        self.webhook_url = config['webhook_url']

        self.createds = 0
        self.retries = 0
        self.webhook_retries = 0

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
            self.SetTitle(f'[One Man Builds Spotify Account Creator] ^| CREATED: {self.createds} ^| WEBHOOK RETRIES: {self.webhook_retries} ^| RETRIES: {self.retries} ^| THREADS: {active_count()-1}')
            sleep(0.1)

    def SendWebhook(self,title,message,icon_url,thumbnail_url,proxy,useragent):
        try:
            timestamp = str(datetime.utcnow())

            message_to_send = {"embeds": [{"title": title,"description": message,"color": 65362,"author": {"name": "AUTHOR'S DISCORD SERVER [CLICK HERE]","url": "https://discord.gg/9bHfzyCjPQ","icon_url": icon_url},"footer": {"text": "MADE BY ONEMANBUILDS","icon_url": icon_url},"thumbnail": {"url": thumbnail_url},"timestamp": timestamp}]}
            
            headers = {
                'User-Agent':useragent,
                'Pragma':'no-cache',
                'Accept':'*/*',
                'Content-Type':'application/json'
            }

            payload = json.dumps(message_to_send)

            if self.use_proxy == 1:
                response = requests.post(self.webhook_url,data=payload,headers=headers,proxies=proxy)
            else:
                response = requests.post(self.webhook_url,data=payload,headers=headers)

            if response.text == "":
                pass
            elif "You are being rate limited." in response.text:
                self.webhook_retries += 1
                self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)
            else:
                self.webhook_retries += 1
                self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)
        except:
            self.webhook_retries += 1
            self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)

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
            proxy = ''

            if self.use_proxy == 1:
                proxy = self.GetRandomProxy()
                create_response = requests.post(create_url, data=payload, headers=create_headers,proxies=proxy,timeout=5)
            else:
                create_response = requests.post(create_url, data=payload, headers=create_headers)

            json_data = json.loads(create_response.text)

            if 'status' in json_data:
                if json_data['status'] == 1:
                    username = json_data['username']
                    if username != '':
                        self.PrintText(Fore.WHITE,Fore.GREEN,'CREATED','{0}:{1} | {2} | {3} | {4}/{5}/{6}'.format(credentails['email'],credentails['password'],credentails['username'],credentails['gender'],credentails['birth_year'],credentails['birth_month'],credentails['birth_day']))
                        self.createds += 1
                        with open('[Data]/[Results]/hits.txt','a') as f:
                            f.write('{0}:{1}\n'.format(credentails['email'],credentails['password']))
                        with open('[Data]/[Results]/detailed_hits.txt','a') as f:
                            f.write('{0}:{1} | {2} | {3} | {4}/{5}/{6}\n'.format(credentails['email'],credentails['password'],credentails['username'],credentails['gender'],credentails['birth_year'],credentails['birth_month'],credentails['birth_day']))
                        if self.webhook_enable == 1:
                            self.SendWebhook('Spotify Account','**COMBO**\n{0}:{1}\n**USERNAME**\n{2}\n**GENDER**\n{3}\n**BIRTHDATE**\n{4}/{5}/{6}'.format(credentails['email'],credentails['password'],credentails['username'],credentails['gender'],credentails['birth_year'],credentails['birth_month'],credentails['birth_day']),'https://cdn.discordapp.com/attachments/776819723731206164/796935218166497352/onemanbuilds_new_logo_final.png','https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Spotify_logo_without_text.svg/768px-Spotify_logo_without_text.svg.png',proxy,self.GetRandomUserAgent())
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
    