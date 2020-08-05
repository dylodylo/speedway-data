from bs4 import BeautifulSoup
import requests
import psycopg2
from config import config
import database


def get_matches_from_season(site):
    page = requests.get(site)
    soup = BeautifulSoup(page.content, 'html.parser')
    rounds = soup.find('p', align="left")
    matches_links = rounds.find_all('a')
    matches = [i.text for i in matches_links]
    print(matches)
    matches_links = ["http://www.speedwayw.pl/" + i['href'] for i in matches_links]
    print(matches_links)
    return matches_links, matches


def get_riders_points(riders_scores, track, match_id):
    for i in riders_scores[:]:
        if i[1] == "brak" or i[2] == "ns":
            riders_scores.remove(i)

    for rider in riders_scores:
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
    team2_scores = scores[10:18]
    return team1_scores, team2_scores


def get_teams(page_content, date, season):
    teams = page_content.find('title')
    teams = teams.text.split(' - ')
    team1 = teams[0]
    team2 = teams[1]
    database.insert_match((team1, team2, 'Ekstraliga', season, date))
    id = database.get_match_id((team1, date))
    return team1, id


def get_date(page_content):
    date = page_content.find('strong')
    date = date.text.split(':')
    date = date[1].split('-')
    date = [i.replace(u'\xa0', '') for i in date]
    date = date[2]+'-'+date[1]+'-'+date[0]
    return date


def scrapping():
    matches_links, matches = get_matches_from_season("http://www.speedwayw.pl/pl_2019.htm")

    for match in matches_links:
        page = requests.get(match)
        soup = BeautifulSoup(page.content, 'html.parser')
        home_scores, away_scores = get_all_scores(soup)
        date = get_date(soup)
        home_team, match_id = get_teams(soup, date, season='2019')
        get_riders_points(home_scores, home_team, match_id)
        get_riders_points(away_scores, home_team, match_id)


if __name__ == "__main__":
    # database.create_tables()
    database.insert_match(('Bydgoszcz', 'Toruń', '1liga', '2020', '2021-08-20'))
    print(database.get_match_id(('Bydgoszcz', '2021-08-20')))
    database.insert_score(('Woźniak', '3', '1', '(1,2,0,0)', '2', 'Bydgoszcz', '5'))
    scrapping()
    pass
