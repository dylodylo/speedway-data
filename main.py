from bs4 import BeautifulSoup
import requests
import psycopg2
from config import config


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


def get_riders_points(riders_scores):
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


def get_teams(page_content):
    teams = page_content.find('title')
    teams = teams.text.split(' - ')
    team1 = teams[0]
    team2 = teams[1]
    return team1, team2


def scrapping():
    matches_links, matches = get_matches_from_season("http://www.speedwayw.pl/pl_2019.htm")

    for match in matches_links:
        page = requests.get(match)
        soup = BeautifulSoup(page.content, 'html.parser')
        home_scores, away_scores = get_all_scores(soup)
        home_team, away_team = get_teams(soup)
        print(home_team, away_team)
        get_riders_points(home_scores)
        get_riders_points(away_scores)


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == "__main__":
    connect()
    scrapping()
    pass
