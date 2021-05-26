import requests
from bs4 import BeautifulSoup


def get_synonyms(word):
    page = requests.get("https://www.thesaurus.com/browse/" + word)
    soup = BeautifulSoup(page.content, 'html.parser')
    meanings = soup.find(id='meanings')
    if meanings:
        return [x.text.strip() for x in meanings.find_all(class_="css-1kg1yv8 eh475bn0")]
    else:
        other_mean = soup.find(id='root').find(class_="css-xgojxx e1wla5065").text.split(":")[1].strip()
        return get_synonyms(other_mean)
    

if __name__ == "__main__":
    pass