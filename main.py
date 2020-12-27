import re
import os
import discord
import platform
import datetime
import requests, subprocess, colorama
from colorama import Fore, init
from discord.ext import commands

token = input("Enter your discord token: ")
os.system('cls')
valid = 0
invalid = 0

os.system("title Evo Sniper [Developed by Evo.black]")
class Sniper(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.token = token

    def client_headers(self):
        return {
            'Authorization': self.token,
            'Content-Type': 'application/json',
        }

    @staticmethod
    def clear_console():
        if platform.system() != 'Linux':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def replace_multiple(text):
        to_be_replaced = ['╗', '╝', '╔', '═', '╝', "║", '╚', 'V', 'o', 'D', 'P']
        for elem in to_be_replaced:
            if elem in text:
                text = text.replace(elem, f'{Fore.RED}{elem}{Fore.RESET}')
        return text

    def start_menu(self):
        banner = self.replace_multiple(f"""
███████╗██╗   ██╗ ██████╗     ███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ 
██╔════╝██║   ██║██╔═══██╗    ██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗
█████╗  ██║   ██║██║   ██║    ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝
██╔══╝  ╚██╗ ██╔╝██║   ██║    ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗
███████╗ ╚████╔╝ ╚██████╔╝    ███████║██║ ╚████║██║██║     ███████╗██║  ██║
╚══════╝  ╚═══╝   ╚═════╝     ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
        """)
        print(banner + f"\n\n\t{Fore.RED}{datetime.datetime.now().strftime('%H:%M:%S %p')}{Fore.RESET} [1] Start nitro sniper")
        print(f"\n\t{Fore.RED}Enter your option{Fore.RESET}", end='')
        try:
            choice = int(input("  :  "))

            if choice == 1:
                self.clear_console()
                self.execute()
            else:
                self.clear_console()
                self.start_menu()

        except ValueError:
            self.clear_console()
            self.start_menu()

    async def on_connect(self):
        print(f"Started at [{Fore.RED}{datetime.datetime.now().strftime('%H:%M:%S %p')}{Fore.RESET}]\n[{Fore.RED}»{Fore.RESET}] Connected User: {self.user.name} | {self.user.id}")
        print(f'[{Fore.RED}»{Fore.RESET}] Total Guilds: {str(len(client.guilds))}')
        print(f'[{Fore.RED}»{Fore.RESET}] Join our discord: {Fore.BLUE}https://discord.gg/WWRuaM7nK5{Fore.RESET}\n')


    async def claim_code(self, code: str):
        r = requests.post(f'https://discordapp.com/api/v8/entitlements/gift-codes/{code}/redeem',
                          headers=self.client_headers(),
                          json={'channel_id': None, 'payment_source_id': None})
        if 'subscription_plan' not in r.text:
            try:
                message = r.json()['message']
            except (AttributeError, IndexError, KeyError):
                message = "cloudflare"
            return {'valid': False, 'message': message}
        else:
            return {'valid': True, 'message': r.json()}
              
    async def on_message(self, message):
        try:
            code = re.search(r'(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)',
                             message.content)
            nitro_code = code.group(2)
            if code:
                if len(nitro_code) == 16 or len(nitro_code) == 24:
                    data = await self.claim_code(nitro_code)
                    data_message = data['message']
                    if 'subscription_plan' in data_message:
                        print(f"{Fore.RESET}\n[{Fore.GREEN}»{Fore.RESET}] Nitro Claimed\n[{Fore.GREEN}»{Fore.RESET}] Guild: {message.guild}\n [{Fore.GREEN}»{Fore.RESET}] Code: {nitro_code}")
                        global valid
                        valid += 1
                    else:
                        print(f"{Fore.RESET}\n[{Fore.RED}»{Fore.RESET}] {data_message}\n[{Fore.RED}»{Fore.RESET}] Guild: {message.guild}\n[{Fore.RED}»{Fore.RESET}] Code: {nitro_code}")
                        global invalid
                        invalid += 1

        except AttributeError:
            pass

    @staticmethod
    def check_if_connection_exists():
        try:
            requests.get('https://google.com/')
            return True
        except:
            return False

    def execute(self):
        """Executes the bot"""
        try:
            if self.check_if_connection_exists():
                super().run(self.token, bot=False)
            else:
                print(f"{Fore.RED}{datetime.datetime.now().strftime('%H:%M:%S %p')}{Fore.RESET} - (CONNECTION_ERR)")
                input("\n\n\nPress any key to exit...\n")
        except discord.errors.LoginFailure as e:
            print(f"{Fore.RED}{datetime.datetime.now().strftime('%H:%M:%S %p')}{Fore.RESET} - ({Fore.RED}{e}{Fore.RESET})")
            input("\n\n\nPress any key to exit...\n")

if __name__ == '__main__':
    if platform.system() != 'Linux':
        init(convert=True)
    client = Sniper()
    client.start_menu()
