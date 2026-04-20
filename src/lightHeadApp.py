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
        self.users.add_user(User("visitor101", "visitor123", "visitor",room_id=101, room_type="basic"))
        self.users.add_user(User("visitor102", "visitor123", "visitor",room_id=102, room_type="basic"))
        self.users.add_user(User("visitor103", "visitor123", "visitor",room_id=103, room_type="basic"))
        self.users.add_user(User("visitor201", "visitor123", "visitor",room_id=201, room_type="basic"))
        self.users.add_user(User("visitor202", "visitor123", "visitor",room_id=201, room_type="basic"))
        self.users.add_user(User("visitor301", "visitor123", "visitor",room_id=301, room_type="suite"))
        self.users.add_user(User("staff", "staff123", "staff"))    

    def run(self):
        while self.running:
            self.login_menu()

    # --- LOGIN ---
    # REQ 007 - The system must be easy to install and scalable
    def login_menu(self):
        mainTitle(Translations.translate(self.current_lang, "welcome"), UI.CYAN)
        title(Translations.translate(self.current_lang, "login"), UI.CYAN)
        breadcrumb(["Login"])
        username = input(Translations.translate(self.current_lang, "login" + ":")).strip()
        password = input(Translations.translate(self.current_lang, "password" + ":")).strip()

        user = self.users.authenticate(username, password)
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
                # FOR DEMO REASONS ALSO LOGS OUT OF APP - IN REAL WORLD THE SYSTEM SHOULD ALWAYS BE IN READY STATE
                print(" 5 - ", Translations.translate(self.current_lang, "visitor_menu_5") + UI.RESET)

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
                self.current_room.available = True
                # FOR DEMO REASONS COMMENTED OUT TO SEE OCCUPANCY IN STAFF MODE
                #self.current_room.occupancy = False
                return
            else:
                error(Translations.translate(self.current_lang, "invalid_choice"))

    # --- STAFF MENU ---
    def staff_menu(self):
        while True:
            title("STAFF MENU", UI.YELLOW)
            breadcrumb(["Staff"])

            print(UI.YELLOW + " 1 - Select a room")
            print(" 2 - Log out of app")

            choice = input("\nInsert your choice: ")

            if choice == "1":
                self.room_selection_menu()
            elif choice == "2":
                success("Logged out.")
                return
            else:
                error("Invalid choice.")

    # --- ROOM OCCUPANCY ---
    # REQ 003 - The system is energy efficient (for example, lights stay off if room is empty)
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
            # REQ 004 - The system control device (touch screen) clearly indicates the status of every light in the room
            # REQ 012 - The control device displays possible rooms (bathroom, kitchen etc) separately
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
    # REQ 012 - The control device displays possible rooms (bathroom, kitchen etc) separately
    def select_room_menu(self):
        while True:
            title(Translations.translate(self.current_lang, "zones"), UI.MAGENTA)
            breadcrumb([Translations.translate(self.current_lang, "visitor"), Translations.translate(self.current_lang, "light_control"), Translations.translate(self.current_lang, "zones").lower().capitalize()])
            zones = list(enumerate(self.current_room.zones))
            for index, zone in zones:
                print(UI.MAGENTA + f" {index+1} - ", Translations.translate(self.current_lang, zone).capitalize())
            print(f" {len(zones)+1} - ", Translations.translate(self.current_lang, "all_zones").capitalize())
            print(f" {len(zones)+2} - ", Translations.translate(self.current_lang, "return").capitalize())
            print(UI.RESET)

            choice = input("\n"+ Translations.translate(self.current_lang, "insert_choice")+":")
            
            try:
                choice = int(choice)
                if choice < 1 or choice > len(zones)+2:
                    raise ValueError("Invalid choice range.")
            except:
                error(Translations.translate(self.current_lang, "invalid_choice"))
                continue
            if choice in range(1, len(zones)+1):
                print("HERE", len(zones), choice)
                self.zone_light_control_menu(zones[choice-1][1])
            elif choice == len(zones)+1:
                self.zone_light_control_menu("all_zones") 
            else:
                return
    # REQ 012 - The control device displays possible rooms (bathroom, kitchen etc) separately
    def zone_light_control_menu(self, zone: str):
         while True:
            room = self.rooms.get_room(self.current_room.id)
            all_zones = zone == "all_zones"
            title(Translations.translate(self.current_lang, zone).capitalize(), UI.MAGENTA)
            breadcrumb([Translations.translate(self.current_lang, "visitor"), Translations.translate(self.current_lang, "light_control"),
                        Translations.translate(self.current_lang, "zones").lower().capitalize(), Translations.translate(self.current_lang, zone).capitalize()])
            if not all_zones:
                settings = room.zones[zone]
            # REQ 004 - The system control device (touch screen) clearly indicates the status of every light in the room
                print(UI.CYAN + (Translations.translate(self.current_lang, "current_color") + ": " + settings.color).ljust(40), 
                    Translations.translate(self.current_lang, "current_brightness") + ": " + str(settings.brightness), "\n")
            else:
                for i_zone in self.current_room.zones:
                    print(UI.CYAN + i_zone.capitalize())
                    print((Translations.translate(self.current_lang, "current_color") + ": " + room.zones[i_zone].color).ljust(40), 
                    Translations.translate(self.current_lang, "current_brightness") + ": " + str(room.zones[i_zone].brightness), "\n")

            print((" + - " + Translations.translate(self.current_lang, "add_brightness")).ljust(40), "- -", Translations.translate(self.current_lang, "lower_brightness"), "\n")
            print((Translations.translate(self.current_lang, "static_colors") + ":").ljust(40), Translations.translate(self.current_lang, "presets") + ":")
            print((" 1 - " +  Translations.translate(self.current_lang, "preset_menu_1")).ljust(40), " 5 - " + Translations.translate(self.current_lang, "white"))
            print((" 2 - " + Translations.translate(self.current_lang, "preset_menu_2")).ljust(40), " 6 - " + Translations.translate(self.current_lang, "red"))
            print((" 3 - " +  Translations.translate(self.current_lang, "preset_menu_3")).ljust(40), " 7 - " + Translations.translate(self.current_lang, "green"))
            print((" 4 - " +  Translations.translate(self.current_lang, "preset_menu_4")).ljust(40), " 8 - " + Translations.translate(self.current_lang, "blue"))
            print(" 9 -", Translations.translate(self.current_lang, "return") + UI.RESET)

            choice = input("\n" + Translations.translate(self.current_lang, "insert_choice")+":")
            
            # REQ 009 - The brightness, color and color temperature can be adjusted
            if not all_zones:
                brightness = self.current_room.get_brightness(zone)
            if choice == "+":
                if all_zones:
                    for i_zone in room.zones:
                        if room.zones[i_zone].brightness + 10 <= 100:
                            room.set_brightness(i_zone, room.get_brightness(i_zone) + 10)
                else:
                    if brightness + 10 <= 100:
                        room.set_brightness(zone, brightness + 10)
                        success(Translations.translate(self.current_lang, "brightness_adjusted") + ": " + str(brightness+10))
                    else:
                        warning(Translations.translate(self.current_lang, "brightness_max"))
            elif choice == "-":
                if all_zones:
                    for i_zone in room.zones:
                        if room.zones[i_zone].brightness - 10 >= 0:
                            room.set_brightness(i_zone, room.get_brightness(i_zone) - 10)
                else:
                    if brightness - 10 >= 0:
                        room.set_brightness(zone, brightness - 10)
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
                    if all_zones:
                        room.set_color_all_zones(choice-1)
                    else:
                        room.set_color(zone, choice-1)
                        success(Translations.translate(self.current_lang, "color_changed") + ": " + str(self.current_room.get_color(zone)))
                else:
                    return

    # --- PRESET MENU ---
    # REQ 009 - The brightness, color and color temperature can be adjusted
    # REQ 013 - The system has pre-installed lightning setups for different moods and situations
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
                self.current_room.set_color_all_zones(choice-1)
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
            rooms = []
            title("ROOM SELECTION", UI.YELLOW)
            breadcrumb(["Staff", "Room Selection"])

            for room_id, data in self.rooms.room_items():
                rooms.append(room_id)
                status = "Occupied" if data.get_occupancy() else "Free"
                print(f"Room {room_id}:")
                print(f"\tRoom type: {data.room_type} {3*" "}|{3*" "} Occupancy: {status}")
            print("\n 9 - Go back")

            choice = input("\nInsert your choice: ")

            try:
                if (int(choice) in rooms or choice == "9"):
                    choice = int(choice)
            except:
                error("Invalid input.")
                continue

            if choice == 9:
                return
            else:
                for room in self.rooms:
                    print(room.id, choice)
                    if room.id == choice:
                        self.current_room = room
                
                if self.current_room.occupancy == True:
                    warning("Room occupied! Cannot enter.")
                else:
                    self.maintenance_menu(self.current_room.id)

    # --- MAINTENANCE MENU ---
    # REQ 005 - every room can be controlled through hotel central system by hotel personnel
    def maintenance_menu(self, room_id):
        while True:
            title(f"MAINTENANCE ROOM {room_id}", UI.RED)
            breadcrumb(["Staff", "Room Selection", f"Room {room_id}", "Maintenance"])

            print(UI.RED + " 1 - Turn on cleaning lights")
            print(UI.RED + " 2 - Control lights")
            print(" 3 - Leave room (Reset lights)" + UI.RESET)

            choice = input("\nInsert your choice: ")

            if choice == "1":
                self.current_room.set_lights_on()
            elif choice == "2":
                self.zone_light_control_menu("all_zones")
            elif choice == "3":
                success("Turning off all lights and resettings presets...")
                return
            else:
                error("Invalid choice.")
        
    """
    # DO WE NEED THIS ????????????????
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
    """

if __name__ == "__main__":
    app = LightHeadApp()
    app.run()
