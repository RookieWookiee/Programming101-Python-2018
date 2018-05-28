from menu.menu import Menu
from database_layer.database import DBConnector


def main():
    # db = DBConnector()
    # db.create()

    Menu().start()


if __name__ == '__main__':
    main()
