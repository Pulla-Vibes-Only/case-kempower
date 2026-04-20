# rooms.py

from dataclasses import dataclass, field


'''
# You can create a room with only an ID room101 = Room(101) --> Room with default sections and LightingSettings
#
# Special rooms with more sections can be created with room helper function from_zone_names
# You can use it like room312 = Room.from_zone_names(ID ,["Basement", "Storageroom"] etc. sets default Lighting settings)
'''

SUITES = {301,302,303}
COLORS = ["Relaxing",
          "Bright energetic",
          "Movie mode",
          "Wild disco caveman",
          "White",
          "Red",
          "Green",
          "Blue"]

@dataclass
class LightingSettings:
    brightness: int = 0
    color: str = "white"

def default_sections():
    return {
        "main": LightingSettings(),
        "bedroom": LightingSettings(),
        "bathroom": LightingSettings()
    }

@dataclass
class Room:
    id: int
    zones: dict[str, LightingSettings] = field(default_factory=default_sections)
    occupancy: bool = False
    available: bool = False
    room_type: str = "basic"

    @classmethod
    def from_zone_names(cls, id: int, names: list[str]):
        if id in SUITES:
            roomtype = "suite"
        else:
            print("TÄÄLLÄ")
            roomtype = "basic"
        return cls(
            id=id,
            zones={name: LightingSettings() for name in names},
            occupancy = False,
            available = True,
            room_type = roomtype
        )

    def get_sections(self):
        return list(self.zones.keys())

    def get_brightness(self, zone: str):
        return self.zones[zone].brightness

    def set_brightness(self, zone: str, value: int):
        self.zones[zone].brightness = value

    def get_color(self, zone: str):
        return self.zones[zone].color
    
    def set_color(self, zone: str, color: int):
        self.zones[zone].color = COLORS[color]
    
    def get_occupancy(self):
        return self.occupancy
    
    def set_lights_off(self):
        for zone in self.zones:
            self.zones[zone].brightness = 0
            self.zones[zone].color = COLORS[4]

    def set_lights_on(self):
        for zone in self.zones:
            self.zones[zone].brightness = 100
            self.zones[zone].color = COLORS[4]

    def set_color_all_zones(self, color: int):
        for zone in self.zones:
            self.zones[zone].color = COLORS[color]

class Rooms:
    def __init__(self):
        self._rooms: dict[int, Room] = {}

    def add_room(self, room: Room):
        self._rooms[room.id] = room

    def get_room(self, room_id: int):
        return self._rooms[room_id]
    
    # To get room id and zones all at once
    def room_items(self):
        return sorted(self._rooms.items())
    
    def __iter__(self):
        return iter(self._rooms.values())
    
if __name__ == "__main__":
    room201 = Room(201)
    room101 = Room(304)
    room1 = Room(405)
    room2 = Room.from_zone_names(7, ["base", "test", "a"])

    rooms = Rooms()
    rooms.add_room(room101)
    rooms.add_room(room201)
    rooms.add_room(room1)
    rooms.add_room(room2)
    for room in rooms:
        print(room)
    room1.occupancy = True
    for room in rooms:
        print(room)