# lightHeadApp.py
# PullA Vibes

from ui import UI, mainTitle, title, breadcrumb, success, warning, error
from translations import Translations

# UI Colors:
# LoginMenu: CYAN
# VisitorMenu: GREEN
# StaffMenu: YELLOW
# LightControlMenu: BLUE
# PresetMenu: MAGENTA
# MaintenanceMenu: RED
#
# Current Languages:
# ENG = English
# FIN = Finnish
# SWE = Swedish

class LightHeadApp:
    def __init__(self):
        self.rooms = {
            1: {"occupied": False, "lights": {"main": False, "bathroom": False, "bed": False}},
            2: {"occupied": True},
            3: {"occupied": False},
            4: {"occupied": True},
            5: {"occupied": True},
        }
        self.current_user = None
        self.running = True
        self.current_lang = "ENG"

    def run(self):
        while self.running:
            self.login_menu()

    # --- LOGIN ---
    def login_menu(self):
        mainTitle(Translations.translate(self.current_lang, "welcome"), UI.CYAN)
        title(Translations.translate(self.current_lang, "login"), UI.CYAN)
        breadcrumb(["Login"])
        username = input(Translations.translate(self.current_lang, "login" + ":")).strip()
        password = input(Translations.translate(self.current_lang, "password" + ":")).strip()

        if username == "visitor" and password == "visitor123":
            self.current_user = "visitor"
            self.visitor_menu()
        elif username == "staff" and password == "staff123":
            self.current_user = "staff"
            self.staff_menu()
        else:
            error(Translations.translate(self.current_lang, "invalid_credentials"))

    # --- VISITOR MENU ---
    def visitor_menu(self):
        while True:
            title(Translations.translate(self.current_lang, "visitor_menu"), UI.GREEN)
            breadcrumb([Translations.translate(self.current_lang, "visitor")])

            print(UI.GREEN + " 1 - ", Translations.translate(self.current_lang, "visitor_menu_1"))
            print(" 2 - ", Translations.translate(self.current_lang, "visitor_menu_2"))
            print(" 3 - ", Translations.translate(self.current_lang, "visitor_menu_3"))
            print(" 4 - ", Translations.translate(self.current_lang, "visitor_menu_4"))
            print(" 5 - ", Translations.translate(self.current_lang, "visitor_menu_5"))
            print(" 6 - ", Translations.translate(self.current_lang, "visitor_menu_6") + UI.RESET)

            choice = input("\n"+ Translations.translate(self.current_lang, "insert_choice") +": ")

            if choice == "1":
                self.toggle_room_occupancy(1)
            elif choice == "2":
                self.light_control_menu()
            elif choice == "3":
                self.preset_menu()
            elif choice == "4":
                self.language_menu()
            elif choice == "5":
                success(Translations.translate(self.current_lang, "logged_out"))
                self.current_lang = "ENG"
                return
            elif choice == "6":
                self.logout_hotel()
            else:
                error(Translations.translate(self.current_lang, "invalid_choice"))

    # --- STAFF MENU ---
    def staff_menu(self):
        while True:
            title("STAFF MENU", UI.YELLOW)
            breadcrumb(["Staff"])

            print(UI.YELLOW + " 1 - Select a room")
            print(" 2 - Log out of app")
            print(" 3 - Log out of hotel" + UI.RESET)

            choice = input("\nInsert your choice: ")

            if choice == "1":
                self.room_selection_menu()
            elif choice == "2":
                success("Logged out.")
                return
            elif choice == "3":
                self.logout_hotel()
            else:
                error("Invalid choice.")

    # --- ROOM OCCUPANCY ---
    def toggle_room_occupancy(self, room_id):
        room = self.rooms[room_id]
        if not room["occupied"]:
            success(Translations.translate(self.current_lang, "enter_room"))
            room["occupied"] = True
        else:
            success(Translations.translate(self.current_lang, "exit_room"))
            room["occupied"] = False

    # --- LIGHT CONTROL MENU ---
    def light_control_menu(self):
        while True:
            title("LIGHT CONTROL", UI.BLUE)
            breadcrumb([Translations.translate(self.current_lang, "visitor"), Translations.translate(self.current_lang, "light_control")])

            print(UI.BLUE + " 1 -", Translations.translate(self.current_lang, "light_menu_1"))
            print(" 2 -", Translations.translate(self.current_lang, "light_menu_2"))
            print(" 3 -", Translations.translate(self.current_lang, "light_menu_3"))
            print(" 4 -", Translations.translate(self.current_lang, "light_menu_4"))
            print(" 5 -", Translations.translate(self.current_lang, "light_menu_5"))
            print(" 6 -", Translations.translate(self.current_lang, "light_menu_6") + UI.RESET)

            choice = input("\n"+ Translations.translate(self.current_lang, "insert_choice")+":")

            if choice == "1":
                print("Checking lights (placeholder).")
            elif choice == "2":
                print("Selecting room (placeholder).")
            elif choice == "3":
                print("Turning all lights off (placeholder).")
            elif choice == "4":
                self.preset_menu()
            elif choice == "5":
                success(Translations.translate(self.current_lang, "logged_out"))
                return
            elif choice == "6":
                self.logout_hotel()
            else:
                error(Translations.translate(self.current_lang, "invalid_choice"))

    # --- PRESET MENU ---
    def preset_menu(self):
        while True:
            title(Translations.translate(self.current_lang, "lighting_presets"), UI.MAGENTA)
            breadcrumb([Translations.translate(self.current_lang, "visitor"), Translations.translate(self.current_lang, "presets")])

            print(UI.MAGENTA + " 1 -", Translations.translate(self.current_lang, "preset_menu_1"))
            print(" 2 -", Translations.translate(self.current_lang, "preset_menu_2"))
            print(" 3 -", Translations.translate(self.current_lang, "preset_menu_3"))
            print(" 4 -", Translations.translate(self.current_lang, "preset_menu_4"))
            print(" 5 -", Translations.translate(self.current_lang, "preset_menu_5"))
            print(" 6 -", Translations.translate(self.current_lang, "preset_menu_6"))
            print(" 7 -", Translations.translate(self.current_lang, "preset_menu_7") + UI.RESET)

            choice = input("\n"+ Translations.translate(self.current_lang, "insert_choice")+":")

            if choice in ["1", "2", "3", "4"]:
                success(f"{Translations.translate(self.current_lang, "preset")} {choice} {Translations.translate(self.current_lang, "selected")}")
            elif choice == "5":
                success(Translations.translate(self.current_lang, "logged_out"))
                return
            elif choice == "6":
                self.logout_hotel()
            elif choice == "7":
                return
            else:
                error(Translations.translate(self.current_lang, "invalid_choice"))

    # REQ-002 The guest is able to choose the operating system language
    def language_menu(self):
        while True:
            title(Translations.translate(self.current_lang, "language_menu"), UI.MAGENTA)
            breadcrumb([Translations.translate(self.current_lang, "visitor"), Translations.translate(self.current_lang, "language")])

            print(UI.MAGENTA + " 1 -", Translations.translate(self.current_lang, "lang_menu_1"))
            print(" 2 -", Translations.translate(self.current_lang, "lang_menu_2"))
            print(" 3 -", Translations.translate(self.current_lang, "lang_menu_3"))
            print(" 4 -", Translations.translate(self.current_lang, "lang_menu_4"))
            print(" 5 -", Translations.translate(self.current_lang, "lang_menu_5"))
            print(" 6 -",Translations.translate(self.current_lang, "lang_menu_6") + UI.RESET)

            choice = input("\n"+Translations.translate(self.current_lang, "insert_choice")+":")

            if choice == "1":
                self.current_lang = "ENG"
                success(f"{Translations.translate(self.current_lang, "lang_menu_1")} {Translations.translate(self.current_lang, "selected")}")
            elif choice == "2":
                self.current_lang = "FIN"
                success(f"{Translations.translate(self.current_lang, "lang_menu_2")} {Translations.translate(self.current_lang, "selected")}")
            elif choice == "3":
                self.current_lang = "SWE"
                success(f"{Translations.translate(self.current_lang, "lang_menu_3")} {Translations.translate(self.current_lang, "selected")}")
            elif choice == "4":
                success("Logged out.")
                return
            elif choice == "5":
                self.logout_hotel()
            elif choice == "6":
                return
            else:
                error(Translations.translate(self.current_lang, "invalid_choice"))

    # --- STAFF ROOM SELECTION ---
    def room_selection_menu(self):
        while True:
            title("ROOM SELECTION", UI.YELLOW)
            breadcrumb(["Staff", "Room Selection"])

            for i, data in self.rooms.items():
                status = "occupied" if data["occupied"] else "free"
                print(f" {i} - Room {i}: {status}")

            print("\n 6 - Log out of app")
            print(" 7 - Log out of hotel")
            print(" 8 - Go back")

            choice = input("\nInsert your choice: ")

            if choice.isdigit():
                room_id = int(choice)
                if room_id in self.rooms:
                    if self.rooms[room_id]["occupied"]:
                        warning("Room occupied! Cannot enter.")
                    else:
                        self.maintenance_menu(room_id)
                elif room_id == 6:
                    success("Logged out.")
                    return
                elif room_id == 7:
                    self.logout_hotel()
                elif room_id == 8:
                    return
                else:
                    error("Invalid room number.")
            else:
                error("Invalid input.")

    # --- MAINTENANCE MENU ---
    def maintenance_menu(self, room_id):
        while True:
            title(f"MAINTENANCE ROOM {room_id}", UI.RED)
            breadcrumb(["Staff", "Room Selection", f"Room {room_id}", "Maintenance"])

            print(UI.RED + " 1 - Turn on/off main lights")
            print(" 2 - Test system")
            print(" 3 - Log out of app")
            print(" 4 - Log out of hotel")
            print(" 5 - Go back" + UI.RESET)

            choice = input("\nInsert your choice: ")

            if choice == "1":
                self.toggle_main_lights(room_id)  
            elif choice == "2":
                print("Testing system (placeholder).")
            elif choice == "3":
                success("Logged out.")
                return
            elif choice == "4":
                self.logout_hotel()
            elif choice == "5":
                return
            else:
                error("Invalid choice.")

    # TODO: KeyError: 'lights' when trying to toggle lights in unoccupied room.
    # TODO: IMPLEMENTOI HUONE LUOKKA
    def toggle_main_lights(self, room_id):
        room = self.rooms[room_id]
        current = room["lights"]["main"]
        room["lights"]["main"] = not current
        room["lights"]["bathroom"] = not current
        state = "on" if room["lights"]["main"] else "off"
        success(f"{Translations.translate(self.current_lang, "main_lights_turned")} {Translations.translate(self.current_lang, state)}.")

    # --- LOGOUT HOTEL ---
    def logout_hotel(self):
        warning("\n"+Translations.translate(self.current_lang, "logging_out_hotel"))
        print(Translations.translate(self.current_lang, "turn_lights_reset"))
        for room in self.rooms.values():
            if "lights" in room:
                for light in room["lights"]:
                    room["lights"][light] = False
        print(UI.RED + Translations.translate(self.current_lang, "end_msg") + UI.RESET)
        exit()

if __name__ == "__main__":
    app = LightHeadApp()
    app.run()
