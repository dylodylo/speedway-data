from bs4 import BeautifulSoup
import requests
import database
import time


def get_matches_from_season(site):
    page = requests.get(site)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_links = soup.find_all('a')
    matches_links = []
    for i in all_links:
        if i.text[:2].isnumeric() and len(i.text) == 5:
            matches_links.append(i)
    matches_links = ["http://www.speedwayw.pl/" + i['href'] for i in matches_links]
    print(matches_links)
    return matches_links


def get_riders_points(riders_scores, track, match_id):
    for i in riders_scores[:]:
        if not i[0].isnumeric():
            riders_scores.remove(i)
        elif i[1] == "brak" or i[2] == "ns" or i[2] == "zastępstwo" or i[3] == "zastępstwo" or i[2] == "u/ns":
            riders_scores.remove(i)

    for rider in riders_scores:
        number = rider[0]
        if not rider[2][0].isnumeric():
            rider[1] = rider[1]+' '+rider[2]
            rider[2] = rider[3]
            rider[3] = rider[4]
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
        database.insert_score((name, points, bonuses, details_points, number, track, match_id))
        print(name, full_points, points, bonuses, details_points, heats)


def get_all_scores(page_content):
    scores = page_content.find('p')
    scores = scores.find_all('tt')
    scores = scores[1].text
    scores = scores.split("\n")
    scores = [i.replace(u'\xa0', ' ') for i in scores]
    scores = [' '.join(i.split()) for i in scores]
    scores = [i.split() for i in scores]
    team1_scores = scores[1:9]
    team2_scores = scores[9:18]
    return team1_scores, team2_scores


def get_teams(page_content, date, season, league):
    teams = page_content.find('title')
    teams = teams.text.split(' - ')
    team1 = teams[0]
    team2 = teams[1]
    database.insert_match((team1, team2, league, season, date))
    match_id = database.get_match_id((team1, date))
    return team1, match_id


def get_date(page_content):
    date = page_content.find('strong')
    date = date.text.split(':')
    a = ['DMP', 'DM1L', 'DM2L']
    match = next((x for x in a if x in date[0]), False)
    leagues = {
        'DMP': 'Ekstraliga',
        'DM1L': '1 liga',
        'DM2L': '2 liga'
    }
    league = leagues[match]
    date = date[1].split(' ')
    date = date[-1].split('-')
    date = [i.replace(u'\xa0', '') for i in date]
    date = date[2]+'-'+date[1]+'-'+date[0]
    return date, league


def scrapping():
    for i in range(2016, 2020):
        matches_links = get_matches_from_season("http://www.speedwayw.pl/pl_"+str(i)+".htm")

        for match in matches_links:
            try:
                page = requests.get(match)
            except requests.exceptions.ConnectionError:
                print("Connection error. Waiting for reconnect.")
                time.sleep(10)
                page = requests.get(match)
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                home_scores, away_scores = get_all_scores(soup)
                date, league = get_date(soup)
                home_team, match_id = get_teams(soup, date, i, league)
            except:
                print("Some error with website")
                print(match)
            try:
                get_riders_points(home_scores, home_team, match_id)
            except IndexError as error:
                print("INDEX ERROR")
                print(error)
                print(home_team, date)
            try:
                get_riders_points(away_scores, home_team, match_id)
            except IndexError as error:
                print("INDEX ERROR")
                print(error)
                print(home_team, date)


if __name__ == "__main__":
    database.delete_tables()
    database.create_tables()
    scrapping()
    pass
