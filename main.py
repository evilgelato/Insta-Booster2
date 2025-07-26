import os
import tempfile
import webbrowser
from colorama import Fore, Style, init
from datetime import timedelta
import json
import re
import time
import requests
import sys

CONFIG_FILE = "config.json"

VIDEO_URL = "https://instagram.com/reel/xxxx"
AMOUNT_OF_BOOSTS = 100
TYPE = "views"


quantity_types = {
    'views' : 500,
    'likes' : 20
}
delay_types = {
    'views' : 5,
    'likes':3
}
service_id = {
    'views':237,
    'likes':234
}
init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_version():
    CURR = open("version.md","r").read()
    GITHUB_VER = requests.get("https://raw.githubusercontent.com/Sneezedip/Insta-Booster/refs/heads/main/version.md").text
    if CURR != GITHUB_VER.strip():
        print(f"{Fore.RED}VERSION MISMATCH! UPDATE FROM https://github.com/Sneezedip/Insta-Booster")
        sys.exit()

def show_credits():
    print(f"{Fore.BLUE}Developed by Sneezedip.")
    print(f"{Fore.BLUE}https://discord.gg/nAa5PyxubF{Style.RESET_ALL}")
    time.sleep(1)

def is_first_run():
    file_path = os.path.join(tempfile.gettempdir(), 'insta-booster.txt')
    if not os.path.isfile(file_path):
        with open(file_path, "w") as file:
            file.write("First run check for Insta-Booster.")
        webbrowser.open("https://discord.gg/nAa5PyxubF")
        return True
    return False

def load_config():
    global VIDEO_URL, AMOUNT_OF_BOOSTS
    if os.path.isfile(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                VIDEO_URL = data.get('video_url', VIDEO_URL)
                AMOUNT_OF_BOOSTS = data.get('amount_of_boosts', AMOUNT_OF_BOOSTS)
                TYPE = AMOUNT_OF_BOOSTS = data.get('type', TYPE)
        except Exception as e:
            print(f"{Fore.RED}Error loading config: {e}{Style.RESET_ALL}")
    else:
        save_config() 

def save_config():
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({
                'video_url': VIDEO_URL,
                'amount_of_boosts': AMOUNT_OF_BOOSTS,
                'type' : TYPE
            }, f, indent=4)
    except Exception as e:
        print(f"{Fore.RED}Error saving config: {e}{Style.RESET_ALL}")

def convert_hours(hours = 'ind',sec = 'ind'):
    """
    Convert hours or seconds into HH:MM:SS format
    
    Parameters
    ----------
    - hours : int (or 'ind' if nothing is passed)
        - Amount of hours to transform in hhmmss
    - seconds : int (or 'ind' if nothing is passed)
        - Amount of seconds to transform in hhmmss 
    
    Returns
    -------
    - str
        - the hhmmss based on the parameter passed.
    """

    if hours == 'ind':
        td = timedelta(seconds=sec)
    else:
        td = timedelta(seconds=int(hours * 3600))

    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    hhmmss = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    return hhmmss

def color_boost_amount(amount):
    if amount < 7:
        return Fore.GREEN
    elif amount < 15:
        return Fore.YELLOW
    elif amount < 50:
        return Fore.LIGHTYELLOW_EX
    elif amount < 100:
        return Fore.RED
    else:
        return Fore.LIGHTRED_EX
def wait_time(seconds):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timeformat = f"{Fore.YELLOW}Waiting: {mins:02d}:{secs:02d} remaining...{Style.RESET_ALL}"
        print(timeformat, end='\r')
        time.sleep(1)
    print(' ' * 50, end='\r')
def is_valid_reel_url(url):
    """Check if the URL is a valid Instagram Reel link."""
    pattern = r"^https?://(www\.)?instagram\.com/reel/[\w\-]+/?$"
    return re.match(pattern, url) is not None

def main():
    global VIDEO_URL, AMOUNT_OF_BOOSTS,TYPE
    clear()
    show_credits()
    is_first_run()
    load_config()
    while True:
        os.system("cls")
        print(f"{Fore.CYAN}Type Selected: {TYPE.upper()}")
        print(f"{Fore.CYAN}{'-'*35}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}VIDEO FOR BOOST [{Fore.YELLOW}{VIDEO_URL}{Fore.MAGENTA}]")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{TYPE.upper()} TO BE ADDED [{Fore.YELLOW}{AMOUNT_OF_BOOSTS*quantity_types[TYPE]} {TYPE.upper()} ({AMOUNT_OF_BOOSTS} Boosts){Fore.MAGENTA}] {color_boost_amount(AMOUNT_OF_BOOSTS)}(Time Est. {convert_hours(round((AMOUNT_OF_BOOSTS*delay_types[TYPE])/60, 2))} Hours)")
        print(f"{Fore.CYAN}{'-'*35}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[1] {Style.BRIGHT}START BOOST")
        print(f"{Fore.BLUE}[2] Change Video URL")
        print(f"{Fore.BLUE}[3] Change Boost Amount")
        print(f"{Fore.BLACK}-"*30)
        print(f"{Fore.BLUE}[4] {Style.BRIGHT}{Fore.YELLOW}[NEW] Change TYPE (Likes / Views)")
        print(f"{Fore.BLACK}-"*30)
        print(f"{Fore.RED}[5] Exit{Style.RESET_ALL}")

        choice = input(f"\n{Fore.WHITE}-> {Style.RESET_ALL}")

        if choice == "1":
            used = 0
            from zefame import Zefame
            zefame = Zefame(VIDEO_URL,service_id[TYPE])
            while used < AMOUNT_OF_BOOSTS:
                response = zefame.send_boost()
                if type(response) == bool:
                    if response == True:
                        print(f"{Fore.GREEN}Boost {used+1} sent!{Style.RESET_ALL}")
                        used += 1
                    else:
                        wait_time(300)
                elif type(response) == int:
                    wait_time(response)
        elif choice == "2":
            new_url = input("Enter the new video URL: ")
            if is_valid_reel_url(new_url):
                VIDEO_URL = new_url
                save_config()
            else:
                print(f"{Fore.RED}Invalid URL! Please enter a valid Instagram Reel link.{Style.RESET_ALL}")
        elif choice == "3":
            try:
                AMOUNT_OF_BOOSTS = int(input("Enter the new boost amount: "))
                save_config()
            except ValueError:
                print(f"{Fore.RED}Invalid number!{Style.RESET_ALL}")
        elif choice == "4":
            if TYPE == 'views':
                TYPE = 'likes'
            else:
                TYPE = 'views'
            save_config()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")

if __name__ == "__main__":
    check_version()
    show_credits()
    is_first_run()
    main()