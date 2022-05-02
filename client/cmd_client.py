import requests
import json

URL = "http://127.0.0.1:5000"

class User:
    id: int = None
    username: str = None
    password: str = None
    email: str = None
    access_token: str = None

    def __init__(self, username, password, email = None, access_token=None, user_id=None):
        self.username = username
        self.password = password
        self.email = email
        self.access_token = access_token
        self.user_id = user_id

    def login_json_schema(self):
        return {
            "username": self.username,
            "password": self.password
            }
    
    def signup_json_schema(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email
        }
    
    def login(self):
        response = requests.post(f"{URL}/login", json=self.login_json_schema())
        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
            self.user_id = response.json()["payload"]["id"]
            return True
        else:
            return False
    
    def signup(self):
        response = requests.post(f"{URL}/signup", json=self.signup_json_schema())
        if response.status_code == 201:
            return True
        else:
            return False
    
    def get_profile(self, user_id=None):
        if user_id:
            response = requests.get(f"{URL}/user/{user_id}/profile", headers={"Authorization": f"Bearer {self.access_token}"})
        else:
            response = requests.get(f"{URL}/user/{self.user_id}/profile", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()

    def add_profile(self, bio, status):
        response = requests.post(f"{URL}/user/{self.user_id}/profile",
         headers={"Authorization": f"Bearer {self.access_token}"},
          json={"bio": bio, "status": status})
        return response.json()
    
    def update_profile(self, bio, status):
        response = requests.put(f"{URL}/user/{self.user_id}/profile",
            headers={"Authorization": f"Bearer {self.access_token}"},
            json={"bio": bio, "status": status})
        return response.json()
    
    def get_all_games(self):
        response = requests.get(f"{URL}/games", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()

    def get_game_by_id(self, game_id):
        response = requests.get(f"{URL}/games/{game_id}", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()
    
    def get_game_by_name(self, game_name):
        response = requests.get(f"{URL}/games/{game_name}", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()
    
    def add_game(self, game_id):
        response = requests.post(f"{URL}/user/{self.id}/games/{game_id}", 
                headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()


def print_start():
    print("""
    ********************************************************************************
    ***************************** WELCOME TO **************************************
    ***************************** THE **********************************************
    ***************************** GAME *********************************************
    ***************************** CLIENT *******************************************
    ***************************** **************************************************
    ********************************************************************************
    1 - for login
    2 - for signup
    """)


def print_help():
    print("""
        0 - clear
        1 - profile
            1 - get a profile
            2 - add profile (bio, status)
            3 - update profile (bio, status)
        2 - games
            1 - get all games
            2 - get game by id
            3 - get game by name
            4 - add a game to your list

    """)


if __name__ == "__main__":
    print_start()
    inp = input("Enter your choice: ")
    if inp == "1":
        user = User(input("Enter username: "), input("Enter password: "))
        if user.login():
            print("Login successful")
        else:
            print("Login failed")
    elif inp == "2":
        user = User(input("Enter username: "), input("Enter password: "), input("Enter email: "))
        if user.signup():
            print("Signup successful")
            user.login()
        else:
            print("Signup failed")
            exit(0)
    print_help()
    while 1:
        inp = input("Enter command: # type help for list of commands\n")
        if inp == "help":
            print_help()
        elif inp == "0":
            print("Clearing...")
            user = None
        elif inp == "1":
            print("Profile...")
            print("""
            1 - get a profile
            2 - add profile (bio, status)
            3 - update profile (bio, status)
            4 - get my games
            5 - get my friends
            """)
            inp1 = input("Enter command: ")
            if inp1 == "1":
                print(user.get_profile())
            elif inp1 == "2":
                print(user.add_profile(input("Enter bio: "), input("Enter status: ")))
            elif inp1 == "3":
                print(user.update_profile(input("Enter bio: "), input("Enter status: ")))
        elif inp == "2":
            print("Games...")
            print("""
            1 - get all games
            2 - get game by id
            3 - get game by name
            4 - add a game to your list
            """)
            inp1 = input("Enter command: ")
            if inp1 == "1":
                print(user.get_all_games())
            elif inp1 == "2":
                print(user.get_game_by_id(input("Enter game id: ")))
            elif inp1 == "3":
                print(user.get_game_by_name(input("Enter game name: ")))
            elif inp1 == "4":
                print(user.add_game(input("Enter game id: ")))
        