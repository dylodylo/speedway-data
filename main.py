from bs4 import BeautifulSoup
import requests

def get_matches_from_season():
    page = requests.get("http://www.speedwayw.pl/pl_2019.htm")
    soup = BeautifulSoup(page.content, 'html.parser')
    rounds = soup.find('p', align="left")
    matches_links = rounds.find_all('a')
    matches = [i.text for i in matches_links]
    print(matches)
    matches_links = ["http://www.speedwayw.pl/" + i['href'] for i in matches_links]
    print(matches_links)
    return matches_links, matches

matches_links, matches = get_matches_from_season()
page = requests.get(matches_links[0])
soup = BeautifulSoup(page.content, 'html.parser')
scores = soup.find('p')
scores = scores.find_all('tt')
scores = scores[1].text
scores = scores.split("\n")
scores = [i.replace(u'\xa0', ' ') for i in scores]
scores = [' '.join(i.split()) for i in scores]
scores = [i.split() for i in scores]
home_scores = [scores[1:9]]
away_scores = [scores[10:18]]
print(home_scores)
print(away_scores)


if __name__ == "main":
    pass