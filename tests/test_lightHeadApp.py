"""
test_lightHeadApp.py
# PullA Vibes

Integration tests for lightHeadApp.py — LightHeadApp flows

These tests cover the core app logic (occupancy toggling, preset selection,
staff access) without invoking the interactive menus that require user input.

Run with: pytest test_lightHeadApp.py -v
"""

import sys
import pytest

from rooms import Room, Rooms, COLORS
from userhandler import User, UserManager
from lightHeadApp import LightHeadApp


class TestAppInit:
    def setup_method(self):
        self.app = LightHeadApp()

    def test_default_language_english(self):
        assert self.app.current_lang == "ENG"

    def test_rooms_initialized(self):
        # Default rooms: 101, 102, 103, 201, 202, 301
        ids = [room.id for room in self.app.rooms]
        for expected in [101, 102, 103, 201, 202, 301]:
            assert expected in ids

    def test_suite_301_has_custom_zones(self):
        room = self.app.rooms.get_room(301)
        assert set(room.zones.keys()) == {"main", "sauna", "balcony"}

    def test_users_initialized(self):
        assert self.app.users.authenticate("visitor101", "visitor123") is not None
        assert self.app.users.authenticate("staff", "staff123") is not None

    def test_invalid_user_not_authenticated(self):
        assert self.app.users.authenticate("nobody", "wrong") is None


class TestOccupancyToggle:
    def setup_method(self):
        self.app = LightHeadApp()
        user = self.app.users.authenticate("visitor101", "visitor123")
        self.app.current_user = user
        self.app.current_room = self.app.rooms.get_room(user.room_id)

    def test_entering_room_sets_occupancy(self):
        self.app.toggle_room_occupancy(self.app.current_room.id)
        assert self.app.current_room.get_occupancy() is True

    def test_entering_room_sets_main_brightness(self):
        self.app.toggle_room_occupancy(self.app.current_room.id)
        assert self.app.current_room.get_brightness("main") == 50

    def test_exiting_room_clears_occupancy(self):
        self.app.toggle_room_occupancy(self.app.current_room.id)  # enter
        self.app.toggle_room_occupancy(self.app.current_room.id)  # exit
        assert self.app.current_room.get_occupancy() is False

    def test_exiting_room_turns_off_all_lights(self):
        self.app.toggle_room_occupancy(self.app.current_room.id)  # enter
        self.app.current_room.set_brightness("bedroom", 80)
        self.app.toggle_room_occupancy(self.app.current_room.id)  # exit
        for zone in self.app.current_room.zones:
            assert self.app.current_room.get_brightness(zone) == 0


class TestPresetSelection:
    def setup_method(self):
        self.app = LightHeadApp()
        user = self.app.users.authenticate("visitor101", "visitor123")
        self.app.current_user = user
        self.app.current_room = self.app.rooms.get_room(user.room_id)

    def test_preset_1_relaxing(self):
        self.app.current_room.set_color_all_zones(0)
        for zone in self.app.current_room.zones:
            assert self.app.current_room.get_color(zone) == COLORS[0]

    def test_preset_2_bright_energetic(self):
        self.app.current_room.set_color_all_zones(1)
        for zone in self.app.current_room.zones:
            assert self.app.current_room.get_color(zone) == COLORS[1]

    def test_preset_3_movie_mode(self):
        self.app.current_room.set_color_all_zones(2)
        for zone in self.app.current_room.zones:
            assert self.app.current_room.get_color(zone) == COLORS[2]

    def test_preset_4_wild_disco(self):
        self.app.current_room.set_color_all_zones(3)
        for zone in self.app.current_room.zones:
            assert self.app.current_room.get_color(zone) == COLORS[3]


class TestStaffAccess:
    def setup_method(self):
        self.app = LightHeadApp()

    def test_staff_authenticate(self):
        user = self.app.users.authenticate("staff", "staff123")
        assert user.role == "staff"

    def test_staff_can_access_unoccupied_room(self):
        room = self.app.rooms.get_room(101)
        assert room.occupancy is False

    def test_staff_sees_occupied_room(self):
        room = self.app.rooms.get_room(101)
        room.occupancy = True
        assert self.app.rooms.get_room(101).occupancy is True

    def test_maintenance_lights_on(self):
        room = self.app.rooms.get_room(101)
        room.set_lights_on()
        for zone in room.zones:
            assert room.get_brightness(zone) == 100

    def test_maintenance_lights_reset(self):
        room = self.app.rooms.get_room(101)
        room.set_lights_on()
        room.set_lights_off()
        for zone in room.zones:
            assert room.get_brightness(zone) == 0


class TestLanguageSwitching:
    def setup_method(self):
        self.app = LightHeadApp()

    def test_switch_to_finnish(self):
        self.app.current_lang = "FIN"
        assert self.app.current_lang == "FIN"

    def test_switch_to_swedish(self):
        self.app.current_lang = "SWE"
        assert self.app.current_lang == "SWE"

    def test_switch_back_to_english(self):
        self.app.current_lang = "FIN"
        self.app.current_lang = "ENG"
        assert self.app.current_lang == "ENG"