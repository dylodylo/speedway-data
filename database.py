import psycopg2
from config import config


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


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS matches (
            id SERIAL PRIMARY KEY,
            team1 VARCHAR(255) NOT NULL,
            team2 VARCHAR(255) NOT NULL,
            league VARCHAR(255) NOT NULL,
            season VARCHAR(255) NOT NULL,
            date DATE NOT NULL
        )
        """,
        """ CREATE TABLE IF NOT EXISTS scores (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                points INTEGER NOT NULL,
                bonuses INTEGER NOT NULL,
                details VARCHAR(255) NOT NULL,
                number INTEGER NOT NULL,
                track VARCHAR(255) NOT NULL,
                match_id INT NOT NULL,
                FOREIGN KEY (match_id)
                REFERENCES matches(id)
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
            conn.commit()
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_match(values):
    command = """INSERT INTO matches(team1, team2, league, season, date) VALUES(%s, %s, %s, %s, %s);"""
    conn = None
    if not check_if_match_exist(values[0], values[1], values[4]):
        try:
            # read the connection parameters
            params = config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # create table one by one
            cur.execute(command, (values[0], values[1], values[2], str(values[3]), values[4]))
            conn.commit()
            # close communication with the PostgreSQL database server
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    else:
        print("Match already exists")


def check_if_match_exist(team1, team2, date):
    command = """SELECT * FROM matches WHERE team1=%s AND team2=%s AND date=%s;"""
    conn = None
    match = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command, (team1, team2, date))
        match = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    if match:
        return True
    else:
        return False


def get_match_id(values):
    command = """SELECT id FROM matches WHERE team1=%s AND date=%s"""
    conn = None
    match_id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command, (values[0], values[1]))
        match_id = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    if match_id:
        return match_id[0][0]



def insert_score(values):
    command = """INSERT INTO scores(name,points,bonuses,details,number,track,match_id) VALUES(%s, %s, %s, %s, %s,%s, %s);"""
    conn = None
    if not check_if_score_exists(values[0], values[6]):
        try:
            # read the connection parameters
            params = config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # create table one by one
            cur.execute(command, (values[0], values[1], values[2], values[3], values[4], values[5], values[6]))
            conn.commit()
            # close communication with the PostgreSQL database server
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    else:
        print("Score already exists")


def check_if_score_exists(rider_name, match_id):
    command = """SELECT * FROM scores WHERE name=%s AND match_id=%s;"""
    conn = None
    score = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command, (rider_name, match_id))
        score = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    if score:
        return True
    else:
        return False
