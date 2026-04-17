# lightHeadApp.py
# PullA Vibes

from ui import UI, mainTitle, title, breadcrumb, success, warning, error
from translations import Translations
from rooms import Rooms, Room
from userhandler import UserManager, User

'''
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
'''

class LightHeadApp:
    def __init__(self):
        self.rooms = Rooms()
        self.current_user = None
        self.running = True
        self.current_lang = "ENG"
        self.users = UserManager()
        self.current_room = None

        self._init_rooms()
        self._init_users()

    def _init_rooms(self):
        default_rooms = [101, 102, 103, 201, 202]

        for room_id in default_rooms:
            self.rooms.add_room(Room(room_id))

        self.rooms.add_room(Room.from_zone_names(301, ["main", "sauna", "balcony"]))

    def _init_users(self):
        self.users.add_user(User("visitor", "visitor123", "visitor",room_id=101, room_type="basic"))
        self.users.add_user(User("staff", "staff123", "staff"))    

    def run(self):
        while self.running:
            self.login_menu()

    # --- LOGIN ---
    def login_menu(self):
        mainTitle(Translations.translate(self.current_lang, "welcome"), UI.CYAN)
        title(Translations.translate(self.current_lang, "login"), UI.CYAN)
        breadcrumb(["Login"])
        username = "visitor"# input(Translations.translate(self.current_lang, "login" + ":")).strip()
        password = "visitor123" # input(Translations.translate(self.current_lang, "password" + ":")).strip()

        user = self.users.authenticate(username, password)
        print(user)
        if user:
            self.current_user = user
            if user.role == "visitor":
                self.current_room = self.rooms.get_room(user.room_id)
                self.visitor_menu()
            elif user.role == "staff":
                self.staff_menu()
        else:
            error(Translations.translate(self.current_lang, "invalid_credentials"))

    # --- VISITOR MENU ---
    def visitor_menu(self):
        while True:
            title(Translations.translate(self.current_lang, "visitor_menu"), UI.GREEN)
            breadcrumb([Translations.translate(self.current_lang, "visitor"), f"Room: {str(self.current_room.id)}"])
            occupancy = self.current_room.get_occupancy()
            print(UI.GREEN + " 1 - ", Translations.translate(self.current_lang, "visitor_menu_1_exit" if occupancy else "visitor_menu_1_enter"))
            if occupancy:
                print(" 2 - ", Translations.translate(self.current_lang, "visitor_menu_2"))
                print(" 3 - ", Translations.translate(self.current_lang, "visitor_menu_3"))
                print(" 4 - ", Translations.translate(self.current_lang, "visitor_menu_4"))
                print(" 5 - ", Translations.translate(self.current_lang, "visitor_menu_5"))
                print(" 6 - ", Translations.translate(self.current_lang, "return") + UI.RESET)

            choice = input("\n"+ Translations.translate(self.current_lang, "insert_choice") +": ")

            if choice == "1":
                self.toggle_room_occupancy(self.current_room.id)
            elif choice == "2" and occupancy:
                self.light_control_menu()
            elif choice == "3" and occupancy:
                self.preset_menu()
            elif choice == "4" and occupancy:
                self.language_menu()
            elif choice == "5" and occupancy:
                success(Translations.translate(self.current_lang, "logged_out"))
                self.current_lang = "ENG"
                return
            elif choice == "6" and occupancy:
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
        room = self.current_room
        if not room.get_occupancy():
            success(Translations.translate(self.current_lang, "enter_room"))
            room.occupancy = True
            room.set_brightness("main", 50)
        else:
            success(Translations.translate(self.current_lang, "exit_room"))
            room.occupancy = False
            room.set_lights_off()

    # --- LIGHT CONTROL MENU ---
    def light_control_menu(self):
        while True:
            title("LIGHT CONTROL", UI.BLUE)
            breadcrumb([Translations.translate(self.current_lang, "visitor"), Translations.translate(self.current_lang, "light_control")])

            print(UI.BLUE + " 1 -", Translations.translate(self.current_lang, "light_menu_1"))
            print(" 2 -", Translations.translate(self.current_lang, "light_menu_2"))
            print(" 3 -", Translations.translate(self.current_lang, "light_menu_3"))
            print(" 4 -", Translations.translate(self.current_lang, "light_menu_4"))
            print(" 5 -", Translations.translate(self.current_lang, "return") + UI.RESET)

            choice = input("\n"+ Translations.translate(self.current_lang, "insert_choice")+":")

            if choice == "1":
                print("Light status:")
                room = self.rooms.get_room(self.current_room.id)
                for zone in room.zones:
                    settings = room.zones[zone]
                    print(f"{zone.capitalize()}:")
                    print(f"\t Brightness: {settings.brightness}")
                    print(f"\t Color: {settings.color}")
            elif choice == "2":
                self.select_room_menu()
            elif choice == "3":
                self.current_room.set_lights_off()
                success(Translations.translate(self.current_lang, "turn_lights_reset"))
            elif choice == "4":
                self.preset_menu()
            elif choice == "5":
                return
            else:
                error(Translations.translate(self.current_lang, "invalid_choice"))

    def select_room_menu(self):
        while True:
            title(Translations.translate(self.current_lang, "zones"), UI.MAGENTA)
            breadcrumb([Translations.translate(self.current_lang, "visitor"), Translations.translate(self.current_lang, "light_control"), Translations.translate(self.current_lang, "zones").lower().capitalize()])
            zones = list(enumerate(self.current_room.zones))
            for index, zone in zones:
                print(UI.MAGENTA + f" {index+1} - ", Translations.translate(self.current_lang, zone).capitalize())
            print(f" {len(zones)+1} - ", Translations.translate(self.current_lang, "return").capitalize())
            print(UI.RESET)

            choice = input("\n"+ Translations.translate(self.current_lang, "insert_choice")+":")
            
            try:
                choice = int(choice)
                if choice < 1 or choice > len(zones)+1:
                    raise ValueError("Invalid choice range.")
            except:
                error(Translations.translate(self.current_lang, "invalid_choice"))
                continue

            if choice in range(1, len(zones)+1):
                self.zone_light_control_menu(zones[choice-1][1])
            else:
                return
    
    def zone_light_control_menu(self, zone: str):
         while True:
            title(Translations.translate(self.current_lang, zone).capitalize(), UI.MAGENTA)
            breadcrumb([Translations.translate(self.current_lang, "visitor"), Translations.translate(self.current_lang, "light_control"),
                        Translations.translate(self.current_lang, "zones").lower().capitalize(), Translations.translate(self.current_lang, zone).capitalize()])
            room = self.rooms.get_room(self.current_room.id)
            settings = room.zones[zone]

            print(UI.CYAN + ("Current Color: " +  settings.color).ljust(40), "Current Brightness:", settings.brightness, "\n")
            print((" + - " + Translations.translate(self.current_lang, "add_brightness")).ljust(40), "- -", Translations.translate(self.current_lang, "lower_brightness"), "\n")
            print((Translations.translate(self.current_lang, "static_colors") + ":").ljust(40), Translations.translate(self.current_lang, "presets") + ":")
            print((" 1 - " +  Translations.translate(self.current_lang, "preset_menu_1")).ljust(40), " 5 - " + Translations.translate(self.current_lang, "white"))
            print((" 2 - " + Translations.translate(self.current_lang, "preset_menu_2")).ljust(40), " 6 - " + Translations.translate(self.current_lang, "red"))
            print((" 3 - " +  Translations.translate(self.current_lang, "preset_menu_3")).ljust(40), " 7 - " + Translations.translate(self.current_lang, "green"))
            print((" 4 - " +  Translations.translate(self.current_lang, "preset_menu_4")).ljust(40), " 8 - " + Translations.translate(self.current_lang, "blue"))
            print(" 9 -", Translations.translate(self.current_lang, "return") + UI.RESET)

            choice = input("\n" + Translations.translate(self.current_lang, "insert_choice")+":")

            brightness = self.current_room.get_brightness(zone)
            if choice == "+":
                if brightness + 10 <= 100:
                    self.current_room.set_brightness(zone, brightness + 10)
                    success(Translations.translate(self.current_lang, "brightness_adjusted") + ": " + str(brightness+10))
                else:
                    warning(Translations.translate(self.current_lang, "brightness_max"))
            elif choice == "-":
                if brightness - 10 >= 0:
                    self.current_room.set_brightness(zone, brightness - 10)
                    success(Translations.translate(self.current_lang, "brightness_adjusted") + ": " + str(brightness-10))
                else:
                    warning(Translations.translate(self.current_lang, "brightness_min"))
            else:
                try:
                    choice = int(choice)
                    if choice < 1 or choice > 9:
                        raise ValueError("Invalid choice range.")
                except:
                    error(Translations.translate(self.current_lang, "invalid_choice"))
                    continue

                if choice in range(1, 9):
                    self.current_room.set_color(zone, choice-1)
                    success(Translations.translate(self.current_lang, "color_changed") + ": " + str(self.current_room.get_color(zone)))
                else:
                    return

    # --- PRESET MENU ---
    def preset_menu(self):
        while True:
            title(Translations.translate(self.current_lang, "lighting_presets"), UI.MAGENTA)
            breadcrumb([Translations.translate(self.current_lang, "visitor"), Translations.translate(self.current_lang, "presets")])

            print(UI.MAGENTA + " 1 -", Translations.translate(self.current_lang, "preset_menu_1"))
            print(" 2 -", Translations.translate(self.current_lang, "preset_menu_2"))
            print(" 3 -", Translations.translate(self.current_lang, "preset_menu_3"))
            print(" 4 -", Translations.translate(self.current_lang, "preset_menu_4"))
            print(" 5 -", Translations.translate(self.current_lang, "preset_menu_7") + UI.RESET)

            choice = input("\n"+ Translations.translate(self.current_lang, "insert_choice")+":")

            try:
                choice = int(choice)
                if choice < 1 or choice > 5:
                    raise ValueError("Invalid choice range.")
            except:
                error(Translations.translate(self.current_lang, "invalid_choice"))
                continue

            if choice in range(1, 5):
                self.current_room.set_lights_all_zones(choice-1)
                success(f"{Translations.translate(self.current_lang, "preset")} {choice} {Translations.translate(self.current_lang, "selected")}")
            else:
                return
       
    # REQ-002 The guest is able to choose the operating system language
    def language_menu(self):
        while True:
            title(Translations.translate(self.current_lang, "language_menu"), UI.MAGENTA)
            breadcrumb([Translations.translate(self.current_lang, "visitor"), Translations.translate(self.current_lang, "language")])

            print(UI.MAGENTA + " 1 -", Translations.translate(self.current_lang, "lang_menu_1"))
            print(" 2 -", Translations.translate(self.current_lang, "lang_menu_2"))
            print(" 3 -", Translations.translate(self.current_lang, "lang_menu_3"))
            print(" 4 -",Translations.translate(self.current_lang, "lang_menu_6") + UI.RESET)

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
                return
            else:
                error(Translations.translate(self.current_lang, "invalid_choice"))

    # --- STAFF ROOM SELECTION ---
    def room_selection_menu(self):
        while True:
            title("ROOM SELECTION", UI.YELLOW)
            breadcrumb(["Staff", "Room Selection"])

            for room_id, data in self.rooms.room_items():
                status = "occupied" if data.get_occupancy() else "free"
                print(f" {data.room_type} - Room {room_id}: {status}")

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
        room = self.rooms.get_room(room_id)
        current = room["lights"]["main"]
        room["lights"]["main"] = not current
        room["lights"]["bathroom"] = not current
        state = "on" if room["lights"]["main"] else "off"
        success(f"{Translations.translate(self.current_lang, "main_lights_turned")} {Translations.translate(self.current_lang, state)}.")

    # --- LOGOUT HOTEL ---
    # TODO : Implementoi room
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
