CREATE_USER_TABLE = """create table if not exists
    users(id SERIAL PRIMARY KEY,
            username VARCHAR(128),
            password VARCHAR(128),
    is_active INTEGER NOT NULL DEFAULT 0)
"""

CREATE_MOVIES_TABLE = """create table if not exists
    movies(id SERIAL PRIMARY KEY,
            name VARCHAR(128),
            rating INTEGER)
"""

CREATE_PROJECTIONS_TABLE = '''create table if not exists
        projections(id SERIAL PRIMARY KEY,
                    type VARCHAR(3),
                    date date,
                    time time,
                    movie_id integer REFERENCES movies)'''

CREATE_RESERVATION_TABLE = '''create table if not exists
        reservations(id SERIAL PRIMARY KEY,
                    row integer,
                    col integer,
                    user_id integer REFERENCES users,
                    projection_id integer REFERENCES projections)
    '''

CREATE_MOVIE = '''INSERT INTO movies (name, rating)
                  VALUES (%s, %s);'''

LIST_MOVIES = '''SELECT * FROM movies'''
