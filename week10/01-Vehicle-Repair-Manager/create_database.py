


import sqlite3

DB_NAME = "vehicle_management.db"

db = sqlite3.connect(DB_NAME)
db.row_factory = sqlite3.Row
c = db.cursor()

drop_db = """DROP TABLE IF EXISTS BASE_USER"""
c.execute(drop_db)
db.commit()

create_base_user_table = """
CREATE TABLE IF NOT EXISTS BASE_USER (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  USER_NAME TEXT NOT NULL,
  EMAIL TEXT NOT NULL,
  PHONE_NUMBER INTEGER NOT NULL,
  ADDRESS TEXT NOT NULL
)
"""
c.execute(create_base_user_table)
db.commit()

user_name = 'Roza'
email = 'roza@roza.com'
phone_number = 12344544
address = 'Sofia, Hack Bulgaria'

insert_base_user = """
INSERT INTO BASE_USER (user_name, email, phone_number, address)
VALUES(?, ?, ?, ?)
"""


c.execute(insert_base_user, (user_name, email, phone_number, address))
db.commit()


insert_base_user_2 = """
INSERT INTO BASE_USER (user_name, email, phone_number, address)
VALUES(:user_name, :email, :phone_number, :address)
"""


c.execute(insert_base_user_2, {'user_name': 'Robi',
                               'email': 'robi@the.dog',
                               'phone_number':7654,
                               'address': 'Pri pandite'})
db.commit()


users = [("Kiki", "kiki@kiki.com", 90, 'Sofia, Hack Bulgaria'),
            ("Bace", "bace@bace.com", 80, 'Sofia, Hack Bulgaria'),
            ("Panda", "bace@bace.com", 59, 'Sofia, Hack Bulgaria')]

c.executemany(insert_base_user, users)
db.commit()



list_users = """SELECT * FROM BASE_USER """
result = c.execute(list_users)
for row in result:
    print(row[0])
    print(row['user_name'])
# # c.execute(list_patients)
# # print(c.fetchall())
# # print(c.fetchone())
# # print(c.fetchone())
# db.commit()
