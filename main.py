import os
import random
import string
import requests
import threading
from colorama import Fore
from tqdm import tqdm
import concurrent.futures


class Stats():
    def __init__(self):
        self.alive = 0
        self.taken = 0
        self.checked = 0

def generate_username(length, use_numbers):
    letters = string.ascii_lowercase
    if use_numbers:
        letters += string.digits
    return "".join(random.SystemRandom().choice(letters) for _ in range(length))

def check_username(username, stats):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-GB',
        'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        'Connection': 'keep-alive',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'https://www.twitch.tv',
        'Referer': 'https://www.twitch.tv/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = '[{"operationName":"UsernameValidator_User","variables":{"username":"' + username + '"},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"fd1085cf8350e309b725cf8ca91cd90cac03909a3edeeedbd0872ac912f3d660"}}}]'

    r = requests.post('https://gql.twitch.tv/gql', headers=headers, data=data).json()[0]["data"]["isUsernameAvailable"]
    
    stats.checked += 1
    if r == True:
        stats.alive += 1
        stats.checked += 1
        print(f"{Fore.GREEN}+{Fore.RESET} [{username}]")
        with open('usernames.txt', 'a') as file:
            file.write(f"{username}\n")
    else:
        stats.taken += 1
        stats.checked += 1
        print(f"{Fore.RED}-{Fore.RESET} [{username}]")

def username_generator(threads, use_numbers, length):
    stats = Stats()
    usernames = [generate_username(length, use_numbers) for _ in range(threads)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_username = {executor.submit(check_username, username, stats): username for username in usernames}
        for future in concurrent.futures.as_completed(future_to_username):
            username = future_to_username[future]
            try:
                future.result()
            except Exception as exc:
                print(f"Error checking username {username}: {exc}")

if __name__ == "__main__":
    threads = int(input("Threads > "))
    use_numbers = input("Do you want numbers in usernames? (y/n) ").lower() == 'y'
    length_option = input("Do you want to specify the username length? (y/n) ").lower() == 'y'
    if length_option:
        length = int(input("Enter the desired username length (4-25): "))
        length = max(4, min(25, length))
    else:
        random_lengths = [6, 7, 8, 9, 10]
        length = random.choice(random_lengths)
    username_generator(threads, use_numbers, length)