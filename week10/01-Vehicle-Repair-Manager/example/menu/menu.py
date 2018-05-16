from controllers.controller import Controller


class Menu:
    controller = Controller()
    def start(self):
        user_name = input('Hello!\nProvide your user_name:\n>>> ')
        # user = get_user_by_user_name(user_name)
        user = None
        if user:
            pass
        else:
            print('Unknown user!\n Would you like to create new user?')
            create_new = input('>>> ')
            if create_new.lower() in ['y', 'yes']:
                user_type = input('Are you a Client or Mechanic?\n>>> ')
                if len(user_type) == 0:
                    print('Invalid user type!')
                    sys.exit()
                new_user_name = input('Provide user_name:\n>>> ')
                if len(new_user_name) == 0:
                    print('Invalid user name!')
                    sys.exit()
                new_phone_number = input("Provide phone_number:\n>>>")
                if len(new_phone_number) == 0:
                    print('Invalid phone number!')
                    sys.exit()
                new_email = input("Provide email:\n>>>")
                if len(new_email) == 0:
                    print('Invalid email!')
                    sys.exit()
                new_address = input("Provide address:\n>>>")
                if len(new_address) == 0:
                    print('Invalid address!')
                    sys.exit()

                def on_click():


                    self.controller.create_user(
                        new_user_name,
                        new_phone_number,
                        new_email,
                        new_address,
                        user_type
                    )
            else:
                sys.exit()
