# lightHeadApp.py
# PullA Vibes

class LightHeadApp:
    def __init__(self):
        self.rooms = {
            1: {"occupied": False, "lights": {"main": False, "bathroom": False}},
            2: {"occupied": True},
            3: {"occupied": False},
            4: {"occupied": True},
            5: {"occupied": True},
        }
        self.current_user = None
        self.running = True

    def run(self):
        while self.running:
            self.login_menu()

    # --- LOGIN ---
    def login_menu(self):
        print("\nWelcome to our Hotel! Please log in.")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username == "visitor" and password == "visitor123":
            self.current_user = "visitor"
            self.visitor_menu()
        elif username == "staff" and password == "staff123":
            self.current_user = "staff"
            self.staff_menu()
        else:
            print("Invalid credentials. Try again.")

    # --- VISITOR MENU ---
    def visitor_menu(self):
        while True:
            print("\nWelcome visitor!")
            print("1 - Enter/Exit your room")
            print("2 - Control lights")
            print("3 - Select lightning preset")
            print("4 - Log out of app")
            print("5 - Log out of hotel")
            choice = input("Insert your choice: ")

            if choice == "1":
                self.toggle_room_occupancy(1)
            elif choice == "2":
                self.light_control_menu()
            elif choice == "3":
                self.preset_menu()
            elif choice == "4":
                print("Logging out...")
                return
            elif choice == "5":
                self.logout_hotel()
            else:
                print("Invalid choice.")

    # --- STAFF MENU ---
    def staff_menu(self):
        while True:
            print("\nWelcome staff member!")
            print("1 - Select a room")
            print("2 - Log out of app")
            print("3 - Log out of hotel")
            choice = input("Insert your choice: ")

            if choice == "1":
                self.room_selection_menu()
            elif choice == "2":
                print("Logging out...")
                return
            elif choice == "3":
                self.logout_hotel()
            else:
                print("Invalid choice.")

    # --- ROOM OCCUPANCY ---
    def toggle_room_occupancy(self, room_id):
        room = self.rooms[room_id]
        if not room["occupied"]:
            print("Entering your room...")
            room["occupied"] = True
        else:
            print("Exiting your room...")
            room["occupied"] = False

    # --- LIGHT CONTROL MENU ---
    def light_control_menu(self):
        while True:
            print("\nLight control menu")
            print("1 - Check lights")
            print("2 - Select a room")
            print("3 - Turn every light off")
            print("4 - Select lightning preset")
            print("5 - Log out of app")
            print("6 - Log out of hotel")
            choice = input("Insert your choice: ")

            if choice == "1":
                print("Checking lights (placeholder).")
            elif choice == "2":
                print("Selecting room (placeholder).")
            elif choice == "3":
                print("Turning all lights off (placeholder).")
            elif choice == "4":
                self.preset_menu()
            elif choice == "5":
                print("Logging out...")
                return
            elif choice == "6":
                self.logout_hotel()
            else:
                print("Invalid choice.")

    # --- PRESET MENU ---
    def preset_menu(self):
        while True:
            print("\nChoose a lightning preset")
            print("1 - Relaxing")
            print("2 - Bright energetic")
            print("3 - Movie mode")
            print("4 - Wild disco caveman")
            print("5 - Log out of app")
            print("6 - Log out of hotel")
            print("7 - Go back")
            choice = input("Insert your choice: ")

            if choice in ["1", "2", "3", "4"]:
                print(f"Preset {choice} selected (placeholder).")
            elif choice == "5":
                print("Logging out...")
                return
            elif choice == "6":
                self.logout_hotel()
            elif choice == "7":
                return
            else:
                print("Invalid choice.")

    # --- STAFF ROOM SELECTION ---
    def room_selection_menu(self):
        while True:
            print("\nRoom selection:")
            for i, data in self.rooms.items():
                status = "occupied" if data["occupied"] else "free"
                print(f"{i} - Room {i}: {status}")
            print("6 - Log out of app")
            print("7 - Log out of hotel")
            print("8 - Go back")
            choice = input("Insert your choice: ")

            if choice.isdigit():
                room_id = int(choice)
                if room_id in self.rooms:
                    if self.rooms[room_id]["occupied"]:
                        print("Room occupied! Cannot enter.")
                    else:
                        self.maintenance_menu(room_id)
                elif room_id == 6:
                    print("Logging out...")
                    return
                elif room_id == 7:
                    self.logout_hotel()
                elif room_id == 8:
                    return
                else:
                    print("Invalid room number.")
            else:
                print("Invalid input.")

    # --- MAINTENANCE MENU ---
    def maintenance_menu(self, room_id):
        while True:
            print(f"\nMaintenance menu for Room {room_id}")
            print("1 - Turn on/off main lights")
            print("2 - Test system")
            print("3 - Log out of app")
            print("4 - Log out of hotel")
            print("5 - Go back")
            choice = input("Insert your choice: ")

            if choice == "1":
                self.toggle_main_lights(room_id)
            elif choice == "2":
                print("Testing system (placeholder).")
            elif choice == "3":
                print("Logging out...")
                return
            elif choice == "4":
                self.logout_hotel()
            elif choice == "5":
                return
            else:
                print("Invalid choice.")

    def toggle_main_lights(self, room_id):
        room = self.rooms[room_id]
        current = room["lights"]["main"]
        room["lights"]["main"] = not current
        room["lights"]["bathroom"] = not current
        state = "on" if room["lights"]["main"] else "off"
        print(f"Main lights turned {state}.")

    # --- LOGOUT HOTEL ---
    def logout_hotel(self):
        print("\nLogging out of hotel...")
        print("Turning off all lights and resetting presets...")
        for room in self.rooms.values():
            if "lights" in room:
                for light in room["lights"]:
                    room["lights"][light] = False
        print("Goodbye! Hotel system shutting down.")
        exit()

if __name__ == "__main__":
    app = LightHeadApp()
    app.run()
