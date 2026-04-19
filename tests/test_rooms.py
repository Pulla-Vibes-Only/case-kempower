"""
test_rooms.py
# PullA Vibes

Tests for rooms.py — Room, Rooms, LightingSettings

Run with: pytest test_rooms.py -v
"""

import sys
import pytest

from rooms import Room, Rooms, LightingSettings, COLORS, SUITES


class TestLightingSettings:
    def test_default_brightness(self):
        ls = LightingSettings()
        assert ls.brightness == 0

    def test_default_color(self):
        ls = LightingSettings()
        assert ls.color == "white"

    def test_custom_values(self):
        ls = LightingSettings(brightness=75, color="Red")
        assert ls.brightness == 75
        assert ls.color == "Red"


class TestRoomDefaults:
    def test_default_zones_exist(self):
        room = Room(101)
        assert "main" in room.zones
        assert "bedroom" in room.zones
        assert "bathroom" in room.zones

    def test_default_occupancy_false(self):
        room = Room(101)
        assert room.occupancy is False

    def test_default_available_false(self):
        room = Room(101)
        assert room.available is False

    def test_default_room_type_basic(self):
        room = Room(101)
        assert room.room_type == "basic"

    def test_room_id_stored(self):
        room = Room(202)
        assert room.id == 202


class TestRoomFromZoneNames:
    def test_custom_zones(self):
        room = Room.from_zone_names(999, ["main", "sauna", "balcony"])
        assert set(room.zones.keys()) == {"main", "sauna", "balcony"}

    def test_available_true_after_creation(self):
        room = Room.from_zone_names(101, ["main", "bathroom"])
        assert room.available is True

    def test_suite_room_type_for_suite_id(self):
        suite_id = next(iter(SUITES))
        room = Room.from_zone_names(suite_id, ["main", "sauna"])
        assert room.room_type == "suite"

    def test_basic_room_type_for_non_suite_id(self):
        room = Room.from_zone_names(999, ["main"])
        assert room.room_type == "basic"

    def test_all_zones_have_default_lighting(self):
        room = Room.from_zone_names(101, ["main", "sauna"])
        for zone in room.zones.values():
            assert zone.brightness == 0


class TestRoomBrightness:
    def setup_method(self):
        self.room = Room(101)

    def test_get_brightness_default(self):
        assert self.room.get_brightness("main") == 0

    def test_set_and_get_brightness(self):
        self.room.set_brightness("main", 80)
        assert self.room.get_brightness("main") == 80

    def test_set_brightness_zero(self):
        self.room.set_brightness("bedroom", 50)
        self.room.set_brightness("bedroom", 0)
        assert self.room.get_brightness("bedroom") == 0

    def test_set_brightness_max(self):
        self.room.set_brightness("bathroom", 100)
        assert self.room.get_brightness("bathroom") == 100

    def test_brightness_isolated_per_zone(self):
        self.room.set_brightness("main", 90)
        self.room.set_brightness("bedroom", 30)
        assert self.room.get_brightness("main") == 90
        assert self.room.get_brightness("bedroom") == 30


class TestRoomColor:
    def setup_method(self):
        self.room = Room(101)

    def test_get_color_default(self):
        assert self.room.get_color("main") == "white"

    def test_set_color_by_index(self):
        self.room.set_color("main", 0)
        assert self.room.get_color("main") == COLORS[0]

    def test_set_color_all_valid_indices(self):
        for i, color in enumerate(COLORS):
            self.room.set_color("main", i)
            assert self.room.get_color("main") == color

    def test_set_color_all_zones(self):
        self.room.set_color_all_zones(2)
        for zone in self.room.zones:
            assert self.room.get_color(zone) == COLORS[2]

    def test_color_isolated_per_zone(self):
        self.room.set_color("main", 1)
        self.room.set_color("bedroom", 3)
        assert self.room.get_color("main") == COLORS[1]
        assert self.room.get_color("bedroom") == COLORS[3]


class TestRoomOccupancy:
    def test_get_occupancy_default(self):
        room = Room(101)
        assert room.get_occupancy() is False

    def test_set_occupancy_true(self):
        room = Room(101)
        room.occupancy = True
        assert room.get_occupancy() is True


class TestRoomLightsSwitching:
    def setup_method(self):
        self.room = Room(101)

    def test_set_lights_off(self):
        self.room.set_brightness("main", 80)
        self.room.set_color("main", 1)
        self.room.set_lights_off()
        for zone in self.room.zones:
            assert self.room.get_brightness(zone) == 0
            assert self.room.get_color(zone) == COLORS[4]  # White

    def test_set_lights_on(self):
        self.room.set_lights_on()
        for zone in self.room.zones:
            assert self.room.get_brightness(zone) == 100
            assert self.room.get_color(zone) == COLORS[4]  # White

    def test_lights_off_after_on(self):
        self.room.set_lights_on()
        self.room.set_lights_off()
        for zone in self.room.zones:
            assert self.room.get_brightness(zone) == 0

    def test_get_sections(self):
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
        assert self.rooms.get_room(101).id == 101

    def test_get_second_room(self):
        assert self.rooms.get_room(202).id == 202

    def test_iteration_over_rooms(self):
        ids = [room.id for room in self.rooms]
        assert 101 in ids
        assert 202 in ids

    def test_room_items_sorted(self):
        keys = [k for k, _ in self.rooms.room_items()]
        assert keys == sorted(keys)

    def test_add_room_overwrites_same_id(self):
        new_room = Room(101)
        new_room.occupancy = True
        self.rooms.add_room(new_room)
        assert self.rooms.get_room(101).occupancy is True