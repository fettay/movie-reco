import os 
import random


dir_path = os.path.dirname(os.path.realpath(__file__))
proxies_path = os.path.join(dir_path, "proxies-list.txt")
with open(proxies_path) as f:
    proxies = f.read().splitlines()

def get_random_proxy():
    proxy = proxies[random.randint(0, len(proxies) - 1)]
    return {
    "http": proxy, 
    "https": proxy
    }
    

if __name__ == "__main__":
    print(get_random_proxy())
