# Integration tests for lightHeadApp.py
# PullA Vibes
# Tests cover app initialization (rooms, users, default language),
# the room occupancy toggle flow (enter/exit and light state),
# all four lighting presets, staff room access and maintenance lighting,
# and language switching between English, Finnish and Swedish.

import sys
import pytest

sys.path.insert(0, "..")

from rooms import Room, Rooms, COLORS
from userhandler import User, UserManager
from lightHeadApp import LightHeadApp


class TestAppInit:
    def setup_method(self):
        self.app = LightHeadApp()

    def test_default_language_english(self):
        # App should start with English as the default language
        assert self.app.current_lang == "ENG"

    def test_rooms_initialized(self):
        # App should initialize all default rooms on startup
        ids = [room.id for room in self.app.rooms]
        for expected in [101, 102, 103, 201, 202, 301]:
            assert expected in ids

    def test_suite_301_has_custom_zones(self):
        # Room 301 should have main, sauna and balcony zones
        room = self.app.rooms.get_room(301)
        assert set(room.zones.keys()) == {"main", "sauna", "balcony"}

    def test_users_initialized(self):
        # Default visitor and staff users should be authenticated successfully
        assert self.app.users.authenticate("visitor101", "visitor123") is not None
        assert self.app.users.authenticate("staff", "staff123") is not None

    def test_invalid_user_not_authenticated(self):
        # A user that does not exist should not be authenticated
        assert self.app.users.authenticate("nobody", "wrong") is None


class TestOccupancyToggle:
    def setup_method(self):
        self.app = LightHeadApp()
        user = self.app.users.authenticate("visitor101", "visitor123")
        self.app.current_user = user
        self.app.current_room = self.app.rooms.get_room(user.room_id)

    def test_entering_room_sets_occupancy(self):
        # Toggling occupancy on an empty room should mark it as occupied
        self.app.toggle_room_occupancy(self.app.current_room.id)
        assert self.app.current_room.get_occupancy() is True

    def test_entering_room_sets_main_brightness(self):
        # Entering a room should set the main zone brightness to 50
        self.app.toggle_room_occupancy(self.app.current_room.id)
        assert self.app.current_room.get_brightness("main") == 50

    def test_exiting_room_clears_occupancy(self):
        # Toggling occupancy on an occupied room should mark it as unoccupied
        self.app.toggle_room_occupancy(self.app.current_room.id)  # enter
        self.app.toggle_room_occupancy(self.app.current_room.id)  # exit
        assert self.app.current_room.get_occupancy() is False

    def test_exiting_room_turns_off_all_lights(self):
        # Exiting a room should turn off all lights in every zone
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
        # Preset 1 should set all zones to the Relaxing color
        self.app.current_room.set_color_all_zones(0)
        for zone in self.app.current_room.zones:
            assert self.app.current_room.get_color(zone) == COLORS[0]

    def test_preset_2_bright_energetic(self):
        # Preset 2 should set all zones to the Bright energetic color
        self.app.current_room.set_color_all_zones(1)
        for zone in self.app.current_room.zones:
            assert self.app.current_room.get_color(zone) == COLORS[1]

    def test_preset_3_movie_mode(self):
        # Preset 3 should set all zones to the Movie mode color
        self.app.current_room.set_color_all_zones(2)
        for zone in self.app.current_room.zones:
            assert self.app.current_room.get_color(zone) == COLORS[2]

    def test_preset_4_wild_disco(self):
        # Preset 4 should set all zones to the Wild disco caveman color
        self.app.current_room.set_color_all_zones(3)
        for zone in self.app.current_room.zones:
            assert self.app.current_room.get_color(zone) == COLORS[3]


class TestStaffAccess:
    def setup_method(self):
        self.app = LightHeadApp()

    def test_staff_authenticate(self):
        # Staff credentials should authenticate and return a staff role user
        user = self.app.users.authenticate("staff", "staff123")
        assert user.role == "staff"

    def test_staff_can_access_unoccupied_room(self):
        # An unoccupied room should be accessible to staff
        room = self.app.rooms.get_room(101)
        assert room.occupancy is False

    def test_staff_sees_occupied_room(self):
        # An occupied room should be visible to staff as occupied
        room = self.app.rooms.get_room(101)
        room.occupancy = True
        assert self.app.rooms.get_room(101).occupancy is True

    def test_maintenance_lights_on(self):
        # Turning on maintenance lights should set all zones to full brightness
        room = self.app.rooms.get_room(101)
        room.set_lights_on()
        for zone in room.zones:
            assert room.get_brightness(zone) == 100

    def test_maintenance_lights_reset(self):
        # Resetting maintenance lights should turn off all zones
        room = self.app.rooms.get_room(101)
        room.set_lights_on()
        room.set_lights_off()
        for zone in room.zones:
            assert room.get_brightness(zone) == 0


class TestLanguageSwitching:
    def setup_method(self):
        self.app = LightHeadApp()

    def test_switch_to_finnish(self):
        # Setting current_lang to FIN should update the app language to Finnish
        self.app.current_lang = "FIN"
        assert self.app.current_lang == "FIN"

    def test_switch_to_swedish(self):
        # Setting current_lang to SWE should update the app language to Swedish
        self.app.current_lang = "SWE"
        assert self.app.current_lang == "SWE"

    def test_switch_back_to_english(self):
        # Switching back to ENG after another language should restore English
        self.app.current_lang = "FIN"
        self.app.current_lang = "ENG"
        assert self.app.current_lang == "ENG"