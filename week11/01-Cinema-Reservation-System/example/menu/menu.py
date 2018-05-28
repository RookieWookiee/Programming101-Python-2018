from controllers.controller import Controller


class Menu:
    controller = Controller()

    def start(self):
        name = input('Hello!\nMovie name:\n>>> ')
        rating = input('\nMovie rating:\n>>> ')

        self.controller.create_movie(name, rating)
        self.controller.show_movies()
