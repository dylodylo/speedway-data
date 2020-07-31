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

for match in matches_links:
    page = requests.get(match)
    soup = BeautifulSoup(page.content, 'html.parser')
    scores = soup.find('p')
    scores = scores.find_all('tt')
    scores = scores[1].text
    scores = scores.split("\n")
    scores = [i.replace(u'\xa0', ' ') for i in scores]
    scores = [' '.join(i.split()) for i in scores]
    scores = [i.split() for i in scores]
    home_scores = scores[1:9]
    away_scores = scores[10:18]
    for i in home_scores[:]:
        if i[1] == "brak" or i[2] == "ns":
            home_scores.remove(i)

    for i in away_scores[:]:
        if i[1] == "brak" or i[2] == "ns":
            away_scores.remove(i)
    for rider in home_scores:
        number = rider[0]
        name = rider[1]
        full_points = rider[2]
        if "+" in full_points:
            points = full_points.split("+")
            bonuses = points[1]
            points = points[0]
        else:
            points = full_points
            bonuses = 0

        details_points = rider[3]
        heats = len(details_points.split(','))
        print(name, full_points, points, bonuses, details_points, heats)

    for rider in away_scores:
        number = rider[0]
        name = rider[1]
        full_points = rider[2]
        details_points = rider[3]
        print(name, full_points)




if __name__ == "main":
    pass