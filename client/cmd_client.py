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
            print("user_id is: ", self.user_id)
            return True
        else:
            return False
    
    def signup(self):
        response = requests.post(f"{URL}/signup", json=self.signup_json_schema())
        if response.status_code == 201:
            return True
        else:
            return False

    def get_user(self, user_id):
        response = requests.get(f"{URL}/user/{user_id}", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()
    
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

    def get_games(self, user_id=None):
        response = requests.get(f"{URL}/user/{self.user_id if user_id is None else user_id}/games", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()
    
    def get_friends(self):
        response = requests.get(f"{URL}/user/{self.user_id}/friends", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()

    def get_my_games(self):
        response = requests.get(f"{URL}/user/{self.user_id}/games", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()

    def get_my_friends(self):
        response = requests.get(f"{URL}/user/{self.user_id}/friends", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()

    def remove_a_friend(self, friend_id):
        response = requests.delete(f"{URL}/user/{self.user_id}/friends", 
                        headers={"Authorization": f"Bearer {self.access_token}"},
                        json={"user2_id": friend_id})
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
        response = requests.post(f"{URL}/user/{self.user_id}/games", 
                headers={"Authorization": f"Bearer {self.access_token}"},
                json={"game_id": game_id})
        return response.json()

    def get_game_genres(self, game_id):
        response = requests.get(f"{URL}/genres/{game_id}", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()
    
    def get_pending_requests(self):
        response = requests.get(f"{URL}/friends/{self.user_id}/pending", 
                        headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()
    
    def get_sent_requests(self):
        response = requests.get(f"{URL}/friends/{self.user_id}/sent", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()
    
    def add_friend(self, user_id):
        response = requests.post(f"{URL}/friends/{self.user_id}", headers={"Authorization": f"Bearer {self.access_token}"}, json={"user2_id": user_id})
        return response.json()
    
    def accept_friend(self):
        request_list = self.get_pending_requests()
        for request in request_list["payload"]:
            request.pop("@controls")
            print_json(request)

        friend_request_id = input("Choose a friend request id: ")
        response = requests.post(f"{URL}/friends/{self.user_id}/accept/{friend_request_id}", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()

    def cancel_friend_request(self):
        request_list = self.get_sent_requests()
        for request in request_list["payload"]:
            # request.pop("@controls")
            print_json(request)
        friend_request_id = input("Choose a friend request id: ")
        if friend_request_id in ["cancel", "c", ""]:
            return {"canceled": True}
        response = requests.delete(f"{URL}/friends/{self.user_id}/cancel/{friend_request_id}", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()

    def reject_friend_request(self, friend_request_id):
        response = requests.delete(f"{URL}/friends/{self.user_id}/reject/{friend_request_id}", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()

    def get_invitations(self):
        response = requests.get(f"{URL}/invitation/{self.user_id}", headers={"Authorization": f"Bearer {self.access_token}"})
        return response.json()

    def create_invitation(self, user_id, game_id, suggested_time):
        game_id = int(game_id)
        user_id = int(user_id)
        response = requests.post(f"{URL}/invitation/{self.user_id}",
                            headers={"Authorization": f"Bearer {self.access_token}"},
                            json={"receiver_id": user_id, "game_id": game_id, "suggestedTime": suggested_time})
        return response.json()

    def delete_invitation(self):
        invitation_list = self.get_invitations()
        for invitation in invitation_list["payload"]:
            print_json(invitation)
        invitation_id = input("Choose an invitation id: ")
        if invitation_id in ["cancel", "c", ""]:
            return {"canceled": True}
        invitation_id = int(invitation_id)
        response = requests.delete(f"{URL}/invitation/{self.user_id}",
         headers={"Authorization": f"Bearer {self.access_token}"}, json={"invite_id": invitation_id})
        return response.json()

    def update_invitation(self):
        invitation_list = self.get_invitations()
        for invitation in invitation_list["payload"]:
            print_json(invitation)
        invitation_id = input("Choose an invitation id: ")
        if invitation_id in ["cancel", "c", ""]:
            return {"canceled": True}
        invitation_id = int(invitation_id)
        accepted = input("Accepted? (y/n): ")
        accepted = True if accepted in ["y", "yes", "true"] else False
        response = requests.put(f"{URL}/invitation/{self.user_id}",
                        headers={"Authorization": f"Bearer {self.access_token}"},
                        json={"invite_id": invitation_id, "accepted": accepted})
        return response.json()

    


def print_json(json_data):
    print(json.dumps(json_data, indent=4, sort_keys=True))

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
        2 - games
        3 - friends request
        4 - invitations
        5 - users
        
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
            exit(0)
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
        elif inp == "exit":
            exit(1)
        elif inp == "0":
            print("Clearing...")
            #user = None
        elif inp == "1":
            print("Profile...")
            print("""
                0 - back
                1 - get a profile
                2 - add profile (bio, status)
                3 - update profile (bio, status)
                4 - get my games
                5 - get my friends
                6 - remove a friend
                """)
            while 1:

                inp1 = input("Enter command: ")
                if inp1 == "help":
                    print("""
                        0 - back
                        1 - get a profile
                        2 - add profile (bio, status)
                        3 - update profile (bio, status)
                        4 - get my games
                        5 - get my friends
                        6 - remove a friend
                        """)
                if inp1 == "0":
                    break
                elif inp1 == "1":
                    print_json(user.get_profile())
                elif inp1 == "2":
                    print_json(user.add_profile(input("Enter bio: "), input("Enter status: ")))
                elif inp1 == "3":
                    print_json(user.update_profile(input("Enter bio: "), input("Enter status: ")))
                elif inp1 == "4":
                    print_json(user.get_my_games())
                elif inp1 == "5":
                    print_json(user.get_my_friends())
                elif inp1 == "6":
                    print_json(user.remove_a_friend(input("Enter friend id: ")))

        elif inp == "2":
            print("Games...")
            print("""
                0 - back
                1 - get all games
                2 - get game by id
                3 - get game by name
                4 - add a game to your list
                5 - show genres of a game
                """)
            while 1:
                inp1 = input("Enter command: ")
                if inp1 == "help":
                    print("""
                        0 - back
                        1 - get all games
                        2 - get game by id
                        3 - get game by name
                        4 - add a game to your list
                        5 - show genres of a game
                        """)
                if inp1 == "0":
                    break
                elif inp1 == "1":
                    print_json(user.get_all_games())
                elif inp1 == "2":
                    print_json(user.get_game_by_id(input("Enter game id: ")))
                elif inp1 == "3":
                    print_json(user.get_game_by_name(input("Enter game name: ")))
                elif inp1 == "4":
                    print_json(user.add_game(input("Enter game id: ")))
                elif inp1 == "5":
                    print_json(user.get_game_genres(input("Enter game id: ")))
        
        elif inp == "3":
            print("Friends request...")
            print("""
                0 - back
                1 - get pending requests
                2 - get sent requests
                3 - add friend
                4 - accept friend
                5 - cancel friend request
                6 - reject friend request
                """)
            while 1:
                inp1 = input("Enter command: ")
                if inp1 == "help":
                    print("""
                        0 - back
                        1 - get pending requests
                        2 - get sent requests
                        3 - add friend
                        4 - accept friend
                        5 - cancel friend request
                        6 - reject friend request
                        """)
                if inp1 == "0":
                    break
                elif inp1 == "1":
                    print_json(user.get_pending_requests())
                elif inp1 == "2":
                    print_json(user.get_sent_requests())
                elif inp1 == "3":
                    print_json(user.add_friend(input("Enter user id: ")))
                elif inp1 == "4":
                    print_json(user.accept_friend())
                elif inp1 == "5":
                    print_json(user.cancel_friend_request())
                elif inp1 == "6":
                    print_json(user.reject_friend_request(input("Enter friend request id: ")))
        elif inp == "4":
            print("Invitations...")
            print("""
                0 - back
                1 - get invitations
                2 - send invitation
                3 - delete invitation
                4 - update invitation status
                """)
            while 1:
                inp1 = input("Enter command: ")
                if inp1 == "help":
                    print("""
                        0 - back
                        1 - get invitations
                        2 - send invitation
                        3 - delete invitation
                        4 - update invitation status
                        """)
                if inp1 == "0":
                    break
                elif inp1 == "1":
                    print_json(user.get_invitations())
                elif inp1 == "2":
                    print_json(user.create_invitation(input("Enter user id: "), input("Enter game id: "), input("Enter suggested time: ")))
                elif inp1 == "3":
                    print_json(user.delete_invitation())
                elif inp1 == "4":
                    print_json(user.update_invitation())
        elif inp == "5":
            print("Users...")
            print("""
                0 - back
                1 - get a user
                2 - get user's profile
                3 - get user's games
                """)
            while 1:
                inp1 = input("Enter command: ")
                if inp1 == "help":
                    print("""
                        0 - back
                        1 - get a user
                        2 - get user's profile
                        3 - get user's games
                        """)
                if inp1 == "0":
                    break
                elif inp1 == "1":
                    print_json(user.get_user(input("Enter user id: ")))
                elif inp1 == "2":
                    print_json(user.get_profile(input("Enter user id: ")))
                elif inp1 == "3":
                    print_json(user.get_games(input("Enter user id: ")))

