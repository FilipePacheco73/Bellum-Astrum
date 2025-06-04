'''
Code to create the Database
'''

from create_database import engine, Base
from database.add_initial_data import add_ships, add_users

def create_db():
    Base.metadata.create_all(bind=engine)
    print("Database created")

def start_ships():
    ships_to_add = [
        {
            'ship_name': 'USS Enterprise',
            'attack': 20,
            'shield': 5,
            'evasion': 0,
            'fire_rate': 1,
            'hp': 120,
            'value': 1000
        },
        {
            'ship_name': 'Millennium Falcon',
            'attack': 25,
            'shield': 10,
            'evasion': .05,
            'fire_rate': 1,
            'hp': 100,
            'value': 2000
        }
    ]

    add_ships(ships_to_add)

def start_users():
    users_to_add = [
        {
            'nickname': 'Luke',
            'rank_elo': 1000,
            'currency_value': 1500,
        },
        {
            'nickname': 'Anakyn',
            'rank_elo': 1000,
            'currency_value': 1500
        }
    ]

    add_users(users_to_add)

if __name__ == "__main__":

    create_db()

    start_ships()

    start_users()