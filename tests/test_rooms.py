# Tests for rooms.py
# PullA Vibes
# Tests cover LightingSettings defaults, Room construction (default and from_zone_names),
# brightness and color control per zone, occupancy, lights on/off switching,
# and the Rooms collection (add, get, iterate, sort).

import sys
import pytest

sys.path.insert(0, "..")

from rooms import Room, Rooms, LightingSettings, COLORS, SUITES


class TestLightingSettings:
    def test_default_brightness(self):
        # LightingSettings should initialize with brightness 0
        ls = LightingSettings()
        assert ls.brightness == 0

    def test_default_color(self):
        # LightingSettings should initialize with color "white"
        ls = LightingSettings()
        assert ls.color == "white"

    def test_custom_values(self):
        # LightingSettings should store custom brightness and color values
        ls = LightingSettings(brightness=75, color="Red")
        assert ls.brightness == 75
        assert ls.color == "Red"


class TestRoomDefaults:
    def test_default_zones_exist(self):
        # A default Room should have main, bedroom and bathroom zones
        room = Room(101)
        assert "main" in room.zones
        assert "bedroom" in room.zones
        assert "bathroom" in room.zones

    def test_default_occupancy_false(self):
        # A new Room should not be occupied
        room = Room(101)
        assert room.occupancy is False

    def test_default_available_false(self):
        # A Room created with Room() should not be marked available
        room = Room(101)
        assert room.available is False

    def test_default_room_type_basic(self):
        # A default Room should have room_type "basic"
        room = Room(101)
        assert room.room_type == "basic"

    def test_room_id_stored(self):
        # Room should store the given ID correctly
        room = Room(202)
        assert room.id == 202


class TestRoomFromZoneNames:
    def test_custom_zones(self):
        # from_zone_names should create exactly the zones given
        room = Room.from_zone_names(999, ["main", "sauna", "balcony"])
        assert set(room.zones.keys()) == {"main", "sauna", "balcony"}

    def test_available_true_after_creation(self):
        # from_zone_names should mark the room as available
        room = Room.from_zone_names(101, ["main", "bathroom"])
        assert room.available is True

    def test_suite_room_type_for_suite_id(self):
        # A room ID in SUITES should get room_type "suite"
        suite_id = next(iter(SUITES))
        room = Room.from_zone_names(suite_id, ["main", "sauna"])
        assert room.room_type == "suite"

    def test_basic_room_type_for_non_suite_id(self):
        # A room ID not in SUITES should get room_type "basic"
        room = Room.from_zone_names(999, ["main"])
        assert room.room_type == "basic"

    def test_all_zones_have_default_lighting(self):
        # All zones created with from_zone_names should start at brightness 0
        room = Room.from_zone_names(101, ["main", "sauna"])
        for zone in room.zones.values():
            assert zone.brightness == 0


class TestRoomBrightness:
    def setup_method(self):
        self.room = Room(101)

    def test_get_brightness_default(self):
        # Brightness should be 0 before any changes
        assert self.room.get_brightness("main") == 0

    def test_set_and_get_brightness(self):
        # set_brightness should update the zone brightness correctly
        self.room.set_brightness("main", 80)
        assert self.room.get_brightness("main") == 80

    def test_set_brightness_zero(self):
        # Brightness should be settable back to 0
        self.room.set_brightness("bedroom", 50)
        self.room.set_brightness("bedroom", 0)
        assert self.room.get_brightness("bedroom") == 0

    def test_set_brightness_max(self):
        # Brightness should accept 100 as maximum value
        self.room.set_brightness("bathroom", 100)
        assert self.room.get_brightness("bathroom") == 100

    def test_brightness_isolated_per_zone(self):
        # Setting brightness in one zone should not affect other zones
        self.room.set_brightness("main", 90)
        self.room.set_brightness("bedroom", 30)
        assert self.room.get_brightness("main") == 90
        assert self.room.get_brightness("bedroom") == 30


class TestRoomColor:
    def setup_method(self):
        self.room = Room(101)

    def test_get_color_default(self):
        # Color should be "white" before any changes
        assert self.room.get_color("main") == "white"

    def test_set_color_by_index(self):
        # set_color should map index 0 to the first color in COLORS
        self.room.set_color("main", 0)
        assert self.room.get_color("main") == COLORS[0]

    def test_set_color_all_valid_indices(self):
        # Every index in COLORS should be settable and retrievable correctly
        for i, color in enumerate(COLORS):
            self.room.set_color("main", i)
            assert self.room.get_color("main") == color

    def test_set_color_all_zones(self):
        # set_color_all_zones should update every zone to the same color
        self.room.set_color_all_zones(2)
        for zone in self.room.zones:
            assert self.room.get_color(zone) == COLORS[2]

    def test_color_isolated_per_zone(self):
        # Setting color in one zone should not affect other zones
        self.room.set_color("main", 1)
        self.room.set_color("bedroom", 3)
        assert self.room.get_color("main") == COLORS[1]
        assert self.room.get_color("bedroom") == COLORS[3]


class TestRoomOccupancy:
    def test_get_occupancy_default(self):
        # A new room should return False for occupancy
        room = Room(101)
        assert room.get_occupancy() is False

    def test_set_occupancy_true(self):
        # Setting occupancy to True should be reflected by get_occupancy
        room = Room(101)
        room.occupancy = True
        assert room.get_occupancy() is True


class TestRoomLightsSwitching:
    def setup_method(self):
        self.room = Room(101)

    def test_set_lights_off(self):
        # set_lights_off should set brightness to 0 and color to White in all zones
        self.room.set_brightness("main", 80)
        self.room.set_color("main", 1)
        self.room.set_lights_off()
        for zone in self.room.zones:
            assert self.room.get_brightness(zone) == 0
            assert self.room.get_color(zone) == COLORS[4]  # White

    def test_set_lights_on(self):
        # set_lights_on should set brightness to 100 and color to White in all zones
        self.room.set_lights_on()
        for zone in self.room.zones:
            assert self.room.get_brightness(zone) == 100
            assert self.room.get_color(zone) == COLORS[4]  # White

    def test_lights_off_after_on(self):
        # Calling set_lights_off after set_lights_on should reset brightness to 0
        self.room.set_lights_on()
        self.room.set_lights_off()
        for zone in self.room.zones:
            assert self.room.get_brightness(zone) == 0

    def test_get_sections(self):
        # get_sections should return all zone names
        sections = self.room.get_sections()
        assert "main" in sections
        assert "bedroom" in sections
        assert "bathroom" in sections


class TestRooms:
    def setup_method(self):
        self.rooms = Rooms()
        self.room101 = Room(101)
        self.room202 = Room(202)
        self.rooms.add_room(self.room101)
        self.rooms.add_room(self.room202)

    def test_add_and_get_room(self):
        # A room added to Rooms should be retrievable by its ID
        assert self.rooms.get_room(101).id == 101

    def test_get_second_room(self):
        # Multiple rooms should be independently retrievable
        assert self.rooms.get_room(202).id == 202

    def test_iteration_over_rooms(self):
        # Iterating over Rooms should yield all added rooms
        ids = [room.id for room in self.rooms]
        assert 101 in ids
        assert 202 in ids

    def test_room_items_sorted(self):
        # room_items should return rooms sorted by ID
        keys = [k for k, _ in self.rooms.room_items()]
        assert keys == sorted(keys)

    def test_add_room_overwrites_same_id(self):
        # Adding a room with an existing ID should replace the old room
        new_room = Room(101)
        new_room.occupancy = True
        self.rooms.add_room(new_room)
        assert self.rooms.get_room(101).occupancy is True